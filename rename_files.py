import os 

path_to_videos = "raw_videos/"
files = os.listdir(path_to_videos)
counter = 0
current_date = None

for filename in sorted(files, key = lambda x: x[-6:-4]):
    split = filename.split("-")
    # Data-Centric-AI-[angle]-2024jan[date].mp4
    angle = split[3].lower()
    date = filename[-6:-4]

    if date != current_date:
        current_date = date
        counter += 1

    new_filename = f"dcai_lec{counter:02d}_{angle}.mp4"
    print(f"Renaming {filename} to {new_filename}.")
    old_path = os.path.join(path_to_videos, filename)
    new_path = os.path.join(path_to_videos, new_filename)
    os.rename(old_path, new_path)
