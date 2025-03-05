import tkinter as tk
import random
import time

def start_game():
    global current_round, reaction_times
    current_round = 0
    reaction_times = []
    next_flash()

def next_flash():
    global current_round
    if current_round >= rounds:
        end_game()
        return
    current_round += 1
    delay = random.uniform(0.5, 2)  # Random delay between 0.5-2 seconds
    root.after(int(delay * 1000), flash)

def flash():
    global current_color, start_time
    current_color = random.choice(list(colors.keys()))
    canvas.configure(bg=colors[current_color])
    start_time = time.time()

def check_reaction(event):
    if event.char == current_color:
        reaction_time = time.time() - start_time
        reaction_times.append(reaction_time)
        canvas.configure(bg='white')
        next_flash()

def end_game():
    avg_time = sum(reaction_times) / len(reaction_times) if reaction_times else 0
    canvas.create_text(200, 200, text=f"Avg Reaction Time: {avg_time:.3f} sec", font=("Arial", 16))
    root.unbind("<KeyPress>")

print("Welcome to the Reaction Time Game!\nA color will appear on the screen, and you must press the corresponding key ('r' for red, 'g' for green, etc.) as quickly as possible.\nLet's see how fast your reactions are!")
rounds = int(input("Enter the number of rounds (Recommended: 10-30): "))

root = tk.Tk()
root.title("Reaction Time Game")
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

colors = {'r': 'red', 'g': 'green', 'b': 'blue', 'y': 'yellow', 'o': 'orange'}
current_color = None
start_time = None
reaction_times = []
current_round = 0

root.bind("<KeyPress>", check_reaction)
start_game()
root.mainloop()
