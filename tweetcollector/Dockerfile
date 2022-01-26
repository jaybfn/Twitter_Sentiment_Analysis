FROM python:3.9-slim

WORKDIR /app

ADD . /app

RUN pip install --trusted-host pipy.python.org -r requirements.txt

CMD ["python", "/app/get_twitter.py"]