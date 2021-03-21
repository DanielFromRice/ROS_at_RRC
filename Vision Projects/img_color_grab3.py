import cv2
import sys
import numpy as np

path = 'D:\\PyCharmDir\\OpenCV\\venv\\Lib\\site-packages\\~v2\\data'

# video_capture = cv2.VideoCapture(0)

# while True:
    # Capture frame-by-frame
    # ret, frame = video_capture.read()
frame = cv2.imread('.\\rubik.png')
scale_percent = 60
width = int(frame.shape[1] * scale_percent / 100)
height = int(frame.shape[0] * scale_percent / 100)
dim = (width, height)
frame = cv2.resize(frame, dim, None)
dim = (width, height)

hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
# red
# boundaries = [([17, 15, 50], [90, 80, 255])]
# Green
boundaries = [([40, 50, 50], [75, 255, 255])]
# blue
# boundaries = [([100, 20, 30], [230, 200, 100])]
# yellow
# boundaries = [([20, 50, 50], [35, 255, 255])]
output = None
for (lower, upper) in boundaries:
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(hsv, hsv, mask=mask)
gray = output[:,:,2]
nonzero = cv2.countNonZero(gray)
print(nonzero)
print(gray.size)
print(nonzero * 100 / gray.size)
cv2.imshow('original', frame)
cv2.imshow('output', cv2.cvtColor(output, cv2.COLOR_HSV2BGR))

green_img = cv2.cvtColor(output, cv2.COLOR_HSV2BGR)
image, contours, heirarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
green_img = cv2.drawContours(green_img, contours, -1, (0, 0, 255), 3)
cv2.imshow('contours', green_img)
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
