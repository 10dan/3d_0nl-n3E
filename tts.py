from pathlib import Path
from openai import OpenAI
from moviepy.editor import AudioFileClip, ImageClip

client = OpenAI()

# Path to your MP3 file
speech_file_path = Path(__file__).parent / "speech_onyx.mp3"
response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input="The sooner we stop listening to their messages, the sooner we will be liberated. I will speak for a long time, but. not. forever."
)

response.stream_to_file(speech_file_path)

# Load audio file
audio_clip = AudioFileClip(str(speech_file_path))
audio_duration = audio_clip.duration

# Desired dimensions for the video
width, height = 1080, 1920

# Load image and get its size
image_path = 'img.png'  # Replace with your image path
image_clip = ImageClip(image_path)
image_width, image_height = image_clip.size

# Calculate aspect ratios
video_aspect_ratio = width / height
image_aspect_ratio = image_width / image_height

# Crop image to match video aspect ratio
if image_aspect_ratio > video_aspect_ratio:
    # Image is wider than desired, crop horizontally
    new_width = int(image_height * video_aspect_ratio)
    x_center = image_width / 2
    cropped_image_clip = image_clip.crop(x1=x_center - new_width / 2, x2=x_center + new_width / 2, y1=0, y2=image_height)
else:
    # Image is taller than desired, crop vertically
    new_height = int(image_width / video_aspect_ratio)
    y_center = image_height / 2
    cropped_image_clip = image_clip.crop(x1=0, x2=image_width, y1=y_center - new_height / 2, y2=y_center + new_height / 2)

cropped_image_clip = cropped_image_clip.set_duration(audio_duration)

# Set the audio of the video clip as your mp3
video_clip = cropped_image_clip.set_audio(audio_clip)

# Output video file
video_clip.write_videofile('output_video.mp4', codec='libx264', fps=24)
