import os
import faust
from models import EventModel, Classifier


KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
COMMENTS_TOPIC = os.environ.get('COMMENTS_TOPIC')


app = faust.App('comment-classification', broker=KAFKA_BROKER_URL)
comments_topic = app.topic(COMMENTS_TOPIC, value_type=EventModel)
classifer = Classifier()


@app.agent(comments_topic)
async def classify_comments(events):
    async for event in events:
        pred = classifer.predict(event.comment)
        result = {
            'user_id': event.user_id,
            'comment': event.comment,
            'datetime':event.datetime,
            'data': pred
        }
        print(result)


if __name__ == '__main__':
    app.main()
