import sys
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

# ─────────────────────────────────────────
#  USER DATA
# ─────────────────────────────────────────
class UserData:
    def __init__(self, goal, target_weight, weeks, age, height, weight, gender, exercise, category):
        self.goal     = goal.lower()
        self.target_weight = float(target_weight)
        self.weeks    = int(weeks)
        self.age      = int(age)
        self.height   = float(height)
        self.weight   = float(weight)
        self.gender   = gender.upper()
        self.exercise = exercise.lower()
        self.category = [c.lower() for c in category] if isinstance(category, list) else [category.lower()]


# ─────────────────────────────────────────
#  FITNESS SYSTEM
# ─────────────────────────────────────────
class FitnessSystem:
    def __init__(self, user: UserData):
        self.user = user

        self.exercises = {
            'aerobic': {
                'beginner':     ['Brisk Walking', 'Stationary Bike', 'Marching in Place'],
                'intermediate': ['Brisk Walking', 'Stationary Bike', 'Jump Rope', 'Stair Climbing'],
                'advanced':     ['Running', 'Jump Rope', 'Battle Ropes', 'Rowing Machine', 'Burpees'],
            },
            'strength': {
                'beginner':     ['Bodyweight Squats', 'Push-ups (Knee)', 'Seated Dumbbell Press'],
                'intermediate': ['Goblet Squats', 'Push-ups', 'Dumbbell Rows', 'Plank'],
                'advanced':     ['Barbell Back Squats', 'Bench Press', 'Deadlifts', 'Pull-ups', 'Weighted Lunges'],
            },
            'balance': {
                'beginner':     ['Single Leg Stand', 'Heel-to-Toe Walk'],
                'intermediate': ['Single Leg Stand', 'Tree Pose', 'Side Leg Raises'],
                'advanced':     ['Single Leg Pistol Squat', 'BOSU Ball Stand', 'Single Leg Deadlift', 'Warrior III'],
            },
            'flexibility': {
                'beginner':     ['Seated Forward Bend', 'Cat-Cow Stretch'],
                'intermediate': ['Downward Dog', 'Pigeon Pose', 'Seated Spinal Twist'],
                'advanced':     ['Full Splits', 'Deep Forward Fold', 'King Pigeon', 'Wheel Pose'],
            },
        }

        self.sets_reps = {
            'beginner':     {'sets': 2, 'reps': '10-15', 'duration': '20-30s'},
            'intermediate': {'sets': 3, 'reps': '8-12',  'duration': '30-45s'},
            'advanced':     {'sets': 4, 'reps': '6-10',  'duration': '45-60s'},
        }

        self.foods = {
            'protein': ['Chicken breast (100g)', 'Eggs (2 large)', 'Greek yogurt (150g)',
                        'Tuna (100g)', 'Whey protein (1 scoop)'],
            'carbs':   ['Oats (50g)', 'Sweet potato (200g)', 'Brown rice (100g)',
                        'Quinoa (100g)', 'Banana (1 large)'],
            'fats':    ['Avocado (1/2)', 'Almonds (30g)', 'Olive oil (1 tbsp)',
                        'Peanut butter (1 tbsp)', 'Salmon (100g)'],
        }

    # ── calculations ──────────────────────
    def bmi(self):
        return self.user.weight / ((self.user.height / 100) ** 2)

    def bmr(self):
        w, h, a = self.user.weight, self.user.height, self.user.age
        if self.user.gender == "M":
            return 88.362 + (13.397 * w) + (4.799 * h) - (5.677 * a)
        return 447.593 + (9.247 * w) + (3.098 * h) - (4.330 * a)

    def calories(self):
        activity = {'beginner': 1.2, 'intermediate': 1.55, 'advanced': 1.9}
        tdee = self.bmr() * activity[self.user.exercise]
        return tdee + 500 if self.user.goal == "gain" else tdee - 500

    def macros(self):
        cal = self.calories()
        if self.user.goal == "gain":
            ratios = {'protein': 0.30, 'carbs': 0.50, 'fats': 0.20}
        else:
            ratios = {'protein': 0.35, 'carbs': 0.40, 'fats': 0.25}
        return {
            "protein": round(cal * ratios['protein'] / 4),
            "carbs":   round(cal * ratios['carbs']   / 4),
            "fats":    round(cal * ratios['fats']     / 9),
        }

    def get_exercises(self):
        result = []
        for c in self.user.category:
            if c in self.exercises:
                result.extend(self.exercises[c][self.user.exercise])
        return list(dict.fromkeys(result))

    def get_sets_reps(self):
        return self.sets_reps[self.user.exercise]

    def get_foods(self):
        return {k: v[:3] for k, v in self.foods.items()}


