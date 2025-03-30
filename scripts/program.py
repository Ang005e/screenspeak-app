
# import keyboard # use keyboard so that search can be accessed even when focus is not on the tkinter app
from appmodel import AppModel
from appview import AppView
from appcontroller import AppController
import logging
import util


# Note: ** marks a completed feature

# ideas:
# focus and event handling will be hard (alt-F4). so move window off the screen when not in use? move back when searching, and when displaying?

# PROTOTYPE 1:
# create transparent, click through application frame with tkinter      **************
# using cv, create a rectangle on a transparent image                   **************
# display transparent, outlined image on tkinter canvas                 **************

# make showable and hideable searchbox                                  **************

# PROTOTYPE 2:
# using pytesseract, search for characters on the screen.               # CURRENT WORK 
# draw a rect around the found area
# display rect


# Future features:
# get and use voice input
# search within certain page selection
# overly complex: do an automated "sweep" search (scroll to top, scroll down 
# until bottom of scrollable element is reached, parse images from screenshots)
# get keypresses through other applications



###### DEFENITIONS ######

# set the close, show and search events to be the below functions:


# MAIN CODE:

# ToDo: .... ....

# Explanation...
# 
# 1. Creates any required application images
#   - Initialises AppImage objects with 2 formats - MatLike and PIL Image
#   - Waits until AppImage.activate() has been called to initialise the 3rd format (PhotoImage) due to dependancy on tk.Tk() (GUI) being initialised
# 
# 2. Initialises and builds the application
#   - Initialises the root tk.Tk() application
#   - Controller calls markup_image.activate() to make _gui_image availble
#   - .


image_folder_name = 'images'
canvas_image_path = util.resourcePath(util.buildPath(image_folder_name, 'canvas_image.png'))
search_image_path = util.resourcePath(util.buildPath(image_folder_name, 'search_image.png')) 
result_image_path = util.resourcePath(util.buildPath(image_folder_name, 'result_image.png'))

logging.basicConfig(filename='app_debug.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

try:

    view = AppView()
    model = AppModel()

    controller = AppController(
        view, 
        model,
        canvas_image_path, 
        search_image_path, 
        result_image_path
        )

    if __name__ == '__main__':
        controller.begin()

except Exception as e:
    logging.exception("An error occurred")

"""
def loadEvent():
    markupImage.activate()
    
def closeEvent(app : AppView):
    app.showInterface(app.txt_searchbar)

def showEvent(app : AppView):
    app.hideInterface(app.root, app.searchbar_stringvar)

def searchEvent(app : AppView):
    start_coords, end_coords = ocr.performSearch(app.image_panel, app.searchbar_stringvar, app.markup_image)
    AppImage.drawRect(app.markup_image, start_coords, end_coords) # draw on the image

    self.image_panel.configure(image=self.markup_image)
    self.image_panel.image = self.markup_image
    self.image_panel.update()

    # remove old highlighting:
    gui.GuiHelpers.opaqueScreenImage(self.markup_image)


AppController.cancel = closeEvent
AppController.enter = showEvent
AppController.search = searchEvent
AppController.load = loadEvent
"""

