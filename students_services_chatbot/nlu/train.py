import spacy

from sklearn import preprocessing
from keras.models import load_model

from nlu.nlu_markdown import NluMarkdownReader
from utils.util import *
from nlu.model import build_model

# Load the spacy model: nlp
# nlp = spacy.load("en_core_web_md")
nlp = spacy.load("../models/spacy/")

# Calculate the dimensionality of nlp
embedding_dim = nlp.vocab.vectors_length

f = open("../data/nlu/nlu.md", "r")

markdown_reader = NluMarkdownReader()
training_data = markdown_reader.read(f.read())
f.close()

texts, targets = training_data.intents_training_data()
texts = np.array(texts)
targets = np.array(targets).reshape(-1, 1)

# Shuffle
texts, targets = shuffle_matrix(texts, targets)

# One hot encoder
one_hot_encoder = preprocessing.OneHotEncoder()
one_hot_encoder.fit(targets)
targets_encoded = one_hot_encoder.transform(targets).toarray()

# Save one_hot_encoder object
pickle_save_object(one_hot_encoder, "../models/encoder/nlu_one_hot_encoder.obj")
# # Load one_hot_encoder object
# one_hot_encoder = pickle_load_object("../models/encoder/nlu_one_hot_encoder.obj")

X = np.zeros((len(texts), embedding_dim))
y = np.zeros(targets_encoded.shape)

for i in range(X.shape[0]):
    X[i] = nlp(str(texts[i])).vector
    y[i] = targets_encoded[i]

model = build_model(X, y)
model.fit(X, y, epochs=50, batch_size=32)

model.save("../models/nlu/nlu.h5")

model = load_model("../models/nlu/nlu.h5")

# TODO:
y_pred = model.predict(X)
y_oh = softmax_to_one_hot(y_pred)
for i in range(50):
    print(y[i], "~", y_oh[i])

