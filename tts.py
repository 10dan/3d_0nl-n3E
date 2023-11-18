from pathlib import Path
from openai import OpenAI
from moviepy.editor import AudioFileClip, ColorClip

client = OpenAI()

speech_file_path = Path(__file__).parent / "speech_onyx.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="onyx",
  input="The sooner we stop listening to their messages, the sooner we will be liberated. i will speak for a long time, but. not. forever."
)

response.stream_to_file(speech_file_path)



audio_clip = AudioFileClip(str(speech_file_path))
audio_duration = audio_clip.duration

# Create a black screen with the aspect ratio of a phone screen (9:16)
# Adjust the width and height as needed
width = 1080
height = 1920
color = (1,0,0)  # Black

video_clip = ColorClip(size=(width, height), color=color, duration=audio_duration)

# Set the audio of the video clip as your mp3
video_clip = video_clip.set_audio(audio_clip)

# Replace 'output_video.mp4' with your desired output file name
video_clip.write_videofile('output_video.mp4', codec='libx264', fps=24)
