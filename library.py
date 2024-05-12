import json
import mpv


def library_func(client):
    try:
        # Load the credentials from the file
        with open(".credentials.json", "r") as file:
            client.config.data["auth.ssl"] = True
            credentials = json.load(file)
            client.authenticate({"Servers": [credentials]}, discover=False)
            print('Library categories:')
            media_folders = client.jellyfin.get_media_folders()
            for folder in media_folders.get('Items', []):
                print(folder['Name'])
            choice = input('Do you want to explore a category? (y/n): ')
            if choice == "y":
                category = input('Enter the category name: ').lower()
                for folder in media_folders.get('Items', []):
                    if folder['Name'].lower() == category:
                        category_id = folder['Id']
                try:
                    # Dict to store media ID's for playback
                    media_dict = {}
                    # Grabs the relevant category ID for the user's choice
                    if category == "movies":
                        category = client.jellyfin.user_items(params={'Recursive': True, 'ParentId': category_id})
                        print('Movies:')
                        # Prints the movies in the category
                        for i, video in enumerate(category.get('Items', []), start=1):
                            print(f"{i}. {video['Name']}")
                            media_dict[i] = video['Id']
                        playback = input("Do you want to play a video (y/n): ")

                    elif category == "shows":
                        # Shows are handled differently due to season/episode structure.
                        # The user must select a show, then a season, then an episode.
                        category = client.jellyfin.user_items(params={'Recursive': False, 'ParentId': category_id})
                        print('TV Shows:')
                        for i, show in enumerate(category.get('Items', []), start=1):
                            print(f"{i}. {show['Name']}")
                            media_dict[i] = show['Id']
                        choice = input("Do you want to select a show (y/n): ")
                        if choice == "y":
                            show_num = int(input('Enter show number: '))
                            show_id = media_dict.get(show_num)
                            show = client.jellyfin.user_items(params={'Recursive': False, 'ParentId': show_id})
                            print('Seasons:')
                            for i, season in enumerate(show.get('Items', []), start=1):
                                print(f"{i}. {season['Name']}")
                                media_dict[i] = season['Id']
                            season_choice = input("Do you want to select a season (y/n): ")
                            if season_choice == "y":
                                season_num = int(input('Enter season number: '))
                                season_id = media_dict.get(season_num)
                                season = client.jellyfin.user_items(params={'Recursive': False, 'ParentId': season_id})
                                print('Episodes:')
                                for i, episode in enumerate(season.get('Items', []), start=1):
                                    print(f"{i}. {episode['Name']}")
                                    media_dict[i] = episode['Id']
                                playback = input("Do you want to play an episode (y/n): ")

                    elif category == "music":
                        # Music is handled differently due to album/song structure.
                        # The user must select an album then song to play.

                        # TODO: Figure out why MPV displays nothing when playing music.
                        category = client.jellyfin.user_items(params={'Recursive': False, 'ParentId': category_id})
                        print('Music: ')
                        for i, song in enumerate(category.get('Items', []), start=1):
                            print(f"{i}. {song['Name']}")
                            media_dict[i] = song['Id']
                        choice = input("Do you want to select an album (y/n): ")
                        if choice == "y":
                            album_num = int(input('Enter the album number: '))
                            album_id = media_dict.get(album_num)
                            album = client.jellyfin.user_items(params={'Recursive': False, 'ParentId': album_id})
                            print('Songs:')
                            for i, song in enumerate(album.get('Items', []), start=1):
                                print(f"{i}. {song['Name']}")
                                media_dict[i] = song['Id']
                            playback = input("Do you want to play a song (y/n): ")
                    if playback == "y":
                        # User must input the media ID to play the video.
                        video_num = int(input('Enter the media number: '))
                        video_id = media_dict.get(video_num)
                        # Plays the video in mpv
                        player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, osc=True)
                        player.register_key_binding("CLOSE_WIN", "quit")
                        player.fullscreen = True
                        player.play(client.jellyfin.video_url(video_id))

                        # Handles cleanly closing the video
                        player.wait_for_playback()
                        player.terminate()
                    else:
                        print('Exiting...')
                except:
                    print('ERROR: Invalid input!')

    # If credentials.json not found, prompt the user to login.
    except FileNotFoundError:
        print("ERROR: Please log in to the server first!")
