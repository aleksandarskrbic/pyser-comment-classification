import os
import datetime
import pandas as pd
from faker import Faker

CLASSES = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']
TEXT = 'comment_text'


def get_comments() -> list:
    df_train = pd.read_csv('./data/train.csv')
    df_test = pd.read_csv('./data/test.csv')
    comments = [list(df_train[df_train[class_name] == 1].sample(450)[TEXT]) for class_name in CLASSES]
    comments.append(list(df_test[TEXT].sample(2000)))
    comments = [comment for list_of_comments in comments for comment in list_of_comments]
    return comments


def generate_event(faker: Faker, comment: str) -> dict:
    profile: dict = faker.simple_profile()
    return {
        'user_id': faker.uuid4(),
        'ip': faker.ipv4(),
        'datetime': str(datetime.datetime.utcnow()),
        'comment': comment
    }

