import tkinter as tk
from tkinter import ttk, messagebox
from logic import UserData, AppLogic   # IMPORTANT: your logic file must be named logic.py


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('DisciFit - Fitness Planner')
        self.root.configure(bg="#D0E8F2")
        self.root.geometry("450x750")

        self.app_logic = AppLogic(root)

        # --- Fonts ---
        self.label_font = ("Arial", 14, "bold")
        self.entry_font = ("Arial", 12)
        self.width = 25

        self.build_ui()

    def build_ui(self):
        tk.Label(
            self.root,
            text="DisciFit",
            font=("Arial", 28, "bold"),
            bg="#D0E8F2"
        ).pack(pady=15)

        # Goal
        self.create_label("Target Goal:")
        self.goal = ttk.Combobox(self.root, values=["Gain", "Loss"], state="readonly", width=self.width)
        self.goal.current(0)
        self.goal.pack(pady=5)

        # Target weight
        self.create_label("Target Weight (kg):")
        self.target_weight = tk.Entry(self.root, font=self.entry_font)
        self.target_weight.pack(pady=5)

        # Weeks
        self.create_label("Target Timeframe (weeks):")
        self.weeks = tk.Entry(self.root, font=self.entry_font)
        self.weeks.pack(pady=5)

        # Age
        self.create_label("Age:")
        self.age = tk.Entry(self.root, font=self.entry_font)
        self.age.pack(pady=5)

        # Height
        self.create_label("Height (cm):")
        self.height = tk.Entry(self.root, font=self.entry_font)
        self.height.pack(pady=5)

        # Weight
        self.create_label("Current Weight (kg):")
        self.weight = tk.Entry(self.root, font=self.entry_font)
        self.weight.pack(pady=5)

        # Gender
        self.create_label("Gender:")
        self.gender = ttk.Combobox(self.root, values=["Male", "Female"], state="readonly", width=self.width)
        self.gender.current(0)
        self.gender.pack(pady=5)

        # Exercise mode
        self.create_label("Exercise Level:")
        self.exercise = ttk.Combobox(
            self.root,
            values=["Beginner", "Intermediate", "Advanced"],
            state="readonly",
            width=self.width
        )
        self.exercise.current(0)
        self.exercise.pack(pady=5)

        # Category (IMPORTANT FIX)
        self.create_label("Workout Category:")
        self.category = ttk.Combobox(
            self.root,
            values=["Aerobic", "Strength", "Balance", "Flexibility"],
            state="readonly",
            width=self.width
        )
        self.category.current(0)
        self.category.pack(pady=5)

        # Button
        tk.Button(
            self.root,
            text="Generate Plan",
            font=("Arial", 14, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.submit_data
        ).pack(pady=20)

    def create_label(self, text):
        tk.Label(self.root, text=text, font=self.label_font, bg="#D0E8F2").pack(pady=3)

    def submit_data(self):
        try:
            # Validate inputs
            user = UserData(
                goal=self.goal.get(),
                target_weight=float(self.target_weight.get()),
                weeks=int(self.weeks.get()),
                age=int(self.age.get()),
                height=float(self.height.get()),
                weight=float(self.weight.get()),
                gender=self.gender.get(),
                exercise=self.exercise.get(),
                category=self.category.get()
            )

            # Send to logic layer
            self.app_logic.show_results(user)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers in all fields!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()