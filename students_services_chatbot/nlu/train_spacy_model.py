import spacy
import random

from spacy.util import minibatch, compounding
from pathlib import Path

from nlu.nlu_markdown import NluMarkdownReader

f = open("../data/nlu/nlu.md", "r")

markdown_reader = NluMarkdownReader()
training_data = markdown_reader.read(f.read())
f.close()

def extract_spacy_train_data(training_examples):
    """Extract train data for spacy from training examples in markdown file"""
    train_data = []
    for ex in training_examples:
        if "entities" in ex.data and len(ex.data["entities"]) > 0:
            text = ex.text
            entities = []
            for ent in ex.data["entities"]:
                entities.append((ent["start"], ent["end"], ent["entity"].upper()))

            train_data.append((text, {"entities": entities}))

    return train_data


def update_spacy_model(train_data, model=None, output_dir=None, n_iter=100):
    """Load the model, set up t he pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in train_data:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]

    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        if model is None:
            nlp.begin_training()

        for itn in range(n_iter):
            random.shuffle(train_data)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(train_data, size=compounding(4.0, 32.0, 1.001))
            # batches = [training_data]
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in train_data:
            doc = nlp2(text)
            print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])

    return nlp


train_data = extract_spacy_train_data(training_data.training_examples)
nlp = update_spacy_model(train_data, 'en_core_web_md', '../models/spacy/')
