import tkinter as tk
from tkinter import ttk
import threading
import os
from pytube import YouTube, Playlist

class YouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("450x400")

        self.option_label = tk.Label(root, text="Select Option:")
        self.option_label.pack()

        self.option_var = tk.StringVar()
        self.option_combobox = ttk.Combobox(root, textvariable=self.option_var, values=["Single Video", "More Videos", "Channel", "Playlist", "Short"])
        self.option_combobox.pack()

        self.link_label = tk.Label(root, text="Enter Video Link:")
        self.link_label.pack()

        self.link_entry = tk.Entry(root)
        self.link_entry.pack()

        self.path_label = tk.Label(root, text="Enter Save Path:")
        self.path_label.pack()

        self.path_entry = tk.Entry(root)
        self.path_entry.pack()

        self.log_text = tk.Text(root, height=10, width=50)
        self.log_text.pack()

        self.start_button = tk.Button(root, text="Start Download", command=self.start_download)
        self.start_button.pack()

        self.stop_button = tk.Button(root, text="Stop Download", command=self.stop_download)
        self.stop_button.pack()

        self.clear_button = tk.Button(root, text="Clear", command=self.clear_log)
        self.clear_button.pack()

        self.download_thread = None
        self.stop_event = threading.Event()

    def start_download(self):
        option = self.option_var.get()
        link = self.link_entry.get()
        path = self.path_entry.get()

        if not link or not path:
            self.log("Please enter video link and save path.")
            return

        if not os.path.exists(path):
            os.makedirs(path)

        if option == "Single Video":
            self.download_thread = threading.Thread(target=self.download_single_video, args=(link, path))
        elif option == "More Videos":
            self.download_thread = threading.Thread(target=self.download_more_videos, args=(link, path))
        elif option == "Channel":
            self.download_thread = threading.Thread(target=self.download_channel, args=(link, path))
        elif option == "Playlist":
            self.download_thread = threading.Thread(target=self.download_playlist, args=(link, path))
        elif option == "Short":
            self.download_thread = threading.Thread(target=self.download_short_videos, args=(link, path))

        self.stop_event.clear()
        self.download_thread.start()

    def stop_download(self):
        if self.download_thread and self.download_thread.is_alive():
            self.stop_event.set()
            self.log("Download stopped.")

    def clear_log(self):
        self.log_text.delete("1.0", tk.END)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")

    def download_single_video(self, link, path):
        self.log(f"Downloading Single Video from {link}...")
        yt = YouTube(link)
        stream = yt.streams.get_highest_resolution()
        stream.download(output_path=path)
        self.log("Single Video Downloaded.")

    def download_more_videos(self, link, path):
        self.log("Downloading More Videos...")
        # Implement your logic for downloading multiple videos here
        self.log("More Videos Downloaded.")

    def download_channel(self, link, path):
        self.log("Downloading Channel...")
        # Implement your logic for downloading entire channel here
        self.log("Channel Downloaded.")

    def download_playlist(self, link, path):
        self.log("Downloading Playlist...")
        playlist = Playlist(link)
        for video in playlist.video_urls:
            if self.stop_event.is_set():
                break
            yt = YouTube(video)
            stream = yt.streams.get_highest_resolution()
            stream.download(output_path=os.path.join(path, playlist.title))
            self.log(f"Video Downloaded: {yt.title}")
        self.log("Playlist Downloaded.")

    def download_short_videos(self, link, path):
        self.log("Downloading Short Videos...")

        # Importing necessary libraries
        from pytube import YouTube
        import re

        # Maximum duration for short videos (in seconds)
        max_duration = 300  # 5 minutes

        # Perform search on YouTube for the given query
        search_results = YouTube(link).streams.filter(adaptive=True)

        # Iterate over the search results and download short videos
        for video in search_results:
            # Extract video duration from metadata
            metadata = video.player_config_args['player_response']
            duration = int(metadata['videoDetails']['lengthSeconds'])

            if duration <= max_duration:
                stream = video.streams.get_highest_resolution()
                stream.download(output_path=path)
                self.log(f"Short Video Downloaded: {video.title}")

        self.log("Short Videos Downloaded.")

if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderApp(root)
    root.mainloop()
