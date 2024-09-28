# spotify-to-ytmusic

Transfer liked songs from your Spotify account to your YouTube Music account.

## Setup 

Must have [pdm](https://pdm-project.org) installed

Install dependencies using `pdm install`

Create an app in the [Spotify developer dashboard](https://developer.spotify.com/)

Create the `auth_headers.json` and `.env` files in the root of the project

For information about how to get the `auth_headers.json`, visit [ytmusicapi docs](https://ytmusicapi.readthedocs.io/en/stable/setup/browser.html)

```env
SPOTIPY_CLIENT_ID="your-client-id"
SPOTIPY_CLIENT_SECRET="your-client-secret"
SPOTIPY_REDIRECT_URI="your-redirect-uri"
```

## Usage

Authenticate to Spotify using `pdm run python src/spotify_to_ytmusic/authorize.py`

Run `pdm run python src/spotify_to_ytmusic/__main__.py` to transfer liked songs from your Spotify account to your YouTube Music account.




