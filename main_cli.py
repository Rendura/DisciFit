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
                'beginner':     ['Brisk Walking - A low-impact aerobic exercise that elevates heart rate, improves cardiovascular health, burns calories, and is accessible for all fitness levels.', 'Stationary Bike - A seated cardio workout that targets legs, builds endurance, and minimizes joint stress.', 'Marching in Place - A simple, no-equipment cardio move that boosts heart rate, improves coordination, and warms up muscles.'],
                'intermediate': ['Brisk Walking - A low-impact aerobic exercise that elevates heart rate, improves cardiovascular health, burns calories, and is accessible for all fitness levels.', 'Stationary Bike - A seated cardio workout that targets legs, builds endurance, and minimizes joint stress.', 'Jump Rope - High-intensity cardio that enhances agility, coordination, foot speed, and burns fat quickly. Use a properly sized rope.', 'Stair Climbing - A full-body calorie torcher that strengthens legs, glutes, and cardio system. Use stairs or a stepper.'],
                'advanced':     ['Running - Powerful full-body cardio that builds speed, endurance, and leg strength. Suitable outdoors or treadmill.', 'Jump Rope - High-intensity cardio that enhances agility, coordination, foot speed, and burns fat quickly. Use a properly sized rope.', 'Battle Ropes - Explosive upper-body and core cardio that spikes heart rate, builds power, and engages full body.', 'Rowing Machine - A full-body cardiovascular exercise that works the entire body, improving endurance and strength.', 'Burpees - High-intensity full-body exercise combining strength and cardio for maximum calorie burn and metabolism boost.'],
            },
            'strength': {
                'beginner':     ['Bodyweight Squats - A fundamental exercise that targets the legs, glutes, and core. Great for building foundational strength.', 'Push-ups (Knee) - A modified push-up variation that reduces intensity while still targeting the chest, shoulders, and triceps.', 'Seated Dumbbell Press - A seated exercise that focuses on the shoulders and triceps, using light dumbbells for controlled movement.'],
                'intermediate': ['Goblet Squats - A squat variation that emphasizes the quads and glutes while improving core stability.', 'Push-ups - A classic upper-body exercise that builds chest, shoulder, and tricep strength.', 'Dumbbell Rows - A back exercise that targets the rhomboids, middle traps, and rear deltoids.', 'Plank - A core exercise that strengthens the entire midsection and improves posture.'],
                'advanced':     ['Barbell Back Squats - A compound exercise that targets the back, glutes, and legs, building overall strength and power.', 'Bench Press - A classic upper-body exercise that builds chest, shoulder, and tricep strength.', 'Deadlifts - A compound exercise that targets the back, glutes, and legs, building overall strength and power.', 'Pull-ups - A bodyweight exercise that builds back and arm strength.', 'Weighted Lunges - A unilateral exercise that targets the legs and glutes while improving balance and coordination.'],
            },
            'balance': {
                'beginner':     ['Single Leg Stand - A balance exercise that improves stability and proprioception.', 'Heel-to-Toe Walk - A walking exercise that enhances balance and coordination.'],
                'intermediate': ['Single Leg Stand - A balance exercise that improves stability and proprioception.', 'Tree Pose - A yoga pose that enhances balance, flexibility, and focus.', 'Side Leg Raises - A lateral movement exercise that strengthens the hips and improves stability.'],
                'advanced':     ['Single Leg Pistol Squat - A challenging single-leg exercise that builds strength and balance.', 'BOSU Ball Stand - A balance exercise that uses a BOSU ball to challenge stability.', 'Single Leg Deadlift - A unilateral exercise that targets the legs and glutes while improving balance.', 'Warrior III - A yoga pose that enhances balance, flexibility, and core strength.'],
            },
            'flexibility': {
                'beginner':     ['Seated Forward Bend - A gentle stretch that targets the hamstrings and lower back.', 'Cat-Cow Stretch - A dynamic stretch that improves spinal mobility and relieves tension.'],
                'intermediate': ['Downward Dog - A yoga pose that stretches the hamstrings and calves while strengthening the arms and shoulders.', 'Pigeon Pose - A hip opener that stretches the hip flexors and glutes.', 'Seated Spinal Twist - A gentle twist that improves spinal mobility and relieves tension.'],
                'advanced':     ['Full Splits - A challenging stretch that improves flexibility and range of motion.', 'Deep Forward Fold - A deep stretch that targets the hamstrings and lower back.', 'King Pigeon - A challenging hip opener that stretches the hip flexors and glutes.', 'Wheel Pose - A backbend that improves flexibility and strengthens the core.'],
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
    labels  = ["Protein", "Carbs", "Fats"]
    values  = [macros["protein"], macros["carbs"], macros["fats"]]
    colors  = ["#4CAF50", "#2196F3", "#FF9800"]
    total   = sum(values)

    fig, (ax_bar, ax_table) = plt.subplots(
        2, 1,
        figsize=(7, 7),
        gridspec_kw={"height_ratios": [3, 1]},
    )
    fig.suptitle("Macronutrient Distribution", fontsize=14, fontweight="bold", y=0.98)

    # ── Bar chart ─────────────────────────
    bars = ax_bar.bar(labels, values, color=colors, width=0.5, zorder=3)
    ax_bar.set_ylabel("Grams")
    ax_bar.set_ylim(0, max(values) * 1.25)
    ax_bar.yaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
    ax_bar.set_axisbelow(True)

    for bar, val in zip(bars, values):
        ax_bar.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(values) * 0.02,
            f"{val}g",
            ha="center", va="bottom", fontsize=11, fontweight="bold",
        )

    # ── Summary table inside figure ───────
    ax_table.axis("off")
    pct = [f"{v / total * 100:.1f}%" for v in values]
    cal = [
        f"{macros['protein'] * 4} kcal",
        f"{macros['carbs']   * 4} kcal",
        f"{macros['fats']    * 9} kcal",
    ]
    total_kcal = macros['protein'] * 4 + macros['carbs'] * 4 + macros['fats'] * 9
    table_data = [
        ["Protein", f"{values[0]}g", pct[0], cal[0]],
        ["Carbs",   f"{values[1]}g", pct[1], cal[1]],
        ["Fats",    f"{values[2]}g", pct[2], cal[2]],
        ["Total",   f"{total}g",     "100%", f"{total_kcal} kcal"],
    ]
    col_labels = ["Macro", "Grams", "% of Total", "Calories"]

    tbl = ax_table.table(
        cellText  = table_data,
        colLabels = col_labels,
        cellLoc   = "center",
        loc       = "center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 1.5)

    header_color = "#333333"
    row_colors   = ["#E8F5E9", "#E3F2FD", "#FFF3E0", "#F5F5F5"]
    for (row, col), cell in tbl.get_celld().items():
        if row == 0:
            cell.set_facecolor(header_color)
            cell.set_text_props(color="white", fontweight="bold")
        else:
            cell.set_facecolor(row_colors[row - 1])
        cell.set_edgecolor("#CCCCCC")

    plt.tight_layout()
    plt.show()


def show_progress_graph(start_weight: float, target_weight: float, weeks: int, finished: bool):
    if weeks <= 0:
        weeks = 1

    week_nums = list(range(1, weeks + 1))
    weights   = list(np.linspace(start_weight, target_weight, weeks))
    title     = "Completed Progress" if finished else "Partial Progress"
    diff      = target_weight - start_weight

    fig, (ax_line, ax_table) = plt.subplots(
        2, 1,
        figsize=(8, 7),
        gridspec_kw={"height_ratios": [3, 1]},
    )
    fig.suptitle(f"Weight Progress — {title}", fontsize=14, fontweight="bold", y=0.98)

    # ── Line chart ────────────────────────
    line_color = "#4CAF50" if finished else "#2196F3"
    ax_line.plot(week_nums, weights, marker="o", color=line_color, linewidth=2.5,
                 markersize=6, zorder=3)
    ax_line.fill_between(week_nums, weights, alpha=0.15, color=line_color)
    ax_line.set_xlabel("Week")
    ax_line.set_ylabel("Weight (kg)")
    ax_line.yaxis.grid(True, linestyle="--", alpha=0.5, zorder=0)
    ax_line.set_axisbelow(True)

    # Annotate first and last points
    for idx in (0, -1):
        ax_line.annotate(
            f"{weights[idx]:.1f} kg",
            xy=(week_nums[idx], weights[idx]),
            xytext=(0, 10), textcoords="offset points",
            ha="center", fontsize=9, color=line_color, fontweight="bold",
        )

    # ── Summary table inside figure ───────
    ax_table.axis("off")
    direction = "▲ Gain" if diff >= 0 else "▼ Loss"
    col_labels = ["Start Weight", "Target Weight", "Change", "Duration"]
    table_data = [[
        f"{start_weight:.1f} kg",
        f"{target_weight:.1f} kg",
        f"{direction} {abs(diff):.1f} kg",
        f"{weeks} week(s)",
    ]]

    tbl = ax_table.table(
        cellText  = table_data,
        colLabels = col_labels,
        cellLoc   = "center",
        loc       = "center",
    )
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 2)

    header_color = "#333333"
    data_color   = "#E8F5E9" if finished else "#E3F2FD"
    for (row, col), cell in tbl.get_celld().items():
        if row == 0:
            cell.set_facecolor(header_color)
            cell.set_text_props(color="white", fontweight="bold")
        else:
            cell.set_facecolor(data_color)
        cell.set_edgecolor("#CCCCCC")

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
    while not (120 <= height <= 300):
        print("  ⚠  Must be 120–300 cm.")
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
    while True:
        section("GRAPHS")
        print("  1) Show Macronutrient Distribution Graph")
        print("  2) Show Weight Progress Graph")
        print("  3) Skip")

        choice = input("\n  Choose an option: ").strip()

        if choice not in ("1", "2", "3"):
            print("  ❌ Invalid choice. Please enter 1, 2, or 3.")
            continue

        if choice == "3":
            break

        if choice == "1":
            show_graph(macros)
        elif choice == "2":
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
            # Need at least 2 data points to draw a meaningful line graph
            if completed < 2:
                print("  ⚠  At least 2 completed weeks are needed to plot a progress graph.")
                print(f"     Come back once you've logged week 2 or beyond!")
            else:
                # Estimate current weight based on linear progress so far.
                # e.g. if user is 4/12 weeks in, interpolate 4/12 of the way
                # from start to target — not the target itself.
                progress_ratio = completed / user.weeks
                estimated_current = user.weight + (user.target_weight - user.weight) * progress_ratio
                show_progress_graph(user.weight, estimated_current, completed, finished=False)


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