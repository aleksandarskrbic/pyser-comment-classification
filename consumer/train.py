import os
import re
import numpy as np
import pandas as pd
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import clean


CLASSES = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
TEXT = 'comment_text'


class TrainingTask():
    def __init__(self) -> None:
        self._load_data()
        self._vectorize_text()
        self._train_model()
        self._persist_model()

    def _load_data(self) -> None:
        print('Loading and preprocessing data...')
        self._train_data = pd.read_csv( 'data/train.csv')
        self._test_data = pd.read_csv('data/test.csv')
        self._train_data[TEXT] = [clean(s) for s in self._train_data[TEXT]]
        self._test_data[TEXT] = [clean(s) for s in self._test_data[TEXT]]
        
    def _vectorize_text(self) -> None:
        print('Vectorizing text...')
        self._word_vectorizer = TfidfVectorizer(
            sublinear_tf=True,
            strip_accents='unicode',
            analyzer='word',
            token_pattern=r'\w{1,}',
            ngram_range=(1, 1),
            max_features=15000)
        self._word_vectorizer.fit(self._train_data[TEXT])
        self._train_word_features = self._word_vectorizer.transform(self._train_data[TEXT])

    def _train_model(self) -> None:
        print('Training classifiers...')
        self._models = []
        for class_name in CLASSES:
            model = LogisticRegression(solver='lbfgs', max_iter=150,  n_jobs=2)
            target = self._train_data[class_name]

            x_train, x_test, y_train, y_test = train_test_split(
                self._train_word_features,
                target,
                test_size=0.33,
                random_state=42)

            model.fit(x_train, y_train)
            predictions = model.predict(x_test)
            acc = accuracy_score(y_test, predictions)
            print('Accuracy for class {} is {:0.2f}'.format(class_name, acc))
            self._models.append((class_name, model))

    def _persist_model(self) -> None:
        classifier = {
            'models': self._models,
            'vectorizer': self._word_vectorizer
        }
        if not os.path.exists('model'):
            os.mkdir('model')
        joblib.dump(classifier, 'model/classifier')


if __name__ == '__main__':
    TrainingTask()

