from lib import *

lec_num = 5
prefix = "raw_videos/"
left = prefix + f"dcai_lec{lec_num:02d}_leftchalk.mp4"
right = prefix + f"dcai_lec{lec_num:02d}_rightchalk.mp4"
center = prefix + f"dcai_lec{lec_num:02d}_centerchalk.mp4"
wide = prefix + f"dcai_lec{lec_num:02d}_wide.mp4"
pc = prefix + f"dcai_lec{lec_num:02d}_centerpc.mp4"
tracking = prefix + f"dcai_lec{lec_num:02d}_tracking.mp4"
audio_source= prefix + f"dcai_lec{lec_num:02d}_tracking.mp4"

tracking = Fullscreen(tracking, delay=0/30)
left = Fullscreen(left, delay=-16/30)
center = Fullscreen(center, delay=-4/30)
right = Fullscreen(right, delay=-11/30)
wide = Fullscreen(wide, delay=-16/30)
audio = Audio(audio_source, delay=2/30)

Multitrack([
    Clip(tracking, start="05:32"),
    Clip(left, start="08:05"),
    Clip(tracking, start="08:15", end="90:00")
    ], audio).render(f"dcai_lec{lec_num:02d}.mp4")