import numpy as np

from keras.models import load_model
from core.stories_markdown import StoriesMarkdownReader
from core.model import build_model
from utils.util import shuffle_matrix
from utils.domain_yml import DomainYmlReader
from core.tracker import Tracker


domain_stream = open("../domain.yml", "r")
domain_data = DomainYmlReader().read(domain_stream)
domain_stream.close()

f = open("../data/stories/stories.md", "r")
stories_md = StoriesMarkdownReader()
stories_md.read(f.read())
stories_content = stories_md.content
f.close()

tracker = Tracker(domain_data, stories_content)
tracker.convert_stories_content_to_states()
tracker.stories_states_to_training_examples(tracker.stories_states)
training_examples = tracker.training_examples

X = np.array(training_examples["X"])
y = np.array(training_examples["y"])

for i in range(7):
    X = np.concatenate((X, X), axis=0)
    y = np.concatenate((y, y), axis=0)

X, y = shuffle_matrix(X, y)

model = build_model(X, y)

model.fit(X, y, batch_size=128, epochs=50, verbose=1)

model.save("../models/core/core.h5")

model = load_model("../models/core/core.h5")

score, acc = model.evaluate(X, y, batch_size=128)
print('Train score:', score)
print('Train accuracy:', acc)
print("-----")


# state = State(domain_data)
# for i in range(len(X)):
#     y_pred = model.predict(np.array([X[i]]))
#     y_pred = softmax_to_one_hot(y_pred)
#     print("Predicted:", y_pred)
#     print("Actual:", y[i])
#     print("Predicted:", state.training_example_to_state(y_pred[0]))
#     print("Actual:", state.training_example_to_state(y[i]))
#     print("---------")
