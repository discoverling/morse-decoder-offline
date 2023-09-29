# Train a machine-learning model to classify Morse code input
#
# Requirements
# - SciKit-Learn to create the model
#
# These dependencies can be installed from command-line as follows:
# pip install -U scikit-learn

import numpy as np
from glob import glob
from os.path import basename
from sklearn.ensemble import RandomForestClassifier

# Load training dataset from csv files 
def load_features(folder):
    dataset = None
    classmap = {}
    for class_idx, filename in enumerate(glob('%s/*.csv' % folder)):
        class_name = basename(filename)[:-4]
        classmap[class_idx] = class_name
        samples = np.loadtxt(filename, dtype=float, delimiter=',')
        labels = np.ones((len(samples), 1)) * class_idx
        samples = np.hstack((samples, labels))
        dataset = samples if dataset is None else np.vstack((dataset, samples))
    return dataset, classmap

# Create random forest classifier
def load_classifier(folder):
    print("Loading training data...")
    features, classmap = load_features('training_data')
    print("Loading classifier...")
    # Create classifier function from feature set
    X, y = features[:, :-1], features[:, -1]
    classifier = RandomForestClassifier(20, max_depth=10).fit(X, y)
    return classifier, classmap





