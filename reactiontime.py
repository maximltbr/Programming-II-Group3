import tkinter as tk  # tkinter for GUI
import random  # generating random delays and colors for the game
import time  # measuring reaction time for each click and calculate average later

def rexecute(parent_root=None):
    """
    this function has all the steps/instructions for the reaction time game
    :param parent_root: use the root window creates in main.py file if called from main.py file, 
                        if not it will create a new root indow, this is so that the window can be 
                        reused if called from main.py file to avoid problems
    :return: None
    """
    if parent_root is None:
        root = tk.Tk() # creates a new root window if called from this file, meaning that no root window currently exists
    else:
        root = tk.Toplevel(parent_root) # if called from main.py file, use the root window created in main.py file
        
    root.title("BRAINTRAIN REACTION TIME") # set the title of the window
    root.geometry("450x575") # set the size of the window
    root.configure(bg="white") # set the background color of the window

    # dict that has all the variables for the game
    game_state = {
        'current_color': None,  # stores the current color key
        'start_time': None,  # stores the time when the color appears
        'reaction_times': [],  # list for reaction times
        'current_round': 0,  # tracks current round
        'rounds': 10  # default number of rounds
    }

    def tutorial():
        """
        opens a window which is the tutorial 
        :param: None
        :return: None
        """
        tutorial_window = tk.Toplevel(root) # create a new window
        tutorial_window.title("TUTORIAL") # set the title of the window
        tutorial_window.geometry("500x575") # set the size of the window
        tutorial_window.configure(bg="white") # set the background color of the window
        tutorial_window.transient(root)  # makes a 'child' window of the root window, this window depends on the root window
        
        # Add tutorial text
        tutorial_text = """
        Welcome to the Reaction Time Game!
        
        Game Objective:
        Test your reaction speed by responding to colored squares as quickly as possible.
        
        How to Play:
        1. Click the "Begin" button to start.
        2. A colored square will appear on the screen after a random delay.
        3. Press the key that corresponds to the color shown:
        • Press 'r' for RED
        • Press 'g' for GREEN
        • Press 'b' for BLUE
        • Press 'y' for YELLOW
        • Press 'o' for ORANGE
        4. Your reaction time will be measured for each correct key press.
        5. After all rounds are complete, you'll see your average reaction time.
        
        Tips:
        • Focus on the screen and keep your fingers ready on the keyboard.
        • The delay between rounds is random, so stay alert!
        • Try to improve your average time with each game.
        
        Have fun and test your reflexes!
        """
        
        # adds the tutorial text 
        tutorial_label = tk.Label(tutorial_window, text=tutorial_text, justify=tk.LEFT, wraplength=460, bg='white', fg='#000066')
        tutorial_label.pack(pady=10)
        
        # adds a back button
        back_button = tk.Button(tutorial_window, text="Back", command=tutorial_window.destroy, highlightbackground="white", fg='#000066', highlightthickness='2')
        back_button.pack(pady=10)


    def start_game():
        """

        :param: None
        :return: None
        """
        try:
            game_state['rounds'] = int(rounds_spinbox.get()) # get round number
        except ValueError:
            game_state['rounds'] = 10  # default to 10 if invalid input
        
        game_state['current_round'] = 0 # reset the round count when the game starts
        game_state['reaction_times'] = [] # reset the reaction times when the game starts
        canvas.delete("all")  # clear any previous game text
        canvas.configure(bg='white')  # reset background color
        
        # display "Get Ready" message
        canvas.create_text(200, 150, text="Get Ready...", fill="#000066")
        root.update()  # force update to show message
        
        # re-enable the start button for future games
        start_button.config(state="normal")
        
        # wait 1.5 seconds before starting
        root.after(1500, next_flash)


    def next_flash():
        """
        schedules the next color pop up with a delay between 0.5 - 2 seconds
        also ends the game if all rounds are completed
        :param: None
        :return: None
        """
        game_state['current_round'] += 1  # adds to the round counter 
        if game_state['current_round'] > game_state['rounds']:  # if the round counter is greater than the total rounds, end the game
            end_game()
            return
        
        # show current round number
        canvas.delete("all")
        canvas.create_text(200, 30, text=f"Round {game_state['current_round']} of {game_state['rounds']}", fill="#000066")
        
        
        delay = random.uniform(0.5, 2)  # random delay between 0.5 - 2 seconds
        root.after(int(delay * 1000), flash)  # Wait for the delay, then call flash()


    def flash():
        """
        change the color of the canvas to a random color and get the start time
        :param: None
        :return: None
        """
        game_state['current_color'] = random.choice(list(colors.keys()))  #random color key (red, green, ...)
        canvas.configure(bg=colors[game_state['current_color']])  # change canvas background to the chosen color
        game_state['start_time'] = time.time()  # record the start time for reaction


    def check_reaction(key_pressed):
        """
        checks if the user keypress is correct
        if correct, time will be recorded and we will go to the next round

        :param: event (tkinter.Event): key that is pressed by the user to check if they got the right color
        :return: None
        """
        if game_state['current_color'] is None:  # Ignore keypresses before any color is shown
            return
            
        if key_pressed.char.lower() == game_state['current_color']:  # check if the pressed key matches the current color
            reaction_time = time.time() - game_state['start_time']  # calc reaction time
            game_state['reaction_times'].append(reaction_time)  # add reaction time to the list
            canvas.configure(bg='white')  # reset background color
            game_state['current_color'] = None  # reset to prevent multiple keypresses
            
            # Show feedback
            canvas.delete("all")
            feedback_text = f"Good! {reaction_time:.3f}s" #3f means 3 decimal places and the type is float
            canvas.create_text(200, 150, text=feedback_text, fill="#000066")
            root.update()  # force update to show message
            
            # add delays between next round
            root.after(500, next_flash)  # after delay, call next_flash() to start the next round
        else:
            # show wrong key feedback
            canvas.delete("all")
            canvas.create_text(200, 150, text="Wrong key!", fill="#FF0000")
            canvas.configure(bg='white')  # reset background color
            game_state['current_color'] = None  # reset to prevent multiple keypresses
            root.update()  # force update to show message
            
            # add delay before next round
            root.after(1000, next_flash) # after delay, call next_flash() to start the next round


    def end_game():
        """
        function is called when all rounds are completed, it shows the avg reaction time
        :param: None
        :return: None
        """
        if not game_state['reaction_times']:  # check if any reactions were recorded
            avg_time = 0
        else:
            avg_time = sum(game_state['reaction_times']) / len(game_state['reaction_times'])  # calculate average reaction time
        
        canvas.delete("all")  # clear canvas
        canvas.configure(bg='white')  # reset background color
        
        result_text = f"Game Over!\nAvg Reaction Time: {avg_time:.3f} sec" #3f means 3 decimal places and the type is float
        canvas.create_text(200, 130, text=result_text, fill="#000066", justify=tk.CENTER)
        
        # display round information
        rounds_text = f"Completed {len(game_state['reaction_times'])} of {game_state['rounds']} rounds"
        canvas.create_text(200, 160, text=rounds_text, fill="#000066")
        
        # display fastest and slowest times if available
        if game_state['reaction_times']: # if list is not empty
            fastest = min(game_state['reaction_times'])
            slowest = max(game_state['reaction_times'])
            stats_text = f"Fastest: {fastest:.3f} sec\nSlowest: {slowest:.3f} sec"
            canvas.create_text(200, 250, text=stats_text, fill="#000066")
        
        game_state['current_color'] = None  # ensure no more color checks

    # colors and their corresponding key bind
    colors = {'r': 'red', 'g': 'green', 'b': 'blue', 'y': 'yellow', 'o': 'orange'}

    # add title and brief description
    title_label = tk.Label(root, text="Welcome to the reaction time game! If this is your first time, please press 'Tutorial' to view the tutorial. Otherwise, press 'Begin':",wraplength=380, bg='white', fg='#000066')
    title_label.pack(pady=10)

    def validate_spinbox(value):
        """
        retrieves the input of the spinbox (number box), number of rounds
        :param: value (str): value of the spinbox
        :return: bool: true if the value is valid, false otherwise
        """
        if value == "":
            return True
        try:
            num = int(value)
            return 0 <= num <= 50
        except ValueError:
            return False

    # creates a frame for the number of rounds input box
    rounds_frame = tk.Frame(root, bg="white")
    rounds_frame.pack(pady=10)

    rounds_label = tk.Label(rounds_frame, text="Number of Rounds:", bg='white', fg='#000066')
    rounds_label.pack(side=tk.LEFT, padx=5)

    rounds_spinbox = tk.Spinbox(rounds_frame, from_=0, to=50, width=5,validate='key' ,validatecommand=(root.register(validate_spinbox), '%P'), takefocus=True) # validate='key' means that the validate command will be called whenever the user changes the value. the %P is a special Tkinter substitution parameter that represents the new value of the Spinbox as a string after the change is made. the validatecommand passes this new value to the 'validate_spinbox' function to check whether the value is valid
    rounds_spinbox.insert(0, "10") # defualt value is 10
    rounds_spinbox.pack(side=tk.LEFT, padx=5)

    # add focus out event to validate final value
    def on_focus_out():
        """
        confirms the value of the spinbox when the user presses out
        :param: None
        :return: None
        """
        try:
            value = int(rounds_spinbox.get()) # tries to turn the value into an integer
            if value < 0:
                rounds_spinbox.insert(0, "0") # if the value is less than 0, it will be set to 0
            elif value > 50:     
                rounds_spinbox.insert(0, "50") # if the value is greater than 50, it will be set to 50
        except ValueError:
            rounds_spinbox.insert(0, "10") # if the value is invalud, it will be set to 10

    rounds_spinbox.bind('<FocusOut>', on_focus_out) # when the user presses out of the spinbox, the on_focus_out function will be called, confirming the value

    # create canvas for color display
    canvas = tk.Canvas(root, width=400, height=200, bg='white', highlightthickness=1, highlightbackground='black')
    canvas.pack(pady=10)

    # display color key frame
    key_frame = tk.Frame(root, bg="white")
    key_frame.pack(pady=10)

    key_label = tk.Label(key_frame, text="Color Keys:", bg='white', fg='#000066')
    key_label.grid(row=0, column=0, columnspan=5, pady=5)

    # display color reference
    col = 0
    for key, color in colors.items(): # adds the color and key to the frame
        color_frame = tk.Frame(key_frame, width=30, height=30, bg="white")
        color_frame.grid(row=1, column=col, padx=5)
        color_square = tk.Canvas(color_frame, width=30, height=30, bg=color, highlightthickness=0)
        color_square.pack()
        
        key_text = tk.Label(key_frame, text=f"'{key}'", bg='white', fg='#000066')
        key_text.grid(row=2, column=col, padx=5)
        col += 1

    # create button frame for Tutorial and Begin buttons
    button_frame = tk.Frame(root, bg="white")
    button_frame.pack(pady=10)

    tutorial_button = tk.Button(button_frame, text="Tutorial", command=tutorial, highlightbackground='white', fg='#000066')
    tutorial_button.pack(side=tk.LEFT, padx=10)

    start_button = tk.Button(button_frame, text="Begin", command=start_game, highlightbackground='white', fg='#000066')
    start_button.pack(side=tk.LEFT, padx=10)

    # back Button
    back_button = tk.Button(root, text="Back", command=root.destroy, highlightbackground="white", fg='#000066', highlightthickness='2')
    back_button.pack(pady=10)

    root.bind("<KeyPress>", check_reaction) # checks user input when a key is pressed and calls the check_reaction function

    if parent_root is None:
        root.mainloop() # starts the main loop of the program if called from this file, if called from main.py, the main loop will not need to be started


if __name__ == "__main__":
    # this will only run if flashcards.py is executed directly
    rexecute()