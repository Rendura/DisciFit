import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

# USER DATA
class UserData:
    def __init__(self, goal, target_weight, weeks, age, height, weight, gender, exercise, category):
        self.goal = goal.lower()  # "gain" or "loss"
        self.target_weight = float(target_weight)
        self.weeks = int(weeks)
        self.age = int(age)
        self.height = float(height)
        self.weight = float(weight)
        self.gender = gender.upper()  # "M" or "F"
        self.exercise = exercise.lower()  # beginner/intermediate/advanced

        if isinstance(category, list):
            self.category = [c.lower() for c in category]
        else:
            self.category = [category.lower()]


# -----------------------------
# FITNESS SYSTEM
# -----------------------------
class FitnessSystem:
    def __init__(self, user):
        self.user = user

        # EXERCISES
        self.exercises = {
            'aerobic': {
                'beginner': ['Brisk Walking', 'Stationary Bike', 'Marching in Place'],
                'intermediate': ['Brisk Walking', 'Stationary Bike', 'Jump Rope', 'Stair Climbing'],
                'advanced': ['Running', 'Jump Rope', 'Battle Ropes', 'Rowing Machine', 'Burpees']
            },
            'strength': {
                'beginner': ['Bodyweight Squats', 'Push-ups (Knee)', 'Seated Dumbbell Press'],
                'intermediate': ['Goblet Squats', 'Push-ups', 'Dumbbell Rows', 'Plank'],
                'advanced': ['Barbell Back Squats', 'Bench Press', 'Deadlifts', 'Pull-ups', 'Weighted Lunges']
            },
            'balance': {
                'beginner': ['Single Leg Stand', 'Heel-to-Toe Walk'],
                'intermediate': ['Single Leg Stand', 'Tree Pose', 'Side Leg Raises'],
                'advanced': ['Single Leg Pistol Squat', 'BOSU Ball Stand', 'Single Leg Deadlift', 'Warrior III']
            },
            'flexibility': {
                'beginner': ['Seated Forward Bend', 'Cat-Cow Stretch'],
                'intermediate': ['Downward Dog', 'Pigeon Pose', 'Seated Spinal Twist'],
                'advanced': ['Full Splits', 'Deep Forward Fold', 'King Pigeon', 'Wheel Pose']
            }
        }

        # SETS / REPS
        self.sets_reps = {
            'beginner': {'sets': 2, 'reps': '10-15', 'duration': '20-30s'},
            'intermediate': {'sets': 3, 'reps': '8-12', 'duration': '30-45s'},
            'advanced': {'sets': 4, 'reps': '6-10', 'duration': '45-60s'}
        }

        # FOOD LIST
        self.foods = {
            'protein': ['Chicken breast (100g)', 'Eggs (2 large)', 'Greek yogurt (150g)', 'Tuna (100g)', 'Whey protein (1 scoop)'],
            'carbs': ['Oats (50g)', 'Sweet potato (200g)', 'Brown rice (100g)', 'Quinoa (100g)', 'Banana (1 large)'],
            'fats': ['Avocado (1/2)', 'Almonds (30g)', 'Olive oil (1 tbsp)', 'Peanut butter (1 tbsp)', 'Salmon (100g)']
        }

    # -----------------------------
    # CALCULATIONS
    # -----------------------------
    def bmi(self):
        return self.user.weight / ((self.user.height / 100) ** 2)

    def bmr(self):
        if self.user.gender == "M":
            return 88.362 + (13.397 * self.user.weight) + (4.799 * self.user.height) - (5.677 * self.user.age)
        else:
            return 447.593 + (9.247 * self.user.weight) + (3.098 * self.user.height) - (4.330 * self.user.age)

    def calories(self):
        activity = {'beginner': 1.2, 'intermediate': 1.55, 'advanced': 1.9}
        tdee = self.bmr() * activity[self.user.exercise]

        if self.user.goal == "gain":
            return tdee + 500
        else:  # loss
            return tdee - 500

    def macros(self):
        cal = self.calories()

        # Goal-based macro distribution
        if self.user.goal == "gain":
            ratios = {'protein': 0.30, 'carbs': 0.50, 'fats': 0.20}
        else:
            ratios = {'protein': 0.35, 'carbs': 0.40, 'fats': 0.25}

        return {
            "protein": round(cal * ratios['protein'] / 4),
            "carbs": round(cal * ratios['carbs'] / 4),
            "fats": round(cal * ratios['fats'] / 9)
        }

    # EXERCISE FUNCTIONS
    def get_exercises(self):
        result = []
        for c in self.user.category:
            if c in self.exercises:
                result.extend(self.exercises[c][self.user.exercise])
        return list(dict.fromkeys(result))

    def get_sets_reps(self):
        return self.sets_reps[self.user.exercise]

    # FOOD SUGGESTIONS
    def get_foods(self):
        return {
            "protein": self.foods['protein'][:3],
            "carbs": self.foods['carbs'][:3],
            "fats": self.foods['fats'][:3]
        }

    def get_exercises(self):
        result = []
        for c in self.user.category:
            if c in self.exercises:
                result.extend(self.exercises[c][self.user.exercise])
        return list(dict.fromkeys(result))

    def get_sets_reps(self):
        return self.sets_reps[self.user.exercise]


# GRAPH
def show_graph(macros):
    labels = ["Protein", "Carbs", "Fats"]
    values = [macros["protein"], macros["carbs"], macros["fats"]]

    plt.figure()
    plt.bar(labels, values)
    plt.title("Macronutrient Distribution")
    plt.show()


