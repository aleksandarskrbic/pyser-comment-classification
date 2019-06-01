import math
import faust
from sklearn.externals import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import clean


class EventModel(faust.Record):
    user_id: str
    ip: str
    datetime: str
    comment: str


class Classifier():
    def __init__(self) -> None:
        model = joblib.load('./model/classifier')
        self._models = model['models']
        self._vectorizer = model['vectorizer']

    def predict(self, comment: str) -> dict:
        comment = clean(comment)
        vectorized_comment = self._vectorizer.transform([comment])

        predictions = {}
        for class_name, model in self._models:
            prediction = model.predict_proba(vectorized_comment)[0][1]
            prediction = math.floor(prediction*100) / 100
            predictions[class_name] = prediction

        return predictions
