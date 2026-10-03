import streamlit as st
import requests
import json
import subprocess
import os
from dotenv import load_dotenv, set_key
import pandas as pd
from scipy.sparse import hstack, csr_matrix
import ui
import importlib
importlib.reload(ui)

st.set_page_config(page_title="Spotify Recommender", layout="wide")
ui.inject_global_styles()

load_dotenv()
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
link = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri=http://127.0.0.1:8888/callback&scope=user-top-read&state=random_string"

if "hide" not in st.session_state:
    st.session_state.hide = False
if "df_one" not in st.session_state:
    st.session_state.df_one = None
if "df_two" not in st.session_state:
    st.session_state.df_two = None
if "recs" not in st.session_state:
    st.session_state.recs = None
if "custom_recs" not in st.session_state:
    st.session_state.custom_recs = None
if "picked_song" not in st.session_state:
    st.session_state.picked_song = None
if "picked_source" not in st.session_state:
    st.session_state.picked_source = "short"
if "next_url" not in st.session_state:
    st.session_state.next_url = None
if "error" not in st.session_state:
    st.session_state.error = None
if "loading" not in st.session_state:
    st.session_state.loading = {}

if not st.session_state.hide and st.session_state.next_url is None:
    try:
        r = requests.get(link)
        r.raise_for_status()
        st.session_state.next_url = r.url
    except Exception as e:
        st.session_state.error = {"auth": f"Could not reach Spotify authorization service: {e}"}

next_url = st.session_state.next_url or link


def enrich_tracks(track_tuples):
    if not track_tuples:
        return []
    from logic import df as corpus_df
    enriched = []
    for item in track_tuples:
        if isinstance(item, dict):
            enriched.append(item)
            continue
        title, artists, similarity = item[0], item[1], item[2]
        album = ""
        genres = []

        match = corpus_df[corpus_df["Song"] == title]
        if len(match) == 0 and st.session_state.df_one is not None:
            match = st.session_state.df_one[st.session_state.df_one["Song"] == title]
        if len(match) == 0 and st.session_state.df_two is not None:
            match = st.session_state.df_two[st.session_state.df_two["Song"] == title]

        if len(match) > 0:
            row = match.iloc[0]
            album = row.get("album_name", "")
            genres = row.get("genre(s)", [])

        enriched.append({
            "title": title,
            "artists": artists,
            "album": album,
            "genres": genres,
            "similarity": similarity,
        })
    return enriched


def build_vector_for_df(df_target):
    from logic import preprocessor, mlb_genres, mlb_artists, handle_messystrings, messy_strings
    df_copy = df_target.copy()
    handle_messystrings(df_copy, messy_strings)
    genres = mlb_genres.transform(df_copy["genre(s)"])
    artists = mlb_artists.transform(df_copy["artist(s)"])
    rest = df_copy.drop(columns=["genre(s)", "artist(s)", "Song", "song_code"], errors="ignore")
    pre = preprocessor.transform(rest)
    return hstack([pre, csr_matrix(genres), csr_matrix(artists)]).tocsr()


short_csv_exists = os.path.exists("output_short_i.csv")
long_csv_exists = os.path.exists("output_long_ii.csv")

if short_csv_exists and long_csv_exists:
    df_one = pd.read_csv("output_short_i.csv")
    df_two = pd.read_csv("output_long_ii.csv")
    st.session_state.df_one = df_one
    st.session_state.df_two = df_two

    top1_song = df_one.iloc[0]["Song"] if len(df_one) > 0 else ""
    if st.session_state.recs is None or st.session_state.get("cached_top1") != top1_song:
        from logic import recommend_from_one
        short_matrix = build_vector_for_df(df_one)
        short_1_raw = recommend_from_one(short_matrix[0], top_k=5)

        long_matrix = build_vector_for_df(df_two)
        long_1_raw = recommend_from_one(long_matrix[0], top_k=5)

        idx_10_short = min(9, len(df_one) - 1) if len(df_one) > 0 else 0
        short_10_raw = recommend_from_one(short_matrix[idx_10_short], top_k=5)

        idx_10_long = min(9, len(df_two) - 1) if len(df_two) > 0 else 0
        long_10_raw = recommend_from_one(long_matrix[idx_10_long], top_k=5)

        st.session_state.recs = {
            "short_1": enrich_tracks(short_1_raw),
            "long_1": enrich_tracks(long_1_raw),
            "short_10": enrich_tracks(short_10_raw),
            "long_10": enrich_tracks(long_10_raw),
        }
        st.session_state.cached_top1 = top1_song
        st.session_state.hide = True


