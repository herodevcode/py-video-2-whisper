import streamlit as st
from moviepy.editor import VideoFileClip
import whisper
import os
import tempfile
import imageio_ffmpeg as ffmpeg

st.title("Video to Transcription")

# Upload the video file
video_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi", "mkv"])

# Function to convert video to audio
def convert_video_to_audio(video_stream):
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmpfile:
        # Write the uploaded video file to a temporary file
        tmpfile.write(video_stream.read())
        tmpfile_path = tmpfile.name
    
    # Load the temporary video file with MoviePy and extract audio
    with VideoFileClip(tmpfile_path) as video:
        audio = video.audio
        # Define the audio file path
        audio_file_path = os.path.join(tempfile.gettempdir(), 'temp_audio.mp3')
        audio.write_audiofile(audio_file_path)
    # Remove the temporary video file
    os.unlink(tmpfile_path)
    return audio_file_path

# Function to transcribe audio using Whisper
def transcribe_audio(audio_path):
    model = whisper.load_model("base")  # You can change the model size as needed
    result = model.transcribe(audio_path)
    return result["text"]

if video_file is not None:
    # Convert video to audio and save the audio file path
    audio_file_path = convert_video_to_audio(video_file)

    with st.spinner('Transcribing audio...'):
        # Transcribe the audio file
        transcription = transcribe_audio(audio_file_path)

        # Remove the temporary audio file
        os.unlink(audio_file_path)

    # Display the transcription
    st.text_area("Transcription", transcription, height=300)