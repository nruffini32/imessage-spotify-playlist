# Spotify Playlist from iMessage Group Chat

### Overview
This project allows you to create a Spotify playlist with Spotify links sent in an iMessage group chat.
By filling out the config.py, you can run the main.py script to generate a Spotify playlist.

Must run this on a Mac with iMessage enabled.

### Usage
1. Create an Application through the Spotify Developer Portal - https://developer.spotify.com/
2. Clone this directory with `git clone`
3. Configure config.py
  - `GROUP_CHAT` is the name of your iMessage group chat.
  - `DB_PATH` is the file path to your chat.db file. This sqlite database that contains your iMessage data.
    - Default location is `"/Users/[profile_name]/Library/Messages/chat.db"`
  - `SPOTIPY_CLIENT_ID` `SPOTIPY_CLIENT_SECRET` `SPOTIPY_REDIRECT_URI` are your credentials from your Spotify Application.
3. cd into the directory and run the following commands to install dependencies
  ```
  cd path/to/imessage-spotify-playlist/
  python3 -m venv <your-env>
  source <your-env>/bin/activate
  pip3 install -r requirements.txt
  ```
4. Run main.py - `python3 main.py`
  - You will be redirected to a URL you specified in the Spotify dev portal and will be prompted to enter that url.
  - A playlist named "[GROUP_CHAT] GM" will be created in your Spotify account with all the links sent in the specified group chat.

Any following runs will add songs to that existing playlist. 

###### Disclaimer - Only Spotify links and iMessage group chats are currently supported.
