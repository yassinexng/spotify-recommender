import pandas as pd


def space():
    for i in range(7):
        print("")

df = pd.read_csv("AI_generated_.csv")
df = df.drop(columns="song_code")
df.info()

print(df.head(5))
space()

import ast

space()

def handle_messystrings(ddf, messy_strings):
    for col in messy_strings:
        ddf[col] = ddf[col].apply(ast.literal_eval)


messy_strings = ["artist(s)", "genre(s)"]
handle_messystrings(df, messy_strings)

df.info()
space()
print(df.head(5))
space()


from sklearn.preprocessing import StandardScaler, LabelEncoder, OneHotEncoder, MultiLabelBinarizer
from sklearn.compose import ColumnTransformer
from scipy.sparse import hstack, csr_matrix
from sklearn.neighbors import NearestNeighbors
import numpy as np


scaler = StandardScaler()
laabelencoder = LabelEncoder()

categorical_cols = ["album_name"]
numerical_cols = ["acousticness", "danceability", "energy", "instrumentalness", "key", "liveness", "loudness", "mode", "speechiness", "tempo", "valence"]


X = df
song_lookup = X["Song"].reset_index(drop=True)
artist_lookup = X["artist(s)"].reset_index(drop=True)

mlb_genres = MultiLabelBinarizer()
mlb_artists = MultiLabelBinarizer()

preprocessor = ColumnTransformer(
    transformers=[
        ('numerical', scaler, numerical_cols),
        ('categorical', OneHotEncoder(handle_unknown="ignore"), categorical_cols)
    ]
)

X_genres = mlb_genres.fit_transform(X["genre(s)"])
X_artists = mlb_artists.fit_transform(X["artist(s)"])

X_rest = X.drop(columns=["genre(s)", "artist(s)", "Song"])

preprocessed_X = preprocessor.fit_transform(X_rest)

feature_matrix_training = hstack([
    preprocessed_X,
    csr_matrix(X_genres),
    csr_matrix(X_artists)
]).tocsr()


df_short = pd.read_csv("output_short_i.csv")

handle_messystrings(df_short, messy_strings)

df_short.info()

user_genres = mlb_genres.transform(df_short["genre(s)"])
user_artists = mlb_artists.transform(df_short["artist(s)"])
user_restofinfo = df_short.drop(columns=["genre(s)", "artist(s)", "Song", "song_code"])

preprocessed_userinfo = preprocessor.transform(user_restofinfo)

feature_matrix_user = hstack([
    preprocessed_userinfo,
    csr_matrix(user_genres),
    csr_matrix(user_artists)
]).tocsr()


space()
print("Training matrix shape:", feature_matrix_training.shape)
print("User matrix shape:", feature_matrix_user.shape)
space()


nn = NearestNeighbors(n_neighbors=6, metric="cosine")
nn.fit(feature_matrix_training)

def recommend_from_one(user_row, top_k=5):
    distances, indices = nn.kneighbors(user_row, n_neighbors=top_k + 1)
    distances = distances[0]
    indices = indices[0]
    results = []
    for dist, idx in zip(distances, indices):
        title = song_lookup.iloc[idx]
        artists = artist_lookup.iloc[idx]
        similarity = (1 - dist) * 100
        results.append((title, artists, similarity))
    return results[1:]


def recommend_from_many(user_rows, top_k=5):
    averaged = np.asarray(user_rows.mean(axis=0))
    distances, indices = nn.kneighbors(averaged, n_neighbors=top_k + user_rows.shape[0])
    distances = distances[0]
    indices = indices[0]
    results = []
    for dist, idx in zip(distances, indices):
        title = song_lookup.iloc[idx]
        artists = artist_lookup.iloc[idx]
        similarity = (1 - dist) * 100
        results.append((title, artists, similarity))
    return results[user_rows.shape[0]:]