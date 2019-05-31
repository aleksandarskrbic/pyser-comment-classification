FROM python:3.6

WORKDIR /

ADD ./requirements.txt ./
RUN pip install -r requirements.txt
ADD ./ ./

CMD ["faust", "-A", "app", "worker", "-l", "info"]