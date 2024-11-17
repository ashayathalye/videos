from lib import *
import numpy as np

lec_num = 5
prefix = "raw_videos/"
left = prefix + f"dcai_lec{lec_num:02d}_leftchalk.mp4"
right = prefix + f"dcai_lec{lec_num:02d}_rightchalk.mp4"
center = prefix + f"dcai_lec{lec_num:02d}_centerchalk.mp4"
wide = prefix + f"dcai_lec{lec_num:02d}_wide.mp4"
pc = prefix + f"dcai_lec{lec_num:02d}_centerpc.mp4"
tracking = prefix + f"dcai_lec{lec_num:02d}_tracking.mp4"
audio_source= prefix + f"dcai_lec{lec_num:02d}_tracking.mp4"

# lec 2
# intervals = [
#   ("08:45", "08:55"), # writing on board => 3/30
#   ("31:24", "31:34") # talking => 3/30
# ]

# # lec 3
# intervals = [
#   ("34:42", "34:52"), # writing on board => 2/30
#   ("15:52", "16:02") # talking => 2/30
# ]

# lec 4
# intervals = [
#   ("13:37", "13:54") # writing on board + talking => 2/30
# ]

# # lec 5 
# intervals = [
#   ("38:00", "38:10"), # writing on board
#   ("26:25", "26:35") # talking => 2/30
# ]

# lec 6
# no writing, assume it stays at 2/30 


for i, interval in enumerate(intervals):
  start, end = interval
  r = np.arange(-30, 31, 1)
  for j, val in enumerate(r):
    video = Fullscreen(tracking, delay=0/30)
    audio = Audio(audio_source, delay=val/30)
    filename = f"async/sync_{lec_num:02d}_interval_{i}_audio_{val}_{start}_to_{end}.mp4"
    Multitrack([Clip(video, start=start, end=end)], audio).render(filename)
