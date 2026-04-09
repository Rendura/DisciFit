import tkinter as tk

root = tk.Tk()
root.title('Group 3 Final Project')
root.geometry("400x600")

# Main Title
label = tk.Label(root, text="DisciFit", font=("JetBrains Mono", 30, "bold"))
label.pack(pady=20)  # Add vertical spacing

# Variable to store the choice
goal_var = tk.StringVar(value="Gain")  # default value

# Radiobuttons for Goal
tk.Label(root, text="Target Goal:", font=("JetBrains Mono", 14)).pack(pady=(10,0))
tk.Radiobutton(root, text="Gain", variable=goal_var, value="Gain", font=("JetBrains Mono", 12)).pack()
tk.Radiobutton(root, text="Loss", variable=goal_var, value="Loss", font=("JetBrains Mono", 12)).pack()

# Target Weight Label + Entry
tk.Label(root, text="Set Your Target Weight (KG):", font=("JetBrains Mono", 14)).pack(pady=(10,0))
entry1 = tk.Entry(root, font=("JetBrains Mono", 12), justify="center")
entry1.pack(pady=(0,10))

# Timeframe Label + Entry
tk.Label(root, text="Enter Your Target Timeframe (Weeks):", font=("JetBrains Mono", 14)).pack(pady=(10,0))
entry2 = tk.Entry(root, font=("JetBrains Mono", 12), justify="center")
entry2.pack(pady=(0,10))

# Height Label + Entry
tk.Label(root, text="Enter your height in cm:", font=("JetBrains Mono", 14)).pack(pady=(10,0))
entry3 = tk.Entry(root, font=("JetBrains Mono", 12), justify="center")
entry3.pack(pady=(0,10))

# Current Weight Label + Entry
tk.Label(root, text="Enter your current weight in kg:", font=("JetBrains Mono", 14)).pack(pady=(10,0))
entry4 = tk.Entry(root, font=("JetBrains Mono", 12), justify="center")
entry4.pack(pady=(0,10))

# Variable to store the choice
gender_var = tk.StringVar(value="Male")  # default value

# Radiobuttons for gender
gender_var = tk.StringVar(value="Male")

tk.Label(root, text="Gender:", font=("JetBrains Mono", 14)).pack(pady=(10,5))

# Frame to hold buttons
frame = tk.Frame(root)
frame.pack()

tk.Radiobutton(frame, text="Male", variable=gender_var, value="Male", font=("JetBrains Mono", 12)).pack(side="left", padx=10)
tk.Radiobutton(frame, text="Female", variable=gender_var, value="Female", font=("JetBrains Mono", 12)).pack(side="left", padx=10)

root.mainloop()