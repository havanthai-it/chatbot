from core.objects.constants import *


class State(object):
    def __init__(self, domain_data):
        self.data = {}
        # self.state_type = None
        self.init_states(domain_data)

    def init_states(self, domain_data):
        for slot in domain_data["slots"].items():
            self.data[SLOT_PREFIX + slot[0]] = None

        for intent in domain_data["intents"]:
            self.data[INTENT_PREFIX + intent] = None

        for intent in domain_data["intents"]:
            self.data[PREV_INTENT_PREFIX + intent] = None

        for action in domain_data["actions"]:
            self.data[ACTION_PREFIX + action] = None
        self.data[ACTION_PREFIX + "action_listen"] = None

    def set(self, attr_type, attr, value):
        # self.state_type = attr_type
        if attr_type == "slot":
            attr = SLOT_PREFIX + attr
            if attr in self.data:
                self.data[attr] = value
        elif attr_type == "intent":
            attr = INTENT_PREFIX + attr
            if attr in self.data:
                self.data[attr] = value
        elif attr_type == "prev_intent":
            attr = PREV_INTENT_PREFIX + attr
            if attr in self.data:
                self.data[attr] = value
        elif attr_type == "action":
            attr = ACTION_PREFIX + attr
            if attr in self.data:
                self.data[attr] = value

    def to_training_example(self):
        """This function will convert state object to vector of 0 or 1"""
        training_example = []
        for key in self.data:
            if self.data[key] is not None:
                training_example.append(1)
            else:
                training_example.append(0)

        return training_example

    @staticmethod
    def training_example_to_state(vector, domain_data):
        state = State(domain_data)
        for i in range(len(vector)):
            if vector[i] == 1:
                key = list(state.data.keys())[i]
                state.data[key] = 1
        return state

# domain = DomainYmlReader().read(open("../../domain.yml"))
# state = State(domain)
