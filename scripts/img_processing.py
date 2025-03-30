import cv2 as cv
import numpy as np

# proccess an image to remove noise
def processImage(image_path : str, blur : bool = False, threshold : bool = False, open : bool = False):

    # conversions to grascale, guassian blur, and Otsu's threshold
    image = cv.imread(image_path)
    processed_image : np.array = cv.cvtColor(image, cv.COLOR_BGR2GRAY) # convert to greyscale 
    if (blur):
        processed_image = cv.GaussianBlur(processed_image, (3, 3), 0) # (3, 3) is the blur amount (3px by 3px). 0 is the "blur distribution"
    if (threshold):
        processed_image = cv.threshold(processed_image, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)[1] 

    # remove noise
    if (open):
        kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
        processed_image = cv.morphologyEx(processed_image, cv.MORPH_OPEN, kernel, iterations=1)

    cv.imwrite('./images/print_image.png', processed_image)

    return processed_image
