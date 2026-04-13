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

        # Resize + center fix
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

        self.canvas.coords(
            self.window_id,
            canvas_width // 2,
            0
        )

    # ---------------- SCROLL FUNCTIONS ----------------
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _scroll_up(self, event):
        self.canvas.yview_scroll(-3, "units")

    def _scroll_down(self, event):
        self.canvas.yview_scroll(3, "units")

    # ---------------- FORM ----------------
    def build_form(self, parent):
        tk.Label(
            parent,
            text="DisciFit",
            font=("Arial", 30, "bold"),
            bg="#D0E8F2"
        ).pack(pady=20)

        # COMBOBOX TARGET GOAL
        self.create_label(parent, "Target Goal:")
        self.goal = ttk.Combobox(parent, values=["Gain", "Loss"], state="readonly",
                                 width=self.width, font=self.entry_font, justify='center')
        self.goal.current(0)
        self.goal.pack(pady=8, ipady=6)

        # USER INPUT TARGET WEIGHT
        self.create_label(parent, "Target Weight (kg):")
        self.target_weight = tk.Entry(parent, font=self.entry_font, width=self.width, justify='center')
        self.target_weight.pack(pady=8, ipady=8)

        # USER INPUT TARGET TIME FRAME
        self.create_label(parent, "Target Timeframe (weeks):")
        self.weeks = tk.Entry(parent, font=self.entry_font, width=self.width, justify='center')
        self.weeks.pack(pady=8, ipady=8)

        # USER INPUT AGE
        self.create_label(parent, "Age:")
        self.age = tk.Entry(parent, font=self.entry_font, width=self.width, justify='center')
        self.age.pack(pady=8, ipady=8)

        # USER INPUT HEIGHT
        self.create_label(parent, "Height (cm):")
        self.height = tk.Entry(parent, font=self.entry_font, width=self.width, justify='center')
        self.height.pack(pady=8, ipady=8)

        # USER INPUT CURRENT WEIGHT
        self.create_label(parent, "Current Weight (kg):")
        self.weight = tk.Entry(parent, font=self.entry_font, width=self.width, justify='center')
        self.weight.pack(pady=8, ipady=8)

        # COMBOBOX GENDER
        self.create_label(parent, "Gender:")
        self.gender = ttk.Combobox(parent, values=["Male", "Female"], state="readonly",
                                   width=self.width, font=self.entry_font, justify='center')
        self.gender.current(0)
        self.gender.pack(pady=8, ipady=6)

        # COMBOBOX EXERCISE LEVEL
        self.create_label(parent, "Exercise Level:")
        self.exercise = ttk.Combobox(parent,
                                     values=["Beginner", "Intermediate", "Advanced"],
                                     state="readonly",
                                     width=self.width,
                                     font=self.entry_font, justify='center')
        self.exercise.current(0)
        self.exercise.pack(pady=8, ipady=6)

        # COMBOBOX WORKOUT CATEGORY
        self.create_label(parent, "Workout Category:")
        self.category = ttk.Combobox(parent,
                                     values=["Aerobic", "Strength", "Balance", "Flexibility"],
                                     state="readonly",
                                     width=self.width,
                                     font=self.entry_font, justify='center')
        self.category.current(0)
        self.category.pack(pady=8, ipady=6)

        # BUTTON
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
            # ---------------- CONVERSION ----------------
            target_weight = float(self.target_weight.get())
            weeks = int(self.weeks.get())
            age = int(self.age.get())
            height = float(self.height.get())
            current_weight = float(self.weight.get())

            # ---------------- VALIDATION RULES ----------------

            if not (0 < target_weight <= 300):
                messagebox.showerror(
                    "Invalid Target Weight",
                    "Target Weight must be between 1 and 300 kg"
                )
                return

            if not (0 < weeks <= 52):
                messagebox.showerror(
                    "Invalid Timeframe",
                    "Target Timeframe must be between 1 and 52 weeks"
                )
                return

            if not (0 < age <= 100):
                messagebox.showerror(
                    "Invalid Age",
                    "Age must be between 1 and 100 years"
                )
                return

            if not (0 < height <= 300):
                messagebox.showerror(
                    "Invalid Height",
                    "Height must be between 1 and 300 cm"
                )
                return

            if not (0 < current_weight <= 300):
                messagebox.showerror(
                    "Invalid Weight",
                    "Current Weight must be between 1 and 300 kg"
                )
                return

            # ---------------- CREATE USER OBJECT ----------------
            user = UserData(
                goal=self.goal.get(),
                target_weight=target_weight,
                weeks=weeks,
                age=age,
                height=height,
                weight=current_weight,
                gender=self.gender.get(),
                exercise=self.exercise.get(),
                category=self.category.get()
            )

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Please enter valid numbers in all fields!"
            )

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()