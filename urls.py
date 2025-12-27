import yt_dlp
import tempfile
import os

ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'sleep_interval': 1,
    'merge_output_format': 'mp4',
    'quiet': True,
    'noplaylist': True,
    "quiet": True,
    "no_warnings": True
}

def preview_video_based_on_url(url):
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # download=True ensures it downloads AND returns the info dict
            info = ydl.extract_info(url, download=False)
            # Extract video/audio URLs
            video_url = info.get("url")
            audio_url = info.get("url")
            
            if 'requested_formats' in info:
                for fmt in info['requested_formats']:
                    if fmt.get('vcodec') != 'none':
                        video_url = fmt.get('url')
                    if fmt.get('acodec') != 'none':
                        audio_url = fmt.get('url')
            return {
                "title": info.get("title"),
                "author": info.get("uploader"),
                "thumbnail": info.get("thumbnail"),
                "views": info.get("view_count"),
                "duration": info.get("duration"),
                "description": info.get("description"),
                "video": video_url,
                "audio": audio_url
            }
    except Exception as e:
        print(f"Error downloading: {e}")
        return None

def download_video_based_on_url(url):
    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            # Update ydl_opts to download to temp directory
            ydl_opts_temp = {
                **ydl_opts,  # Keep your existing options
                'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            }
            
            with yt_dlp.YoutubeDL(ydl_opts_temp) as ydl:
                # Get video info and download
                info = ydl.extract_info(url, download=True)
                
                # Get the filename that was created
                filename = ydl.prepare_filename(info)
                
                # Read the file as bytes
                with open(filename, 'rb') as f:
                    video_bytes = f.read()
                
                # Return bytes and the original filename
                return video_bytes, os.path.basename(filename)      
    except Exception as e:
        print(f"Error downloading: {e}")
        return None, None

if __name__ == "__main__":
    print(preview_video_based_on_url("https://www.bilibili.com/video/BV1uxs8zLEMB"))