from lib import *
import argparse
from fractions import Fraction
import numpy as np

lec_num = 7
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
#   ("06:37", "06:47") # => pc is -13/30
# ]

# lec 3 
# intervals = [
#   ("11:15", "11:25") # pc is -14/30, left is -16/30, wide is -24/30
# ]

# lec 4
# intervals = [
#   # ("13:37", "13:54"), # wide is -23/30, left is -16/30
#   # ("27:47", "27:57"), # center is -3/30
#   # ("47:00", "47:10") # right is -11/30
# ]

# lec 5
# intervals = [
#   # ("07:25", "07:30") # wide is -16/30, left is -16/30
#   # ("34:33", "34:40"), # center is -4/30
#   # ("53:33", "53:40") # right is -11/30
# ]

# lec 6 
# intervals = [
#   ("6:12", "6:18") # pc is -14/30
# ]

# lec 7 
# intervals = [
#   ("07:42", "07:48") # pc is 10/30
# ]

video_1 = Fullscreen(tracking, delay=0/30)
video_2 = Fullscreen(pc, delay=0/30)
video_3 = Fullscreen(wide, delay=0/30)
video_4 = Fullscreen(right, delay=0/30)
audio = Audio(audio_source, delay=2/30)

for i, interval in enumerate(intervals):
  start, end = interval
  r = np.arange(-30, 30, 1)
  for j, val in enumerate(r):
    video_2.delay = val/30
    filename = f"vsync/sync_{lec_num:02d}_interval_{i}_video_{val}_{start}_to_{end}.mp4"
    Multitrack([Clip(Tile(video_1, video_2, video_3, video_4), start=start, end=end)], audio).render(filename)

