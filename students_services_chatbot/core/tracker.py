import json
import random
import re

from core.actions import *
from core.core_utils import *
from core.objects.constants import *
from utils.util import *


slot_regex = re.compile(r"^([^{]+)([{].+)?")


class Tracker:
    def __init__(self, domain_data, stories_content):
        self.TOTAL_STEPS = 8
        self.domain_data = domain_data
        self.stories_content = stories_content
        self.stories_states = {}
        self.training_examples = {"X": [], "y": []}
        self.actions = {}
        self.load_actions()
        self.actions_end_story = []
        self.load_actions_end_story()

    def load_actions_end_story(self):
        """Get all actions at the end of each story"""

        for block_story in self.stories_content:
            n_items = len(self.stories_content[block_story])
            if self.stories_content[block_story][n_items - 1]["type"] == "action":
                self.actions_end_story.append(self.stories_content[block_story][n_items - 1]["value"])

    def convert_stories_content_to_states(self):
        for block_story in self.stories_content:

            self.stories_states[block_story] = []
            previous_intent = None
            previous_action = None

            for item in self.stories_content[block_story]:

                if item["type"] == "intent":
                    # Don't add action_listen at the beginning of story
                    if len(self.stories_states[block_story]) > 0:
                        # Add action_listen state before any user_intent
                        action_listen_state = init_state(self.domain_data)

                        # set prev_action if previous_action is not None
                        if previous_action is not None:
                            set_state_attr(action_listen_state, "prev_action", previous_action, 1)

                        set_state_attr(action_listen_state, "action", "action_listen", 1)

                        self.stories_states[block_story].append(action_listen_state)

                        previous_action = "action_listen"

                    # Add user_intent state
                    user_intent_state = init_state(self.domain_data)
                    matches = re.match(slot_regex, item["value"])
                    if matches.group(2) is not None:
                        slot = json.loads(matches.group(2))
                        for key in slot:
                            set_state_attr(user_intent_state, "slot", key, slot[key])

                    if previous_intent is not None:
                        set_state_attr(user_intent_state, "prev_intent", previous_intent, 1)

                    # CAUTION: Set intent has to execute after set slot because it's may be overwrite
                    set_state_attr(user_intent_state, "intent", matches.group(1).strip(), 1)

                    # Assign previous_intent by new intent
                    previous_intent = matches.group(1).strip()

                    # Append state to its block story
                    self.stories_states[block_story].append(user_intent_state)
                elif item["type"] == "action":
                    action_state = init_state(self.domain_data)

                    # set prev_action if previous_action is not None
                    if previous_action is not None:
                        set_state_attr(action_state, "prev_action", previous_action, 1)

                    set_state_attr(action_state, "action", item["value"].strip(), 1)

                    # Append state to its block story
                    self.stories_states[block_story].append(action_state)
                    # Set previous action
                    previous_action = item["value"].strip()

            # Add action_listen at the end of each block story
            action_listen_state = init_state(self.domain_data)

            # set prev_action if previous_action is not None
            if previous_action is not None:
                set_state_attr(action_listen_state, "prev_action", previous_action, 1)

            set_state_attr(action_listen_state, "action", "action_listen", 1)

            self.stories_states[block_story].append(action_listen_state)

    def stories_states_to_training_examples(self, stories_states):
        """This function will parse stories_states to training examples"""

        for block_story in stories_states:
            story = stories_states[block_story]
            training_example = init_a_training_example(self.TOTAL_STEPS, self.domain_data)

            for state in story:
                # If state is not user_intent
                # Append this training example to training_examples
                if is_action_state(state):
                    self.training_examples["X"].append(list(training_example))
                    self.training_examples["y"].append(convert_state_to_training_example(state, False))

                # Remove first element
                training_example.pop(0)
                # Append state element at last
                training_example.append(convert_state_to_training_example(state))

        return self.training_examples.copy()

    def load_actions(self):
        for subclass in Action.__subclasses__():
            arr = subclass.__module__.split(".")
            filename = arr[len(arr) - 1]
            self.actions[filename] = subclass

    def exec_action(self, action_key, dialog):
        """Return tuple (result, error)"""

        # Return (None, None) if action_key is default action
        if action_key == "action_listen":
            return None, None

        if action_key[0:len(ACTION_UTTER_PREFIX)] == ACTION_UTTER_PREFIX:  # 'utter_'
            """Execute if action_key is an utter action"""

            # Check if utter is not defined in domain file
            if action_key not in self.domain_data["templates"]:
                return None, ERROR_ACTION_NOT_DEFINED

            utter_templates = self.domain_data["templates"][action_key]
            return random.choice(utter_templates)["text"], None
        elif action_key[0:len(ACTION_CUSTOM_PREFIX)] == ACTION_CUSTOM_PREFIX:   # 'action_'
            """Execute if action_key is an custom action"""

            if len(action_key) > len(ACTION_STORE_PREFIX) and action_key[0:len(ACTION_STORE_PREFIX)] == ACTION_STORE_PREFIX:
                """If action_key is an action_store"""

                slot = action_key[len(ACTION_STORE_PREFIX):]
                # TODO: handle if slot does not provided in temporary_slots

                if SLOT_PREFIX + slot not in dialog["temporary_slots"]:
                    return None, ERROR_SLOT_NOT_PROVIDED

                dialog["slots"][SLOT_PREFIX + slot] = dialog["temporary_slots"][SLOT_PREFIX + slot]
                return None, None
            else:

                # Check if action class is not defined
                if action_key not in self.actions:
                    return None, ERROR_ACTION_NOT_DEFINED

                # Call 'run' method in action class
                result = self.actions[action_key]().run(dialog, self)
                return result, None

    @staticmethod
    def _process_nlu(message, nlu_model, matcher, nlu_oh_enc, nlp):
        """Return (intent, intent probability, entities)"""
        if message is None or message.strip() == "":
            return None, None, None

        # Get vector and entities
        doc = nlp(message.strip())
        x = doc.vector

        # Predict intent
        y_pred = nlu_model.predict(np.array([x]))
        y_oh, intent_max_proba = softmax_to_one_hot(y_pred)
        target_pred = nlu_oh_enc.inverse_transform(y_oh)
        user_intent = target_pred[0][0]

        entities = {}
        # Get entities through doc.ents
        for ent in doc.ents:
            label = ent.label_.lower()
            entities[label] = ent.text
        # Get entities through matcher
        matches = matcher(doc)
        for match_id, start, end in matches:
            label = nlp.vocab.strings[match_id]  # Get string representation
            span = doc[start:end]  # The matched span
            entities[label] = span.text     # It can overwrite entities

        print("entities:", entities)
        print("( " + user_intent + " -", intent_max_proba[0][0], ")")

        return user_intent, intent_max_proba[0][0], entities

    def message_inference(self, dialog, message, nlu_model, matcher, core_model, nlu_oh_enc, nlp):
        list_responses = []
        user_intent, intent_prob, entities = self._process_nlu(message, nlu_model, matcher, nlu_oh_enc, nlp)

        # Compare predicted probability vs intent_threshold
        if intent_prob < INTENT_THRESHOLD:
            return [MSG_DO_NOT_UNDERSTAND]

        # Create state object for user's message
        intent_state = self.create_intent_state(user_intent, entities, dialog)

        # Add state to tracker object
        dialog["states"].append(intent_state)

        # Set previous intent by new intent
        dialog["prev_intent"] = user_intent

        is_clear_dialog_memory = False

        while True:
            X = states_to_training_examples(self.TOTAL_STEPS, dialog["states"], self.domain_data)

            # Predict next action
            y_pred = core_model.predict(np.array([X]))
            y_pred, action_max_proba = softmax_to_one_hot(y_pred)

            # Convert vector to state
            y_pred_state = convert_training_example_to_state(y_pred[0], self.domain_data)

            # Get predicted action key
            predicted_action_key = get_predicted_action_key(y_pred_state)

            print("( " + predicted_action_key + " -", action_max_proba[0][0], ")")

            # Compare predicted_probability vs threshold
            if action_max_proba[0][0] < ACTION_THRESHOLD:
                clear_dialog_memory(dialog)
                return [MSG_CAN_NOT_PREDICT_NEXT_ACTION]

            result, error = self.exec_action(predicted_action_key, dialog)

            if error is None:
                # Set prev_action attribute
                if dialog["prev_action"] is not None:
                    set_state_attr(y_pred_state, "prev_action", dialog["prev_action"], 1)

                # Add predicted action state to tracker
                dialog["states"].append(y_pred_state)

                # Set previous_action by predicted_action_key
                dialog["prev_action"] = predicted_action_key

                if result is not None:
                    list_responses.append(result)
            else:
                """Handle error"""
                if error == ERROR_SLOT_NOT_PROVIDED:
                    # TODO: ask slot again
                    clear_dialog_memory(dialog)
                    return [MSG_NOT_ENOUGH_INFORMATION]
                elif error == ERROR_ACTION_NOT_DEFINED:
                    # TODO:
                    clear_dialog_memory(dialog)
                    return [MSG_ACTION_NOT_DEFINED]

            if predicted_action_key in self.actions_end_story:
                is_clear_dialog_memory = True

            # Break if predicted action is action_listen
            if y_pred_state["action_listen"] == 1:
                break

        if is_clear_dialog_memory:
            clear_dialog_memory(dialog)

        return list_responses

    def create_intent_state(self, user_intent, entities, dialog):
        state = init_state(self.domain_data)

        for label, text in entities.items():
            slot = label.lower()
            set_state_attr(state, "slot", slot, text)
            dialog["temporary_slots"][SLOT_PREFIX + slot] = text

        if dialog["prev_intent"] is not None:
            set_state_attr(state, "prev_intent", dialog["prev_intent"], 1)

        set_state_attr(state, "intent", user_intent, 1)

        return state
