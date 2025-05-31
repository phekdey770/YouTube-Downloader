import os
import threading
import tkinter as tk
from tkinter import messagebox, filedialog
from pytube import YouTube

def download_youtube_short(video_url, save_path, result):
    try:
        yt = YouTube(video_url)
        ys = yt.streams.get_highest_resolution()

        # Fix encoding issues by ignoring characters that can't be encoded
        title = yt.title.encode('ascii', 'ignore').decode('ascii')

        print(f"Downloading: {title}")
        ys.download(save_path)
        print("Download completed!")
        result.append(f"Downloaded: {title}")
    except KeyError:
        print(f"An error occurred: {video_url} is age restricted, and can't be accessed without logging in.")
        result.append(f"Error: {video_url} is age restricted, and can't be accessed without logging in.")
    except Exception as e:
        print(f"An error occurred: {e}")
        result.append(f"An error occurred: {e}")

def start_download():
    urls = text_urls.get("1.0", tk.END).strip().split()
    save_path = entry_path.get()

    if not urls:
        messagebox.showwarning("Warning", "Please enter video URLs.")
        return

    if not save_path:
        messagebox.showwarning("Warning", "Please select a save path.")
        return

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    result = []

    def download_videos():
        for video_url in urls:
            download_youtube_short(video_url, save_path, result)
        
        messagebox.showinfo("Download Completed", "\n".join(result))

    threading.Thread(target=download_videos).start()

def browse_directory():
    folder_selected = filedialog.askdirectory()
    entry_path.delete(0, tk.END)
    entry_path.insert(0, folder_selected)

# Create the main window
root = tk.Tk()
root.title("YouTube Shorts Downloader")

# URL label and text box
label_urls = tk.Label(root, text="Enter YouTube Shorts URLs (one per line):")
label_urls.pack()

text_urls = tk.Text(root, height=10, width=50)
text_urls.pack()

# Path label and entry box
label_path = tk.Label(root, text="Save Path:")
label_path.pack()

entry_path = tk.Entry(root, width=50)
entry_path.pack()

# Browse button
button_browse = tk.Button(root, text="Browse", command=browse_directory)
button_browse.pack()

# Download button
button_download = tk.Button(root, text="Download", command=start_download)
button_download.pack()

# Run the GUI event loop
root.mainloop()
