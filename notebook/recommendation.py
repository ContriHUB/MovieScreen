#!/usr/bin/env python
# coding: utf-8

# In[81]:


import numpy as np # linear algebra
import pandas as pd # data processing
import matplotlib.pyplot as plt

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

paths = {
    "movies.csv": os.path.join(BASE_DIR, "data/movies.csv"),
    "ratings.csv": os.path.join(BASE_DIR, "data/ratings.csv")
}

# In[82]:


from sklearn.preprocessing import MultiLabelBinarizer # one-hot encoding 
from sklearn.neighbors import NearestNeighbors # KNN


# In[83]:


# ratings = pd.read_csv(paths["ratings.csv"])
movies = pd.read_csv(paths["movies.csv"])

print("Datasets loaded")


# In[84]:


(movies.shape)
movies.head()



# In[86]:


# unique_users = len(ratings["userId"].unique())
movies_count = len(movies["movieId"].unique())


# In[89]:


data = movies

# one-hot encoding
mlb = MultiLabelBinarizer()
genre_encoded = mlb.fit_transform(data['genres'].str.split('|'))
genre_df = pd.DataFrame(genre_encoded, columns=mlb.classes_)

data = pd.concat([data, genre_df], axis=1)
data.head()


# # Model 1: KNN Based Genre Similarity
# This model employs a K-Nearest Neighbors (KNN) algorithm to recommend movies based solely on their genres. By creating a feature matrix that includes only the movie titles and their associated genres, it simplifies the data to focus exclusively on genre similarity. When a user inputs a movie, the model identifies the K nearest movies in the feature space based on their genre composition. This approach allows for quick recommendations of films that are closely aligned in genre.

# In[90]:


features = data.drop(columns=[
#     'userId', 'rating', 'timestamp', 
    'genres', 'title', 'movieId'])

features.head()


# In[91]:


knn_model_genres = NearestNeighbors(n_neighbors=5, algorithm='auto')
knn_model_genres.fit(features)


# In[139]:


def recommend_similar_movies_model1(movie_title, *, n=5, model=knn_model_genres, data=movies, features=features):
    movie_idx = data[data['title'] == movie_title].index[0]
    distances, indices = model.kneighbors(features.iloc[movie_idx, :].values.reshape(1, -1), n_neighbors=n)
    recommended_movies = data.iloc[indices.flatten()]
    return recommended_movies

recommend_similar_movies_model1("Toy Story (1995)")