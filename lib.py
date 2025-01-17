import ffmpeg # type: ignore
from typing import List, Optional, Union, Tuple, Dict
from abc import ABC, abstractmethod
from enum import Enum, auto
from PIL import Image

class Audio:
  def __init__(self, filename: str, delay: float = 0, loudness: float = -12.0):
    self.filename = filename
    self.delay = delay
    self.loudness = loudness

  def to_stream(self, start_timestamp: float, end_timestamp: float):
    dur = end_timestamp - start_timestamp
    stream = ffmpeg.input(self.filename, ss=start_timestamp-self.delay, t=dur)
    audio = stream.audio.filter('loudnorm', i=self.loudness)
    return audio

class Stream(ABC):
  @abstractmethod
  def to_stream(self, start_timestamp: float, end_timestamp: float):
    raise NotImplementedError

class Fullscreen(Stream):
  def __init__(self, filename: str, delay: float = 0):
    self.filename = filename
    self.delay = delay

  def to_stream(self, start_timestamp: float, end_timestamp: float):
    dur = end_timestamp - start_timestamp
    stream = ffmpeg.input(self.filename, ss=start_timestamp-self.delay, t=dur)
    return stream

class Location(Enum):
  MIDDLE_RIGHT = auto()
  TOP_CENTER = auto()
  TOP_RIGHT = auto()

class Overlay(Stream):
  def __init__(self, main: Stream, inside: Stream, *, crop_x: int, crop_y: int, crop_width: int, crop_height: Optional[int] = None, opacity: float = 1, margin: int = 25, width: int = 480, location: Location = Location.MIDDLE_RIGHT):
    self.main = main
    self.inside = inside
    self.crop_x = crop_x
    self.crop_y = crop_y
    self.crop_width = crop_width
    self.crop_height = crop_height
    self.opacity = opacity
    self.margin = margin
    self.width = width
    self.location = location

  def to_stream(self, start_timestamp: float, end_timestamp: float):
    main = self.main.to_stream(start_timestamp, end_timestamp)
    inside = self.inside.to_stream(start_timestamp, end_timestamp)
    crop_height = self.crop_height
    if crop_height is None:
      crop_height = self.crop_width * 9 // 16
    crop = inside.crop(x=self.crop_x, y=self.crop_y, width=self.crop_width, height=crop_height)

    overlay_w = self.width
    overlay_h = crop_height * self.width // self.crop_width
    scaled = crop.filter('scale', overlay_w, -1)
    if self.opacity == 1:
      translucent = scaled
    else:
      translucent = scaled.filter('format', 'rgba').filter('colorchannelmixer', aa=self.opacity)
    overlay_margin = self.margin
    if self.location == Location.MIDDLE_RIGHT:
      overlay_x = 1920 - overlay_margin - overlay_w
      overlay_y = (1080 - overlay_h) // 2
    elif self.location == Location.TOP_CENTER:
      overlay_x = 1920//2 - overlay_w//2
      overlay_y = overlay_margin
    elif self.location == Location.TOP_RIGHT:
      overlay_x = 1920 - overlay_margin - overlay_w
      overlay_y = overlay_margin
    else:
      raise ValueError(f'bad location: {self.location}')
    overlay = ffmpeg.overlay(main, translucent, x=overlay_x, y=overlay_y)
    return overlay

class Tile(Stream):
  def __init__(self, video_1: Stream, video_2: Stream, video_3: Stream, video_4: Stream):
    self.video_1 = video_1
    self.video_2 = video_2
    self.video_3 = video_3
    self.video_4 = video_4

  def to_stream(self, start_timestamp, end_timestamp):
    dummy = self.video_1.to_stream(start_timestamp, end_timestamp)
    video_1 = self.video_1.to_stream(start_timestamp, end_timestamp)
    video_2 = self.video_2.to_stream(start_timestamp, end_timestamp)
    video_3 = self.video_3.to_stream(start_timestamp, end_timestamp)
    video_4 = self.video_4.to_stream(start_timestamp, end_timestamp)
    overlay = ffmpeg.overlay(dummy, video_1.filter('scale', 960, -1), x=0, y=0)
    overlay = ffmpeg.overlay(overlay, video_2.filter('scale', 960, -1), x=960, y=0)
    overlay = ffmpeg.overlay(overlay, video_3.filter('scale', 960, -1), x=0, y=540)
    overlay = ffmpeg.overlay(overlay, video_4.filter('scale', 960, -1), x=960, y=540)
    return overlay

