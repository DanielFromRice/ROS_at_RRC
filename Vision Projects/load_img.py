import cv2
import numpy as np
# CV2 = OpenCV vision processing libary, numpy = underlying data science library to handle arrays

# Load Image
cube = cv2.imread("rubik.png")

# Decrease intensity of image
dark_cube = (cube * .5).astype(np.uint8)

# View Image Array matrix
# print(cube)

# Take a slice of the image array, get just red values
red_img = cube[:,:,2]
# NOTE: shows as greyscale because the slice is 2-dimensional - doesn't have any color data
cv2.imshow("red", red_img)
print(red_img.shape)

# Reconstruct color image from the red slice
zero = np.zeros(cube.shape)
zero[:,:,2] = red_img
# cv2.imshow("red2", zero)

# Basic thresholding: remove all values that are greater than 250 red value (on scale of 0 to 255)
truth_vals = red_img < 250
# truth_vals is a matrix of boolean values, False = 0, True = 1
# print(truth_vals)
thresholded = truth_vals * red_img # Multiplication by 0/1 will either remove value or restore original value
zero[:,:,2] = thresholded
cv2.imshow("red3", zero)

# MUST INCLUDE THESE LINES: defines an end to the program so OpenCV can close the image windows
cv2.waitKey(0)
cv2.destroyAllWindows()