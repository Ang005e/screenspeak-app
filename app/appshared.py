import numpy as np
from PIL import Image
from tkinter import PhotoImage, TclError
from cv2 import imread, imwrite
from multipledispatch import dispatch
from pyautogui import screenshot


##### AppImage class ######

# PURPOSE:
# Easy translation of image formats. 
# The app's GUI, OCR, and image editor libraries all have different image format requirements.
# So... if i make a change to a MatLike image, and I want to display that image to the GUI, or search in it for text, I'd need to:
#   1. Translate it to the PIL Image format
#   2. Save it to the base .PNG file
#   3. Somehow know exactly when to update the image format object I'm targeting (presumebly using a complex, centralised event system)
#   4. Update the target.
# ... every single time. Far easier if instead, a base image path is passed to this object, and it creates image format objects, just WAITING 
# to be referenced cleanly. It can handle translations between formats, copying between base (.png) images, cleaning up after unused 
# image files, and syncing all of the above changes between multiple formats. 
#
#   in short, this is handled by referencing a base .PNG image file, and linking it to different "views" of the image
#   (the view for the GUI, the view for Optical Character Recognition, and the view for the screenwriter/image editor).
# 
# RULES:
# The base file may be written to using a new image of another format
# the base filename may not be changed after initialisation 
# 
# INTERNAL LOGIC
#   - On initialisation:
#    -    All components will be...
#       * created with default values.
#       * linked to the base file.
#    -    Argument shall be:
#       * filepath to a base image to reference AND save changes to
#
#   - When changing the base file using another format:
#       1. The correct method will be called from outside the class (setWithMatlike, setWithPilImage or setWithPath)
#       2. The format being changed will be saved to the corresponding property (i.e. self._matlike = new_matlike)
#       3. The base (.png) file will have changes applied from the external format (but retain .png format)
#       4. The self.syncComponents() method will be called, applying changes from the base .png file to the other components.
#
# NOTES:
#   - The Gui image is only writeable, but the PIL image and MatLike are both read/write
#   - the PhotoImage object at self._gui_image should never be replaced, only updated internally, due to the way it is 
#     referenced by third parties.

class GeneralImage():
    def __init__(self, read_callback, write_callback, sync_callback):
        self._image = NotImplemented
        self._readCallback = read_callback
        self._writeCallback = write_callback
        self._syncCallback = sync_callback
        super().__init__()
    def get(self):
        return self._image
    def readFromFile(self):
        self._image = self._readCallback()
    def overwrite(self):
        self._writeCallback()
        self._syncCallback(self)
    
class MatlikeImage(GeneralImage):
    def __init__(self, path, sync_callback):
        self._image: np.ndarray
        super().__init__(lambda: imread(path), lambda: imwrite(path, self._image), sync_callback)

class PilImage(GeneralImage):
    def __init__(self, path, sync_callback):
        self._image: Image.Image
        super().__init__(lambda: Image.open(path), lambda: Image.Image.save(self._image, path), sync_callback)

class GuiImage(GeneralImage):
    def __init__(self, path, sync_callback):
        self._image: PhotoImage
        super().__init__(lambda: PhotoImage(file=path), lambda: PhotoImage.configure(self._image, file=path), sync_callback)


class ImageController():
    """
    A readable, writeable image, viewable by Tkinter, openCV, and tesseract.
    Provides references to the file path, base image file, tk PhotoImage and the PIL Image.
    """

    def __init__(self, base_image_path, image_types: list):
        """Params: \n
        base_image_path - file path to the image to create this AppImage object from"""
        
        self.gui_image_active = False
        self._PATH: str = base_image_path
        #self._GUI_IMAGE_PATH: str = f"{self._PATH.split(".png")[0]}_forDisplay.png"
        

        self._matlike = MatlikeImage(self._PATH, self.syncChanges) if MatlikeImage in image_types else NotImplemented
        self._pil_image = PilImage(self._PATH, self.syncChanges) if PilImage in image_types else NotImplemented
        self._gui_image = GuiImage(self._PATH, self.syncChanges) if GuiImage in image_types else NotImplemented

        self._images: list[GeneralImage] = [self._matlike, self._pil_image, self._gui_image]

        self.overwriteWith(base_image_path)

    def initialiseGuiImage(self):
        try:
            if self._gui_image is NotImplemented:
                raise ValueError(f"{self.initialiseGuiImage.__name__} may not be called if a {self._gui_image.__str__()} instance is not included in '_images' {self._images.__str__()}.")
            #self.createGuiImage(self.asMatLike())
            self.gui_image_active = True
            self._gui_image.readFromFile()
        except TclError:
            print("ERROR: View must be initialised before creating a photoimage")
            raise TclError.add_note(f"The View must be initialised before calling {self.initialiseGuiImage.__name__}!")


    @dispatch(np.ndarray)
    def overwriteWith(self, new_image: np.ndarray):
        self._matlike._image = new_image
        self._matlike.overwrite()
    @dispatch(Image.Image)
    def overwriteWith(self, new_image: Image.Image):
        self._pil_image._image = new_image
        self._pil_image.overwrite()
    @dispatch(PhotoImage)
    def overwriteWith(self, new_image: PhotoImage):
        self._gui_image._image = new_image
        self._gui_image.overwrite()
    @dispatch(str)
    def overwriteWith(self, path: str):
        self._matlike._image = imread(path)
        self._matlike.overwrite()


    def syncChanges(self, caller: GeneralImage):
        for image in self._images:
            if (image is NotImplemented):
                continue # if the image type isn't active
            if ((not self.gui_image_active) and isinstance(image, GuiImage)):
                continue # if it's the GuiImage and the Gui isn't active yet
            if (not image is caller):
                image.readFromFile()

    
    # Accessor functions
    def asPath(self):
        return self._PATH
    def asMatLike(self):
        return self._matlike._image
    def asPhotoImage(self):
        try:
            return self._gui_image._image
        except AttributeError:
            raise ValueError(f"{self.asPhotoImage.__name__} may not be called if a {GuiImage.__name__} instance is not included in '_images' {self._images.__str__()}.")
    def asPilImage(self):
        return self._pil_image._image


    # Misc
    def overwriteWithScreenshot(self):
        screen = screenshot(self._PATH)
        self.overwriteWith(screen)


    # make transparent
    def clear(self):
        pix_y, pix_x = self.asPilImage().size
        transparent_matlike = np.zeros((pix_x, pix_y, 4), np.uint8) # clear image. array format is x, y and channels (4, BGRA)
        self.overwriteWith(transparent_matlike)

    # workaround for image file locks - make a copy for the GUI to access.
    #def createGuiImage(self, img):
    #    try:
    #        imwrite(self._GUI_IMAGE_PATH, img=img)
    #    except FileExistsError:
    #        raise FileExistsError("bit of a twit, aren't you? (a file with the same name already exists)")
        