import datetime
import combine

folder_path = "./recordings"
output_path = f"output_combined_video{datetime.datetime.now().strftime('%d-%m-%Y')}.avi"

combine.combine_videos(folder_path, output_path)
