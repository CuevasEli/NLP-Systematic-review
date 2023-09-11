FROM python:3.10.6-buster
WORKDIR /prod
COPY api api
COPY nlp_systematic_review nlp_systematic_review
COPY setup.py setup.py
COPY requirements.txt requirements.txt
COPY useful-proposal-392710-6af2051b8d4b.json useful-proposal-392710-6af2051b8d4b.json

ENV GOOGLE_APPLICATION_CREDENTIALS=useful-proposal-392710-6af2051b8d4b.json
#RUN apt-get update && apt-get install -y build-essential
RUN pip install -r requirements.txt
RUN pip install .


CMD uvicorn api.topic_api:app --host 0.0.0.0 --port $PORT
#magnetic-cairn-393111-9f94f5aa0876.json
