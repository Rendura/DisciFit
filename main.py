import tkinter as tk
from tkinter import ttk, messagebox
from logic import UserData, AppLogic


class App:
    def __init__(self, root):
        self.root = root
        self.root.title('DisciFit - Fitness Planner')
        self.root.configure(bg="#D0E8F2")
        self.root.geometry("500x800")

        self.app_logic = AppLogic(root)

        # Fonts
        self.label_font = ("Arial", 16, "bold")
        self.entry_font = ("Arial", 16)
        self.width = 30

        self.build_ui()

    # ---------------- UI ----------------
    def build_ui(self):
        container = tk.Frame(self.root, bg="#D0E8F2")
        container.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(container, bg="#D0E8F2", highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = tk.Frame(self.canvas, bg="#D0E8F2")

        self.window_id = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="n"
        )

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.root.bind("<Up>", self._scroll_up)
        self.root.bind("<Down>", self._scroll_down)

        self.build_form(self.scrollable_frame)

    # ---------------- CENTER ----------------
    def on_canvas_configure(self, event):
        canvas_width = event.width
        max_width = 550
        frame_width = min(canvas_width, max_width)

        self.canvas.itemconfig(self.window_id, width=frame_width)
        self.canvas.coords(self.window_id, canvas_width // 2, 0)

    # ---------------- SCROLL ----------------
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _scroll_up(self, event):
        self.canvas.yview_scroll(-3, "units")

    def _scroll_down(self, event):
        self.canvas.yview_scroll(3, "units")

    # ---------------- FORM ----------------
    def build_form(self, parent):
        tk.Label(parent, text="DisciFit", font=("Arial", 30, "bold"), bg="#D0E8F2").pack(pady=20)

        # Goal
        self.create_label(parent, "Target Goal:")
        self.goal = ttk.Combobox(parent, values=["Gain", "Loss"], state="readonly",
                                 width=self.width, font=self.entry_font, justify='center')
        self.goal.current(0)
        self.goal.pack(pady=8, ipady=6)

        # Target Weight
        self.create_label(parent, "Target Weight (kg):")
        self.target_weight = tk.Entry(parent, font=self.entry_font, width=self.width, justify='center')
        self.target_weight.pack(pady=8, ipady=8)

        # Weeks
        self.create_label(parent, "Target Timeframe (weeks):")
        self.weeks = tk.Entry(parent, font=self.entry_font, width=self.width, justify='center')
        self.weeks.pack(pady=8, ipady=8)

        # Age
        self.create_label(parent, "Age:")
        self.age = tk.Entry(parent, font=self.entry_font, width=self.width, justify='center')
        self.age.pack(pady=8, ipady=8)

        # Height
        self.create_label(parent, "Height (cm):")
        self.height = tk.Entry(parent, font=self.entry_font, width=self.width, justify='center')
        self.height.pack(pady=8, ipady=8)

        # Weight
        self.create_label(parent, "Current Weight (kg):")
        self.weight = tk.Entry(parent, font=self.entry_font, width=self.width, justify='center')
        self.weight.pack(pady=8, ipady=8)

        # Gender
        self.create_label(parent, "Gender:")
        self.gender = ttk.Combobox(parent, values=["Male", "Female"], state="readonly",
                                   width=self.width, font=self.entry_font, justify='center')
        self.gender.current(0)
        self.gender.pack(pady=8, ipady=6)

        # Exercise Level
        self.create_label(parent, "Exercise Level:")
        self.exercise = ttk.Combobox(parent,
                                     values=["Beginner", "Intermediate", "Advanced"],
                                     state="readonly",
                                     width=self.width,
                                     font=self.entry_font, justify='center')
        self.exercise.current(0)
        self.exercise.pack(pady=8, ipady=6)

        # ---------------- MULTI-SELECT CATEGORY ----------------
        self.create_label(parent, "Workout Category:")

        self.category_frame = tk.Frame(parent, bg="#D0E8F2")
        self.category_frame.pack(pady=8)

        self.category_options = ["Aerobic", "Strength", "Balance", "Flexibility"]
        self.category_vars = {}

        for option in self.category_options:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(
                self.category_frame,
                text=option,
                variable=var,
                font=self.entry_font,
                bg="#D0E8F2",
                activebackground="#D0E8F2"
            )
            chk.pack(anchor="center")
            self.category_vars[option] = var

        # Button
        tk.Button(
            parent,
            text="Generate Plan",
            font=("Arial", 18, "bold"),
            bg="#4CAF50",
            fg="white",
            command=self.submit_data
        ).pack(pady=30, ipadx=15, ipady=12)

    # ---------------- LABEL ----------------
    def create_label(self, parent, text):
        tk.Label(parent, text=text, font=self.label_font, bg="#D0E8F2").pack(pady=5)

    # ---------------- LOGIC ----------------
    def submit_data(self):
        try:
            target_weight = float(self.target_weight.get())
            weeks = int(self.weeks.get())
            age = int(self.age.get())
            height = float(self.height.get())
            current_weight = float(self.weight.get())

            goal_value = self.goal.get()

            # -------- VALIDATION --------
            if not (0 < target_weight <= 300):
                messagebox.showerror("Invalid Target Weight", "1–300 kg only")
                return

            if goal_value == "Gain" and target_weight <= current_weight:
                messagebox.showerror("Invalid Goal", "Target must be GREATER than current weight")
                return

            if goal_value == "Loss" and target_weight >= current_weight:
                messagebox.showerror("Invalid Goal", "Target must be LESS than current weight")
                return

            if not (4 <= weeks <= 52):
                messagebox.showerror("Invalid Timeframe", "4–52 weeks only")
                return

            if not (17 <= age <= 100):
                messagebox.showerror("Invalid Age", "17–100 only")
                return

            if not (0 < height <= 300):
                messagebox.showerror("Invalid Height", "1–300 cm only")
                return

            if not (0 < current_weight <= 300):
                messagebox.showerror("Invalid Weight", "1–300 kg only")
                return

            # -------- GENDER --------
            gender_map = {"Male": "M", "Female": "F"}
            gender_value = gender_map[self.gender.get()]

            # -------- MULTI CATEGORY --------
            selected_categories = [
                key.lower() for key, var in self.category_vars.items() if var.get()
            ]

            if not selected_categories:
                messagebox.showerror("Invalid Category", "Please select at least one workout category")
                return

            # -------- CREATE USER --------
            user = UserData(
                goal=goal_value.lower(),
                target_weight=target_weight,
                weeks=weeks,
                age=age,
                height=height,
                weight=current_weight,
                gender=gender_value,
                exercise=self.exercise.get().lower(),
                category=selected_categories
            )

            self.app_logic.show_results(user)

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers!")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()