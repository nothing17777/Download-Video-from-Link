import streamlit as st
import os

st.title("Supported Sites")

# Load the markdown file
try:
    file_path = "text_files/supportedsites.md"
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            content = f.readlines()
            
        st.write(f"Reference list of **{len(content)}** supported sites/extractors.")
        
        # Simple Search Mechanism
        search_term = st.text_input("🔍 Search for a site (e.g., 'youtube', 'bilibili')", "")
        
        if search_term:
            filtered_lines = []
            for line in content:
                # Case insensitive search
                if search_term.lower() in line.lower():
                    filtered_lines.append(line)
            
            if filtered_lines:
                st.success(f"Found {len(filtered_lines)} matches:")
                st.markdown("\n".join(filtered_lines))
            else:
                st.warning("No matches found.")
        else:
            # Display full content if no search
            with st.expander("View Full List", expanded=True):
                st.markdown("".join(content))
            
    else:
        st.error(f"Markdown file not found at: {file_path}")
        
except Exception as e:
    st.error(f"Error loading file: {str(e)}")
