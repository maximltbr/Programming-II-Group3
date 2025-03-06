import tkinter as tk
from tkinter import messagebox
import random
import time

def memexecute(parent_root=None):
    """
    this function has all the steps/instructions for the memory game
    :param parent_root: use the root window creates in main.py file if called from main.py file, 
                        if not it will create a new root indow, this is so that the window can be 
                        reused if called from main.py file to avoid problems
    :return: None
    """
    if parent_root is None:
        root = tk.Tk() # creates a new root window if called from this file, meaning that no root window currently exists
    else:
        root = tk.Toplevel(parent_root) # if called from main.py file, use the root window created in main.py file
        
    root.title("BRAINTRAIN MEMORYGAME") # set the title of the window
    root.geometry("400x350") # set the size of the window
    root.configure(bg="white") # set the background color of the window

    description_label = tk.Label(root, text="Welcome to the Memory Challenge Game!\nSelect Difficulty and Category.", wraplength=380, bg="white", fg="#000066") # create a description label
    description_label.pack(pady=10) # pack the description label

    # Difficulty Selection
    difficulty_frame = tk.Frame(root, bg="white") # create a difficulty frame
    difficulty_frame.pack() # pack the difficulty frame
    tk.Label(difficulty_frame, text="Difficulty:", bg="white", fg="#000066").pack() # create a difficulty label
    difficulty_var = tk.StringVar(value="Easy") # create a difficulty variable
    
    difficulty_easy = tk.Radiobutton(difficulty_frame, text="Easy", variable=difficulty_var, value="Easy", bg="white", fg="#000066") # create a difficulty radio button
    difficulty_easy.pack(anchor='w') # pack the difficulty radio button
    difficulty_medium = tk.Radiobutton(difficulty_frame, text="Medium", variable=difficulty_var, value="Medium", bg="white", fg="#000066") # create a difficulty radio button
    difficulty_medium.pack(anchor='w') # pack the difficulty radio button
    difficulty_hard = tk.Radiobutton(difficulty_frame, text="Hard", variable=difficulty_var, value="Hard", bg="white", fg="#000066")
    difficulty_hard.pack(anchor='w')

    # category Selection
    category_frame = tk.Frame(root, bg="white") # create a category frame
    category_frame.pack(pady=10) # pack the category frame
    tk.Label(category_frame, text="Category:", bg="white", fg="#000066").pack() # create a category label
    category_var = tk.StringVar(root)  # explicitly set the master window
    category_var.set("Colors")  # set initial value
    
    # create radio buttons for categories
    categories = ["Colors", "Animals", "Numbers"] # create a list of categories
    for category in categories:
        rb = tk.Radiobutton(category_frame, text=category, variable=category_var, value=category, bg="white", fg="#000066") # create a radio button
        rb.pack(anchor='w') # pack the radio button

    def get_random_items(difficulty, category):
        """
        this function gets the random items for the memory game based off the difficulty and category
        :param difficulty: the difficulty of the game
        :param category: the category of the game
        :return: the random items for the memory game
        """
        difficulty_levels = {
            "Easy": 5,
            "Medium": 7,
            "Hard": 9
        }
        
        categories = {
            "Colors": ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Pink", "Brown", "White"],
            "Animals": ["Dog", "Cat", "Elephant", "Lion", "Giraffe", "Tiger", "Monkey", "Zebra", "Snake"],
            "Numbers": ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
        }
        
        
        # get the number of items based on selected difficulty
        num_items = difficulty_levels.get(difficulty, 5)
        
        # get the items based on selected category
        category_items = categories.get(category)
        
        if not category_items: # if the category is not found, use the default category which is colors
            category_items = categories["Colors"]
        
        # chooses the number of items based on the number of items in the category
        num_items = min(num_items, len(category_items))
        
        # select random items from the chosen category
        selected_items = random.sample(category_items, num_items)
        return selected_items

    def start_memory_game():
        """
        starts the memory game
        :param: None
        :return: None
        """
        # get the difficulty and category selections
        current_difficulty = difficulty_var.get()
        current_category = category_var.get()
            
        global memory_window, items_label, entry_guess, start_button, submit_button, game_items, missing_item # declare the variables as global so that they can be used in other functions

        memory_window = tk.Toplevel(root) # create a memory window
        memory_window.title(f"MEMORY - {current_category.upper()}") # set the title of the memory window
        memory_window.geometry("500x250") # set the size of the memory window
        memory_window.configure(bg="white") # set the background color of the memory window
        
        # create a label for the memory game
        tk.Label(memory_window, text=f"Memorize the following {current_category.lower()}.", bg="white", fg="#000066").pack(pady=5)

        # show elements
        items_label = tk.Label(memory_window, text="", wraplength=480, bg="white", fg="#000066")
        items_label.pack(pady=10)

        # create an entry for the user to guess the missing item
        entry_guess = tk.Entry(memory_window, width=10, state="disabled")
        entry_guess.pack(pady=5)
        entry_guess.bind("<Return>", check_memory) # when the user presses enter, the check_memory function is called

        # create a button to start the game
        start_button = tk.Button(memory_window, text="Start", command=prepare_game, bg="white", highlightbackground="white")
        start_button.pack(pady=5)
        
        # create a button to submit the user's guess
        submit_button = tk.Button(memory_window, text="Submit", command=check_memory, bg="white", state="disabled", highlightbackground="white")
        submit_button.pack(pady=5)
        
        # create a button to go back to the main menu
        back_button = tk.Button(memory_window, text="Back", command=memory_window.destroy, bg="white", highlightbackground="white")
        back_button.pack(pady=5)

        # prepare game items with current selections
        game_items = get_random_items(current_difficulty, current_category)
        
        # display all items initially
        items_label.config(text=" , ".join(game_items))

    def prepare_game():
        """
        this function prepares the game items for the memory game
        :param: None
        :return: None
        """
        global missing_item # declare the missing item as global so that it can be used in other functions
        
        # remove one item
        missing_item = random.choice(game_items)

        # show the elements but without the missing item
        displayed_items = game_items.copy()
        displayed_items.remove(missing_item)
        
        # update label with remaining items
        items_label.config(text=" , ".join(displayed_items))
        
        # enable entry box and submit button
        entry_guess.config(state="normal") # enable the guess entry
        entry_guess.delete(0, tk.END) # delete the text in the guess entry
        entry_guess.focus() # focus on the guess entry
        submit_button.config(state="normal") # enable the submit button
        start_button.config(state="disabled") # disable the start button

    def check_memory(event=None):
        """
        this function checks the user's guess for the memory game
        :param event: lets the user use the return key to submit their answer
        :return: None
        """
        user_guess = entry_guess.get().strip() # get the user's guess
        
        # check if the user's guess is correct
        if user_guess.lower() == missing_item.lower():
            messagebox.showinfo("Memory Test Result", "Correct! Great memory!")
        else:
            messagebox.showinfo("Memory Test Result", f"Wrong! The missing item was '{missing_item}'")

        # reset for a new round
        items_label.config(text=" , ".join(game_items)) # update the label with the game items
        entry_guess.delete(0, tk.END) # delete the text in the guess entry
        entry_guess.config(state="disabled") # disable the guess entry
        submit_button.config(state="disabled") # disable the submit button
        start_button.config(state="normal") # enable the start button

    def open_tutorial():
        """
        this function opens the tutorial for the memory game
        :param: None
        :return: None
        """
        tutorial_window = tk.Toplevel(root) # create a tutorial window
        tutorial_window.title("TUTORIAL") # set the title of the tutorial window
        tutorial_window.geometry("400x300") # set the size of the tutorial window
        tutorial_window.configure(bg="white") # set the background color of the tutorial window
        
        tutorial_text = (
            "Welcome to the Memory Challenge Game!\n\n"
            "How to Play:\n"
            "1. Select Difficulty and Category.\n"
            "2. Click 'Begin' to open the test.\n"
            "3. All items will be shown first.\n"
            "4. Click 'Start' to remove one item.\n"
            "5. Remember the missing item.\n"
            "6. Type the missing item and press 'Submit'.\n\n"
            "Challenge yourself and improve your memory!"
        )
        
        # create a tutorial label
        tutorial_label = tk.Label(tutorial_window, text=tutorial_text, wraplength=380, bg="white", fg="#000066", justify=tk.LEFT)
        tutorial_label.pack(pady=10)
        
        # create a close button
        close_button = tk.Button(tutorial_window, text="Close", command=tutorial_window.destroy, highlightbackground="white")
        close_button.pack(pady=10)

    # create a frame for the buttons
    main_buttons_frame = tk.Frame(root, bg="white")
    main_buttons_frame.pack()

    # create a tutorial button
    tutorial_button = tk.Button(main_buttons_frame, text="Tutorial", command=open_tutorial, highlightbackground="white", fg="#000066")
    tutorial_button.pack(side=tk.LEFT, padx=10)

    # create a begin button
    begin_button = tk.Button(main_buttons_frame, text="Begin", command=start_memory_game, highlightbackground="white", fg="#000066")
    begin_button.pack(side=tk.LEFT, padx=10)

    # create a back button
    back_button = tk.Button(root, text="Back", command=root.destroy, highlightbackground="white", highlightthickness="2", fg="#000066")
    back_button.pack(pady=10)

    if parent_root is None:
        root.mainloop() # starts the main loop of the program if called from this file, if called from main.py, the main loop will not need to be started


if __name__ == "__main__":
    # this will only run if order.py is executed directly
    memexecute()