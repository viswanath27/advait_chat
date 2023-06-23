from googleapiclient.discovery import build

# Set up the YouTube Data API client
youtube = build('youtube', 'v3', developerKey='AIzaSyA7ho2TPkTfhoQj08TGcW8dxt86lhVlN9s')

# Retrieve video details
def get_video_summary(video_id):
    response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()

    # Extract relevant information from the response
    video = response['items'][0]
    title = video['snippet']['title']
    description = video['snippet']['description']
    channel_title = video['snippet']['channelTitle']
    published_at = video['snippet']['publishedAt']

    return title, description, channel_title, published_at


video_id = 'FsJuCOyglaE'  # Replace with the actual video ID
title, description, channel_title, published_at = get_video_summary(video_id)

print('Title:', title)
print('Description:', description)
print('Channel:', channel_title)
print('Published At:', published_at)
