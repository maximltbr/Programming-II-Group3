import random
import time
import os

def display_list(items):
    """
    Prints a list of items to the user.
    :param items: A list of items for the user to remember
    :return: None
    """
    print("Remember these items:")
    for item in items:
        print(f"- {item}")
    print("\n")

def create_custom_list(min_items):
    """
    Allows the user to create a custom list with a minimum number of items depending on the chosen difficulty.
    :param min_items: the minimum numbers of the custom list, depending on the difficulty level
    :return: A customized list of items
    """
    custom_list = []
    print(f"Create your custom list! You need at least {min_items} items. Enter items one by one. Type 'done' when finished.")
    while True:
        item = input("Add an item: ").strip()
        if item.lower() == "done":
            if len(custom_list) >= min_items:
                break
            else:
                print(f"You need at least {min_items} items. Add more!")
        else:
            custom_list.append(item)
    return custom_list

def remove_item(items):
    """
    Removes a random item from the list and return it.
    :param items: A list of items from which one of the items is going to be removed
    :return: The item that is going to be removed
    """

    removed_item = random.choice(items)
    items.remove(removed_item)
    return removed_item

def clear_screen():
    """
    Clears the screen.
    :return: None
    """
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # MacOS and Linux
        os.system('clear')

def ask_missing_item(items, removed_item):
    """
    Asks the user to introduce the missing item.
    :param items: A list of items with a missing item
    :param removed_item: The item that was removed from the list
    :return: True if the player correctly identifies the missing item, False otherwise.
    """
    print("Now, which item is missing?")
    for item in items:
        print(f"- {item}")

    user_guess = input("Your answer: ").strip()

    if user_guess.lower() == removed_item.lower():
        print("Correct! You have a great memory!")
        return True
    else:
        print(f"Oops! The missing item was '{removed_item}'. Better luck next time!")
        return False

def remember_order_game():
    """
    Main function to run the 'Remember the Order' game.

    The game consists of:
    - Selecting the difficulty level
    - Choose one of the default categories or create a new list of items
    - Memorize a randomly selected list from the chosen category/custom list
    - Identify the missing item

    :return: None
    """

    print("Welcome to the Remember the Order Game!\n")

    # These are the default categories:
    categories = {
        "colors": ["Red", "Blue", "Green", "Yellow", "Purple", "Orange", "Pink", "Brown", "White"],
        "animals": ["Dog", "Cat", "Elephant", "Lion", "Giraffe", "Tiger", "Monkey", "Zebra", "Snake"],
        "numbers": ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    }

    # These are the difficulty levels, consisting of different numbers of items.
    difficulty_levels = {
        "easy": {"num_items": 5},
        "medium": {"num_items": 7},
        "hard": {"num_items": 9}
    }

    score = 0

    while True:
        # First user chooses a difficulty level
        print("Choose a difficulty level:")
        for level in difficulty_levels:
            print(f"- {level}")
        chosen_level = input("Your choice: ").strip().lower()

        if chosen_level not in difficulty_levels:
            print("Invalid difficulty level. Please try again.")
            continue

        num_items = difficulty_levels[chosen_level]["num_items"]


        # Then, the user chooses a category or creates a custom list
        print("Choose a category or create a custom list:")
        print("- colors")
        print("- animals")
        print("- numbers")
        print("- custom")
        chosen_category = input("Your choice: ").strip().lower()

        if chosen_category == "custom":
            print(f"For the '{chosen_level}' difficulty level, your custom list needs at least {num_items} items.")
            items = create_custom_list(num_items)
        elif chosen_category in categories:
            items = random.sample(categories[chosen_category], num_items)
        else:
            print("Invalid choice. Please try again.")
            continue

        # When the user has made their choice of level and category, it displays the full list for memorization
        display_list(items)
        print("You have 5 seconds to memorize the list...")
        time.sleep(5)  # Gives the user 5 seconds to memorize the list

        # Clearing the screen once the time is up
        clear_screen()
        print("Time's up! Now, let's see if you can remember the list.\n")

        # Then, a random item from the list is removed:
        removed_item = remove_item(items)

        # And the user is asked to identify the missing item
        correct = ask_missing_item(items, removed_item)

        if correct:
            score += 1
            print(f"Your current score: {score}")

        # Ask if the user wants to play again
        play_again = input("Do you want to play again? (yes/no): ").strip().lower()
        if play_again != "yes":
            print(f"Thanks for playing! Your final score is {score}. Goodbye!")
            break

if __name__ == "__main__":
    remember_order_game()
