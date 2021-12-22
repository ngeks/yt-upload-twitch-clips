import youtube_dl
import youtube as yt

from os import listdir, makedirs
from os.path import isfile, join, exists
from video_snippets import VideoSnippets
from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips

from datetime import datetime
now = datetime.now()
today = now.strftime('%Y-%m-%d')


def read_text_file(file):
    with open(file, 'r') as file:
        return file.read()


def get_video_snippets(video_snippets_dir):
    video_snippets = []
    for video in listdir(video_snippets_dir):
        if isfile(join(video_snippets_dir, video)):
            video_snippets.append(VideoFileClip(f"{video_snippets_dir}/{video}", target_resolution=(1080, 1920)))
    return video_snippets


def concatenate_video_snippets(video_file_name, video_snippets):
    output = concatenate_videoclips(video_snippets, method='compose')
    if not exists(f"uploads/{today}"):
        makedirs(f"uploads/{today}")
    output.write_videofile(f"uploads/{today}/{video_file_name}.mp4", fps=30)


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
    titles = video_snippets.data()['title']

    if links.empty:
        print("Your data is empty! :peepoExit:")
    else:
        video_file_name = input("Video File Name: ")
        print("\nTask: Downloading video snippets...")
        download_video_snippets(video_file_name, links)
        print("\nTask: Merging video snippets...")
        video_snippets_list = get_video_snippets(f"downloads/{video_file_name}")
        concatenate_video_snippets(video_file_name, video_snippets_list)
        print("\nTask: Set upload parameters")
        timestamps = yt.get_video_timestamps(video_snippets_list)
        yt.write_timestamps_desc(timestamps, titles)
        category_id = input("Category ID: ")
        video_title = input("Video Title: ")
        video_desc = read_text_file('uploads/description.txt')
        video_tags = read_text_file('uploads/tags.txt')
        print("\nTask: Authenticating video upload...")

        try:
            yt.upload(f"uploads/{today}/{video_file_name}.mp4", dict(
                            category_id=category_id,
                            title=video_title,
                            description=video_desc,
                            tags=video_tags))
        except Exception:
            print("\nError: Something went wrong contact the developer.")
        else:
            print("\nTask: Video is now being uploaded...")
            print("Goodbye! :) :peepoExit:")


if __name__ == '__main__':
    run(VideoSnippets('video_snippets.csv'))
