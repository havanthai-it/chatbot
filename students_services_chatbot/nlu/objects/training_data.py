from nlu.objects.message import Message


class TrainingData(object):
    def __init__(self,
                 training_examples=None,
                 entity_synonyms=None,
                 regex_features=None,
                 lookup_tables=None):
        self.training_examples = training_examples if training_examples else []
        self.entity_synonyms = entity_synonyms if entity_synonyms else {}
        self.lookup_tables = lookup_tables if lookup_tables else []
        self.regex_features = regex_features if regex_features else []
        # self.sort_regex_features()

    def intent_examples(self):
        # type:() -> list[Message]
        return [ex
                for ex in self.training_examples
                if ex.get("intent") is not None]

    def intents(self):
        """Returns the set of nlu in the training data."""
        return set([ex.get("intent") for ex in self.training_examples]) - {None}

    def intents_training_data(self):
        """Return a tuple of texts and targets set"""
        texts = []
        targets = []
        for ex in self.training_examples:
            intent = ex.get("intent")
            if intent:
                texts.append(ex.text)
                targets.append(intent)
        return texts, targets
