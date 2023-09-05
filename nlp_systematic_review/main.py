from bertopic import *
import pandas as pd
import numpy as np
from bertopic.representation import KeyBERTInspired


def preprocess_data(path_to_csv, frac):
    """provide the path to csv and the frac of data you want to use and it will
    return the preprocessed dataset in pd.DataFrame format"""

    assert isinstance(path_to_csv, str), "path_to_csv should be a string"
    df = pd.read_csv(path_to_csv)
    df = df.sort_values(by=['abstract_id', 'line_number'])
    df['abstract_text'] = df['abstract_text'].astype(str)
    concatenated_abstract = df.groupby('abstract_id')['abstract_text'].apply(' '.join).reset_index()
    df = df.merge(concatenated_abstract, on='abstract_id', how='left')
    data = df[['abstract_id', 'abstract_text_y']].drop_duplicates().rename(columns={'abstract_text_y': 'abstract_text'})
    data = data.sample(frac=frac).reset_index(drop=True)

    return data


def train_model(processed_df):
    """input a df, it trains the model"""
    topic_model = BERTopic()
    topics, probs = topic_model.fit_transform(processed_df['abstract_text'])

    return topics, probs, topic_model

def get_topic_infos(topic_model):
    """returns a df with Topic, Count, Name, Representation, Representative_Docs"""
    topic_info = topic_model.get_topic_info()

    return topic_info

def visualize_data(processed_df, visu_type):
    """
    Visualizes topics using BERTopic. visu_type: Type of visualization ('circle', 'bar', or 'rank')
    """
    representation_model = KeyBERTInspired()
    topic_model = BERTopic(representation_model=representation_model)
    topics, probs = topic_model.fit_transform(processed_df['abstract_text'])
    if visu_type == 'circle':
        circle = topic_model.visualize_topics()

        return circle

    elif visu_type == 'bar':
        bar = topic_model.visualize_barchart()

        return bar

    elif visu_type == 'rank':
        rank = topic_model.visualize_term_rank()

        return rank

def get_topics_kw(topic_model):
    """returns a df with 10 main keywords for each topic"""

    topics = topic_model.get_topics()
    topic_df = pd.DataFrame({topic_id: [word for word, _ in words] for topic_id, words in topics.items()})
    col_rename = {topic_id: f"{topic_id}" for topic_id in topic_df.columns}
    topic_df.rename(columns=col_rename, inplace=True)

    return topic_df

def get_id_prob_key(topic_model, method, processed_df):
    """Returns a df with the doc_id, the text content, the topic and topic name,
    and the prob of the doc belonging to this topic.
    Methods available: 'main_name' for top word, '10_kw' for 10 keywords with
    respect to the related topic."""

    topics = topic_model.get_topics()
    topic_df = pd.DataFrame({topic_id: [word for word, _ in words] for topic_id, words in topics.items()})
    col_rename = {topic_id: f"{topic_id}" for topic_id in topic_df.columns}
    topic_df.rename(columns=col_rename, inplace=True)
    document = topic_model.get_document_info(processed_df['abstract_text'])
    document_and_proba = document[['Document', 'Topic', 'Probability']]

    if method == 'main_name':
        document_and_proba['Topic_name'] = document_and_proba['Topic'].apply(lambda topic_id: topics.get(int(topic_id), [])[0][0]) #for top word (topic main name)
        doc_with_abstract_id_prob_and_topic_name = document_and_proba.set_index(processed_df.index)

        return doc_with_abstract_id_prob_and_topic_name

    elif method == '10_kw':
        document_and_proba['Topic_name'] = document_and_proba['Topic'].apply(lambda topic_id: ', '.join([word for word, _ in topics.get(int(topic_id), [])])) #for all words with respect to the topic
        doc_with_abstract_id_prob_and_topic_name = document_and_proba.set_index(processed_df.index)

        return doc_with_abstract_id_prob_and_topic_name
