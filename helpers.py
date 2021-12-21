import sys


def _exit():
    sys.exit()


def _video_source_allowed(video_snippet_url, sources):
    for source in sources:
        if source in video_snippet_url:
            return True
        else:
            return False
