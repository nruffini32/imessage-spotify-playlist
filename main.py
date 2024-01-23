import spotipy
from spotipy.oauth2 import SpotifyOAuth
from utils import create_new_playlist_if_not_exists, get_messages, get_spotify_ids, add_tracks_to_playlist


def main():
    # Initialize spotipy instance
    scopes = "playlist-modify-public"
    sp = spotipy.Spotify(client_credentials_manager=SpotifyOAuth(scope=scopes))

    # Create new playlist if it doesn't exists
    playlist_id = create_new_playlist_if_not_exists(sp)

    # Get songs from imessage db established in config
    messages = get_messages()
    # print(messages)
    spot_ids = get_spotify_ids(messages)

    # Add songs to playlist
    add_tracks_to_playlist(sp, playlist_id, spot_ids)


if __name__ == "__main__":
    main()