import pytesseract
from PIL import ImageOps, ImageFilter, Image
from multipledispatch import dispatch
from cv2 import rectangle
from numpy import ndarray
import util


# Build the path to tesseract.exe (compatable with bundling)
tesseract_path = util.resourcePath(util.buildPath('tesseract','tesseract.exe')) 
pytesseract.pytesseract.tesseract_cmd = tesseract_path


class ImageReader():

    def findImageText(self, image: Image.Image, text: str) -> list[tuple[int, int, int, int]]:
        data: dict = self.getImageData(image)
        return self.extractMatchingBoxes(data, text)


    ################ SEARCH #################

    #
    # TODO: IMPLEMENT REGEX IN MATCHING CRITERIA
    #

    def extractMatchingBoxes(self, ocrData: dict, search_text: str) -> list[tuple[int, int, int, int]]:
        """
        Iterates over OCR data and returns a list of bounding boxes (x, y, w, h)
        where the recognized text (after stripping) matches the search_text.
        """
        matching_boxes = []
        boxes = len(ocrData['level'])
        
        # Iterate through each detected text box.
        for i in range(boxes):
            current_text = ocrData['text'][i].strip()
            # Adjust matching criteria as needed (like exact match, case insensitive, = as opposed to in)
            if search_text.lower() in current_text.lower():
                x = ocrData['left'][i]
                y = ocrData['top'][i]
                w = ocrData['width'][i]
                h = ocrData['height'][i]
                matching_boxes.append((x, y, w, h))
        return matching_boxes


    ################## OCR ##################
    def getImageData(self, image: Image.Image) -> dict:
        if not isinstance(image, Image.Image):
            raise TypeError("Expected a PIL.Image.Image object")
        
        # Preprocess the image: convert to grayscale and sharpen it.
        gray_image = ImageOps.grayscale(image)
        gray_image = gray_image.filter(ImageFilter.SHARPEN)
        
        
        # Configure pytesseract:
        # --oem 3 uses the default (LSTM) OCR engine.
        # --psm 6 assumes a uniform block of text.
        custom_config = r'--oem 3 --psm 6'
        
        data = pytesseract.image_to_data(gray_image, output_type='dict', config=custom_config)
        return data



    ############ COMPUTER VISION ############
    @dispatch(ndarray, tuple, tuple)
    def drawRect(self, image, start : tuple[int, int], end : tuple[int, int]):
        """Draws a rectangle over the image.\n
        Takes a start coordinate, end coordinate and path to an image as inputs."""

        colour = (0, 255, 64, 255) # RGBA
        return rectangle(image, start, end, colour, 2)
        
    @dispatch(ndarray, int, int, int, int)
    def drawRect(self, image, x: int, y: int, width: int, height: int):
        return self.drawRect(image, (x, y), (x+width, y-height))

    def highlightArea(self, image, x: int, y: int, width: int, height: int):
        return rectangle(image, (x, y), (x + width, y - height), (0, 255, 0), thickness=-1)