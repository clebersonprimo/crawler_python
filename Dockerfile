FROM python:3.7-slim

ADD . /app
WORKDIR /app

RUN apt-get update
RUN apt-get upgrade

RUN apt-get install -y git

RUN pip install -r requirements.txt

CMD ["python", "app.py"]