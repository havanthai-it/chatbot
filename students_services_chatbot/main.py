import spacy

from nlu.nlu_utils import NluMatcher
from core.tracker import Tracker
from core.core_utils import *
from nlu.nlu_markdown import NluMarkdownReader
from core.stories_markdown import StoriesMarkdownReader
from utils.util import *
from utils.domain_yml import DomainYmlReader
from keras.models import load_model

nlu_model = load_model("./models/nlu/nlu.h5")
core_model = load_model("./models/core/core.h5")
nlu_oh_enc = pickle_load_object("./models/encoder/nlu_one_hot_encoder.obj")
nlp = spacy.load("./models/spacy/")

domain_stream = open("./domain.yml", "r")
domain_data = DomainYmlReader().read(domain_stream)
domain_stream.close()

f = open("./data/stories/stories.md", "r")
stories_md = StoriesMarkdownReader()
stories_md.read(f.read())
stories_content = stories_md.content
f.close()

f = open("./data/nlu/nlu.md", "r")
nlu_markdown_reader = NluMarkdownReader()
nlu_training_data = nlu_markdown_reader.read(f.read())
f.close()

matcher = NluMatcher(nlp, nlu_training_data)

tracker = Tracker(domain_data, stories_content)

dialog = init_dialog()

MESSAGES_QUEUE = ["hi", "i want to suspend subject", "MAE101", "yes"]

for message in MESSAGES_QUEUE:
    print("User:", message)
    list_responses = tracker.message_inference(dialog, message, nlu_model, matcher, core_model, nlu_oh_enc, nlp)
    for response in list_responses:
        print("Bot:", response)
