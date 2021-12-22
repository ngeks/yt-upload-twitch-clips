import youtube_dl

from os import listdir
from os.path import isfile, join
from video_snippets import VideoSnippets
from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips
from time import gmtime, strftime


def get_video_snippets_timestamps(video_snippets_list):
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


def get_video_snippets(video_snippets_dir):
    video_snippets = []
    for video in listdir(video_snippets_dir):
        if isfile(join(video_snippets_dir, video)):
            video_snippets.append(VideoFileClip(f"{video_snippets_dir}/{video}", target_resolution=(1080, 1920)))
    return video_snippets


def concatenate_video_snippets(video_file_name, video_snippets):
    output = concatenate_videoclips(video_snippets, method='compose')
    output.write_videofile(f"uploads/{video_file_name}.mp4", fps=30)


def download_video_snippets(project_name, links):
    with youtube_dl.YoutubeDL(dict(outtmpl=f'downloads/{project_name}/%(id)s.%(ext)s')) as ydl:
        ydl.download(links)


def video_source_allowed(video_snippet_url, sources):
    for source in sources:
        if source in video_snippet_url:
            return True
        else:
            return False


def run(video_snippets):
    actions = ("view", "add", "remove", "clear", "proceed")
    sources = ("clips.twitch.tv", "youtu.be", "youtube.com", "facebook.com", "m.twitch.tv/clip")

    while True:
        action = input("What do you want to do? [view, add, remove, clear, proceed] -> ")

        if action not in actions:
            print("Invalid action. Try again.")
        elif action == 'proceed':
            break
        else:
            data = video_snippets.data()
            if data.empty and action != 'add':
                print(f"Error: Your data is empty there is nothing to {action}.\n")
            elif action == 'view':
                print(f"\n{video_snippets.data()}\n")
            elif action == 'add':
                video_snippet_url = input("Clip Link: ")
                if video_source_allowed(video_snippet_url, sources):
                    video_snippet_title = input("Clip Title: ")
                    video_snippets.add(video_snippet_title, video_snippet_url)
                    print("Video snippet has been added.\n")
                else:
                    print("Error: Video source is not allowed.\n")
            elif action == 'remove':
                try:
                    video_snippets.remove(int(input("Index: ")))
                except KeyError:
                    print("Error: Please enter a valid index number.\n")
                else:
                    print("Product has been removed.\n")
            elif action == 'clear':
                video_snippets.clear()
                print("Video snippets has been cleared.\n")

    # Proceed on downloading and merging video snippets
    links = video_snippets.data()['link']

    if links.empty:
        print("Your data is empty! :peepoExit:")
    else:
        video_file_name = input("Video File Name: ")
        print("\nDownloading video snippets...")
        download_video_snippets(video_file_name, links)
        print("\nMerging video snippets...")
        video_snippets_list = get_video_snippets(f"downloads/{video_file_name}")
        video_snippets_timestamps = get_video_snippets_timestamps(video_snippets_list)
        concatenate_video_snippets(video_file_name, video_snippets_list)
        print(video_snippets_timestamps)


if __name__ == '__main__':
    run(VideoSnippets('video_snippets.csv'))
