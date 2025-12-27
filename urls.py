import yt_dlp
import tempfile
import os

ydl_opts = {
    'format': 'best[ext=mp4]/best',  # Prefer single-file formats to avoid merging issues
    'outtmpl': '%(title)s.%(ext)s',
    'sleep_interval': 1,
    'merge_output_format': 'mp4',
    'quiet': True,
    'noplaylist': True,
    'no_warnings': True,
    'nocheckcertificate': True,  # Bypass SSL certificate verification
    'geo_bypass': True,  # Try to bypass geographic restrictions
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-us,en;q=0.5',
        'Sec-Fetch-Mode': 'navigate',
    }
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
                'quiet': False,  # Enable output for debugging
                'verbose': True,  # More detailed output
            }
            
            with yt_dlp.YoutubeDL(ydl_opts_temp) as ydl:
                # Get video info and download
                print(f"Attempting to download: {url}")
                info = ydl.extract_info(url, download=True)
                
                if not info:
                    print("Failed to extract video info")
                    return None, None
                
                # Get the filename that was created
                filename = ydl.prepare_filename(info)
                print(f"Expected filename: {filename}")
                
                # Check if file exists
                if not os.path.exists(filename):
                    print(f"File not found at: {filename}")
                    # Try to find any file in the temp directory
                    files = os.listdir(temp_dir)
                    print(f"Files in temp dir: {files}")
                    if files:
                        filename = os.path.join(temp_dir, files[0])
                    else:
                        return None, None
                
                # Check file size
                file_size = os.path.getsize(filename)
                print(f"File size: {file_size} bytes")
                
                if file_size == 0:
                    print("ERROR: Downloaded file is empty")
                    return None, None
                
                # Read the file as bytes
                with open(filename, 'rb') as f:
                    video_bytes = f.read()
                
                print(f"Successfully read {len(video_bytes)} bytes")
                
                # Return bytes and the original filename
                return video_bytes, os.path.basename(filename)      
    except Exception as e:
        print(f"Error downloading: {e}")
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    print(preview_video_based_on_url("https://www.bilibili.com/video/BV1uxs8zLEMB"))