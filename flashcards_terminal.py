import random
def load():
    """
    load flashcards from a file
    :param: None
    :return: a dictionary of flashcards, "flashcards"
    """
    flashcards = {}  # Dictionary to store question-answer pairs
    while True:
        filename = input("Which file would you like to load? ")
        filepath = "Flashcard Files/" + filename
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                for line in file:
                    question, answer = line.strip().split("|", 1)
                    flashcards[question.strip()] = answer.strip()
            break
        except FileNotFoundError:
            print("""Flashcard file not found! Make sure you write the name exactly, e.g "macro.txt". Otherwise, make sure it is in the Flashcard Files folder.""")
    return flashcards

def quiz(flashcards):
    """
    quiz the user on flashcards
    :param flashcards: a dictionary of flashcards
    :return: None
    """
    structure = input("Would you like 1. Question -> Answer or 2. Answer -> Question? ")
    order = input("Would you like to go in order or random? (Type 'order' or 'random') ")
    keys  = list(flashcards.keys())
    if order.lower() == "random":
        random.shuffle(keys)
    if structure == "1":
        for question in keys:
            answer = flashcards[question]
            print(f"Concept: {question}")
            user_answer = input("Definition: ").strip()  # Get user input for answer
            
            # Show user's answer and correct answer side by side
            print(f"Correct answer: {answer}\n")
            
            # Optionally, compare the answers and give feedback
            if user_answer.lower() == "":
                print("")
            elif user_answer.lower() == answer.lower():

                print("Correct!\n")
            else:
                print("Not Exactly.\n")
    elif structure == "2":
        for question in keys:
            answer = flashcards[question]
            print(f"Definition: {answer}")
            user_answer = input("Concept: ").strip()
            
            # Show user's answer and correct answer side by side
            print(f"Correct answer: {question}\n")
            
            # Optionally, compare the answers and give feedback
            if user_answer.lower() == "":
                print("")
            elif user_answer.lower() == question.lower():
                print("Correct!\n")
            else:
                print("Not Exactly.\n")
                
def tutorial():
    """
    print a tutorial for the user
    :param: None
    :return: None
    """
    print("This is the flashcard quiz. You will be shown a question or definition, and you will have to provide the corresponding definition or question, respectively.")
    print("You can choose to view the question and provide the answer, or view the answer and provide the question.")
    print("To load a file, please place it in this folder and type the filename (e.g., 'flashcards.txt') when prompted.")
    print("There are a few preset files in a subfolder you can use.")
    print("If you'd like to create your own, please follow this format:")
    print("Question 1|Answer 1")
    print("Question 2|Answer 2")
    print("...")
    print("You must separate the question and answer with a vertical bar '|'. Each pair must be on a new line.")
    print("If you'd like to generate your own flashcards using study material, you can use an external AI agent like ChatGPT with the following prompt:")
    print("")
    print("""Please format the following content into a a flashcard file, where each line contains 'Question | Answer', with each pair of question and answer on a new line. If needed, process the content for clarity. After formatting the content, create a downloadable file for me."
[Paste or upload the content here]""")

def flexecute():
    """
    Executes the flashcard quiz
    :param: None
    :return: None
    """
    opening = input("""Welcome to the flashcard quiz! If this is your first time, please type "new" to view the tutorial. Otherwise, hit enter: """)
    if opening == "new":
        tutorial()
    else:
        pass
    
    flashcards = load() 
    quiz(flashcards)
