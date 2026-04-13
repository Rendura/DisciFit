import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt


# -----------------------------
# USER DATA
# -----------------------------
class UserData:
    def __init__(self, goal, target_weight, weeks, age, height, weight, gender, exercise, category):
        self.goal = goal.lower()
        self.target_weight = float(target_weight)
        self.weeks = int(weeks)
        self.age = int(age)
        self.height = float(height)
        self.weight = float(weight)
        self.gender = gender
        self.exercise = exercise.lower()      
        self.category = category.lower()


# -----------------------------
# FITNESS CALCULATOR
# -----------------------------
class FitnessCalculator:
    def __init__(self, user):
        self.user = user

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

        self.sets_reps = {
            'beginner': {'sets': 2, 'reps': '10-15', 'duration': '20-30s'},
            'intermediate': {'sets': 3, 'reps': '8-12', 'duration': '30-45s'},
            'advanced': {'sets': 4, 'reps': '6-10', 'duration': '45-60s'}
        }

        self.foods = {
            'protein': ['Chicken breast', 'Eggs', 'Tuna'],
            'carbs': ['Rice', 'Oats', 'Banana'],
            'fats': ['Avocado', 'Peanut butter', 'Nuts']
        }

    # -----------------------------
    # CALCULATIONS
    # -----------------------------
    def bmi(self):
        return self.user.weight / ((self.user.height / 100) ** 2)

    def bmr(self):
        if self.user.gender == "Male":
            return 10 * self.user.weight + 6.25 * self.user.height - 5 * self.user.age + 5
        else:
            return 10 * self.user.weight + 6.25 * self.user.height - 5 * self.user.age - 161

    def calories(self):
        activity_map = {
            "beginner": 1.2,
            "intermediate": 1.55,
            "advanced": 1.9
        }

        tdee = self.bmr() * activity_map[self.user.exercise]

        if self.user.goal == "loss":
            return tdee - 500
        return tdee + 500

    def macros(self):
        cal = self.calories()
        return {
            "protein": cal * 0.3 / 4,
            "carbs": cal * 0.4 / 4,
            "fats": cal * 0.3 / 9
        }

    # -----------------------------
    # DATA ACCESS
    # -----------------------------
    def get_foods(self):
        return self.foods

    def get_workout_plan(self):
        category = self.user.category
        level = self.user.exercise

        if category not in self.exercises:
            raise ValueError("Invalid workout category")

        if level not in self.exercises[category]:
            raise ValueError("Invalid exercise level")

        return {
            "category": category,
            "level": level,
            "exercises": self.exercises[category][level],
            "sets_reps": self.sets_reps[level]
        }


# -----------------------------
# APP LOGIC (GUI)
# -----------------------------
class AppLogic:
    def __init__(self, root):
        self.root = root

    def show_results(self, user):
        try:
            calc = FitnessCalculator(user)

            bmi = calc.bmi()
            calories = calc.calories()
            macros = calc.macros()
            plan = calc.get_workout_plan()

            win = tk.Toplevel(self.root)
            win.title("Fitness Plan")
            win.geometry("520x720")

            def label(text, bold=False):
                font = ("Arial", 14, "bold") if bold else ("Arial", 12)
                tk.Label(win, text=text, font=font).pack(pady=2)

            # ---------------- BASIC ----------------
            label(f"BMI: {bmi:.2f}", True)
            label(f"Calories: {calories:.0f}")

            # ---------------- MACROS ----------------
            label("Macros:", True)
            label(f"Protein: {macros['protein']:.0f}g")
            label(f"Carbs: {macros['carbs']:.0f}g")
            label(f"Fats: {macros['fats']:.0f}g")

            # ---------------- WORKOUT ----------------
            label("Workout Plan:", True)
            label(f"Category: {plan['category'].capitalize()}")
            label(f"Level: {plan['level'].capitalize()}")

            label("Exercises:")
            for ex in plan['exercises']:
                label(f"• {ex}")

            sr = plan['sets_reps']
            label("Sets / Reps:", True)
            label(f"Sets: {sr['sets']}")
            label(f"Reps: {sr['reps']}")
            label(f"Duration: {sr['duration']}")

            # ---------------- FOOD ----------------
            label("Food Suggestions:", True)
            for macro, foods in calc.get_foods().items():
                label(f"{macro.capitalize()}: {', '.join(foods)}")

            # ---------------- GRAPH ----------------
            self.show_graph(macros)

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def show_graph(self, macros):
        labels = ["Protein", "Carbs", "Fats"]
        values = [macros["protein"], macros["carbs"], macros["fats"]]

        plt.figure()
        plt.bar(labels, values)
        plt.title("Macronutrient Distribution")
        plt.xlabel("Macronutrients")
        plt.ylabel("Grams")
        plt.show()