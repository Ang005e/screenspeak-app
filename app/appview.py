import tkinter as tk 
import ctypes
from tkinter import PhotoImage
import pyautogui


###### TKINTER APP ###### 

class AppView():

    def __init__(self):

        # prepare properties:
        self.txt_searchbar : tk.Entry
        self.image_panel : tk.Label
        self.searchbar_stringvar : tk.StringVar
        self.result_image: PhotoImage
        
        # create the app components
        self.root = tk.Tk() # initialise the root

        self.create(self.root)

    def create(self, root):

        width, height = pyautogui.size()
        root.geometry(f"{width}x{height}")
        root.configure(bg="black")  # Set the background color
        root.attributes("-topmost", True)  # Keep the window on top
        root.attributes("-transparentcolor", "black")  # Make black color transparent
        root.attributes("-fullscreen", True)

        self.makeAppClickthrough(root)
        
        # make the textvar for the searchbars entered text
        self.searchbar_stringvar = tk.StringVar(self.root, '')

        # make the searchbar
        self.txt_searchbar = tk.Entry(root, textvariable=self.searchbar_stringvar, fg="black", bg="black", font=("Arial", 16), border=0, insertbackground=("white"))
        self.txt_searchbar.pack(padx=10, pady=10)

        # ensure the search bar floats above the transparent image:
        self.txt_searchbar.lift()

        self.result_image = PhotoImage() # temporary photoimage variable

        # set it onto a Label the size of the screen
        self.image_panel = tk.Label(root, name='canvas', background='black', image=self.result_image, width=width, height=height)
        self.image_panel.pack(anchor="nw")



    def makeAppClickthrough(self, window : tk.Tk):
        """Set the window to be click-through (transparent and no interaction).
        Arguments: window - the window to be targeted"""

        if ctypes.windll.user32.IsWindowVisible(window.winfo_id()):
            # Make the window click-through using ctypes (Windows-specific)
            ctypes.windll.user32.SetWindowLongW(window.winfo_id(), -20, 0x80000000)
            ctypes.windll.user32.SetLayeredWindowAttributes(window.winfo_id(), 0, 0, 2)


    def showSearchbar(self):
        # show the searchbar 
        self.txt_searchbar["background"] = 'grey'
        self.txt_searchbar["foreground"] = 'white'
        self.txt_searchbar["border"] = 1

        # focus the searchbar
        self.txt_searchbar.focus_force()


    # TODO: Seperate hiding the searchbar from hiding the other widgets. They are different actions.  
    def hideInterface(self):
        self.searchbar_stringvar.set('')
        self.root.focus()
        for name, widget in self.root.children.items():

            widget : tk.Widget
            try:
                widget["background"] = 'black'
                widget["border"] = 0
                print(f"Sucessfully hid {name}")
            except TypeError:
                print(f'Failed to hide {name}')


    def applyImage(self, newImage: PhotoImage):
        self.result_image = newImage
        self.image_panel.configure(image=self.result_image)
        self.image_panel.update()
