import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk  # For JPG support
import os

def flexecute(parent_root=None):
    """
    this function has all the steps/instructions for the flashcards game
    :param parent_root: use the root window creates in main.py file if called from main.py file, 
                        if not it will create a new root indow, this is so that the window can be 
                        reused if called from main.py file to avoid problems
    :return: None
    """
    if parent_root is None:
        root = tk.Tk() # creates a new root window if called from this file, meaning that no root window currently exists
    else:
        root = tk.Toplevel(parent_root) # if called from main.py file, use the root window created in main.py file
        
    root.title("BRAINTRAIN FLASHCARDS") # set the title of the window
    root.geometry("400x450") # set the size of the window
    root.configure(bg="white") # set the background color of the window

    def show_question():
        """
        this function shows the question and answer to the user
        :param: None
        :return: None
        """
        global index, keys, current_flashcards, quiz_structure # declare the variables as global so that they can be used in other functions

        if index >= len(keys): # if the index is greater than the number of keys, show the user a message and return
            # the IDE says index has a problem, but it works because we define index later in the code
            messagebox.showinfo("Quiz Completed", "You've reached the end of the quiz!")
            return

        question_window = tk.Toplevel(root) # create a new window for the question
        question_window.title("QUESTION")
        question_window.geometry("400x200+100+100")
        question_window.configure(bg="white")
        question_window.transient(root)  # makes a 'child' window of the root window, this window depends on the root window# Make it transient to root

        question_text = keys[index] # get the question from the keys list
        answer_text = current_flashcards[question_text] # get the answer from the current flashcards dictionary

        if quiz_structure == "Question -> Answer": # if the quiz structure is question -> answer, show the question
            prompt = f"Concept: {question_text}"
            correct_answer = answer_text
        else:
            prompt = f"Definition: {answer_text}" # if the quiz structure is answer -> question, show the answer
            correct_answer = question_text

        question = tk.Label(question_window, text=prompt,  bg = 'white', fg="#000066", wraplength=380) # create a label for the question
        question.pack(pady=10)

        entry = tk.Entry(question_window) # create an entry for the user to answer the question
        entry.pack(pady=5)

        def check_answer():
            """
            this function checks the user's answer and provides feedback
            :param: None
            :return: None
            """
            global index
            user_answer = entry.get().strip() # get the user's answer

            if user_answer.lower() == correct_answer.lower(): # if the user's answer is correct, show the user a message
                feedback = "Correct!"
            else:
                feedback = f"Not exactly.\nCorrect answer: {correct_answer}" # if the user's answer is incorrect, show the user the correct answer

            messagebox.showinfo("Feedback", feedback) # show the user the feedback
            question_window.destroy() # destroy the question window
            index += 1 # add 1 to the index
            show_question() # show the next question

        # create a submit button 
        submit_button = tk.Button(question_window, text="Submit", command=check_answer, bg="white", highlightbackground="white") # create a submit button
        submit_button.pack(pady=10)

        # create a back button
        back_button = tk.Button(question_window, text="Back", command=question_window.destroy, highlightbackground="white", highlightthickness='2', fg='#000066')
        back_button.pack(pady=10)

    def open_tutorial():
        """
        this function opens the tutorial
        :param: None
        :return: None
        """ 
        tutorial_window = tk.Toplevel(root) # create a new window
        tutorial_window.title("TUTORIAL") # set the title of the window
        tutorial_window.geometry("400x525") # set the size of the window
        tutorial_window.configure(bg="white") # set the background color of the window
        tutorial_window.transient(root)  # makes a 'child' window of the root window, this window depends on the root window

        tutorial_text = (
            "This is the flashcard quiz. You will be shown a question or definition, and you will have to provide the corresponding definition or question, respectively.\n\n"
            "You can choose to view the question and provide the answer, or view the answer and provide the question.\n\n"
            "To load a file, please place it in this folder and type the filename (e.g., 'flashcards.txt') when prompted.\n\n"
            "There are a few preset files in a subfolder you can use.\n\n"
            "If you'd like to create your own, please follow this format:\n"
            "Question 1|Answer 1\n"
            "Question 2|Answer 2\n"
            "You must separate the question and answer with a vertical bar '|'. Each pair must be on a new line.\n\n"
            "If you'd like to generate your own flashcards using study material, you can use an external AI agent like ChatGPT with the following prompt:\n\n"
            "Please format the following content into a flashcard file, where each line contains 'Question | Answer', with each pair of question and answer on a new line. If needed, process the content for clarity. After formatting the content, create a downloadable file for me.\n"
        )
        # create a tutorial label   
        tutorial_label = tk.Label(tutorial_window, text=tutorial_text, wraplength=380, bg='white', fg='#000066', justify=tk.LEFT)
        tutorial_label.pack(pady=10)
        
        # create a back button
        back_button = tk.Button(tutorial_window, text="Back", command=tutorial_window.destroy, highlightbackground="white", highlightthickness='2')
        back_button.pack(pady=10)

    def begin_quiz(flashcards, structure, order):
        """
        this function begins the quiz
        :param flashcards: the flashcards to be used in the quiz
        :param structure: the structure of the quiz
        :param order: the order of the quiz
        :return: None
        """
        global keys, index, current_flashcards, quiz_structure # declare the variables as global so that they can be used in other functions
        
        quiz_structure = structure # set the quiz structure
        keys = list(flashcards.keys()) # get the keys of the flashcards

        if order == "random": # if the order is random, shuffle the keys
            random.shuffle(keys)

        index = 0 # set the index to 0  
        current_flashcards = flashcards # set the current flashcards to the flashcards
        show_question() # show the first question

    def load_file():
        """
        this function loads the file and creates a dictionary of the flashcards,
        it loads the file where the flashcards are stored
        :param: None
        :return: None
        """
        flashcards = {}
        file_name = file_name_entry.get()
        filepath = "Flashcard Files/" + file_name
        try: # try to open the file and read the flashcards
            with open(filepath, "r", encoding="utf-8") as file: # reads the file
                for line in file:
                    question, answer = line.strip().split("|", 1)
                    flashcards[question.strip()] = answer.strip()
            begin_quiz(flashcards, structure_var.get(), order_var.get()) # calls the function begin_quiz with the flashcards as an argument
        except FileNotFoundError: # if the file is not found, show an error message
            messagebox.showerror("File Not Found", f"'{file_name}' not found! Ensure it's in the Flashcard Files folder.")

    # create a description label
    description_label = tk.Label(root, text="Welcome to the flashcard quiz! If this is your first time, please press 'tutorial' to view the tutorial. Otherwise, press 'begin': ", wraplength=380, bg='white', fg='#000066')
    description_label.pack(pady=10)

    # create a file name label
    file_name_label = tk.Label(root, text="Enter the file name:", bg='white', fg='#000066')
    file_name_label.pack(pady=10)
    # create a file name entry
    file_name_entry = tk.Entry(root, width=15)
    file_name_entry.pack(pady=10)

    # create a structure variable
    structure_var = tk.StringVar(root, value="Question -> Answer")  # Set root as master
    # create a structure label
    structure_label = tk.Label(root, text="Select the structure:", bg='white', fg='#000066')
    structure_label.pack(pady=10)
    # create a structure frame
    structure_frame = tk.Frame(root, bg='white')
    structure_frame.pack(pady=10)
    # create a structure radio button
    structure_q_to_a = tk.Radiobutton(structure_frame, text="Question -> Answer", variable=structure_var, value="Question -> Answer", bg='white', fg='#000066')
    structure_q_to_a.pack(side=tk.LEFT, padx=10)
    # create a structure radio button
    structure_a_to_q = tk.Radiobutton(structure_frame, text="Answer -> Question", variable=structure_var, value="Answer -> Question", bg='white', fg='#000066')
    structure_a_to_q.pack(side=tk.LEFT, padx=10)

    # create an order variable
    order_var = tk.StringVar(root, value="order")  # Set root as master
    # create an order label
    order_label = tk.Label(root, text="Select the order:", bg='white', fg='#000066')
    order_label.pack(pady=10)
    # create an order frame
    order_frame = tk.Frame(root, bg='white')
    order_frame.pack(pady=10)
    # create an order radio button
    order_in_order = tk.Radiobutton(order_frame, text="In Order", variable=order_var, value="order", bg='white', fg='#000066')
    order_in_order.pack(side=tk.LEFT, padx=10)
    # create an order radio button
    order_random = tk.Radiobutton(order_frame, text="Random", variable=order_var, value="random", bg='white', fg='#000066')
    order_random.pack(side=tk.LEFT, padx=10)

    # create a frame
    frame = tk.Frame(root, bg='white')
    frame.pack()
    # create a tutorial button
    tutorial_button = tk.Button(frame, text="Tutorial", command=open_tutorial, highlightbackground='white', fg='#000066')
    tutorial_button.pack(side=tk.LEFT, padx=10, pady=10)
    # create a begin button
    begin_button = tk.Button(frame, text="Begin", command=load_file, highlightbackground='white', fg='#000066')
    begin_button.pack(side=tk.LEFT, padx=10, pady=10)
    # create a back button  
    back_button = tk.Button(root, text="Back", command=root.destroy, highlightbackground="white", fg='#000066', highlightthickness='2')
    back_button.pack(pady=10)

    if parent_root is None:
        root.mainloop() # starts the main loop of the program if called from this file, if called from main.py, the main loop will not need to be started  

if __name__ == "__main__":
    # This will only run if flashcards.py is executed directly
    flexecute()