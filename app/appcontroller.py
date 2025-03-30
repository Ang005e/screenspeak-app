from appview import AppView
from appmodel import AppModel
from appshared import ImageController, GuiImage, MatlikeImage, PilImage
import util


# TODO: 
# * Change the AppImage class to be accessed only by the controller (remove from View).
# * .
# * .

# using image controllers due to the fact that the GUI is not the only component accessing images - OCR 
# needs to be performed too. so seperations of concerns was required.
class AppController():

    def __init__(self, view: AppView, model: AppModel, markup_image_path: str, search_image_path: str, result_image_path: str):

        
        # Application Components:
        self.view = view
        self.model = model

        self.search_images = ImageController(search_image_path, [GuiImage, MatlikeImage, PilImage])
        self.result_images = ImageController(result_image_path, [GuiImage, MatlikeImage, PilImage])
        self.canvas_images = ImageController(markup_image_path, [GuiImage, MatlikeImage, PilImage])

        # View event bindings
        # self.view.root.bind('<Alt-F12>', lambda x: self.activateSearch(x)) now handled by ctypes
        self.view.root.bind('<Return>', lambda x: self.performSearch(x))
        self.view.root.bind('<Escape>', lambda x: self.cancel(x))
        self.view.root.after_idle(self.load)

        return


    def begin(self):
        self.view.root.mainloop()

    # Occurs after application load completes. 
    # Preperatory tasks reliant on a loaded GUI should be performed here.
    def load(self):
        self.canvas_images.initialiseGuiImage()
        self.search_images.initialiseGuiImage()
        self.canvas_images.clear()
        self.view.applyImage(self.canvas_images.asPhotoImage())

        # wire up the "search" hotkey
        util.createHotkeyListener(self.activateSearch)

        return

    # Occurs when the user attempts to search for text (the user must have specified text to be searched for).
    # Should initiate program search logic.
    def performSearch(self, event):
        # perform search and return result
        # display result on the GUI

        self.result_images.clear()
        self.canvas_images.clear()

        self.search_images.overwriteWithScreenshot()
        self.result_images = self.model.locateText(self.view.searchbar_stringvar.get(), self.search_images, self.result_images)

        self.canvas_images.overwriteWith(self.result_images.asMatLike())
        self.view.applyImage(self.canvas_images.asPhotoImage())

        return

    # Occurs when the user attempts to enter the application. 
    # Should bring the application into focus and prompt text entry.
    def activateSearch(self):
        self.view.showSearchbar() # unhide search bar and bring into focus      # self.view.txt_searchbar
        return
        
    # Occurs when the user attempts to cancel/exit an action (such as a search).
    # Should reset the application to default state and hide (defocus) it.
    def cancel(self, event): 
        self.view.hideInterface() # if the interface is active, hide it         # self.view.root, self.view.searchbar_stringvar
        return
    
    # Occurs when the user attempts to quit the application
    # Should close the application and end the program.
    def quit(self, event):
        self.view.root.quit()
        return
    

