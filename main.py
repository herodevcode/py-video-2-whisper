import streamlit as st
from moviepy.editor import VideoFileClip
import whisper

# Define the path for saving the audio file
AUDIO_FILE_PATH = "temp_audio.mp3"

st.title("Video to Transcription")

# Upload the video file
video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])

# Function to convert video to audio
def convert_video_to_audio(video_file):
    with VideoFileClip(video_file.name) as video:
        audio = video.audio
        audio.write_audiofile(AUDIO_FILE_PATH)

# Function to transcribe audio using Whisper
def transcribe_audio(audio_path):
    model = whisper.load_model("base")  # You can change the model size as needed
    result = model.transcribe(audio_path)
    return result["text"]

if video_file is not None:
    # Show a placeholder while processing the file
    with st.spinner('Converting video to audio...'):
        convert_video_to_audio(video_file)

    with st.spinner('Transcribing audio...'):
        transcription = transcribe_audio(AUDIO_FILE_PATH)

    # Display the transcription
    st.text_area("Transcription", transcription, height=300)

if __name__ == '__main__':
    st.run()
