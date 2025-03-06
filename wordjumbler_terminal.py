import random
def load():
    wordjumble = {}  # Dictionary to store question-answer pairs
    while True:
        filename = input("Which file would you like to load? ")
        filepath = "Flashcard Files/" + filename
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                for line in file:
                    question, answer = line.strip().split("|", 1)
                    wordjumble[question.strip()] = answer.strip()
            break
        except FileNotFoundError:
            print("""Flashcard file not found! Make sure you write the name exactly, e.g "macro.txt". Otherwise, make sure it is in the Flashcard Files folder.""")
    return wordjumble
def jumble(wordjumble):
    structure = input("Would you like 1. Shuffle the concept/question 2. Shuffle the definition/answer? ")
    order = input("Would you like to go in order or random? (Type 'order' or 'random') ")
    keys  = list(wordjumble.keys())
    if order.lower() == "random":
        random.shuffle(keys)
    hardmode =  input("Would you like to enable hardmode? All letters will be lowercase. Press h for hardmode: ")
    if structure == "1":
        for question in keys:
            answer = question
            answerwords = answer.split(" ")
            mixedlist = []
            mixedsentence = []
            for word in answerwords:
                for letter in word:
                    mixedlist.append(letter)
                random.shuffle(mixedlist)
                mixedword = "".join(mixedlist) 
                mixedsentence.append(mixedword)
                mixedlist.clear()  
                finalsentence = " ".join(mixedsentence)
            if hardmode.lower() == "h":
                finalsentence = finalsentence.lower()
            print(f"What is: {finalsentence}")
            user_answer = input("Unshuffled: ").strip()  # Get user input for answer
            
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
            answer = wordjumble[question]
            mixedlist = []
            for letter in answer:
                mixedlist.append(letter)
            random.shuffle(mixedlist)
            mixedword = "".join(mixedlist)
            if hardmode.lower() == "h":
                mixedword = mixedword.lower()
            print(f"What is: {mixedword}")
            user_answer = input("Unshuffled: ").strip()
            
            # Show user's answer and correct answer side by side
            print(f"Correct answer: {wordjumble[question]}\n")
            
            # Optionally, compare the answers and give feedback
            if user_answer.lower() == "":
                print("")
            elif user_answer.lower() == wordjumble[question].lower():
                print("Correct!\n")
            else:
                print("Not Exactly.\n")
def tutorial():
    print("This is the word jumble quiz. You will be shown a question or definition with letters out of order, and you will have to unshuffle the letters to remember the concept.")
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

def jexecute():
    opening = input("""Welcome to the Jumble quiz! If this is your first time, please type "new" to view the tutorial. Otherwise, hit enter: """)
    if opening == "new":
        tutorial()
    else:
        pass
    
    flashcards = load() 
    jumble(flashcards)
