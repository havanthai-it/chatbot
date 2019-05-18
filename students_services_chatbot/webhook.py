import spacy
import uuid

from nlu.nlu_utils import NluMatcher
from core.tracker import Tracker
from core.core_utils import *
from nlu.nlu_markdown import NluMarkdownReader
from core.stories_markdown import StoriesMarkdownReader
from utils.util import *
from utils.domain_yml import DomainYmlReader
from keras.models import load_model

from flask import Flask, request, abort, jsonify, session, render_template
from datetime import timedelta


app = Flask(__name__)
app.secret_key = "Students Services Chatbot Secret Key"
app.permanent_session_lifetime = timedelta(hours=1)

nlu_model = load_model("./models/nlu/nlu.h5")
core_model = load_model("./models/core/core.h5")
nlu_oh_enc = pickle_load_object("./models/encoder/nlu_one_hot_encoder.obj")
nlp = spacy.load("./models/spacy/")

# Make predict function work
nlu_model._make_predict_function()
core_model._make_predict_function()

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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/session", methods=["POST"])
def create_session():
    if request.method == "POST":
        # TODO: only be called from login service
        if True:
            dialog = init_dialog()
            roll_number = request.json["roll_number"]
            dialog_id = str(uuid.uuid4())
            # TODO: Use dialog_id instead of roll_number
            session["dialog"] = dialog
            return dialog_id, 200
    else:
        abort(400)


@app.route("/dialog", methods=["POST"])
def webhook():
    if request.method == "POST":
        message = request.json["message"]
        roll_number = request.json["roll_number"]

        dialog = session["dialog"]
        list_responses = tracker.message_inference(dialog, message, nlu_model, matcher, core_model, nlu_oh_enc, nlp)
        session["dialog"] = dialog
        return jsonify({"list_responses": list_responses}), 200
    else:
        abort(400)


if __name__ == "__main__":
    app.run()
