from lib import *
import numpy as np
import cv2
from PIL import Image as im
from PIL import ImageOps
import datetime

file = '../22.01/22.01 Lecture 3-3 - Neutron Discovery.mp4'

# this is just extracting two example Mike Short labels
top = None
bottom = None
cap=cv2.VideoCapture('example.mp4')
while(cap.isOpened()):
    success, frame = cap.read()
    array = frame
    img = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
    top = img[148:148+32, 1920-320:1920-320+88]
    top = (top > 240) * 1
    break
cap=cv2.VideoCapture('example2.mp4')
while(cap.isOpened()):
    success, frame = cap.read()
    array = frame
    img = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
    bottom = img[1080-32:1080, 0:88]
    bottom = (bottom > 240) * 1
    break

# main stuff
threshold = 50
cap = cv2.VideoCapture(file)
fps = cap.get(cv2.CAP_PROP_FPS)
to_process = cv2.VideoCapture(file)
i = 0
predicted_vals = []
while(to_process.isOpened()):
    success, frame = cap.read()
    if not success:
        break
    array = frame
    try:
        img = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
    except:
        continue
    upper = img[148:148+32, 1920-320:1920-320+88]
    upper = (upper > 240) * 1
    lower = img[1080-32:1080, 0:88]
    lower = (lower > 240) * 1
    sec = i // int(fps) # convert frame to seconds
    bottom_loss = np.sum((lower-bottom)**2)
    top_loss = np.sum((upper-top)**2)
    s = ''
    if bottom_loss < threshold or top_loss < threshold:
        s = 'Mike'
    else:
        s = 'Student'
    if s == 'Student':
        predicted_vals.append(sec)
    i += 1

# identify intervals from list of ints
final_intervals = []
curr_start = predicted_vals[0]
for i in range(1, len(predicted_vals)):
    p = predicted_vals
    if p[i] - p[i-1] > 1 or i == len(predicted_vals)-1: # new interval
        final_intervals.append((curr_start, p[i-1]))
        curr_start = p[i]
proper = []
for s, e in final_intervals:
    # buffer, since division by fps isn't perfect translation to seconds
    s -= 1
    e += 1
    entry = ('0' + str(datetime.timedelta(seconds=s)), '0' + str(datetime.timedelta(seconds=e)))
    proper.append(entry)
for s, e in proper:
    print(s, e, 'avatar_large.png')
