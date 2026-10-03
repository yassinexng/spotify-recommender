# spotify-recommender

A Streamlit app that reads your Spotify listening history, builds audio-feature vectors from it, and recommends tracks from a pre-built dataset using k-nearest-neighbour search.

## Requirements

- Python 3.10+
- A Spotify developer app (client_id, client_secret, which require Spotify premium)
- A Last.fm API key (for genre tags, free api given to everyone)
- The packages in requirements (see below)

Install dependencies:

```
pip install streamlit requests python-dotenv pandas scikit-learn scipy numpy
```

I used uv personally for the venv so if you do use it a simple uv in the beginninf would suffice.


## Setup

1. Copy `.env.example` to `.env` and fill in your credentials:

```
client_id=your_spotify_client_id
client_secret=your_spotify_client_secret
API_LASTFM=your_lastfm_api_key
TOKEN=
```
The Token will be automatically filled with the script.


2. Add `http://127.0.0.1:8888/callback` as a redirect URI in your Spotify app settings when configuring the app.

## How to run

```
streamlit run file.py
```


On first load, click "Authorize with Spotify" and complete the OAuth flow. The app fetches your top tracks (short-term and long-term), pulls audio features from reccobeats.com, pulls genre tags from Last.fm, writes two CSVs, and then runs the recommender.It does require a while (~10 minutes) since the api calls fetch a lot of data.

Subsequent loads use the cached CSVs.

## How it works

- `file.py` — Streamlit orchestration. Handles OAuth callback, session state, and ML pipeline calls with a single render dispatch.
- `ui.py` — Pure presentation layer. Contains design tokens, global stylesheet, component primitives, and responsive layout.
- `logic.py` — Builds a feature matrix from `AI_generated_.csv` (the training corpus, a specifically designed csv file to contain most genres), fits a cosine-distance NearestNeighbors model, transforms user tracks into the same feature space, and exposes `recommend_from_one` and `recommend_from_many`.
- `spotify_json_handling.py` — Fetches top tracks from the Spotify API, audio features from reccobeats, genre tags from Last.fm, and returns two DataFrames on the last function.

- `AI_generated_.csv` — The recommendation corpus (~14k tracks with audio features and genre tags).
- `output_short_i.csv` / `output_long_ii.csv` — Cached user listening data written after each successful auth. 

So:
Each month you have new data, a simple re-authentification to Spotify would suffice to re-fetch data and re-suggest songs.
