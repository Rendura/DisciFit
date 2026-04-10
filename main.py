import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title('Group 3 Final Project')
root.configure(bg="#D0E8F2")
root.geometry("450x650")

# --- Common font ---
label_font = ("Arial", 16, "bold")
entry_font = ("Arial", 14)
input_width = 25

# --- Main Title ---
tk.Label(root, text="DisciFit", font=("Arial", 28, "bold"), bg="#D0E8F2").pack(pady=20)

# --- Goal Combobox ---
tk.Label(root, text="Target Goal:", font=label_font, bg="#D0E8F2").pack(pady=5)
goal_options = ["Gain", "Loss"]
goal_combobox = ttk.Combobox(root, values=goal_options, font=entry_font, state="readonly", justify="center", width=input_width)
goal_combobox.current(0)
goal_combobox.pack(pady=5)

# --- Target Weight ---
tk.Label(root, text="Set Your Target Weight (kg):", font=label_font, bg="#D0E8F2").pack(pady=5)
entry1 = tk.Entry(root, font=entry_font, justify="center", width=input_width)
entry1.pack(pady=5)

# --- Timeframe ---
tk.Label(root, text="Enter Your Target Timeframe (Weeks):", font=label_font, bg="#D0E8F2").pack(pady=5)
entry2 = tk.Entry(root, font=entry_font, justify="center", width=input_width)
entry2.pack(pady=5)

# --- Age ---
tk.Label(root, text="Enter your age:", font=label_font, bg="#D0E8F2").pack(pady=5)
entry3 = tk.Entry(root, font=entry_font, justify="center", width=input_width)
entry3.pack(pady=5)

# --- Height ---
tk.Label(root, text="Enter your height in cm:", font=label_font, bg="#D0E8F2").pack(pady=5)
entry4 = tk.Entry(root, font=entry_font, justify="center", width=input_width)
entry4.pack(pady=5)

# --- Current Weight ---
tk.Label(root, text="Enter your current weight in kg:", font=label_font, bg="#D0E8F2").pack(pady=5)
entry5 = tk.Entry(root, font=entry_font, justify="center", width=input_width)
entry5.pack(pady=5)

# --- Gender ---
tk.Label(root, text="Gender:", font=label_font, bg="#D0E8F2").pack(pady=5)
gender_options = ["Male", "Female"]
gender_combobox = ttk.Combobox(root, values=gender_options, font=entry_font, state="readonly", justify="center", width=input_width)
gender_combobox.current(0)
gender_combobox.pack(pady=5)

# --- Exercise Mode ---
tk.Label(root, text="Select Exercise Mode:", font=label_font, bg="#D0E8F2").pack(pady=5)
exercise_modes = ["Beginner", "Intermediate", "Advanced"]
exercise_mode = ttk.Combobox(root, values=exercise_modes, font=entry_font, state="readonly", justify="center", width=input_width)
exercise_mode.current(0)
exercise_mode.pack(pady=10)

# --- Function ---
def submit_data():
    print("Goal:", goal_combobox.get())
    print("Target Weight:", entry1.get())
    print("Timeframe:", entry2.get())
    print("Age:", entry3.get())
    print("Height:", entry4.get())
    print("Current Weight:", entry5.get())
    print("Gender:", gender_combobox.get())
    print("Exercise Mode:", exercise_mode.get())

# --- Generate Plan Button ---
submit_btn = tk.Button(
    text="Generate Plan",
    font=("Arial", 16, "bold"),
    bg="#4CAF50",
    fg="white",
    width=20,
    command=submit_data
)
submit_btn.pack(pady=20)

root.mainloop()