from fastapi import FastAPI, Query
import pandas as pd
import json as json

from typing import List
from nlp_systematic_review.main import preprocess_data, load_model, find_article
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.state.model = load_model()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def root():
    return dict(greeting="Hello test")

@app.get("/topic_search")
def topic_search(query: str):

    query_topics = app.state.model.find_topics(query)
    print(f"format of model: {type(query_topics)}")

    topic_info = app.state.model.get_topic_info()

    topic_list =[]
    print("--- start loop\n")

    for t in range(len(query_topics[0])):
        topic = topic_info[topic_info['Topic'] == query_topics[0][t]]

        topic_id = str(list(topic['Topic'])[0])
        topic_prob = str(query_topics[1][t])
        topic_name = list(topic['Name'])[0]
        topic_representation = list(topic['Representation'])[0]

        topic_dict = dict({"topic_id":topic_id,"topic_prob":topic_prob,"topic_name":topic_name,"topic_representation":topic_representation})
        print(topic_dict)
        topic_list.append(topic_dict)

    print("--- end loop\n")
    print(dict({"recommended_topics":topic_list}))


    #return topic_list #dict({"recommended_topics":topic_list})
    return dict({"recommended_topics":topic_list})
