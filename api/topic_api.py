from fastapi import FastAPI, Query
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
    return dict(greeting="Hello")

@app.get("/topic_search")
def topic_search(query: str):

    model = load_model()

    f_topics, f_prob = model.find_topics(query)
    topic_info = model.get_topic_info()

    recommendations = []

    for t in range(len(f_topics)):
        topic_id = f_topics[t]
        topic_prob = round(f_prob[t]*100, 2)
        topic_name = topic_info['Name'][topic_info['Topic'] == topic_id].values[0]
        article_count = df_with_topics['abstract_id'][df_with_topics['Topic'] == t].count()

        recommendations.append({
            "topic_name": topic_name,
            "probability": topic_prob,
            "article_count": article_count,
            "topic_id": topic_id
        })

    return {"recommended_topics": recommendations}
