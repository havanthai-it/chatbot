from spacy.matcher import Matcher


def NluMatcher(nlp, nlu_training_data):
    matcher = Matcher(nlp.vocab)
    pattern = [{"LOWER": "data"}, {"LOWER": "warehouse"}]
    subject_regex_pattern = [{"TEXT": {"REGEX": "^[a-zA-Z]{3}[0-9]{3}"}}]
    matcher.add("subject", None, pattern)
    matcher.add("subject", None, subject_regex_pattern)

    return matcher
