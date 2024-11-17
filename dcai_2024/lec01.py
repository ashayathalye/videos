from lib import *

lec_num = 1
prefix = "videos/"
left_source = prefix + f"dcai_lec0{lec_num}_left.mp4"
center_source = prefix + f"dcai_lec0{lec_num}_center.mp4"
wide_source = prefix + f"dcai_lec0{lec_num}_wide.mp4"
tracking_source = prefix + f"dcai_lec0{lec_num}_tracking.mp4"
pc_source = prefix + f"dcai_lec0{lec_num}_pc.mp4"
audio_source = prefix + f"dcai_lec0{lec_num}_tracking.mp4"

left = Fullscreen(left_source, delay=-17/30)
center = Fullscreen(center_source, delay=-12/30)
pc = Fullscreen(pc_source, delay=-12/30)
wide = Fullscreen(wide_source, delay=1/30)
tracking = Fullscreen(tracking_source, delay=0/30)
pc_and_tracking = Overlay(pc, tracking, crop_x = 0, crop_y = 0, crop_width = 1920, location = Location.TOP_RIGHT, width = 270, margin = 10)
audio = Audio(audio_source, delay=1/30)

Multitrack([
    Clip(wide, start="12:14"),
    Clip(tracking, start="12:29"),
    Clip(pc_and_tracking, start="14:24"),
    Clip(tracking, start="14:40"),
    Clip(pc_and_tracking, start="15:09"),
    Clip(wide, start="42:56"),
    Clip(tracking, start="44:56"),
    Clip(left, start="53:34"),
    Clip(tracking, start="53:45"),
    Clip(center, start="54:16"),
    Clip(left, start="55:31"),
    Clip(center, start="56:20"),
    Clip(wide, start="59:39", end="59:53")
    ], audio).render(f"dcai_lec{lec_num:02d}.mp4")


