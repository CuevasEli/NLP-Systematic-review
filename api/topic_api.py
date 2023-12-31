from fastapi import FastAPI, Query
import pandas as pd
import json as json

from typing import List
from nlp_systematic_review.main import preprocess_data, load_model,get_latest_data_and_topics,get_article_title
#from nlp_systematic_review.web_scraping import get_article_details
#from nlp_systematic_review.data import get_latest_data_and_topics
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.state.model = load_model()
app.state.topicdata = get_latest_data_and_topics()
app.state.tarticle_title = get_article_title()

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

    topic_info = app.state.model.get_topic_info()

    articles = app.state.topicdata
    article_titles = app.state.tarticle_title

    topic_list =[]

    for t in range(len(query_topics[0])):
        topic = topic_info[topic_info['Topic'] == query_topics[0][t]]

        topic_id = list(topic['Topic'])[0]
        topic_prob = str(query_topics[1][t])
        topic_name = list(topic['Name'])[0]
        topic_representation = list(topic['Representation'])[0]

        #print(f"topic id:{topic_id}")

        article = articles[articles['Topic'] == topic_id].sort_values('Probability',ascending=False)

        article_count = article.shape[0]

        article_list = []


        for r in range(article_count):
            article_id = article.iloc[r][0]
            article_prob = article.iloc[r][2]
            article_url = article.iloc[r][3]

            try:
                article_title_index = article_titles.index[article_titles['article_id'] == article_id].tolist()[0]
                article_title = article_titles.iloc[article_title_index]['article_title']
            except:
                article_title = 'No title available for this article.'

            #article_details = get_article_details(article_id)
            dict_1 = dict({'article_id':str(article_id)
                            ,'article_title':article_title
                              ,'article_prob':str(article_prob)
                              ,'article_url':article_url
                              })

            #dict_1.update(article_details)
            article_list.append(dict_1)

        topic_dict = dict({"topic_id":str(topic_id)
                           ,"topic_prob":str(topic_prob)
                           ,"topic_name":topic_name
                           ,"topic_representation":topic_representation
                           ,'article_count':str(article_count)
                           ,'article_list':article_list
                           })

        topic_list.append(topic_dict)

    return dict({"recommended_topics":topic_list})
