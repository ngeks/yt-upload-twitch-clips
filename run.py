
from helpers import _exit
from helpers import _video_source_allowed
from video_snippets import VideoSnippets


def run(video_snippets):
    actions = ("view", "add", "remove", "clear", "exit")
    sources = ("clips.twitch.tv", "youtu.be", "youtube.com", "facebook.com", "m.twitch.tv/clip")

    while True:
        action = input("What do you want to do? [view, add, remove, clear, exit] -> ")

        if action not in actions:
            print("Invalid action. Try again.")
        elif action == 'exit':
            print("\nNeed help? Send me an email at ngeksdev@gmail.com")
            print("Goodbye! :) *peepoExit*")
            _exit()
        else:
            data = video_snippets.data()
            if data.empty and action != 'add':
                print(f"Error: Your data is empty there is nothing to {action}.\n")
            elif action == 'view':
                print(f"\n{video_snippets.data()}\n")
            elif action == 'add':
                video_snippet_url = input("Clip Link: ")
                if _video_source_allowed(video_snippet_url, sources):
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


if __name__ == '__main__':
    run(VideoSnippets('video_snippets.csv'))
