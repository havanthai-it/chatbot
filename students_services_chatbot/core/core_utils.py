from core.objects.constants import *


def init_dialog():
    return {
        "states": [],
        "temporary_slots": {},
        "slots": {},
        "prev_intent": None,
        "prev_action": None
    }


def clear_dialog_slots(dialog):
    dialog["temporary_slots"] = {}
    dialog["slots"] = {}


def clear_dialog_memory(dialog):
    dialog["temporary_slots"] = {}
    dialog["slots"] = {}
    dialog["states"] = []
    dialog["prev_intent"] = None
    dialog["prev_action"] = None


def init_state(domain_data):
    state = {}
    for slot in domain_data["slots"].items():
        state[SLOT_PREFIX + slot[0]] = None

    for intent in domain_data["intents"]:
        state[INTENT_PREFIX + intent] = None

    for intent in domain_data["intents"]:
        state[PREV_INTENT_PREFIX + intent] = None

    for action in domain_data["actions"]:
        state[ACTION_PREFIX + action] = None

    for action in domain_data["actions"]:
        state[PREV_ACTION_PREFIX + action] = None

    state[ACTION_PREFIX + "action_listen"] = None
    state[PREV_ACTION_PREFIX + "action_listen"] = None

    return state


def set_state_attr(state, attr_type, attr, value):
    if attr_type == "slot":
        attr = SLOT_PREFIX + attr
        if attr in state:
            state[attr] = value

    elif attr_type == "intent":
        attr = INTENT_PREFIX + attr
        if attr in state:
            state[attr] = value

    elif attr_type == "prev_intent":
        attr = PREV_INTENT_PREFIX + attr
        if attr in state:
            state[attr] = value

    elif attr_type == "action":
        attr = ACTION_PREFIX + attr
        if attr in state:
            state[attr] = value

    elif attr_type == "prev_action":
        attr = PREV_ACTION_PREFIX + attr
        if attr in state:
            state[attr] = value


def init_a_training_example(total_steps, domain_data):
    training_example = []
    for i in range(total_steps):
        empty_state = init_state(domain_data)
        training_example.append(convert_state_to_training_example(empty_state))

    return training_example


def convert_state_to_training_example(state, is_get_prev_action=True):
    """This function will convert state dict to vector of 0 or 1"""
    training_example = []
    for key in state:
        if state[key] is not None:
            if is_get_prev_action:
                training_example.append(1)
            else:
                len_prefix = len(PREV_ACTION_PREFIX)
                if len(key) > len_prefix and key[:len_prefix] == PREV_ACTION_PREFIX:
                    training_example.append(0)
                else:
                    training_example.append(1)
        else:
            training_example.append(0)

    return training_example


def convert_training_example_to_state(vector, domain_data):
    state = init_state(domain_data)
    for i in range(len(vector)):
        if vector[i] == 1:
            key = list(state.keys())[i]
            state[key] = 1
    return state


def states_to_training_examples(total_steps, states, domain_data):
    """Convert list of states to training examples"""
    training_examples = {"X": [], "y": []}
    n_states = len(states)
    training_examples["X"] = init_a_training_example(total_steps, domain_data)

    for i in range(n_states):
        training_examples["X"].append(convert_state_to_training_example(states[i]))

    return training_examples["X"][-total_steps:]


def is_action_state(state):
    for key in state:
        if state[key] == 1:
            if len(key) > len(ACTION_CUSTOM_PREFIX) and key[:len(ACTION_CUSTOM_PREFIX)] == ACTION_CUSTOM_PREFIX:
                return True
            if len(key) > len(ACTION_UTTER_PREFIX) and key[:len(ACTION_UTTER_PREFIX)] == ACTION_UTTER_PREFIX:
                return True

    return False


def get_predicted_action_key(state):
    for action_key in state:
        if state[action_key] == 1:
            return action_key

    return None