# ─────────────────────────────────────────
#  GRAPHS
# ─────────────────────────────────────────
def show_graph(macros: dict):
    labels = ["Protein", "Carbs", "Fats"]
    values = [macros["protein"], macros["carbs"], macros["fats"]]
    plt.figure()
    plt.bar(labels, values, color=["#4CAF50", "#2196F3", "#FF9800"])
    plt.title("Macronutrient Distribution (g)")
    plt.ylabel("Grams")
    plt.tight_layout()
    plt.show()


def show_progress_graph(start_weight: float, target_weight: float, weeks: int, finished: bool):
    if weeks <= 0:
        weeks = 1
    weights = np.linspace(start_weight, target_weight, weeks)
    title = "Completed Progress" if finished else "Partial Progress"
    plt.figure()
    plt.plot(range(1, weeks + 1), weights, marker='o', color="#4CAF50")
    plt.xlabel("Weeks")
    plt.ylabel("Weight (kg)")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# ─────────────────────────────────────────
#  CLI HELPERS
# ─────────────────────────────────────────
SEP  = "=" * 52
SEP2 = "-" * 52

def header(text: str):
    print(f"\n{SEP}")
    print(f"  {text}")
    print(SEP)

def section(text: str):
    print(f"\n{SEP2}")
    print(f"  {text}")
    print(SEP2)

def prompt(label: str, default: str = "") -> str:
    hint = f" [{default}]" if default else ""
    return input(f"  {label}{hint}: ").strip() or default

