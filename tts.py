from pathlib import Path
from openai import OpenAI
from moviepy.editor import AudioFileClip, ImageClip
from datetime import datetime

client = OpenAI()
today = datetime.today().strftime("%Y%m%d")

message = """
    The sooner we stop listening to their messages, 
    the sooner we will be liberated...
    Like, Comment and subscribe to manipulate the algorithm.
    Share this message.
    """

speech_file_path = Path(__file__).parent / f"sound/speech_{today}.mp3"
response = client.audio.speech.create(model="tts-1", voice="onyx", input=message)

response.stream_to_file(speech_file_path)

# Load audio file
audio_clip = AudioFileClip(str(speech_file_path))
audio_duration = audio_clip.duration

# Desired dimensions for the video
width, height = 1080, 1920

# Load image and get its size
image_path = "imgs/1.png"  # Replace with your image path
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
    cropped_image_clip = image_clip.crop(
        x1=x_center - new_width / 2, x2=x_center + new_width / 2, y1=0, y2=image_height
    )
else:
    # Image is taller than desired, crop vertically
    new_height = int(image_width / video_aspect_ratio)
    y_center = image_height / 2
    cropped_image_clip = image_clip.crop(
        x1=0, x2=image_width, y1=y_center - new_height / 2, y2=y_center + new_height / 2
    )

cropped_image_clip = cropped_image_clip.set_duration(audio_duration)

# Set the audio of the video clip as your mp3
video_clip = cropped_image_clip.set_audio(audio_clip)

# Output video file
video_clip.write_videofile("out/output_video.mp4", codec="libx264", fps=24)
