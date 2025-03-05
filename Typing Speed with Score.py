import time
import random
import os

def get_random_sentence():
    sentences = [
        "It is what it is my homie, see you around!",
        "What is the definition of Bomboclaat? Mi Bomboclaat",
        "How fast can you really type with your eyes closed?",
        "Practice makes perfect when learning to type quickly.",
        "Hi, welcome to mcdonalds, would you like any fries with that?"
    ]
    return random.choice(sentences)


def load_high_score():
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as file:
            try:
                return float(file.read().strip())
            except ValueError:
                return 0.0
    return 0.0


def save_high_score(score):
    with open("high_score.txt", "w") as file:
        file.write(str(score))


def typing_speed_game(player_name):
    print(f"\n{player_name}, welcome to the Typing Speed Game!")
    print("Type the sentence as fast and accurately as possible.")

    sentence = get_random_sentence()
    print("\nYour sentence:")
    print(sentence)

    input("Press Enter when you are ready to start...")
    start_time = time.time()
    user_input = input("Start typing: ")
    end_time = time.time()

    elapsed_time = end_time - start_time

    # Calculate accuracy
    correct_chars = sum(1 for a, b in zip(sentence, user_input) if a == b)
    accuracy = (correct_chars / len(sentence)) * 100

    # Calculate typing speed (words per minute)
    words = len(sentence.split())
    words_per_minute = (words / elapsed_time) * 60

    print("\nResults:")
    print(f"Time taken: {elapsed_time:.2f} seconds")
    print(f"Typing speed: {words_per_minute:.2f} words per minute")
    print(f"Accuracy: {accuracy:.2f}%")

    return words_per_minute


def main():
    high_score = load_high_score()
    print("\nCurrent High Score (WPM):", high_score)

    # Two players
    player1 = input("Enter Player 1 name: ")
    player2 = input("Enter Player 2 name: ")

    score1 = typing_speed_game(player1)
    score2 = typing_speed_game(player2)

    # Determine the winner
    if score1 > score2:
        print(f"\n{player1} wins with {score1:.2f} WPM!")
    elif score2 > score1:
        print(f"\n{player2} wins with {score2:.2f} WPM!")
    else:
        print("\nIt's a tie!")

    # Check if a new high score was achieved
    new_high_score = max(high_score, score1, score2)
    if new_high_score > high_score:
        save_high_score(new_high_score)
        print(f"New High Score: {new_high_score:.2f} WPM!")
    else:
        print(f"The High Score remains: {high_score:.2f} WPM.")


if __name__ == "__main__":
    main()
