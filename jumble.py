import tkinter as tk
from tkinter import messagebox
import random

def jexecute(parent_root=None):
    """
    this function has all the steps/instructions for the jumble game
    :param parent_root: use the root window creates in main.py file if called from main.py file, 
                        if not it will create a new root indow, this is so that the window can be 
                        reused if called from main.py file to avoid problems
    :return: None
    """

    if parent_root is None:
        root = tk.Tk() # creates a new root window if called from this file, meaning that no root window currently exists
    else:
        root = tk.Toplevel(parent_root) # if called from main.py file, use the root window created in main.py file
          
    root.title("BRAINTIME JUMBLE") # set the title of the window
    root.geometry("400x525") # set the size of the window
    root.configure(bg="white") # set the background color of the window

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
            begin_quiz(flashcards) # calls the function begin_quiz with the flashcards as an argument
        except FileNotFoundError: # if the file is not found, show an error message
            messagebox.showerror("File Not Found", f"'{file_name}' not found! Ensure it's in the Flashcard Files folder.")

    def shuffle_text(text):
        """
        this function shuffles the text if the user chooses random
        :param text: the text to shuffle
        :return: the shuffled text
        """
        words = text.split(" ")
        shuffled_words = ["".join(random.sample(word, len(word))) for word in words]
        return " ".join(shuffled_words)

    def begin_quiz(flashcards):
        """
        this function begins the quiz
        :param flashcards: the flashcards which were loaded
        :return: None
        """
        global keys, index, current_flashcards, quiz_structure, hardmode # need to be global so that they can be used in other functions
        quiz_structure = structure_var.get() # get the quiz structure
        hardmode = hardmode_var.get() # hard mode or not
        keys = list(flashcards.keys()) # get the keys of the flashcards
        if order_var.get() == "random": # if the user chooses random, shuffle the keys
            random.shuffle(keys)
        index = 0 # set the index to 0 so the program know when to stop (index >= len(keys))
        current_flashcards = flashcards # set the current flashcards to the flashcards
        show_question() # call the function show_question

    def show_question():
        """
        this function shows the question
        :param: None
        :return: None
        """
        global index # need to be global so that it can be used in other functions
        if index >= len(keys): # if the index is greater than the length of the keys, show a message box and return. use = to because python is 0 indexed
            messagebox.showinfo("Quiz Completed", "You've reached the end of the quiz!")
            return
        question_window = tk.Toplevel(root) # create a new window
        question_window.title("QUESTION") # set the title of the window
        question_window.geometry("400x250+100+100") # set the size of the window
        question_window.configure(bg="white") # set the background color of the window
        question_window.transient(root)  # makes a 'child' window of the root window, this window depends on the root window
        
        question_text = keys[index] # get the question text
        answer_text = current_flashcards[question_text] # get the answer text
        
        if quiz_structure == "Question -> Answer": # if the quiz structure is question -> answer
            prompt = f"What is: {shuffle_text(answer_text)}" # prompt the user with the shuffled answer
            correct_answer = answer_text # set the correct answer to the answer text
        else: # if the quiz structure is answer -> question
            prompt = f"What is: {shuffle_text(question_text)}" # prompt the user with the shuffled question
            correct_answer = question_text # set the correct answer to the question text
        
        if hardmode == "hard": # if hard mode is on, make the prompt lowercase
            prompt = prompt.lower()
        
        # create a question label
        question_label = tk.Label(question_window, text=prompt, bg='white', fg='#000066', wraplength=380) # create a question label
        question_label.pack(pady=10) # pack the question label into the window
        
        # create an entry for the user to input their answer
        entry = tk.Entry(question_window) # create an entry for the user to input their answer
        entry.pack(pady=5) # pack the entry into the window
        
        def check_answer():
            """
            this function checks the answer
            :param: None
            :return: None
            """
            global index # need to be global so that it can be used in other functions
            user_answer = entry.get().strip() # get the user's answer
            feedback = "" # set the feedback to an empty string
            
            if user_answer.lower() == correct_answer.lower(): # if the user's answer is correct, set the feedback to "Correct!"
                feedback = "Correct!"
            else: # if the user's answer is incorrect, set the feedback to the correct answer
                feedback = f"Not exactly. Correct answer: {correct_answer}"
            
            messagebox.showinfo("Feedback", feedback) # show the feedback
            question_window.destroy() # destroy the question window, a new window is created for each question
            index += 1 # add 1 to the index
            show_question() # call the function show_question
        
        # create a submit button
        submit_button = tk.Button(question_window, text="Submit", command=check_answer, highlightbackground='white', fg='#000066')
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
        tutorial_window.geometry("400x250") # set the size of the window
        tutorial_window.configure(bg="white") # set the background color of the window
        tutorial_window.transient(root)  # makes a 'child' window of the root window, this window depends on the root window
        
        tutorial_text = (
            "This is the Jumble Quiz! You will be shown a scrambled question or answer, and you must unscramble it.\n\n"
            "To load a file, enter the filename (e.g., 'flashcards.txt').\n\n"
            "Flashcards should be formatted as: Question | Answer on each line.\n\n"
            "You can choose to shuffle the answer or the question. Hard mode will make everything lowercase."
        )
        # create a tutorial label
        tutorial_label = tk.Label(tutorial_window, text=tutorial_text, wraplength=380, bg='white', fg='#000066', justify=tk.LEFT)
        tutorial_label.pack(pady=10)
        # create a back button
        tk.Button(tutorial_window, text="Back", command=tutorial_window.destroy, highlightbackground="white").pack(pady=10)

    # create a description label
    description_label = tk.Label(root, text="Welcome to the Jumble Quiz! Press 'Tutorial' for instructions or 'Begin' to start.", wraplength=380, bg='white', fg='#000066')
    description_label.pack(pady=10)

    # create a file name label
    file_name_label = tk.Label(root, text="Enter the file name:", bg='white', fg='#000066')
    file_name_label.pack(pady=10)
    # create a file name entry
    file_name_entry = tk.Entry(root, width=15)
    file_name_entry.pack(pady=10)

    # create a structure label
    structure_label = tk.Label(root, text="Select the structure:", bg='white', fg='#000066')
    structure_label.pack(pady=10)
    # create a structure variable
    structure_var = tk.StringVar(root, value="Question -> Answer")  # set root as master and default value
    # create a structure radio button
    structure_q_to_a = tk.Radiobutton(root, text="Question -> Answer", variable=structure_var, value="Question -> Answer", bg='white', fg='#000066')
    structure_q_to_a.pack(padx=10)
    # create a structure radio button
    structure_a_to_q = tk.Radiobutton(root, text="Answer -> Question", variable=structure_var, value="Answer -> Question", bg='white', fg='#000066')
    structure_a_to_q.pack(padx=10)

    # create an order label
    order_var = tk.StringVar(root, value="order")  # set root as master so that the order variable can be used in other functions
    order_label = tk.Label(root, text="Select the order:", bg='white', fg='#000066') # create a order label
    order_label.pack(pady=10)
    # create an order radio button
    order_in_order = tk.Radiobutton(root, text="In Order", variable=order_var, value="order", bg='white', fg='#000066')
    order_in_order.pack()
    # create an order radio button
    order_random = tk.Radiobutton(root, text="Random", variable=order_var, value="random", bg='white', fg='#000066')
    order_random.pack()

    # create a hardmode label
    hardmode_var = tk.StringVar(root, value="hard")  # set root as master
    hardmode_label = tk.Label(root, text="Hard mode?", bg='white', fg='#000066') # create a hardmode label
    hardmode_label.pack(pady=10)
    # create a hardmode radio button
    hardmode_btn = tk.Radiobutton(root, text="Yes", variable=hardmode_var, value="hard", bg='white', fg='#000066')
    hardmode_btn.pack()
    # create an easymode radio button
    easymode_btn = tk.Radiobutton(root, text="No", variable=hardmode_var, value="easy", bg='white', fg='#000066')
    easymode_btn.pack()

    # create a button frame
    button_frame = tk.Frame(root, bg='white')
    button_frame.pack(pady=10)
    # create a tutorial button
    tutorial_button = tk.Button(button_frame, text="Tutorial", command=open_tutorial, highlightbackground='white', fg='#000066')
    tutorial_button.pack(side=tk.LEFT, padx=10)
    # create a begin button
    begin_button = tk.Button(button_frame, text="Begin", command=load_file, highlightbackground='white', fg='#000066')
    begin_button.pack(side=tk.LEFT, padx=10)
    # create a back button
    back_button = tk.Button(root, text="Back", command=root.destroy, highlightbackground="white", highlightthickness='2', fg='#000066')
    back_button.pack(pady=10)

    if parent_root is None:
        root.mainloop() # starts the main loop of the program if called from this file, if called from main.py, the main loop will not need to be started

if __name__ == "__main__":
    # this will only run if flashcards.py is executed directly
    jexecute()