#  EXERCISE PROGRESS GRAPH
def show_progress_graph(start_weight, target_weight, weeks, finished):

    if weeks <= 0:
        weeks = 1

    weights = np.linspace(start_weight, target_weight, weeks)
    title = "Completed Progress" if finished else "Partial Progress"

    plt.figure()
    plt.plot(range(1, weeks + 1), weights, marker='o')
    plt.xlabel("Weeks")
    plt.ylabel("Weight (kg)")
    plt.title(title)
    plt.grid()
    plt.show()

# ANOTHER UI LOGIC AND RESULTS
class AppLogic:
    def __init__(self, root):
        self.root = root

    def show_results(self, user):
        try:
            system = FitnessSystem(user)

            bmi = system.bmi()
            calories = system.calories()
            macros = system.macros()
            exercises = system.get_exercises()
            sr = system.get_sets_reps()

            # ---------------- WINDOW ----------------
            win = tk.Toplevel(self.root)
            win.title("DisciFit Results")
            win.configure(bg="#D0E8F2")
            win.geometry("500x700")

            # ---------------- SCROLL ----------------
            container = tk.Frame(win, bg="#D0E8F2")
            container.pack(fill="both", expand=True)

            canvas = tk.Canvas(container, bg="#D0E8F2", highlightthickness=0)
            scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)

            scrollable_frame = tk.Frame(canvas, bg="#D0E8F2")

            window_id = canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

            canvas.configure(yscrollcommand=scrollbar.set)

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            def on_canvas_configure(event):
                canvas_width = event.width
                max_width = 550
                frame_width = min(canvas_width, max_width)

                canvas.itemconfig(window_id, width=frame_width)
                canvas.coords(window_id, canvas_width // 2, 0)

            canvas.bind("<Configure>", on_canvas_configure)

            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )

            canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units"))
            win.bind("<Up>", lambda e: canvas.yview_scroll(-3, "units"))
            win.bind("<Down>", lambda e: canvas.yview_scroll(3, "units"))

            parent = scrollable_frame

            # ---------------- CONTENT ----------------
            tk.Label(parent, text="FITNESS RESULT", font=("Arial", 18, "bold"), bg="#D0E8F2").pack(pady=10)

            tk.Label(parent, text=f"BMI: {bmi:.2f}", bg="#D0E8F2", font=("Arial", 12)).pack()
            tk.Label(parent, text=f"Calories: {calories:.0f} kcal", bg="#D0E8F2", font=("Arial", 12)).pack()

            tk.Label(parent, text="\nMACRONUTRIENTS", bg="#D0E8F2", font=("Arial", 14, "bold")).pack()
            tk.Label(parent,
                     text=f"Protein: {macros['protein']:.0f}g\nCarbs: {macros['carbs']:.0f}g\nFats: {macros['fats']:.0f}g",
                     bg="#D0E8F2", font=("Arial", 11)).pack()
            tk.Label(parent, 
                     text="\nWhat is MACRONUTRIENTS?" , bg="#D0E8F2", font=("Arial", 14, "bold")).pack()
            tk.Label(parent,
                     text="These are your daily macronutrient targets based on your goal and activity level. \n PROTEIN helps build muscle, CARBS provide energy, and FATS support overall health. \n Adjust your food intake to meet these targets for optimal results.",
                     bg="#D0E8F2", font=("Arial", 11)).pack()

            tk.Label(parent, text="\nWORKOUT PLAN", bg="#D0E8F2", font=("Arial", 14, "bold")).pack()
            tk.Label(parent,
                     text="\n".join([f"• {ex}" for ex in exercises]),
                     bg="#D0E8F2", font=("Arial", 11)).pack()

            tk.Label(parent,
                     text=f"\nSets: {sr['sets']} | Reps: {sr['reps']}",
                     bg="#D0E8F2", font=("Arial", 11, "bold")).pack()

            tk.Label(
                    parent,
                    text="\nFOOD SUGGESTIONS",
                    bg="#D0E8F2",
                    font=("Arial", 14, "bold")
                ).pack(fill="x")

            food_text = ""
            for k, v in system.foods.items():
                food_text += f"{k.upper()}: {', '.join(v)}\n"

            tk.Label(
                    parent,
                    text=food_text,
                    bg="#D0E8F2",
                    font=("Arial", 11),
                    wraplength=400,   
                    justify="center",   
                    anchor="w"     
                ).pack()

            tk.Button(parent, text="Show Macronutrient Distribution Graph", bg="#4CAF50", fg="white",
                      font=("Arial", 11, "bold"),
                      command=lambda: show_graph(macros)).pack(pady=10)

            # ---------------- WEEK TRACKER ----------------
            tk.Label(parent, text="\nMark Completed Weeks:", bg="#D0E8F2",
                     font=("Arial", 12, "bold")).pack(pady=10)

            weeks_frame = tk.Frame(parent, bg="#D0E8F2")
            weeks_frame.pack()

            week_vars = []

            for i in range(user.weeks):
                var = tk.BooleanVar()
                tk.Checkbutton(
                    weeks_frame,
                    text=f"Week {i+1}",
                    variable=var,
                    bg="#D0E8F2",
                    font=("Arial", 10)
                ).pack(anchor="w")
                week_vars.append(var)

            def check_progress():
                completed = sum(var.get() for var in week_vars)

                if completed == user.weeks:
                    show_progress_graph(user.weight, user.target_weight, user.weeks, True)
                else:
                    messagebox.showwarning(
                        "Incomplete",
                        f"You only completed {completed}/{user.weeks} weeks."
                    )

            tk.Button(parent, text="Show Progress", bg="#2196F3", fg="white",
                      font=("Arial", 11, "bold"),
                      command=check_progress).pack(pady=15)

        except Exception as e:
            messagebox.showerror("Error", str(e))