import tkinter as tk
from PIL import Image, ImageTk  # For JPG support
import os
from flashcards import flexecute
from jumble import jexecute
from mathrand import mexecute
from typingspeed import typexecute
from order import memexecute
from reactiontime import rexecute

def on_button_click(button_number):
    """
    this function will manage/handle the button clicks, when the user presses a button, the appropriate function will be called

    :param button_number: int, this is the number of the button that was clicked
    :return: None
    """
    if button_number == 1:
        flexecute(root)
    if button_number ==2:
        jexecute(root)
    if button_number ==3:
        mexecute(root)
    if button_number ==4:
        typexecute(root)
    if button_number ==5:
        rexecute(root)
    if button_number ==6:
        memexecute(root)
    else:
        return 


# creates the main windoe
root = tk.Tk()
root.title("BRAINTRAIN") # sets the title of the window
root.geometry("400x600")  # change the size of the window
root.configure(bg="white") # sets the background color of the window

# description label
description_label = tk.Label(root, text="Welcome to BrainTrain: All in One Study Companion! "
                                        "This app is designed to enhance your learning experience "
                                        "with interactive study tools, including customizable flashcards, "
                                        "engaging word scramble games, and typing speed tests. Import or create "
                                        "your own question sets, track your progress, and challenge yourself "
                                        "with various educational games tailored to boost your memory and "
                                        "knowledge retention. Get ready to make studying fun and effective!",
                             wraplength=380, bg='white', fg='#000066')
description_label.pack(pady=10) # packs the description label into the window

# frame to hold buttons and descriptions
frame = tk.Frame(root, bg='white')
frame.pack()

# dictionary mapping image file names to their name
images_info = {
    "books.png": "Flashcard Study Tool 📚",
    "memo.png": "Word Scramble Game 📝",
    "division.png": "Math Quiz Generator ➗",
    "keyboard.png": "Typing Speed Tester ⌨️",
    "zap.png": "Reaction Time Tester ⚡",
    "shuffle.png": "Remember the Order Game 🔀"
}

# load images and create buttons/labels
for index, (image_file, name) in enumerate(images_info.items(), start=1): # use enumerate to iterate over a dict
    # load and resize image
    image_path = os.path.join("./images", image_file)  # get all the images from the images folder
    img = ImageTk.PhotoImage(Image.open(image_path).resize((50, 50))) # resize the image to 50x50 so they fit uniformally

    # create button, use lambda to pass the index as the button number
    button = tk.Button(frame, image=img, command=lambda button_number=index: on_button_click(button_number), highlightbackground="#000066", highlightthickness='2')
    button.grid(row=index, column=0, padx=10, pady=5)

    # create label which has the name of each different brain game
    label = tk.Label(frame, text=name, bg='white', fg='#000066')
    label.grid(row=index, column=1, padx=10, pady=5, sticky='w')

    # map the image to the button
    button.image = img

# run the Tkinter event loop, basically creates the window and keeps it open
root.mainloop()
