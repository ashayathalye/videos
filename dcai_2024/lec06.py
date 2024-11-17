from lib import *

lec_num = 6
prefix = "raw_videos/"
left = prefix + f"dcai_lec{lec_num:02d}_leftchalk.mp4"
right = prefix + f"dcai_lec{lec_num:02d}_rightchalk.mp4"
center = prefix + f"dcai_lec{lec_num:02d}_centerchalk.mp4"
wide = prefix + f"dcai_lec{lec_num:02d}_wide.mp4"
pc = prefix + f"dcai_lec{lec_num:02d}_centerpc.mp4"
tracking = prefix + f"dcai_lec{lec_num:02d}_tracking.mp4"
audio_source= prefix + f"dcai_lec{lec_num:02d}_tracking.mp4"

pc = Fullscreen(pc, delay=-14/30)
tracking = Fullscreen(tracking, delay=0/30)
pc_and_tracking = Overlay(pc, tracking, crop_x = 0, crop_y = 0, crop_width = 1920, location = Location.TOP_RIGHT, width = 270, margin = 10)
audio = Audio(audio_source, delay=2/30)

Multitrack([
    Clip(pc_and_tracking, start="06:02", end="90:00")
    ], audio).render(f"dcai_lec{lec_num:02d}.mp4")