def choose(label: str, options: list[str]) -> str:
    """Display a numbered menu and return the chosen value (lowercase)."""
    print(f"\n  {label}")
    for i, opt in enumerate(options, 1):
        print(f"    {i}) {opt}")
    while True:
        raw = input("  Enter number: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1].lower()
        print("  ⚠  Invalid choice, try again.")

def multi_choose(label: str, options: list[str]) -> list[str]:
    """Let the user pick one or more options by number (comma-separated)."""
    print(f"\n  {label}")
    for i, opt in enumerate(options, 1):
        print(f"    {i}) {opt}")
    while True:
        raw = input("  Enter numbers (e.g. 1,3): ").strip()
        picks = [p.strip() for p in raw.split(",")]
        if all(p.isdigit() and 1 <= int(p) <= len(options) for p in picks) and picks:
            return [options[int(p) - 1].lower() for p in picks]
        print("  ⚠  Invalid selection, try again.")

def get_float(label: str) -> float:
    while True:
        raw = input(f"  {label}: ").strip()
        try:
            return float(raw)
        except ValueError:
            print("  ⚠  Please enter a valid number.")

def get_int(label: str) -> int:
    while True:
        raw = input(f"  {label}: ").strip()
        try:
            return int(raw)
        except ValueError:
            print("  ⚠  Please enter a whole number.")


# ─────────────────────────────────────────
#  INPUT COLLECTION & VALIDATION
# ─────────────────────────────────────────
def collect_inputs() -> UserData:
    header("DisciFit — Fitness Planner")

    goal = choose("Target Goal:", ["Gain", "Loss"])

    current_weight = get_float("Current Weight (kg)")
    while not (0 < current_weight <= 300):
        print("  ⚠  Must be 1–300 kg.")
        current_weight = get_float("Current Weight (kg)")

    while True:
        target_weight = get_float("Target Weight (kg)")
        if not (0 < target_weight <= 300):
            print("  ⚠  Must be 1–300 kg.")
        elif goal == "gain" and target_weight <= current_weight:
            print("  ⚠  For Gain, target must be GREATER than current weight.")
        elif goal == "loss" and target_weight >= current_weight:
            print("  ⚠  For Loss, target must be LESS than current weight.")
        else:
            break

    weeks = get_int("Target Timeframe (weeks)")
    while not (4 <= weeks <= 52):
        print("  ⚠  Must be 4–52 weeks.")
        weeks = get_int("Target Timeframe (weeks)")

    age = get_int("Age")
    while not (17 <= age <= 100):
        print("  ⚠  Must be 17–100.")
        age = get_int("Age")

    height = get_float("Height (cm)")
    while not (0 < height <= 300):
        print("  ⚠  Must be 1–300 cm.")
        height = get_float("Height (cm)")

    gender_str = choose("Gender:", ["Male", "Female"])
    gender = "M" if gender_str == "male" else "F"

    exercise = choose("Exercise Level:", ["Beginner", "Intermediate", "Advanced"])

    categories = multi_choose(
        "Workout Category (pick one or more):",
        ["Aerobic", "Strength", "Balance", "Flexibility"]
    )

    return UserData(
        goal=goal,
        target_weight=target_weight,
        weeks=weeks,
        age=age,
        height=height,
        weight=current_weight,
        gender=gender,
        exercise=exercise,
        category=categories,
    )


# ─────────────────────────────────────────
#  RESULTS DISPLAY
# ─────────────────────────────────────────
def display_results(user: UserData):
    system = FitnessSystem(user)

    bmi      = system.bmi()
    calories = system.calories()
    macros   = system.macros()
    exercises = system.get_exercises()
    sr       = system.get_sets_reps()

    header("FITNESS RESULTS")

    # ── Summary table ─────────────────────
    summary_data = [
        ["BMI",      f"{bmi:.2f}"],
        ["Calories", f"{calories:.0f} kcal/day"],
    ]
    print()
    print(tabulate(summary_data, headers=["Metric", "Value"], tablefmt="rounded_outline"))

    # ── Macronutrients table ──────────────
    section("MACRONUTRIENTS")
    macro_data = [
        ["Protein", f"{macros['protein']}g", "Builds muscle"],
        ["Carbs",   f"{macros['carbs']}g",   "Provides energy"],
        ["Fats",    f"{macros['fats']}g",    "Supports health"],
    ]
    print()
    print(tabulate(macro_data, headers=["Macro", "Daily Target", "Role"], tablefmt="rounded_outline"))
    print()
    print("  These are your daily targets based on your goal and activity level.")

    # ── Workout plan table ────────────────
    section("WORKOUT PLAN")
    workout_data = [[ex] for ex in exercises]
    print()
    print(tabulate(workout_data, headers=["Exercise"], tablefmt="rounded_outline"))

    sets_reps_data = [
        ["Sets",     str(sr['sets'])],
        ["Reps",     sr['reps']],
        ["Duration", sr['duration']],
    ]
    print()
    print(tabulate(sets_reps_data, headers=["Parameter", "Value"], tablefmt="rounded_outline"))

    # ── Food suggestions table ────────────
    section("FOOD SUGGESTIONS")
    food_data = []
    for macro_type, items in system.foods.items():
        food_data.append([macro_type.upper(), ", ".join(items)])
    print()
    print(tabulate(food_data, headers=["Macro Type", "Food Options"], tablefmt="rounded_outline"))

    # ── Graph menu ───────────────────────
    section("GRAPHS")
    print("  1) Show Macronutrient Distribution Graph")
    print("  2) Show Weight Progress Graph")
    print("  3) Skip")

    choice = input("\n  Choose an option: ").strip()

    if choice == "1":
        show_graph(macros)

    elif choice == "2":
        week_tracker(user)

    # ── Week tracker ─────────────────────
    if choice != "2":
        print()
        again = input("  Would you also like to track weekly progress? (y/n): ").strip().lower()
        if again == "y":
            week_tracker(user)


def week_tracker(user: UserData):
    section("WEEKLY PROGRESS TRACKER")
    print(f"  Mark each completed week (1–{user.weeks}).")
    print("  Enter week numbers separated by commas, or press Enter to skip.")

    raw = input(f"  Completed weeks (e.g. 1,2,3): ").strip()

    if not raw:
        completed = 0
    else:
        picks = [p.strip() for p in raw.split(",") if p.strip().isdigit()]
        picks = [int(p) for p in picks if 1 <= int(p) <= user.weeks]
        completed = len(set(picks))

    # ── Progress summary table ────────────
    progress_data = [
        ["Completed", f"{completed}/{user.weeks} weeks"],
        ["Remaining", f"{user.weeks - completed} week(s)"],
    ]
    print()
    print(tabulate(progress_data, headers=["Progress", "Status"], tablefmt="rounded_outline"))

    if completed == user.weeks:
        print("\n  🎉 Congratulations! You completed all weeks!")
        show_progress_graph(user.weight, user.target_weight, user.weeks, finished=True)
    else:
        remaining = user.weeks - completed
        print(f"\n  Keep going! {remaining} week(s) remaining.")
        show_partial = input("  Show partial progress graph anyway? (y/n): ").strip().lower()
        if show_partial == "y":
            show_progress_graph(user.weight, user.target_weight, completed or 1, finished=False)


# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
def main():
    try:
        user = collect_inputs()
        display_results(user)
        print(f"\n{SEP}")
        print("  Thanks for using DisciFit. Stay consistent! 💪")
        print(f"{SEP}\n")
    except KeyboardInterrupt:
        print("\n\n  Exiting DisciFit. Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()