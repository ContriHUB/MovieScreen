# Movie Recommendation System

This notebook implements a K-Nearest Neighbors (KNN)-based movie recommendation system using movie genres and user ratings.
Two models are provided: 
1. A simple KNN model based on movie genres.
2. Another model that incorporates user ratings and uses KNN cosine similarity to recommend movies.

## Notebook
The notebook is also avaliable on Kaggle [here](https://www.kaggle.com/code/shivamaryan10/moviescreen)

## Dataset
The movie recommendation dataset from Kaggle [avaliable here](https://www.kaggle.com/datasets/parasharmanas/movie-recommendation-system) is used but any dataset with the movie genre or user ratings can be easily incorporated due to simple data manipulation.

## Prerequisites
- Python 3.x
- Jupyter Notebook or any compatible environment
- Libraries: `pandas`, `numpy`, `scikit-learn`, `matplotlib`

## Usage

### Recommend Movies Based on Genres:
You can use the following function to get similar movies based on genres:
```python
recommend_similar_movies_model1(movie_title='Shrek (2001)', n=5)
```

### Recommend Movies Based on User Ratings:
You can use the following function to get similar movies based on user ratings:
```python
recommend_similar_movies_model2(movie_title='Shrek (2001)', n=5)
```

`movie_title` must be present in the dataset or it can be inserted manually. Return type is a pandas dataframe.

