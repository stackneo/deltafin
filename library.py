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
                print(folder['Id'])
            choice = input('Do you want to explore a category? (y/n): ')
            if choice == "y":
                # TODO: Scrape the ID automatically from the choosen category.
                # TODO: Find an alternative way of scraping TV shows and music categories.
                category_id = input('Enter the category ID: ')
                try:
                    # Searches through the library for that category ID and outputs it.
                    category = client.jellyfin.user_items(params={'Recursive': True, 'ParentId': category_id})
                    print('Media in the category:')
                    for video in category.get('Items', []):
                        print(video['Name'])
                        print(video['Id'])
                    choice = input("Do you want to play a video (y/n): ")
                    if choice == "y":
                        video_id = input('Enter the video ID: ')
                        try:
                            # Plays the video in mpv
                            player = mpv.MPV(input_default_bindings=True, input_vo_keyboard=True, osc=True)
                            player.register_key_binding("CLOSE_WIN","quit")
                            player.fullscreen = True
                            player.play(client.jellyfin.video_url(video_id))

                            # Handles cleanly closing the video
                            player.wait_for_playback()
                            player.terminate()
                        except:
                            print("Invalid video ID!")
                    else:
                        print('Exiting...')
                # TODO: Make the exception handling more specific.
                except:
                    print('ERROR: Invalid category ID!')

    # If credentials.json not found, prompt the user to login.
    except FileNotFoundError:
        print("ERROR: Please log in to the server first!")
