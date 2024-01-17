import sqlite3
import os
import config

os.environ['SPOTIPY_CLIENT_ID'] = config.SPOTIPY_CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = config.SPOTIPY_CLIENT_SECRET
os.environ['SPOTIPY_REDIRECT_URI'] = config.SPOTIPY_REDIRECT_URI


def get_messages():
    conn = sqlite3.connect(config.DB_PATH)
    cur = conn.cursor()

    sql = f"""
        select 
            m.text
        from message m
        join chat_message_join cmj
        on m.ROWID = cmj.message_id
        where cmj.chat_id = (SELECT ROWID FROM chat WHERE display_name = '{config.GROUP_CHAT}') and m.text is not null
    """
    cur.execute(sql)
    results = cur.fetchall()
    
    cur.close()
    conn.close()

    lst = [i[0] for i in results]
    return lst


def get_spotify_ids(messages):
    links = [text for text in messages if text.startswith('https://open.spotify.com/track')]
    
    spot_ids = [] 
    for link in links:  
            id = link.split("track/")[-1].split("?si=")[0]
            spot_ids.append(id)

    return spot_ids


def get_playlist_id(sp, playlist_name):
    data = sp.current_user_playlists()
    playlists = [p["name"] for p in data["items"]]
    id_dic = {i["name"]: i["id"] for i in data["items"]}

    try:
        return id_dic[playlist_name]
    except:
        return f"'{playlist_name}' does not exists."
    
def create_new_playlist_if_not_exists(sp):
    # Get current playlist
    data = sp.current_user_playlists()
    playlists = [p["name"] for p in data["items"]]

    # Create new playlist if it doesn't exists
    new_playlist = f"{config.GROUP_CHAT} GM"
    if new_playlist not in playlists:
        user_id = sp.me()['id']
        sp.user_playlist_create(user_id, new_playlist, description=f"This playlist was created from '{config.GROUP_CHAT}' iMessage group chat.")
        print(f"Created '{new_playlist}' playlist.\n")
    else:
        print(f"'{new_playlist}' already exists.\n")


    # Return id of new playlist
    id = get_playlist_id(sp, new_playlist)
    return id

def get_track_info(sp, id):
    data = sp.track(id)
    return (data["name"], data["uri"])


def add_tracks_to_playlist(sp, playlist_id, spot_ids_to_add):
    # Get dicionary of existing tracks
    data = sp.playlist_items(playlist_id)
    existing_tracks_dic = {item["track"]["id"] : item["track"]["name"] for item in data["items"]}

    # Adding songs to playlist
    for id in spot_ids_to_add:

        # If id not in the playlist then add it
        if id not in existing_tracks_dic.keys():
            track_name, track_uri = get_track_info(sp, id)
            sp.playlist_add_items(playlist_id, [track_uri])
            print(f"'{track_name}' added to playlist.")

        # If id in playlist skip
        else:
            print(f"'{existing_tracks_dic[id]}' already in playlist.")
