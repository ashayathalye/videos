from lib import *

lec_num = 3
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
left = Fullscreen(left, delay=-16/30)
wide = Fullscreen(wide, delay=-24/30)
audio = Audio(audio_source, delay=2/30)

Multitrack([
    Clip(tracking, start="10:38"),
    Clip(pc_and_tracking, start="11:16"),
    Clip(wide, start="13:17"),
    Clip(pc_and_tracking, start="15:30"),
    Clip(wide, start="18:00"),
    Clip(tracking, start="20:15"),
    Clip(wide, start="26:10"),
    Clip(tracking, start="26:20"),
    Clip(wide, start="27:02"),
    Clip(tracking, start="27:16"),
    Clip(pc_and_tracking, start="38:46"),
    Clip(tracking, start="39:11"),
    Clip(pc_and_tracking, start="40:10"),
    Clip(tracking, start="42:23"),
    Clip(pc_and_tracking, start="45:09"),
    Clip(wide, start="48:19"),
    Clip(tracking, start="50:25"),
    Clip(pc_and_tracking, start="52:42"),
    Clip(tracking, start="53:15"),
    Clip(pc_and_tracking, start="53:50"),
    Clip(tracking, start="59:08"),
    Clip(pc_and_tracking, start="59:16", end="90:00")
    ], audio).render(f"dcai_lec{lec_num:02d}.mp4")


