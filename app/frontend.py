import streamlit as st
import requests
import os

st.set_page_config(page_title="Lecture Synthesizer", page_icon="🎙️")

st.title("AI Lecture Synthesizer")
st.markdown("Upload a recording to get a summary and action items in Notion.")

uploaded_file = st.file_uploader("Upload audio or video", type=['mp3', 'wav', 'mp4', 'm4a'])

if uploaded_file is not None:
    st.audio(uploaded_file)
    
    if st.button("Process and Sync to Notion"):
        with st.spinner("Transcribing and analyzing..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
            
            try:
                response = requests.post("http://localhost:8000/process-lecture", files=files)
                
                if response.status_code == 200:
                    st.success("Success! The pipeline has started. Check your Notion board in a minute.")
                    st.balloons()
                else:
                    st.error(f"Error: {response.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")

st.info("Ensure the FastAPI server is running before clicking process.")