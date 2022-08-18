import subprocess
import sys
import os
import signal
try:
    import argparse
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", argparse])
from pytube.cli import on_progress


parser = argparse.ArgumentParser()
parser.add_argument('--playlist', type=str, help="Download playlist")
parser.add_argument('--channel', type=str, help="Download channel")
parser.add_argument('--video', type=str, help="Download one video")
parser.add_argument('--path', type=str, help="Destination folder (absolute  path)")

args = parser.parse_args()
#Defaut path setup
default_path = f"{os.path.expanduser('~')}/Downloads"


def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y' or res == "Y":
        exit(1)


signal.signal(signal.SIGINT, handler)

# Download playlist
if args.playlist:
    from pytube import Playlist
    p = Playlist(args.playlist)
    p_len = p.length
    path = args.path if args.path else f"{default_path}/{p.title}"
    print(f"Downloading {p.title} playlist in {path}")
    for index, video in enumerate(p.videos):
        title = video.title.replace('/', "_")
        print(f"-  {index+1}/{p_len} Downloadind {title}")
        video.register_on_progress_callback(on_progress)
        video.streams.get_highest_resolution().download(output_path=path,
                                                        filename=f"{index+1} - {title}.mp4")

# Download channel
elif args.channel:
    from pytube import Channel
    channel = Channel(args.channel)
    p_len = channel.length
    path = args.path if args.path else f"{default_path}/{channel.title}"
    print(f"Downloading {channel.title} channel in {path}")
    for index, video in enumerate(channel.videos):
        title = video.title.replace('/', "_")
        print(f"-  {index+1}/{p_len} Downloadind {title}")
        video.register_on_progress_callback(on_progress)
        video.streams.get_highest_resolution().download(output_path=path,
                                                        filename=f"{index+1} - {title}.mp4")

# Single video download
elif args.video:
    from pytube import YouTube as YT
    video = YT(args.video)
    title = video.title
    path = args.path if args.path else f"{default_path}/{title}"
    print(f"Downloadind {title} video in {path}")
    video.register_on_progress_callback(on_progress)
    video.streams.get_highest_resolution().download(output_path=path,
                                                    filename=f"{title}.mp4")



# Default 
else:
    print("Use --playlist or --channel or --video")