class Clip:
  def __init__(self, stream: Stream, *, end: Optional[Union[float, str]] = None, start: Optional[Union[float, str]] = None):
    self.stream = stream
    def hms_(ts: Optional[Union[float, str]]) -> Optional[float]: return hms(ts) if ts is not None and isinstance(ts, str) else ts
    self.start: Optional[float] = hms_(start)
    self.end: Optional[float] = hms_(end)

class Multitrack:
  def __init__(self, clips: List[Clip], audio: Audio):
    # You can figure out audio_delay by using VLC's Track Synchronization
    # tool. The sign should match, so you can copy the exactly value from the
    # "Audio track synchronization" in VLC. This value is how much the audio
    # should be delayed with respect to the video.
    if not clips:
      raise ValueError('no clips')
    self.clips = clips
    self.audio = audio

  def streams(self):
    start = self.clips[0].start
    if start is None:
      raise ValueError('first clip has no start')
    current_time = start
    streams = []
    for i, clip in enumerate(self.clips):
      if clip.start is not None and clip.start != current_time:
        raise ValueError(f'time mismatch at index {i}')
      if clip.end is not None:
        end = clip.end
      elif i+1 < len(self.clips) and self.clips[i+1].start is not None:
        end = self.clips[i+1].start
      else:
        raise ValueError(f'cannot determine end time for clip at index {i}')
      if current_time > end:
        raise ValueError(f'time travel at index {i}')
      streams.append(clip.stream.to_stream(current_time, end))
      current_time = end
    video = ffmpeg.concat(*streams)
    audio = self.audio.to_stream(start, current_time)
    return video, audio

  def to_stream(self):
    video, audio = self.streams()
    return ffmpeg.concat(video, audio, a=1, v=1)

  def render(self, output_filename: str) -> None:
    ffmpeg.output(self.to_stream(), output_filename).run()

class Playlist:
  def __init__(self, playlists: List[Multitrack]):
    self.playlists = playlists

  def to_stream(self):
    streams = [p.streams() for p in self.playlists]
    flattened = [s for i in streams for s in i]
    return ffmpeg.concat(*flattened, a=1, v=1)

  def render(self, output_filename: str) -> None:
    ffmpeg.output(self.to_stream(), output_filename).run()

class StaticOverlay(Stream):
    def __init__(self, filename: str, overlays: Dict[str, Dict[str, int]], intervals: List[Tuple[int, int, str]], delay: float = 0):
        self.filename = filename
        self.overlays = overlays
        self.intervals = intervals
        self.delay = delay

    def to_stream(self, start_timestamp: float, end_timestamp: float):
        dur = end_timestamp - start_timestamp
        stream = ffmpeg.input(self.filename, ss=start_timestamp-self.delay, t=dur)
        # do first overlay
        start, end, img_path = self.intervals[0]
        img_info = self.overlays[img_path]
        x = img_info['x']
        y = img_info['y']
        img = ffmpeg.input(img_path)
        v = ffmpeg.filter([stream, img], filter_name='overlay', x=x, y=y, enable='between(t, {}, {})'.format(start, end))
        for i in range(1, len(self.intervals)):
            start, end, img_path = self.intervals[i]
            img_info = self.overlays[img_path]
            x = img_info['x']
            y = img_info['y']
            img = ffmpeg.input(img_path)
            v = ffmpeg.filter([v, img], filter_name='overlay', x=x, y=y, enable='between(t, {}, {})'.format(start, end))
        return v

def hms(timestamp: str) -> float:
  parts = timestamp.split(':')
  assert 1 <= len(parts) <= 3
  s = float(parts[-1])
  m = float(parts[-2]) if len(parts) >= 2 else 0
  h = float(parts[-3]) if len(parts) >= 3 else 0
  return 60*60*h + 60*m + s

def parse_static_overlay_config(filename):
    overlays = {}
    intervals = []
    with open(filename) as file:
        lines = [line.rstrip('\n') for line in file]
        video_path = lines[0]
        num_overlays = int(lines[1])
        for line in lines[2:2+num_overlays]:
            img, x, y, w, h = line.split()
            overlays[img] = {
                'x': int(x),
                'y': int(y),
                'w': int(w),
                'h': int(h)
            }
        for line in lines[2+num_overlays:]:
            start, end, img = line.split()
            intervals.append((int(hms(start)), int(hms(end)), img))
    return video_path, overlays, intervals
