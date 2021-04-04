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
    ret, frame = video_capture.read()

    rubik_small = np.copy(frame)
    cv2.imshow("Original", frame)

    # convert to HSV
    rubikhsv = cv2.cvtColor(rubik_small, cv2.COLOR_BGR2HSV)

    # Filter Image in HSV - outputs binary array
    # Green array (PCB color)
    boundaries = [[55, 40, 40], [90, 255, 255]]
    mask = cv2.inRange(rubikhsv, np.array(boundaries[0]), np.array(boundaries[1]))
    # cv2.imshow("filter", filtered) # Uncomment to show the filter

    # Produce a colored version of the filtered image
    rubik_small[:,:,0] = mask / 255 * rubik_small[:, :, 0]
    rubik_small[:,:,1] = mask / 255 * rubik_small[:, :, 1]
    rubik_small[:,:,2] = mask / 255 * rubik_small[:, :, 2]

    cv2.imshow("post_filter", rubik_small)

    # Generate contours
    mask, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the filtered image
    lines = cv2.drawContours(rubik_small, contours, -1, (0, 255, 0))
    # cv2.imshow("contours", lines)

    # Draw contours on a blank image
    blank = np.zeros(rubik_small.shape)
    blank2 = cv2.drawContours(blank, contours, -1, (0,255,0))
    cv2.imshow("filtered", blank2)

    # Filter out contours with large area
    biggest_contour = max(contours, key=cv2.contourArea)

    # Approximate the contour in different ways
    epsilon = 0.006 * cv2.arcLength(biggest_contour, True)
    approx = cv2.approxPolyDP(biggest_contour, epsilon, True)

    hull = cv2.convexHull(biggest_contour)

    # Compare original to "convex Hull" to "Approximated contour"
    blank = np.zeros(rubik_small.shape)
    big_draw = cv2.drawContours(blank, [biggest_contour], -1, (0, 255, 0))
    blank = np.zeros(rubik_small.shape)
    big_approx_draw = cv2.drawContours(blank, [approx], -1, (0, 255, 0))
    blank = np.zeros(rubik_small.shape)
    hull_img = cv2.drawContours(blank, [hull], -1, (0,255, 0))
    cv2.imshow("biggest", big_draw)
    cv2.imshow("hull", hull_img)
    cv2.imshow("biggest_approx", big_approx_draw)

    # Compute center
    M = cv2.moments(hull)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    output = cv2.circle(frame, (cx, cy), 10, (255,255,0), -1)

    # compute box
    rect = cv2.minAreaRect(hull)
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    output = cv2.drawContours(output, [box], 0, (0, 0, 255), 2)

    cv2.imshow("output", output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
