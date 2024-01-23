import sqlite3
import os
import config
from typedstream.stream import TypedStreamReader


os.environ['SPOTIPY_CLIENT_ID'] = config.SPOTIPY_CLIENT_ID
os.environ['SPOTIPY_CLIENT_SECRET'] = config.SPOTIPY_CLIENT_SECRET
os.environ['SPOTIPY_REDIRECT_URI'] = config.SPOTIPY_REDIRECT_URI

BLACKLIST = []


def decode_messages(messages):
    lst = []
    for m in messages:

        if m is None:
            continue

        for event in TypedStreamReader.from_data(m):
            if type(event) is bytes:
                temp = event.decode("utf-8")
                temp = temp.split("__kIM")[0].strip()
                lst.append(temp)

    filtered_list = [item for item in lst if item != ""]

    return filtered_list


def get_messages():
    conn = sqlite3.connect(config.DB_PATH)
    cur = conn.cursor()

    sql = f"""
        select attributedBody from
        message where
        rowid in
        (select message_id
        from chat_message_join 
        where chat_id = 
        (SELECT ROWID FROM chat WHERE display_name = '{config.GROUP_CHAT}'))
    """

    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    conn.close()

    lst = [i[0] for i in results]
    decoded_lst = decode_messages(lst)

    # Removing duplicates
    final_messages = list(dict.fromkeys(decoded_lst))

    return final_messages


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

def get_all_existing_tracks(sp, playlist_id):
    offset = 0
    dic = {}
    while True:
        response = sp.playlist_items(playlist_id,
                                    offset=offset,
                                    fields='items.track.id,items.track.name',
                                    additional_types=['track'])

        if len(response['items']) == 0:
            break

        offset = offset + len(response['items'])

        data = response["items"]
        for i in data:
            dic[i["track"]["id"]] = i["track"]["name"]

    return dic
    

def add_tracks_to_playlist(sp, playlist_id, spot_ids_to_add):
    existing_tracks_dic = get_all_existing_tracks(sp, playlist_id)

    # Adding songs to playlist
    for id in spot_ids_to_add:

        # Handle blacklist
        if id in BLACKLIST:
            track_name, track_uri = get_track_info(sp, id)
            print(f"{track_name} is blacklisted.")
            continue

        # If id not in the playlist then add it
        if id not in existing_tracks_dic.keys():
            try:
                track_name, track_uri = get_track_info(sp, id)
            except Exception as e:
                # print(f"ERROR WITH {id}")
                continue

            sp.playlist_add_items(playlist_id, [track_uri])
            print(f"'{track_name}' added to playlist.")

        # If id in playlist skip
        else:
            pass
            # print(f"'{existing_tracks_dic[id]}' already in playlist.")
