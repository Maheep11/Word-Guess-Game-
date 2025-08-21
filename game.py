import time
import random
import re
import os

# Constants
WORD_LIST = ["judge", "piano", "robot", "apple", "grape"]  # List of potential random words
WINNERS_FILE = "winners.txt"
MAX_TURNS = 6
TIME_LIMIT = 30

# Helper functions
def load_winners():
    if not os.path.exists(WINNERS_FILE):
        return []
    with open(WINNERS_FILE, "r") as file:
        return file.readlines()

def save_winner(name, time_taken):
    with open(WINNERS_FILE, "a") as file:
        file.write(f"{name} - {time_taken} seconds\n")

def display_winners():
    winners = load_winners()
    if winners:
        print("\nPast Winners:")
        print("".join(winners))
    else:
        print("\nNo winners yet!")

def get_user_input(prompt, timeout):
    start_time = time.time()
    while True:
        user_input = input(prompt)
        if time.time() - start_time > timeout:
            print("Time's up! You missed your turn.")
            return None
        return user_input

def validate_guess(guess):
    return re.match(r"^[a-zA-Z]{5}$", guess) is not None

def provide_clues(answer, guess):
    clues = []
    unused_letters = []
    for i, char in enumerate(guess):
        if char == answer[i]:
            clues.append("*")
        elif char in answer:
            clues.append("+")
        else:
            clues.append("_")
            unused_letters.append(char)
    return clues, unused_letters

# Game Logic
def play_game():
    random_word = random.choice(WORD_LIST)
    name = input("Enter your name or alias: ")
    display_winners()
    print("\nTry to guess the 5-letter word.")
    print("You have 6 turns and 30 seconds per turn.")

    start_time = time.time()
    used_letters = set()

    for turn in range(1, MAX_TURNS + 1):
        print(f"\nTurn {turn}/{MAX_TURNS}")
        guess = get_user_input("Enter your guess: ", TIME_LIMIT)
        if not guess:
            continue
        if guess.lower() == "give up":
            print(f"You gave up! The word was: {random_word}")
            return
        if not validate_guess(guess):
            print("Invalid input. Please enter a 5-letter word.")
            continue

        clues, unused = provide_clues(random_word, guess)
        used_letters.update(unused)

        print("Clues: ", "".join(clues))
        print("Used letters not in the word: ", ", ".join(sorted(used_letters)))

        if guess == random_word:
            time_taken = round(time.time() - start_time, 2)
            print(f"Congratulations, {name}! You guessed the word in {time_taken} seconds.")
            save_winner(name, time_taken)
            return

    print(f"Out of turns! The correct word was: {random_word}")

# Main execution
if __name__ == "__main__":
    while True:
        play_game()
        again = input("\nDo you want to play again? (yes/no): ").lower()
        if again != "yes":
            break
