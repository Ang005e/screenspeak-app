import unittest


from tkinter import PhotoImage
from PIL import Image

from cv2 import imread
from numpy import testing as npt
from numpy import ndarray

from appview import AppView
from appshared import ImageController

class testAppImage(unittest.TestCase):

    def setUp(self):
        self.primary_image_path = './images/default_image.png'
        self.secondary_image_path = './images/canvas_image.png'

        self.primary_matlike = imread(self.primary_image_path)
        self.secondary_matlike = imread(self.secondary_image_path)

        self.app_image = ImageController(self.primary_image_path)


    ### TEST __init__, setWithPath, setWithMatLike, syncComponents
    def testInit(self):
        self.app_image = ImageController(self.primary_image_path)
        self.assertIsInstance(self.app_image.asMatLike(), ndarray, "Matlike is not of the expected type - perhaps it failed to initialise?")


    ### TEST overwriting the image with a path (setWithPath, setWithMatLike)
    def testBaseSet(self): 
        old_matlike = self.primary_matlike
        new_matlike = self.secondary_matlike

        # overwrite the matlike from the secondary image
        self.app_image.setWithPath(self.secondary_image_path)

        npt.assert_array_equal(new_matlike, self.app_image._matlike)
        npt.assert_array_equal(old_matlike, self.app_image._matlike)


    ### TEST setWithPilImage
    def testSetWithPilImage(self):
        self.app_image.setWithPilImage(Image.open(self.secondary_image_path))
        npt.assert_array_equal(self.app_image.asMatLike(), self.secondary_matlike)


    ### TEST setWithMatLike
    def testGetMatLike(self):
        matlike = self.app_image.asMatLike()
        self.assertIsInstance(matlike, ndarray)


    ### TEST getGuiImage, intergration with Tkinter AppGui
    def testGetGuiImage(self):
        root = AppView()
        self.app_image.initialiseGuiImage()
        self.assertIsInstance(self.app_image.asPhotoImage(), PhotoImage)
        
    
    def testRetrieveImageFormats(self):
        root = AppView()
        self.assertIsInstance(self.app_image.asMatLike(), ndarray)
        self.assertIsInstance(self.app_image.asPilImage(), Image.Image)
        self.assertIsInstance(self.app_image.asPhotoImage(), PhotoImage)


    def testMakeOpaque(self):

        app_image = ImageController(self.primary_image_path)
        app_image.setWithPilImage(Image.open(self.secondary_image_path))

        app_image.clear()
        image = app_image.asPilImage()

        self.assertTrue(image.has_transparency_data, "The image has no form of transparency data")

        alpha_channel = image.getchannel("A").getdata()
        for pix in alpha_channel:
            self.assertTrue(pix == 0, "Pixel is not fully transparent")



    

class testApp(unittest.TestCase):

    def setUp(self):
        markup_image = ImageController('./images/canvas_image.png')
        self.app = AppView(markup_image.guiImage)

    
    def create(self):
        self.app.create()










