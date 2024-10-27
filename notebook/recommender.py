import numpy as np
import pandas as pd
from notebook.recommendation import data, features, knn_model_genres

# TMDB to dataset genres mapping
# keys taken from https://api.themoviedb.org/3/genre/movie/list?api_key=TMBD_API_KEY
# values taken from data.columns
tmdb_to_dataset_genres = {
    "Action": ["Action"],
    "Adventure": ["Adventure"],
    "Animation": ["Animation"],
    "Comedy": ["Comedy"],
    "Crime": ["Crime"],
    "Documentary": ["Documentary"],
    "Drama": ["Drama"],
    "Family": ["Children"],  # Mapping Family to Children genre
    "Fantasy": ["Fantasy"],
    "History": [],  # No direct mapping in dataset
    "Horror": ["Horror"],
    "Music": ["Musical"],
    "Mystery": ["Mystery"],
    "Romance": ["Romance"],
    "Science Fiction": ["Sci-Fi"],
    "TV Movie": [],  # No direct mapping in dataset
    "Thriller": ["Thriller"],
    "War": ["War"],
    "Western": ["Western"]
}

# Create a feature vector from TMDB input genres after mapping to dataset genres
def genres_to_feature_vector(input_genres, features=features, genre_mapping=tmdb_to_dataset_genres):
    feature_vector = np.zeros(features.shape[1])
    
    dataset_genres = set()
    for genre in input_genres:
        mapped_genres = genre_mapping.get(genre, [])
        dataset_genres.update(mapped_genres)

    for genre in dataset_genres:
        if genre in features.columns:
            feature_vector[features.columns.get_loc(genre)] = 1
            
    return feature_vector.reshape(1, -1)

# Use the KNN model to find similar movies by list of genres
def recommend_by_genres(input_genres, n=5, model=knn_model_genres, data=data, features=features):
    feature_vector = genres_to_feature_vector(input_genres)
    distances, indices = model.kneighbors(feature_vector, n_neighbors=n)
    recommended_movies = data.iloc[indices.flatten()]
    
    return recommended_movies['title'].tolist()
