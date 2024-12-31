import streamlit as st
from dotenv import load_dotenv

load_dotenv() ##load all the nevironment variables
import os
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi

from youtube_transcript_api._errors import TranscriptsDisabled

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt="""You are a professional summarizer for educational content. 
Take the transcript of a YouTube video and create a concise summary. 

Guidelines:
- Summarize in bullet points.
- Highlight only the key points related to the topic.
- Keep the summary under 250 words.

Transcript:
{transcript}

Please generate the summary:  """


## getting the transcript data from yt videos
def extract_transcript_details(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript
    
    except TranscriptsDisabled:
        st.error("Transcripts are disabled for this video. Please try another video.")
        return None

    except Exception as e:
         st.error(f"An error occurred: {str(e)}")
         raise e
    
## getting the summary based on Prompt from Google Gemini Pro
def generate_gemini_content(transcript_text,prompt):

    model=genai.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

st.title("Educational Video Summarizer")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)

if st.button("Get Detailed Notes"):
    transcript_text=extract_transcript_details(youtube_link)

    if transcript_text:
        summary=generate_gemini_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)
