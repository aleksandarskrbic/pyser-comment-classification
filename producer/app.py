import os
import time
import json
from faker import Faker
from kafka import KafkaProducer
from generator import get_comments
from generator import generate_event


KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
COMMENTS_TOPIC = os.environ.get('COMMENTS_TOPIC')
COMMENTS_PER_SECOND = float(os.environ.get('COMMENTS_PER_SECOND'))
SLEEP_TIME = 1 / COMMENTS_PER_SECOND


if __name__ == '__main__':
    comments = get_comments()
    faker = Faker()

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode()
    )

    i = 0
    while True:
        if i == (len(comments) - 1):
            i = 0
        else:
            event = generate_event(faker, comments[i])
            producer.send(COMMENTS_TOPIC, value=event)
            time.sleep(SLEEP_TIME)
            i += 1
