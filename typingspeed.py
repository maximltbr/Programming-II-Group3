import tkinter as tk
from tkinter import messagebox
import time
import random

def typexecute(parent_root=None):
    """
    this function has all the steps/instructions for the typing speed game
    :param parent_root: use the root window creates in main.py file if called from main.py file, 
                        if not it will create a new root indow, this is so that the window can be 
                        reused if called from main.py file to avoid problems
    :return: None
    """
    if parent_root is None:
        root = tk.Tk() # creates a new root window if called from this file, meaning that no root window currently exists
    else:
        root = tk.Toplevel(parent_root) # if called from main.py file, use the root window created in main.py file
        
    root.title("BRAINTRAIN TYPINGSPEED") # set the title of the window
    root.geometry("400x200") # set the size of the window
    root.configure(bg="white") # set the background color of the window

    def get_random_sentence():
        """
        this function gets a random sentence from the list of sentences
        :param: None
        :return: a random sentence from the list of sentences
        """
        sentences = [
            "It is what it is my homie, see you around!",
            "What is the definition of Bomboclaat? Mi Bomboclaat",
            "How fast can you really type with your eyes closed?",
            "Practice makes perfect when learning to type quickly.",
            "Hi, welcome to McDonald's, would you like any fries with that?"
        ]
        return random.choice(sentences)

    def start_typing_game():
        """
        this function starts the typing speed game
        :param: None
        :return: None
        """
        global typing_window, sentence_label, entry_typing, start_button, submit_button, start_time, target_sentence # need to be global so that they can be used in other functions
        
        typing_window = tk.Toplevel(root) # create a new toplevel window
        typing_window.title("TYPE") # set the title of the window
        typing_window.geometry("500x250") # set the size of the window
        typing_window.configure(bg="white") # set the background color of the window
        typing_window.transient(root)  # makes a 'child' window of the root window, this window depends on the root window
        
        tk.Label(typing_window, text="Press 'Start' to reveal the sentence.", bg="white", fg="#000066").pack(pady=5)

        # sentence starts hidden, the text is ""
        sentence_label = tk.Label(typing_window, text="", wraplength=480, bg="white", fg="black")
        sentence_label.pack(pady=10)

        # create a text entry box
        entry_typing = tk.Entry(typing_window, width=50, state="disabled")
        entry_typing.pack(pady=5)
        entry_typing.bind("<Return>", check_typing_speed) # bind the check_typing_speed function to the return key, you can press enter to submit your answer

        # create a start button
        start_button = tk.Button(typing_window, text="Start", command=start_timer, bg="white", highlightbackground="white")
        start_button.pack(pady=5)
        
        # create a submit button
        submit_button = tk.Button(typing_window, text="Submit", command=check_typing_speed, bg="white", state="disabled", highlightbackground="white")
        submit_button.pack(pady=5)
        
        # create a back button
        back_button = tk.Button(typing_window, text="Back", command=typing_window.destroy, bg="white", highlightbackground="white")
        back_button.pack(pady=5)

    def start_timer():
        """
        this function starts the timer and reveals the sentence
        :param: None
        :return: None
        """
        global start_time, target_sentence # need to be global so that they can be used in other functions

        start_time = time.time() # start the timer
        target_sentence = get_random_sentence() # get a random sentence
        
        # reveal the sentence, since before it was just ""
        sentence_label.config(text=target_sentence) 
        
        # enable typing entry and submit button
        entry_typing.config(state="normal") # enable the typing entry
        entry_typing.delete(0, tk.END) # delete the text in the entry box
        entry_typing.focus() # focus on the entry box
        submit_button.config(state="normal") # enable the submit button
        start_button.config(state="disabled")  # disable start button after clicking

    def check_typing_speed(event=None): 
        """
        this function checks the typing speed
        :param event: lets the user use the return key to submit their answer
        :return: None
        """
        global target_sentence # need to be global so that it can be used in other functions

        end_time = time.time() # end the timer
        elapsed_time = end_time - start_time # calculate the elapsed time

        user_input = entry_typing.get().strip() # get the user's input
        
        correct_chars = sum(1 for a, b in zip(target_sentence, user_input) if a == b) # calculate the number of correct characters
        accuracy = (correct_chars / len(target_sentence)) * 100 if target_sentence else 0 # calculates the accuracy

        words = len(target_sentence.split()) # calculate the number of words
        words_per_minute = (words / elapsed_time) * 60 if elapsed_time > 0 else 0 # calculate the words per minute

        messagebox.showinfo("Typing Speed Results", 
                            f"Time taken: {elapsed_time:.2f} seconds\n"
                            f"Typing speed: {words_per_minute:.2f} words per minute\n"
                            f"Accuracy: {accuracy:.2f}%")

        # clear sentence and reset for a new round
        sentence_label.config(text="") # clear the sentence
        entry_typing.delete(0, tk.END) # delete the text in the entry box
        entry_typing.config(state="disabled") # disable the entry box
        submit_button.config(state="disabled") # disable the submit button
        start_button.config(state="normal")  # re-enable start button for a new test

    def open_tutorial():
        tutorial_window = tk.Toplevel(root)
        tutorial_window.title("TUTORIAL")
        tutorial_window.geometry("400x300")
        tutorial_window.configure(bg="white")
        tutorial_window.transient(root)  # # makes a 'child' window of the root window, this window depends on the root window
        
        tutorial_text = (
            "Welcome to the Typing Speed Game!\n\n"
            "How to Play:\n"
            "1. Click 'Begin' to open the test.\n"
            "2. Click 'Start' to reveal the sentence and begin typing.\n"
            "3. Type the sentence exactly and press 'Enter' or click 'Submit'.\n"
            "4. Your typing speed (WPM), accuracy, and time will be displayed.\n"
            "5. The sentence will disappear, and you can press 'Start' to get a new one.\n\n"
            "Improve your speed by practicing regularly!"
        )
        
        # create a tutorial label
        tutorial_label = tk.Label(tutorial_window, text=tutorial_text, wraplength=380, bg="white", fg="#000066", justify=tk.LEFT)
        tutorial_label.pack(pady=10)
        
        # create a close button
        close_button = tk.Button(tutorial_window, text="Close", command=tutorial_window.destroy, highlightbackground="white")
        close_button.pack(pady=10)

    # create a description label
    description_label = tk.Label(root, text="Welcome to the Typing Speed Game!\nPress 'Begin' to start.", wraplength=380, bg="white", fg="#000066")
    description_label.pack(pady=10)

    # create a main buttons frame
    main_buttons_frame = tk.Frame(root, bg="white")
    main_buttons_frame.pack()

    # create a tutorial button
    tutorial_button = tk.Button(main_buttons_frame, text="Tutorial", command=open_tutorial, highlightbackground="white", fg="#000066")
    tutorial_button.pack(side=tk.LEFT, padx=10)

    # create a begin button
    typing_game_button = tk.Button(main_buttons_frame, text="Begin", command=start_typing_game, highlightbackground="white", fg="#000066")
    typing_game_button.pack(side=tk.LEFT, padx=10)

    # create a back button
    back_button = tk.Button(root, text="Back", command=root.destroy, highlightbackground="white", highlightthickness="2")
    back_button.pack(pady=10)

    if parent_root is None:
        root.mainloop() # starts the main loop of the program if called from this file, if called from main.py, the main loop will not need to be started

if __name__ == "__main__":
    # this will only run if typingspeed.py is executed directly
    typexecute()