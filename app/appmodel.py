from ocr import ImageReader
from appshared import ImageController
from numpy import ndarray

class AppModel():

    _image_reader = ImageReader()

    def performSearch(self, search_text: str, search_image: ImageController, output_image: ImageController):
        # carry out a search, and return the results

        print(f"Searching for: {search_text}")

        highlighted_image: ndarray = output_image.asMatLike()

        boxes = self._image_reader.findImageText(search_image.asPilImage(), search_text)

        for box in boxes:
            highlighted_image = self._image_reader.drawRect(highlighted_image, *box)
            
        output_image.overwriteWith(highlighted_image)

        return output_image