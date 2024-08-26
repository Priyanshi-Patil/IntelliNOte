#importing the necessary libraries
import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import base64
from pytube import YouTube
import requests

load_dotenv() 


genai.configure(api_key=os.getenv("AIzaSyDFBBcDzoXhOHtESxlBVW0nBUrNhd-Wpiw"))

## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url, language="en"):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e

## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

def get_binary_file_downloader_html(bin_file, file_label='File', file_name='file'):
    """
    Generates a link to download the given binary file.
    
    Parameters:
        bin_file: bytes - The binary file to download.
        file_label: str - Label of the download link (default: 'File').
        file_name: str - Name of the file to download (default: 'file').
    
    Returns:
        str: HTML code for downloading the file.
    """
    # Convert the binary file to base64
    bin_file_base64 = base64.b64encode(bin_file.encode()).decode()
    href = f'<a href="data:application/octet-stream;base64,{bin_file_base64}" download="{file_name}">{file_label}</a>'
    return href

st.title("IntelliNote")
st.write("Your study buddy to generate structured notes from a video.")
youtube_link = st.text_input("Enter YouTube Video Link: ")
# languages contain:[ English, Spanish, French, German, Italian, Japanese, Korean, Portuguese, Russian, Chinese(Simplified), Hindi, Marathi, Tamil, Telugu, Gujarati]
language = st.selectbox("Select Video Language:", ["English", "Spanish", "French", "German", "Italian", "Japanese", "Korean", "Portuguese", "Russian", "Chinese Simplified", "Hindi", "Marathi", "Tamil", "Telegu", "Gujarati"])

# Additional functionalities
max_summary_length = st.number_input("Maximum Summary Length (words):", min_value=500, max_value=50000, value=25000)
if youtube_link:
    try:
        video_id = youtube_link.split("=")[1]
        st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)
        yt = YouTube(youtube_link)
        thumbnail_url = yt.thumbnail_url
        response = requests.get(thumbnail_url, verify=True)
        st.image(response.content, caption="YouTube Thumbnail")
    except IndexError:
        st.warning("Invalid YouTube URL. Please enter a valid URL.")

if st.button("Generate My Notes"):
    try:
        transcript_text = extract_transcript_details(youtube_link, language)
    except Exception as e:
        st.error(f"Error extracting transcript: {str(e)}")
        st.stop()

    if transcript_text:
        st.markdown("# Original Transcript:")
        st.write(transcript_text)

        summary = generate_gemini_content(transcript_text, prompt=())
        
        summaries = summary.split("\n")
        
        st.markdown("Detailed Notes: ")
        for s in summaries:
            st.write(s)

        st.markdown("Export the notes:")
        download_text = "\n".join(summaries)
        st.markdown(get_binary_file_downloader_html(download_text, file_label="Download Text", file_name="summary.txt"), unsafe_allow_html=True)