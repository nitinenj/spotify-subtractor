import spotipy
from dotenv import load_dotenv 
from dotenv import find_dotenv
import os
from spotipy.oauth2 import SpotifyClientCredentials

# .env is a file system that we can retreieve our client id and client secret from
load_dotenv(find_dotenv())
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

'''
    Authorization in APIs. 
    This application requests an access token from the API to actually use the API. 
    In order to get it from the API, we give the Accounts Service (in this case, 
    Spotify Accounts Service) a client id, client secret, and grant type. 
    Once we get this access token, our program can trade it to the API (in this case,
    Spotify Web API) and recieve the JSON Object of unscoped data from the API.

    Program gives client info for access token
    Program then gives access token for data
'''

# set up Spotify client credentials
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_playlist_tracks(playlist_url):
    # extract the playlist ID from the URL
    # split the URL based on the '/' character and get the last element
    playlist_id_with_query = playlist_url.split('/')[-1]
    playlist_id = playlist_id_with_query.split('?')[0]

    # get the playlist tracks via json
    results = sp.playlist_items(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

count_mandatory = 2
count = 0
want_another_song = False

list_playlist_url_name_songlist_artist = []

# requesting user to input playlist URLs

while (count < count_mandatory or want_another_song):
    '''
    playlist_url = (input('Enter valid playlist url: \n').strip())
    playlist_data_list = (get_playlist_tracks(playlist_url))
    playlist_name = (sp.playlist(playlist_url)['name'])
    '''

    playlist_url = None
    playlist_data_list = None
    playlist_name = None
    lock = True
    while(lock): # keeps asking so URL is correct
        try:
            playlist_url = (input('ENTER VALID PLAYLIST URL: \n').strip())
            playlist_data_list = (get_playlist_tracks(playlist_url))
            playlist_name = (sp.playlist(playlist_url)['name'])
            lock = False
        

            # convert data list into list of names
            playlist_song_names_list = []
            playlist_artist_list = []
            for song_data in playlist_data_list:
                playlist_song_names_list.append(song_data['track']['name'])
                playlist_artist_list.append(song_data['track']['artists'][0]['name'])

            print('ADDED:', playlist_name)
            list_playlist_url_name_songlist_artist.append((playlist_url, playlist_name, playlist_song_names_list, playlist_artist_list))
            
            count += 1

            if(count >= count_mandatory):
                str_input = input('ADD ANOTHER PLAYLIST FILTER? y/n: ').strip()
                if(str_input.capitalize == 'Y'):
                    want_another_song = True
                else:
                    want_another_song = False
        except:
            print('INVALID URL. ')
            lock = True 

# collected all required playlists, now must sort
        
sorted_list_playlist_url_name_songlist_artist = sorted(list_playlist_url_name_songlist_artist, key=lambda x: len(x[2]), reverse=True)

playlist_name_list = [item[1] for item in sorted_list_playlist_url_name_songlist_artist]

print(f"\nNow filtering the playlists mentioned below from the main playlist of \"{playlist_name_list[0]}\":\n{playlist_name_list[1:]}")


print("\n****************\n")

# now filter the data

# extract songs to filter from 2nd and onwards items in list
songs_and_artists_to_filter = [(song, artist) for playlist in sorted_list_playlist_url_name_songlist_artist[1:] for song, artist in zip(playlist[2], playlist[3])]

# filter songs from first playlist
filtered_songs_and_artists = [(song, artist) for song, artist in zip(sorted_list_playlist_url_name_songlist_artist[0][2], sorted_list_playlist_url_name_songlist_artist[0][3]) if (song, artist) not in songs_and_artists_to_filter]

# matching songs from first playlist
matching_songs_and_artists = [(song, artist) for song, artist in zip(sorted_list_playlist_url_name_songlist_artist[0][2], sorted_list_playlist_url_name_songlist_artist[0][3]) if (song, artist) in songs_and_artists_to_filter]

def format_output(list_song_artist):
    formatted_output = ""
    
    for i, (song, artist) in enumerate(list_song_artist, 1):
        column_num = 2
        phrase = song + ", " + artist
        formatted_output += "{: <64}".format(phrase)
        
        if i % column_num == 0:
            formatted_output += '\n'
    
    return formatted_output

print('>>> ==========The', len(matching_songs_and_artists), 'songs of', playlist_name_list[0], 'that would be taken out: ==========\n')
print(format_output(matching_songs_and_artists))

print('>>> ==========The', len(filtered_songs_and_artists), 'songs that', playlist_name_list[0], 'would have left over: ==========\n')
print(format_output(filtered_songs_and_artists))

