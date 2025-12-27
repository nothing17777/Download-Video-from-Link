import streamlit as st
from urls import preview_video_based_on_url, download_video_based_on_url

def format_duration(s):
    if not s:
        return "0:00"
    s = int(s)
    return f"{s//60}:{s%60:02d}" if s < 3600 else f"{s//3600}:{(s%3600)//60:02d}:{s%60:02d}"

st.title("Download Video Based on URL")

st.write("Enter the URL of the video you want to download")

# Initialize session state
if 'video_data' not in st.session_state:
    st.session_state.video_data = None
if 'filename' not in st.session_state:
    st.session_state.filename = None
if 'last_preview_url' not in st.session_state:
    st.session_state.last_preview_url = ""
if 'video_info' not in st.session_state:
    st.session_state.video_info = None

# Input URL block
with st.container(border=True):
    col1, col2 = st.columns([0.8, 0.2], vertical_alignment="bottom")
    with col1:
        url = st.text_input("URL")
    with col2:
        if st.button("Load Video Data", use_container_width=True):
            if url:
                with st.spinner("Fetching video info..."):
                    try:
                        info = preview_video_based_on_url(url)
                        if info:
                            st.session_state.video_info = info
                            st.session_state.last_preview_url = url
                            # Reset download data for new video
                            st.session_state.video_data = None
                            st.session_state.filename = None
                        else:
                            st.error("Could not fetch video info.")
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                 st.warning("Please enter a URL first.")

# Display Info & Download Block
if st.session_state.video_info:
    video_info = st.session_state.video_info
    
    # Check if URL changed manually without clicking download
    if url != st.session_state.last_preview_url and url != "":
         st.warning("URL changed. Click 'Download' above to update info.")

    title = video_info.get("title")
    author = video_info.get("author")
    thumbnail = video_info.get("thumbnail")
    views = video_info.get("views")
    duration = format_duration(video_info.get("duration"))

    col1, col2 = st.columns([0.5, 0.5])
    
    # Left Column: Information
    with col1:
        with st.container(border=True, height=750):
            st.subheader("Information")
            
            # Video Preview
            with st.container(border=True):
                st.write("**Video Preview**")
                if video_info.get("video"):
                    video_html = f"""
                    <video width="100%" controls poster="{thumbnail}">
                        <source src="{video_info.get('video')}" type="video/mp4">
                        Your browser does not support the video tag.
                    </video>
                    """
                    st.markdown(video_html, unsafe_allow_html=True)
                else:
                    st.error("Video preview unavailable.")
                st.caption("⚠️ Preview may fail on some platforms.")

                # Audio Preview
                st.write("**Audio Preview**")
                if video_info.get("audio"):
                    st.audio(video_info.get("audio"))
                else:
                     st.caption("Audio preview unavailable.")
            
            # Thumbnail
            with st.container(border=True):
                st.write("**Thumbnail**")
                if thumbnail:
                    st.image(thumbnail, use_container_width=True)
            
            # Details
            with st.container(border=True):
                st.write(f"**Title:** {title}")
                st.write(f"**Author:** {author}")
                st.write(f"**Views:** {views:,}" if views else "**Views:** N/A")
                st.write(f"**Duration:** {duration}")

    # Right Column: Download
    with col2:
        with st.container(border=True, height=750):
            st.subheader("Download")
            
            # Automatically prepare download if we don't have data yet
            if st.session_state.video_data is None:
                with st.spinner("Preparing video for download..."):
                    try:
                        # Download using the URL from the loaded info to ensure consistency
                        video_bytes, fname = download_video_based_on_url(url)
                        
                        if video_bytes:
                            st.session_state.video_data = video_bytes
                            st.session_state.filename = fname
                            st.rerun()
                        else:
                            st.error("Failed to download video.")
                    except Exception as e:
                        st.error(f"Download failed: {str(e)}")
            
            # If data is ready (or if the auto-download above succeeded and reran)
            if st.session_state.video_data is not None:
                st.success("✅ Video is ready!")
                
                with st.container(border=True):
                    # Center align the text and button
                    d_col1, d_col2 = st.columns([0.65, 0.35], vertical_alignment="center")
                    with d_col1:
                        st.write("**Download Video with audio**")
                    with d_col2:
                         st.download_button(
                            label="⬇️ Save File",
                            data=st.session_state.video_data,
                            file_name=st.session_state.filename,
                            mime="video/mp4",
                            use_container_width=True
                        )
                
                # Reset button
                if st.button("Start New Download", use_container_width=True):
                    st.session_state.video_data = None
                    st.session_state.filename = None
                    st.session_state.video_info = None
                    st.rerun()