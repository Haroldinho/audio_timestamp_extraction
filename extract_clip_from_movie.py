from moviepy import VideoFileClip

# Load the video
# video from BBC Earth DB
bbc_video_path = "input_videos/planet_earth_01_from_pole_to_pole.mp4"
video = VideoFileClip(bbc_video_path)

# Define start and end times (in seconds)
start_time = 2060  # start at 130s
end_time = 2075  # end at 145s

# Cut the clip
clip = video.subclipped(start_time, end_time)

# Write the result to a file
clip_name = f"input_clips/planet_earth_01_from_pole_to_pole_clip_{start_time}_{end_time}.mp4"
clip.write_videofile(clip_name, codec="libx264", audio_codec="aac")
