#!/usr/bin/env python
# coding: utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

paths = {
    "movies.csv": os.path.join(BASE_DIR, "data/movies.csv"),
    "ratings.csv": os.path.join(BASE_DIR, "data/ratings.csv")
}

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.neighbors import NearestNeighbors

movies = pd.read_csv(paths["movies.csv"])

movies_count = len(movies["movieId"].unique())

data = movies

mlb = MultiLabelBinarizer()
genre_encoded = mlb.fit_transform(data['genres'].str.split('|'))
genre_df = pd.DataFrame(genre_encoded, columns=mlb.classes_)

data = pd.concat([data, genre_df], axis=1)

features = data.drop(columns=['genres', 'title', 'movieId'])

knn_model_genres = NearestNeighbors(n_neighbors=5, algorithm='auto')
knn_model_genres.fit(features)

def recommend_similar_movies_model1(movie_title, *, n=5, model=knn_model_genres, data=movies, features=features):
    movie_idx = data[data['title'] == movie_title].index[0]
    distances, indices = model.kneighbors(features.iloc[movie_idx, :].values.reshape(1, -1), n_neighbors=n)
    recommended_movies = data.iloc[indices.flatten()]
    return recommended_movies