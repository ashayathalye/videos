from lib import *

lec_num = 4
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
center = Fullscreen(center, delay=-3/30)
right = Fullscreen(right, delay=-11/30)
wide = Fullscreen(wide, delay=-23/30)
audio = Audio(audio_source, delay=2/30)

Multitrack([
    Clip(wide, start="06:28"),
    Clip(tracking, start="09:32"),
    Clip(wide, start="10:04"),
    Clip(tracking, start="10:09", end="56:53")
    ], audio).render(f"dcai_lec{lec_num:02d}.mp4")


