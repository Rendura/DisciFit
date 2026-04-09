import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title('Group 3 Final Project')
root.configure(bg="#D0E8F2")
root.geometry("400x600")

# --- Common font ---
label_font = ("Arial", 16, "bold")
entry_font = ("Arial", 14)
input_width = 25  # consistent width for entries and comboboxes

# --- Main Title ---
tk.Label(root, text="DisciFit", font=("Arial", 28, "bold"), bg="#D0E8F2").pack(pady=20)

# --- Goal Combobox ---
tk.Label(root, text="Target Goal:", font=label_font, bg="#D0E8F2").pack(pady=(10,5))
goal_options = ["Gain", "Loss"]
goal_combobox = ttk.Combobox(root, values=goal_options, font=entry_font, state="readonly", justify="center", width=input_width)
goal_combobox.current(0)
goal_combobox.pack(pady=(0,10))

# --- Target Weight Entry ---
tk.Label(root, text="Set Your Target Weight (kg):", font=label_font, bg="#D0E8F2").pack(pady=(10,5))
entry1 = tk.Entry(root, font=entry_font, justify="center", width=input_width)
entry1.pack(pady=(0,10))

# --- Timeframe Entry ---
tk.Label(root, text="Enter Your Target Timeframe (Weeks):", font=label_font, bg="#D0E8F2").pack(pady=(10,5))
entry2 = tk.Entry(root, font=entry_font, justify="center", width=input_width)
entry2.pack(pady=(0,10))

# --- Height Entry ---
tk.Label(root, text="Enter your height in cm:", font=label_font, bg="#D0E8F2").pack(pady=(10,5))
entry3 = tk.Entry(root, font=entry_font, justify="center", width=input_width)
entry3.pack(pady=(0,10))

# --- Current Weight Entry ---
tk.Label(root, text="Enter your current weight in kg:", font=label_font, bg="#D0E8F2").pack(pady=(10,5))
entry4 = tk.Entry(root, font=entry_font, justify="center", width=input_width)
entry4.pack(pady=(0,10))

# --- Gender Combobox ---
tk.Label(root, text="Gender:", font=label_font, bg="#D0E8F2").pack(pady=(10,5))
gender_options = ["Male", "Female"]
gender_combobox = ttk.Combobox(root, values=gender_options, font=entry_font, state="readonly", justify="center", width=input_width)
gender_combobox.current(0)
gender_combobox.pack(pady=(0,10))

# --- Exercise Mode Combobox ---
tk.Label(root, text="Select Exercise Mode:", font=label_font, bg="#D0E8F2").pack(pady=(10,5))
exercise_modes = ["Beginner", "Intermediate", "Advanced"]
exercise_mode = ttk.Combobox(root, values=exercise_modes, font=entry_font, state="readonly", justify="center", width=input_width)
exercise_mode.current(0)
exercise_mode.pack(pady=(0,20))

root.mainloop()