params = st.query_params
if "code" in params:
    code = params["code"]
    st.query_params.clear()

    cmd = [
        "curl",
        "-X", "POST",
        "https://accounts.spotify.com/api/token",
        "-H", "Content-Type: application/x-www-form-urlencoded",
        "-d", "grant_type=authorization_code",
        "-d", f"code={code}",
        "-d", "redirect_uri=http://127.0.0.1:8888/callback",
        "-u", f"{client_id}:{client_secret}",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    try:
        res1 = json.loads(res.stdout)
    except Exception as e:
        st.session_state.error = {"auth": f"Token exchange failed to parse response: {e}\n{res.stdout}"}
        st.rerun()

    if "access_token" in res1:
        token = res1["access_token"]
        set_key(".env", "TOKEN", token, quote_mode="never")
        os.environ["TOKEN"] = token
        st.session_state.error = None

        from spotify_json_handling import test
        df_one, df_two, data = test()
        st.session_state.df_one = df_one
        st.session_state.df_two = df_two

        df_one.to_csv("output_short_i.csv", index=False)
        df_two.to_csv("output_long_ii.csv", index=False)

        from logic import recommend_from_one
        short_matrix = build_vector_for_df(df_one)
        short_1_raw = recommend_from_one(short_matrix[0], top_k=5)

        long_matrix = build_vector_for_df(df_two)
        long_1_raw = recommend_from_one(long_matrix[0], top_k=5)

        idx_10_short = min(9, len(df_one) - 1) if len(df_one) > 0 else 0
        short_10_raw = recommend_from_one(short_matrix[idx_10_short], top_k=5)

        idx_10_long = min(9, len(df_two) - 1) if len(df_two) > 0 else 0
        long_10_raw = recommend_from_one(long_matrix[idx_10_long], top_k=5)

        st.session_state.recs = {
            "short_1": enrich_tracks(short_1_raw),
            "long_1": enrich_tracks(long_1_raw),
            "short_10": enrich_tracks(short_10_raw),
            "long_10": enrich_tracks(long_10_raw),
        }
        st.session_state.cached_top1 = df_one.iloc[0]["Song"] if len(df_one) > 0 else ""
        st.session_state.hide = True
        st.rerun()
    else:
        err_msg = res1.get("error_description", res1.get("error", "Unknown token exchange failure"))
        st.session_state.error = {"auth": f"Spotify authorization error: {err_msg}"}
        st.rerun()


def find_similar_short(song_name: str) -> None:
    from logic import recommend_from_one
    df_one = st.session_state.df_one
    if df_one is None or song_name not in df_one["Song"].values:
        st.session_state.error = {"picker": f"Track '{song_name}' not found in listening data."}
        return

    iloc_idx = df_one[df_one["Song"] == song_name].index[0]
    pos = df_one.index.get_loc(iloc_idx)
    short_matrix = build_vector_for_df(df_one)
    if pos < short_matrix.shape[0]:
        raw_recs = recommend_from_one(short_matrix[pos], top_k=5)
        st.session_state.picked_song = song_name
        st.session_state.custom_recs = enrich_tracks(raw_recs)
        st.session_state.picked_source = "short"
        st.session_state.error = None
    else:
        st.session_state.picked_song = song_name
        st.session_state.custom_recs = None
    st.rerun()


def find_similar_long(song_name: str) -> None:
    from logic import recommend_from_one
    df_two = st.session_state.df_two
    if df_two is None or song_name not in df_two["Song"].values:
        st.session_state.error = {"picker": f"Track '{song_name}' not found in listening data."}
        return

    iloc_idx = df_two[df_two["Song"] == song_name].index[0]
    pos = df_two.index.get_loc(iloc_idx)
    long_matrix = build_vector_for_df(df_two)
    if pos < long_matrix.shape[0]:
        raw_recs = recommend_from_one(long_matrix[pos], top_k=5)
        st.session_state.picked_song = song_name
        st.session_state.custom_recs = enrich_tracks(raw_recs)
        st.session_state.picked_source = "long"
        st.session_state.error = None
    else:
        st.session_state.picked_song = song_name
        st.session_state.custom_recs = None
    st.rerun()


top15_tracks = []
if st.session_state.df_one is not None and "Song" in st.session_state.df_one.columns:
    top15_tracks = st.session_state.df_one["Song"].head(15).tolist()

top5_long_tracks = []
if st.session_state.df_two is not None and "Song" in st.session_state.df_two.columns:
    top5_long_tracks = st.session_state.df_two["Song"].head(5).tolist()

ui.render_full_page(
    authed=st.session_state.hide,
    on_authorize=next_url,
    short_term_df=st.session_state.df_one,
    long_term_df=st.session_state.df_two,
    short_1_recs=st.session_state.recs.get("short_1") if st.session_state.recs else None,
    long_1_recs=st.session_state.recs.get("long_1") if st.session_state.recs else None,
    short_10_recs=st.session_state.recs.get("short_10") if st.session_state.recs else None,
    long_10_recs=st.session_state.recs.get("long_10") if st.session_state.recs else None,
    top15_short_tracks=top15_tracks,
    top5_long_tracks=top5_long_tracks,
    on_find_similar_short=find_similar_short,
    on_find_similar_long=find_similar_long,
    selected_song=st.session_state.picked_song,
    similar_tracks=st.session_state.custom_recs,
    selected_source=st.session_state.get("picked_source", "short"),
    error=st.session_state.error,
    loading=st.session_state.loading,
)