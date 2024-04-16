
import os
import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips
import subprocess
from pathlib import Path

def create_folder(folder_path):
    try:
        Path(folder_path).mkdir(parents=True, exist_ok=True)
        print(f"Folder '{folder_path}' created successfully.")
    except OSError as e:
        print(f"Error creating folder '{folder_path}': {e}")

def combine_videos(folder_path, output_path,compression_codec='libx264', crf=23):
    
    video_clips = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".avi"):  # Assuming all videos are in avi format
            try:
                clip = VideoFileClip(os.path.join(folder_path, filename))
                video_clips.append(clip)
            except Exception as e:
                print(f"Error reading video file '{filename}': {e}")

    if not video_clips:
        print("No valid video files found in the folder.")
        return

    final_clip = concatenate_videoclips(video_clips)
    final_clip.write_videofile(output_path, codec='libx264', temp_audiofile='temp-audio.m4a', remove_temp=True)
    final_clip.close()

    # Compress the video using FFmpeg
    subprocess.run(['ffmpeg', '-y','-i', output_path, '-c:v', compression_codec, '-crf', str(crf), '-preset', 'medium', f"./outputs/output{datetime.datetime.now().strftime('%d-%m-%Y')}/output_combined_video{datetime.datetime.now().strftime('%d-%m-%Y')}.MP4"])


if __name__ == '__main__':
    folder_path = f"./recordings/recordings{datetime.datetime.now().strftime('%d-%m-%Y')}"
    
    create_folder(f"./outputs/output{datetime.datetime.now().strftime('%d-%m-%Y')}")
    
    output_path = f"./outputs/output{datetime.datetime.now().strftime('%d-%m-%Y')}/output_combined_video{datetime.datetime.now().strftime('%d-%m-%Y')}.avi"
    combine_videos(folder_path, output_path)