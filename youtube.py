from google_auth_oauthlib.flow import InstalledAppFlow as IAF
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from time import gmtime, strftime
from math import floor


SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


class AuthenticatedService:
    def __init__(self, client_secret_file):
        self.client_secret_file = client_secret_file

    def get_authenticated_service(self):
        flow = IAF.from_client_secrets_file(self.client_secret_file, SCOPES)
        credentials = flow.run_console()
        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def upload(video_file, request):
    service = AuthenticatedService('client_secret.json')
    service = service.get_authenticated_service()
    body = dict(
            snippet=dict(
                categoryId=request['category_id'],
                title=request['title'],
                titledescription=request['description'],
                tags=request['tags']
            ),
            status=dict(
                privacyStatus='public',
                selfDeclaredMadeForKids=False
            )
        )
    media = MediaFileUpload(video_file)
    return service.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    ).execute()


def get_video_timestamps(video_snippets_list):
    video_snippets_duration = []
    for video_snippet in video_snippets_list:
        video_snippets_duration.append(floor(video_snippet.duration))

    if sum(video_snippets_duration) >= 3600:
        format = '%H:%M:%S'
    else:
        format = '%M:%S'
    timestamps = ['00:00', strftime(format, gmtime(video_snippets_duration[0] + 1))]

    for idx in range(1, len(video_snippets_duration)):
        ts = video_snippets_duration[idx] + video_snippets_duration[idx-1]
        video_snippets_duration[idx] = ts
        timestamps.append(strftime(format, gmtime(ts + 1)))
    return timestamps[:-1]


def write_timestamps_desc(timestamps, titles):
    timestamp_titles = []
    for timestamp, title in zip(timestamps, titles):
        timestamp_titles.append(f"{timestamp} - {title}\n")

    with open('uploads/description.txt', 'r') as file:
        description = file.read()
    updated_description = description.replace('[timestamps]', ''.join(timestamp_titles))

    with open('uploads/description.txt', 'w') as file:
        file.write(updated_description)
