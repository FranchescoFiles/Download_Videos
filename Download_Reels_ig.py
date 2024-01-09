import instaloader
import PySimpleGUI as sg
from pathlib import Path
from tkinter import Tk, filedialog
import shutil
import concurrent.futures

# Create an instance of Instaloader class
L = instaloader.Instaloader()

# Define function to download reel
def download_reel(reel_url, download_directory):
    try:
        post = instaloader.Post.from_shortcode(L.context, reel_url.split("/")[-2])

        # Download the video directly to the current working directory
        L.download_post(post, target=download_directory)

        # Construct the source and target file paths
        source_file = download_directory / f"{post.owner_username}_{post.shortcode}.mp4"
        target_file = download_directory / f"{post.shortcode}.mp4"

        # Move the downloaded file to the desired location
        shutil.move(source_file, target_file)

        return True, target_file
    except Exception as e:
        print(f"Error downloading reel: {e}")
        return False, None

def download_reels(values):
    reel_urls = values['-URLS-'].split('\n')

    # Open a Tkinter window to select the download directory
    root = Tk()
    root.withdraw()  # Hide the main window
    download_directory = Path(filedialog.askdirectory(title="Select download directory"))

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(download_reel, reel_urls, [download_directory]*len(reel_urls)))

    if all(results):
        sg.Popup('Success', 'All reels downloaded successfully.')
    else:
        sg.Popup('Error', 'One or more reels failed to download.')

# Define GUI layout
layout = [
    [sg.Text('Enter Instagram Reel URLs (one URL per line):')],
    [sg.Multiline(size=(50, 10), key='-URLS-')],
    [sg.Text('-----------------'), sg.Text('', key='-SELECTED_DIR-')],
    [sg.Button('Download Reels'), sg.Button('Exit')]
]

# Create GUI window
window = sg.Window('Instagram Reel Downloader', layout)

# Event loop to process "Download Reels" and "Exit" buttons
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Download Reels':
        download_reels(values)
    elif event == '-DIR-':
        window['-SELECTED_DIR-'].update(values['-DIR-'])

# Close GUI window
window.close()
