import tkinter as tk
from tkinter import messagebox
import random
import operator
import sympy as sp

def mexecute(parent_root=None):
    """
    this function has all the steps/instructions for the math game
    :param parent_root: use the root window creates in main.py file if called from main.py file, 
                        if not it will create a new root indow, this is so that the window can be 
                        reused if called from main.py file to avoid problems
    :return: None
    """
    if parent_root is None:
        root = tk.Tk() # creates a new root window if called from this file, meaning that no root window currently exists
    else:
        root = tk.Toplevel(parent_root) # if called from main.py file, use the root window created in main.py file
        
    root.title("BRAINTRAIN MATH") # set the title of the window
    root.geometry("400x225") # set the size of the window
    root.configure(bg="white") # set the background color of the window

    def generate_math():
        """
        this function generates a random simple problem
        :param: None
        :return: a random simple math problem and the answer to the problem
        """
        operators = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
            "/": operator.truediv
        }
        
        num1 = random.randint(1, 100)
        num2 = random.randint(1, 100)
        op = random.choice(list(operators.keys()))

        if op == "/":
            num1 = num2 * random.randint(1, 10)

        problem = f"{num1} {op} {num2}"
        answer = operators[op](num1, num2)
        return problem, answer

    def generatedifint():
        """
        this function generates a random differential/integrate math problem
        :param: None
        :return: a random differential/integrate math problem and the solution to the problem
        """
        x = sp.Symbol('x')
        coefficient = random.randint(1, 10)
        exponent = random.randint(1, 5)
        func = coefficient * x**exponent
        
        if random.choice(["differentiate", "integrate"]) == "differentiate":
            problem = f"Differentiate: d/dx ({sp.latex(func)})"
            solution = sp.diff(func, x)
        else:
            problem = f"Integrate: ∫ ({sp.latex(func)}) dx"
            solution = sp.integrate(func, x)
        return problem, solution

    def math_challenge():
        """
        this function generates a math problem based on what the user wants
        :param: None
        :return: a random math problem and the answer to the problem
        """
        if math_type_var.get() == "simple":
            problem, answer = generate_math()
        else:
            problem, answer = generatedifint()
        
        math_label.config(text=problem) # sets the problem to the math label
        math_label.answer = answer # sets the answer to the math label
        entry_math.delete(0, tk.END) # deletes the text in the math entry

    def check_math_answer():
        """
        this function checks the answer with the user input
        :param: None
        :return: None
        """
        try:
            user_answer = entry_math.get().strip() # gets the user input
            if user_answer == str(math_label.answer): # checks if the user input is correct
                messagebox.showinfo("Feedback", "Correct!") # shows a message box if the user input is correct
            else:
                messagebox.showinfo("Feedback", f"Wrong! The correct answer is {math_label.answer}") # shows a message box if the user input is incorrect
            math_challenge()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid answer.") # shows a message box if the user input is invalid

    def start_math_quiz():
        """
        this function starts the math quiz
        :param: None
        :return: None
        """
        global math_label, entry_math, math_window # need to be global so that they can be used in other functions
        
        math_window = tk.Toplevel(root) # creates a new window
        math_window.title("QUESTION") # sets the title of the window
        math_window.geometry("400x200+100+100") # sets the size of the window
        math_window.configure(bg="white") # sets the background color of the window
        math_window.transient(root)  # makes a 'child' window of the root window, this window depends on the root window
        
        math_label = tk.Label(math_window, text="", bg='white', fg='#000066', wraplength=380) # creates a label for the math problem
        math_label.pack(pady=10) # packs the label into the window

        # create a math entry
        entry_math = tk.Entry(math_window) # creates an entry for the user to input their answer
        entry_math.pack(pady=5)
        
        # create a submit button
        submit_button = tk.Button(math_window, text="Submit", command=check_math_answer, bg="white", highlightbackground="white", fg='#000066')
        submit_button.pack(pady=10)
        
        # create a back button
        back_button = tk.Button(math_window, text="Back", command=math_window.destroy, bg="white", highlightbackground="white", fg='#000066')
        back_button.pack(pady=10)
        
        # calls the function generate a math problem based off user input
        math_challenge()

    def open_tutorial():
        """
        this function opens a tutorial window
        :param: None
        :return: None
        """
        tutorial_window = tk.Toplevel(root) # creates a new window
        tutorial_window.title("TUTORIAL") # sets the title of the window
        tutorial_window.geometry("400x275") # sets the size of the window
        tutorial_window.configure(bg="white") # sets the background color of the window
        tutorial_window.transient(root)  # makes a 'child' window of the root window, this window depends on the root window
        
        tutorial_text = (
            "This is the Math Challenge!\n\n"
            "- Math Challenge: Solve math problems or differentiate/integrate.\n\n"
            "Choose your preferred type of math problem and click Begin to start."
        )
        # create a tutorial label
        tutorial_label = tk.Label(tutorial_window, text=tutorial_text, wraplength=380, bg='white', fg='#000066', justify=tk.LEFT)
        tutorial_label.pack(pady=10)
        # create a back button
        tk.Button(tutorial_window, text="Back", command=tutorial_window.destroy, highlightbackground="white").pack(pady=10)

    # create a description label
    description_label = tk.Label(root, text="Choose an activity: Basic Math or Calculus.", wraplength=380, bg='white', fg='#000066')
    description_label.pack(pady=10)

    math_type_var = tk.StringVar(root, value="math")  # set root as master
    # create a math type label
    math_type_label = tk.Label(root, text="Select Math Type:", bg='white', fg='#000066')
    math_type_label.pack(pady=5)
    # create a math radio button
    math_radio = tk.Radiobutton(root, text="Solve Math Problems", variable=math_type_var, value="simple", bg='white', fg='#000066')
    math_radio.pack()
    # create a differential/integrate radio button
    difint_radio = tk.Radiobutton(root, text="Differentiate/Integrate", variable=math_type_var, value="difint", bg='white', fg='#000066')
    difint_radio.pack()

    # create a main buttons frame
    main_buttons_frame = tk.Frame(root, bg='white')
    main_buttons_frame.pack()
    # create a tutorial button
    tutorial_button = tk.Button(main_buttons_frame, text="Tutorial", command=open_tutorial, highlightbackground='white', fg='#000066')
    tutorial_button.pack(side=tk.LEFT, padx=10)
    # create a start quiz button
    math_quiz_button = tk.Button(main_buttons_frame, text="Begin", command=start_math_quiz, highlightbackground='white', fg='#000066')
    math_quiz_button.pack(side=tk.LEFT, padx=10)
    # create a back button
    back_button = tk.Button(root, text="Back", command=root.destroy, highlightbackground="white", fg='#000066', highlightthickness='2')
    back_button.pack(pady=10)

    if parent_root is None:
        root.mainloop() # starts the main loop of the program if called from this file, if called from main.py, the main loop will not need to be started

if __name__ == "__main__":
    # this will only run if flashcards.py is executed directly
    mexecute()