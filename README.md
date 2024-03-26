# Spotify Playlist from iMessage Group Chat

### Overview
This project allows you to create a Spotify playlist with Spotify links sent in an iMessage group chat.
By filling out the config.py, you can run the main.py script to generate a Spotify playlist.

### Usage
1. Create an Application through the Twitter Developer Portal - https://developer.twitter.com/en
2. Configure config.py
  - `GROUP_CHAT` is the name of your iMessage group chat.
  - `DB_PATH` is the file path to your chat.db file. This sqlite database contains your iMessage data.
    - Default location is `"/Users/[profile_name]/Library/Messages/chat.db"`
  - `SPOTIPY_CLIENT_ID` `SPOTIPY_CLIENT_SECRET` `SPOTIPY_REDIRECT_URI` are your credentials from your Twitter Application.
3. Make sure the following dependencies are installed
  - `pytypedstream`
  - `spotipy`
4. Run main.py
  - On the first run you will be prompted with a SSO page to Spotify. All preceding runs will used this cached information.
  - A playlist named "[GROUP_CHAT] GM" will be created in your Spotify account with all the links sent in the specified group chat.


###### Disclaimer - Only Spotify links and iMessage group chats are currently supported.
