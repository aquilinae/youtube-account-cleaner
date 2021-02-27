"""
Known issues:
1. If there are more than 50 entities to interact script needed to run multiple times
"""

from globals import MY_CHANNEL_ID
from credentilas_getter import get_credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


"""
DOCS:
1. https://github.com/googleapis/google-api-python-client/blob/master/docs/start.md
2. https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.html
"""
with build(serviceName='youtube', version='v3', credentials=get_credentials()) as service:

    def __clear_playlist(playlist_name: str):
        """
        Clear playlist
        https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.playlists.html
        :param playlist_name: your playlist to clear.
        :return: None
        """
        playlists = service.playlists().list(part='snippet', mine=True).execute()
        for playlist in playlists['items']:
            if playlist['snippet']['title'] == playlist_name:
                playlist_id_to_clear = playlist['id']
                playlist_to_clear_content = service.playlistItems().list(
                    part='snippet', maxResults=100,
                    playlistId=playlist_id_to_clear
                ).execute()
                if playlist_to_clear_content and playlist_to_clear_content.get('items'):
                    for item in playlist_to_clear_content['items']:
                        service.playlistItems().delete(id=item['id']).execute()
                else:
                    print(f'Playlist "{playlist_name}" already empty')
                break
        else:
            print(f'No "{playlist_name}" playlist was found')

    def __remove_rating_from_all_videos(rate_type: str = 'like'):
        """
        Remove all rated from videos
        https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.videos.html
        :param rate_type: 'like' or 'dislike'
        :return: None
        """
        rated_videos = service.videos().list(part='snippet', myRating=rate_type, maxResults=50).execute()
        rated_videos = rated_videos['items']
        if rated_videos:
            for rated_video in rated_videos:
                rated_video_id = rated_video['id']
                rated_video_url = f'https://youtu.be/{rated_video_id}'
                try:
                    service.videos().rate(id=rated_video_id, rating='none').execute()
                    print(f'Remove rating for "{rated_video["snippet"]["title"]}" -> {rated_video_url}')
                except HttpError as e:
                    print(f'Unable to remove rating for video {rated_video_url} -> "{e.error_details}"')
        else:
            print(f'You have no "{rate_type}" rated videos')

    def __clear_watch_later_list():
        # Unable to do due to https://developers.google.com/youtube/v3/revision_history#january-28,-2021
        # Workaround https://gist.github.com/astamicu/eb351ce10451f1a51b71a1287d36880f#gistcomment-3535495
        raise NotImplementedError

    def __remove_all_subscriptions():
        """
        Remove all subscriptions
        https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.subscriptions.html
        :return: None
        """
        subscriptions = service.subscriptions().list(part='snippet', channelId=MY_CHANNEL_ID, maxResults=50).execute()
        subscriptions = subscriptions['items']
        if subscriptions:
            for subscription in subscriptions:
                service.subscriptions().delete(id=subscription['id']).execute()
                print(
                    f'Unsubscribed from "{subscription["snippet"]["title"]}" -> '
                    f'https://www.youtube.com/channel/{subscription["snippet"]["resourceId"]["channelId"]}'
                )
        else:
            print('You are not subscribed to anyone')

    def __remove_all_added_playlists():
        # Unable to do due to https://stackoverflow.com/a/36264839
        raise NotImplementedError

    print(
        '\nWhat do you want to do?'
        '\n1. Clear playlist'
        '\n2. Remove liked videos'
        '\n3. Clear "Watch later" list'
        '\n4. Remove all subscriptions'
        '\n5. Remove all added playlists'
    )
    option = input('Choose: ')
    if option == '1':
        __clear_playlist(input('Type a playlist to clear name: '))
    elif option == '2':
        __remove_rating_from_all_videos()
    elif option == '3':
        __clear_watch_later_list()
    elif option == '4':
        __remove_all_subscriptions()
    elif option == '5':
        __remove_all_added_playlists()
    else:
        raise ValueError('Unable to choose option -> possible variants are (1, 2, 3, 4, 5)')
