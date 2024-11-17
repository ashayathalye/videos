 # https://stackoverflow.com/questions/25891342/creating-a-video-from-a-single-image-for-a-specific-duration-in-ffmpeg 

import subprocess

# expect names of files as "[class_abbreviation]_lec[lecture_number]_title.png"
folder = "content/"
prefix = "dcai"
suffix = "png"
num_lectures = 7
duration = 3
framerate = 25

files = []
for i in range(num_lectures):
	filename = f"{folder}{prefix}_lec{i+1:02d}_title.{suffix}"
	files.append(filename)

for input_file in files:
	output_file = input_file[:-4] + ".mp4"
	command = [
		"ffmpeg",
		"-framerate",
		str(framerate),
		"-i",
		input_file,
		"-t",
		str(duration),
		"-c:v",
		"libx264",
		"-x265-params",
		"lossless=1",
		"-pix_fmt",
		"yuvj420p",
		"-vf",
		"scale=1920:1080",
		output_file,
		"-f",
		"lavfi",
		"-i",
		"anullsrc",
		"-c:a",
		"aac",
		"-shortest"
	]

	try:
		subprocess.run(command, check=True)

	except subprocess.CalledProcessError as e:
		print(f"Error during conversion: {e}")