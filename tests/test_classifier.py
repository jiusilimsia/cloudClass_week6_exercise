import numpy as np
import pandas as pd
from sklearn import linear_model, datasets, metrics
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.utils import to_categorical
import logging
import pytest


@pytest.fixture(scope="module")
def iris_data():
    # Load the Iris dataset
    iris = datasets.load_iris()
    X = iris.data
    y = iris.target
    yield X, y


@pytest.fixture(scope="module")
def split_data(iris_data):
    X, y = iris_data
    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42)
    yield X_train, X_test, y_train, y_test


@pytest.fixture(scope="module")
def model():
    # Create a neural network model
    model = Sequential()
    model.add(Dense(16, input_shape=(4,)))
    model.add(Activation('sigmoid'))
    model.add(Dense(3))
    model.add(Activation('softmax'))
    model.compile(optimizer='adam',
                  loss='categorical_crossentropy', metrics=["accuracy"])
    yield model


#def test_data_shape(iris_data):

def test_model_accuracy(model, split_data):
    X_train, X_test, y_train, y_test = split_data

    y_test_ohe = to_categorical(y_test)

    y_train_ohe = to_categorical(y_train)
    model.fit(X_train,y_train_ohe, epochs=10,batch_size=5,verbose=0)

    loss, accuracy = model.evaluate(X_test, y_test_ohe, verbose=0)
    assert accuracy >= 0.7

#def test_data_leakage(model, iris_data, split_data):

#def test_model_predictions(model, split_data):