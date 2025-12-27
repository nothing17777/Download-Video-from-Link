# Streamlit Video Downloader

A minimal and powerful web application built with **Streamlit** and **yt-dlp** that allows users to download videos from thousands of supported websites directly to their computer.

## Features

- **Universal Downloader**: Paste a URL from YouTube, Bilibili, and [thousands of other sites](pages/supported_sites.py) to download video and audio.
- **Smart Previews**: Automatically fetches and displays video thumbnails, titles, views, and duration before downloading.
- **Background Processing**: Downloads are processed on the server and then served as a direct file download for the user.
- **Supported Sites Browser**: Includes a searchable list of all supported extraction sites.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nothing17777/Download-Video-from-Link.git
   cd Download-Video-from-Link
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install ffmpeg** (required for merging video and audio streams):
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```
   
   **Ubuntu/Debian:**
   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```
   
   **Windows:**
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Or use [Chocolatey](https://chocolatey.org/): `choco install ffmpeg`
   
   **Verify installation:**
   ```bash
   ffmpeg -version
   ```

## Usage

Run the Streamlit application:

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`.

## How it Works

1. **Enter URL**: Paste a link to a video.
2. **Preview**: The app extracts metadata using `yt-dlp`.
3. **Download**: The video is downloaded to a temporary location on the server.
4. **Save**: A "Save File" button appears, allowing you to save the final MP4 file to your local device.

## Technologies Used

- [Streamlit](https://streamlit.io/) - The fastest way to build data apps in Python.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - A command-line program to download videos from YouTube.com and other video platforms.
