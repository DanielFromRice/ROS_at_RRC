import numpy as np
import cv2


def resize(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(img, dim, None)

# Read in Video
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, rubik_small = video_capture.read()

    # resize image
    # rubik_small = resize(rubik, 60)

    # convert to HSV
    rubikhsv = cv2.cvtColor(rubik_small, cv2.COLOR_BGR2HSV)

    # Filter Image in HSV - outputs binary array
    boundaries = [[40, 50, 50], [75, 255, 255]]
    filtered = cv2.inRange(rubikhsv, np.array(boundaries[0]), np.array(boundaries[1]))
    # cv2.imshow("filter", filtered) # Uncomment to show the filter

    # Produce a colored version of the filtered image
    rubik_small[:,:,0] = filtered/255 * rubik_small[:,:,0]
    rubik_small[:,:,1] = filtered/255 * rubik_small[:,:,1]
    rubik_small[:,:,2] = filtered/255 * rubik_small[:,:,2]

    cv2.imshow("post_filter", rubik_small)

    # Generate contours
    filtered, contours, hierarchy = cv2.findContours(filtered, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the filtered image
    lines = cv2.drawContours(rubik_small, contours, -1, (0, 255, 0))
    # cv2.imshow("contours", lines)

    # Draw contours on a blank image
    blank = np.zeros(rubik_small.shape)
    blank2 = cv2.drawContours(blank, contours, -1, (0,255,0))
    cv2.imshow("filtered", blank2)

    # Filter out contours with large area
    big_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]
    blank = np.zeros(rubik_small.shape)
    blank3 = cv2.drawContours(blank, big_contours, -1, (0, 255, 0))
    cv2.imshow("big", blank3)

    # Approximate contours to a straighter polygon
    big_approx = []
    centroids = []
    for bc in big_contours:
        epsilon = 0.0075 * cv2.arcLength(bc, True)
        approx = cv2.approxPolyDP(bc, epsilon, True)
        big_approx.append(approx)

    blank = np.zeros(rubik_small.shape)
    blank4 = cv2.drawContours(blank, big_approx, -1, (0, 255, 0))
    cv2.imshow("big_approx", blank4)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
