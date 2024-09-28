import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic
import os
import time
from dotenv import load_dotenv
from typing import Any

load_dotenv()

SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URI = os.environ["SPOTIPY_REDIRECT_URI"]
SCOPE = "user-library-read playlist-read-private"

sp_oauth = SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SCOPE,
    cache_path=".cache",
)
ytmusic = YTMusic("headers_auth.json")


def check_token():
    token_info = sp_oauth.get_cached_token()

    if not token_info:
        print("Error: No valid token found in cache. Please authenticate first.")
        exit(1)

    if sp_oauth.is_token_expired(token_info):
        print("Token expired, refreshing token...")
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])

    return token_info


def auth_spotify(token_info: dict[str, Any]):
    SPOTIFY_TOKEN = token_info["access_token"]
    return spotipy.Spotify(auth=SPOTIFY_TOKEN)


def create_yt_music_liked_songs(sp: spotipy.Spotify):
    i = 100
    liked_songs = sp.current_user_saved_tracks(limit=50, offset=i)["items"]

    while liked_songs:
        for song in liked_songs:
            song_title = song["track"]["name"]
            song_artist = song["track"]["artists"][0]["name"]

            # Search for the song on YouTube Music
            search_results = ytmusic.search(
                query=f"{song_title} {song_artist}", filter="songs"
            )

            if search_results:
                first_result = search_results[0]
                song_id = first_result["videoId"]
                print(
                    f"Found YouTube Music song: {first_result['title']} by {song_artist}"
                )
                ytmusic.rate_song(song_id, "LIKE")  # add song to 'liked songs'
            else:
                print(f"Could not find {song_title} by {song_artist} on YouTube Music")

            time.sleep(0.5)  # Add a 0.5 second delay between requests for rate limiting

        i += 50
        liked_songs = sp.current_user_saved_tracks(limit=50, offset=i)["items"]


def main():
    token_info = check_token()
    sp = auth_spotify(token_info)
    create_yt_music_liked_songs(sp)


if __name__ == "__main__":
    main()
