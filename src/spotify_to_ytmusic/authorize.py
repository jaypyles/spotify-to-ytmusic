import spotipy
from spotipy.oauth2 import SpotifyOAuth
from ytmusicapi import YTMusic


def authorize():
    """
    Authenticate with Spotify and obtain an access token.

    This function uses the SpotifyOAuth class to authenticate with Spotify and obtain an access token.
    The access token is then returned and can be used to make API requests to Spotify.

    Parameters:
        None

    Returns:
        str: The access token obtained from Spotify, or None if authentication fails.
    """
    SCOPE = "user-library-read playlist-read-private"
    sp_oauth = SpotifyOAuth(scope=SCOPE, open_browser=True)

    # Obtain the access token using the embedded browser
    token_info = sp_oauth.get_cached_token()

    if not token_info:
        # Prompt the user to authenticate and authorize the application
        auth_url = sp_oauth.get_authorize_url()
        print(f"Please visit this URL to authorize the application: {auth_url}")

        # Wait for the user to complete the authentication process
        response = input("Enter the URL you were redirected to: ")
        code = sp_oauth.parse_response_code(response)

        # Exchange the authorization code for a token
        token_info = sp_oauth.get_access_token(code)

    if token_info:
        return token_info["access_token"]
    else:
        return None


def main():
    authorize()  # Authorize the application and get the access token


if __name__ == "__main__":
    main()
