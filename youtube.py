import pandas

from google_auth_oauthlib.flow import InstalledAppFlow as IAF
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from time import gmtime, strftime


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


def upload(request, video_file):
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
                privacyStatus=request['privacy_status'],
                selfDeclaredMadeForKids=False
            )
        )
    media = MediaFileUpload(f"uploads/{video_file}")
    return service.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    ).execute()


def get_video_timestamps(video_snippets_list):
    if sum(video_snippets_list) >= 3600:
        format = '%H:%M:%S'
    else:
        format = '%M:%S'
    timestamps = ['00:00', strftime(format, gmtime(video_snippets_list[0] + 1))]

    video_snippets_duration = []
    for video_snippet in video_snippets_list:
        video_snippets_duration.append(video_snippet.duration)

    for idx in range(1, len(video_snippets_list)):
        ts = video_snippets_list[idx] + video_snippets_list[idx-1]
        video_snippets_list[idx] = ts
        timestamps.append(f"{strftime(format, gmtime(ts + 1))}")
    return timestamps[:-1]


def generate_timestamps_desc(timestamps, titles):
    pass