import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import GridSearchCV

def load_and_encode_data():
    global label_encoder
    with open('aberrations_array.json', 'r') as f:
        aberrations_array = json.load(f)
    aberrations_array = [np.array(arr) for arr in aberrations_array]

    with open('beasts_array.json', 'r') as f:
        beasts_array = json.load(f)
    beasts_array = [np.array(arr) for arr in beasts_array]

    with open('celestials_array.json', 'r') as f:
        celestials_array = json.load(f)
    celestials_array = [np.array(arr) for arr in celestials_array]

    with open('constructs_array.json', 'r') as f:
        constructs_array = json.load(f)
    constructs_array = [np.array(arr) for arr in constructs_array]

    with open('dragons_array.json', 'r') as f:
        dragons_array = json.load(f)
    dragons_array = [np.array(arr) for arr in dragons_array]

    with open('elementals_array.json', 'r') as f:
        elementals_array = json.load(f)
    elementals_array = [np.array(arr) for arr in elementals_array]

    with open('fey_array.json', 'r') as f:
        fey_array = json.load(f)
    fey_array = [np.array(arr) for arr in fey_array]

    with open('fiends_array.json', 'r') as f:
        fiends_array = json.load(f)
    fiends_array = [np.array(arr) for arr in fiends_array]

    with open('giants_array.json', 'r') as f:
        giants_array = json.load(f)
    giants_array = [np.array(arr) for arr in giants_array]

    with open('monstrosoties_array.json', 'r') as f:
        monstrosoties_array = json.load(f)
    monstrosoties_array = [np.array(arr) for arr in monstrosoties_array]

    with open('oozes_array.json', 'r') as f:
        oozes_array = json.load(f)
    oozes_array = [np.array(arr) for arr in oozes_array]

    with open('plants_array.json', 'r') as f:
        plants_array = json.load(f)
    plants_array = [np.array(arr) for arr in plants_array]

    with open('undead_array.json', 'r') as f:
        undead_array = json.load(f)
    undead_array = [np.array(arr) for arr in undead_array]

    data = aberrations_array + beasts_array + celestials_array + constructs_array + dragons_array + elementals_array + fey_array + fiends_array + giants_array + monstrosoties_array + oozes_array + plants_array + undead_array
    labels = ['Aberrations'] * len(aberrations_array) + ['Beasts'] * len(beasts_array) + ['Celestials'] * len(celestials_array) + ['Constructs'] * len(constructs_array) + ['Dragons'] * len(dragons_array) + ['Elementals'] * len(elementals_array) + ['Fey'] * len(fey_array) + ['Fiends'] * len(fiends_array) + ['Giants'] * len(giants_array) + ['Monstrosoties'] * len(monstrosoties_array) + ['Oozes'] * len(oozes_array) + ['Plants'] * len(plants_array) + ['Undead'] * len(undead_array)
    # Encode labels to numerical format
    label_encoder = LabelEncoder()
    encoded_labels = label_encoder.fit_transform(labels)

    # Split the data into training and testing sets
    
    X_train, X_test, y_train, y_test = train_test_split(data, encoded_labels, stratify=encoded_labels, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test

X_train, X_test, y_train, y_test = load_and_encode_data()

# Create the model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)
print(label_encoder.classes_)
print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(report)

# Define parameter grid
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_features': ['auto', 'sqrt', 'log2'],
    'max_depth': [None, 10, 20, 30],
    'criterion': ['gini', 'entropy']
}

# Create GridSearchCV object
grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)

# Fit the model
grid_search.fit(X_train, y_train)

# Get the best model
best_model = grid_search.best_estimator_

# Evaluate the best model
best_y_pred = best_model.predict(X_test)
best_accuracy = accuracy_score(y_test, best_y_pred)
best_report = classification_report(y_test, best_y_pred, target_names=label_encoder.classes_)

print(f'Best Model Accuracy: {best_accuracy}')
print('Best Model Classification Report:')
print(best_report)