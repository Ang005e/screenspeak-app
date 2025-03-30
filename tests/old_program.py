import numpy as np
import random

import tkinter as tk
import pyautogui 
import keyboard # use keyboard so that search can be accessed even when focus is not on the tkinter app

import cv2 as cv
import pytesseract
from PIL import Image
from pandas import DataFrame

import ctypes



pytesseract.pytesseract.tesseract_cmd = 'E:\\TAFE\\ICTPRG_440_python\\Computer-Vision-Prototype\\tesseract\\tesseract.exe'


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


def drawRect(image_path : str, start : tuple[int, int], end : tuple[int, int]):
    """Draws a rectangle over the image at the given file path.\n
    Takes a start coordinate, end coordinate and path to an image as inputs."""

    img = cv.imread(image_path)
    colour = (255, 0, 0, 255) # RGBA
    drawn_img = cv.rectangle(img, start, end, colour, 1)
    cv.imwrite(image_path, drawn_img)


# TKINTER WINDOW:


def makeWindowClickthrough(window : tk.Tk):
    """Set the window to be click-through (transparent and no interaction).
    Arguments: window - the window to be targeted"""

    if ctypes.windll.user32.IsWindowVisible(window.winfo_id()):
        # Make the window click-through using ctypes (Windows-specific)
        ctypes.windll.user32.SetWindowLongW(window.winfo_id(), -20, 0x80000000)
        ctypes.windll.user32.SetLayeredWindowAttributes(window.winfo_id(), 0, 0, 2)


########
def createOverlay(highlighted_image_path : str, clear_image_path : str, search_text_element : tk.StringVar):

    root = tk.Tk()
    width, height = pyautogui.size()
    root.geometry(f"{width}x{height}")
    root.configure(bg="black")  # Set the background color
    root.attributes("-topmost", True)  # Keep the window on top
    root.attributes("-transparentcolor", "black")  # Make black color transparent
    root.attributes("-fullscreen", True)

    makeWindowClickthrough(root)

    txt_searchbar = tk.Entry(root, textvariable=search_text_element, fg="black", bg="black", font=("Arial", 16), border=0, insertbackground=("white"))
    txt_searchbar.pack(padx=10, pady=10)
    # ensure the search bar floats above the transparent image:
    txt_searchbar.lift()

    highlighted_image = tk.PhotoImage(highlighted_image_path)

    # set it onto a Label the size of the screen
    image_panel = tk.Label(root, name='canvas', background='black', image=highlighted_image, width=width, height=height)
    image_panel.pack(anchor="nw")

    clear_image = tk.PhotoImage(file=clear_image_path)

    root.bind('<Alt-F12>', lambda x: showSearchBar(txt_searchbar))
    root.bind('<Escape>', lambda x: hideWidgets(root, search_text_element, clear_image))
    root.bind('<Return>', lambda x: performSearch(image_panel, search_text_element, highlighted_image_path))

    return root


######## Main Functions #########



# (on enter key event) get user input, take screenshot
def findScreenText(text : str, search_image_path):

    # read screenshot to find text in
    search_image = pyautogui.screenshot(search_image_path)

    # perform text extraction
    # image = Image.open(search_image) not needed?
    
    # filter text by search criteria,

    # get coords, return tuple array i.e. for tup in arr: startx, starty, endx, endy = tup
    data = pytesseract.image_to_data(search_image, output_type='dict')
    boxes = len(data['level'])
    image_matlike = cv.imread(search_image)
    adjacent_words = []
    for i in range(boxes):

        # the current code is for taking seperated words that are adjacent to eachother and checking if they are 
        # (when put together) the search text. is that needed, though?

        # check if the current text is equal to the searched text. if not, compare to the naxt run in case it's only part of the string.
        current_text : str = data['text'][i] # should i strip for the matching operation? would that break it? (think, matching whole words)

        if current_text in text:
            adjacent_words.append(current_text.strip())
        else:
            adjacent_words.clear() # there's a break in the matches, so empty the adjacent matches array.

        # combine adjacent words and check if they are in the search text altogether
        (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
        # Draw box        
        drawn_img = cv.rectangle(image_matlike, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv.imwrite('./images/outlined_img.png', drawn_img)

######## COMPUTER VISION HELPERS ########

def opaqueScreenImage(path : str):
    pix_y, pix_x = pyautogui.size()
    img = np.zeros((pix_x, pix_y, 4), np.uint8) # opaque image. array format is x, y and channels (4, BGRA)
    cv.imwrite(path, img)


######## GUI HELPERS #########


def showSearchBar(txt_searchbar : tk.Text):
    txt_searchbar["background"] = 'grey'
    txt_searchbar["foreground"] = 'white'
    txt_searchbar["border"] = 1
    txt_searchbar.focus_force()


def hideWidgets(root : tk.Tk, search_text : tk.StringVar, clear_image : tk.PhotoImage):
    search_text.set('')
    root.focus()
    for name, widget in root.children.items():

        widget : tk.Widget
        print(f"Attempting to hide widget: {name}")
        try:
            widget["background"] = 'black'
            widget["border"] = 0
            print(f"Sucessfully hid {name}")
        except TypeError:
            print(f'Failed to hide {name}')

        if type(widget) == tk.Label: # if its the label holding the image:
            widget.configure(image=clear_image)


def run(root : tk.Tk):
    # keyboard.on_press(keyChecker) # detect when the user presses any key
    root.mainloop()


def performSearch(image_panel : tk.Label, search_text_element : tk.StringVar, highlighted_image_path : str):
    # carry out a search, and update GUI with the results

    # do the find screen text function here 
    
    # update the "canvas image" with the highlighted results
    start_coords = random.randint(200, 1000)
    end_coords = random.randint(200, 1000)
    drawRect(highlighted_image_path, start_coords, end_coords) # draw on the image

    img = tk.PhotoImage(file=highlighted_image_path)

    image_panel.configure(image=img)
    image_panel.image = img
    image_panel.update()

    # remove old highlighting:
    opaqueScreenImage(highlighted_image_path)





# Globals
image_panel : tk.Label
highlighted_image : tk.PhotoImage

# MAIN CODE:

# ToDo:
# add file path argument to the drawRect function
# add search_img_path argument to findScreenText function

search_img_path = './images/search_image.png'

highlighted_image_path = './images/canvas_image.png' 
clear_image_path = './images/default_image.png' 
opaqueScreenImage(highlighted_image_path) # create a transparent image the size of the screen to draw on
opaqueScreenImage(clear_image_path) # create a transparent image the size of the screen to hide the drawn image

# Create the overlay
search_text_element = tk.StringVar('')
root = createOverlay(highlighted_image_path, clear_image_path, search_text_element)

run(root)

cv.waitKey(0)
cv.destroyAllWindows()