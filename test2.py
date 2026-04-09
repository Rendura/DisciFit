import math

class FitnessPlanner:
    def __init__(self):
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
            'protein': ['Chicken breast (100g)', 'Eggs (2 large)', 'Greek yogurt (150g)', 'Tuna (100g)', 'Whey protein (1 scoop)'],
            'carbs': ['Oats (50g)', 'Sweet potato (200g)', 'Brown rice (100g)', 'Quinoa (100g)', 'Banana (1 large)'],
            'fats': ['Avocado (1/2)', 'Almonds (30g)', 'Olive oil (1 tbsp)', 'Peanut butter (1 tbsp)', 'Salmon (100g)']
        }

    def safe_input(self, prompt, input_type=str, valid_options=None, min_val=None, max_val=None):
        """🔧 FIXED: Safe input with proper type handling"""
        while True:
            try:
                # Get raw input as string first
                raw_input = input(prompt).strip()
                
                # Check if empty
                if not raw_input:
                    print("❌ Error input, try again!")
                    continue
                
                # Convert to requested type
                value = input_type(raw_input)
                
                # Check valid options (convert options to lowercase strings for comparison)
                if valid_options:
                    if isinstance(value, str):
                        if value.lower() not in [opt.lower() for opt in valid_options]:
                            print("❌ Error input, try again!")
                            continue
                    else:
                        # For numeric options, convert to strings for comparison
                        val_str = str(value).lower()
                        if val_str not in [str(opt).lower() for opt in valid_options]:
                            print("❌ Error input, try again!")
                            continue
                
                # Check numeric range
                if min_val is not None and value < min_val:
                    print("❌ Error input, try again!")
                    continue
                if max_val is not None and value > max_val:
                    print("❌ Error input, try again!")
                    continue
                
                return value
                
            except ValueError:
                print("❌ Error input, try again!")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                exit()

    def display_exercise_menu(self, category, level):
        """Display numbered menu for exercise selection"""
        exercises = self.exercises[category][level]
        print(f"\n{category.upper()} EXERCISES (Choose {len(exercises)}):")
        print("-" * 40)
        for i, exercise in enumerate(exercises, 1):
            print(f"{i}. {exercise}")
        print("-" * 40)

    def get_exercise_choices(self, category, level, num_choices):
        """Get user exercise selections with validation"""
        exercises = self.exercises[category][level]
        selected = []
        
        while len(selected) < num_choices:
            self.display_exercise_menu(category, level)
            print(f"Select exercise #{len(selected)+1} (1-{len(exercises)}): ", end='')
            
            choice = self.safe_input("", int, valid_options=[str(i) for i in range(1, len(exercises)+1)])
            choice_idx = choice - 1
            
            if choice_idx not in selected:
                selected.append(choice_idx)
                print(f"✅ Added: {exercises[choice_idx]}")
            else:
                print("❌ Already selected, choose another!")
        
        return [exercises[i] for i in selected]

    def get_user_input(self):
        """Collect all user inputs with validation"""
        print("🏋️ PERSONALIZED FITNESS PLANNER 🏋️")
        print("=" * 50)
        
        goal_options = ['gain', 'lose']
        goal_type = self.safe_input("Goal (gain/lose): ", str, valid_options=goal_options)
        
        target_weight = self.safe_input("Target weight (kg) [40-150]: ", float, min_val=40, max_val=150)
        duration_weeks = self.safe_input("Duration (weeks) [8-52]: ", int, min_val=8, max_val=52)
        height = self.safe_input("Height (cm) [0-220]: ", float, min_val=0, max_val=220)
        current_weight = self.safe_input("Current weight (kg) [40-200]: ", float, min_val=40, max_val=200)
        age = self.safe_input("Age [16-80]: ", int, min_val=16, max_val=80)
        
        gender_options = ['m', 'f']
        gender = self.safe_input("Gender (M/F): ", str, valid_options=gender_options).upper()
        
        level_options = ['beginner', 'intermediate', 'advanced']
        level = self.safe_input("Level (beginner/intermediate/advanced): ", str, valid_options=level_options)
        
        return {
            'goal_type': goal_type,
            'target_weight': target_weight,
            'duration_weeks': duration_weeks,
            'height': height,
            'current_weight': current_weight,
            'age': age,
            'gender': gender,
            'level': level
        }

    def select_exercises(self, user_data):
        """Interactive exercise selection for all categories"""
        level = user_data['level']
        num_choices = {'beginner': 2, 'intermediate': 3, 'advanced': 4}[level]
        sr = self.sets_reps[level]
        
        selected_exercises = {}
        
        print(f"\n🎯 SELECT YOUR EXERCISES (Level: {level.upper()})")
        print(f"📋 Choose {num_choices} exercises per category")
        
        for category in self.exercises.keys():
            print(f"\n🏃‍♂️ {category.upper()} CATEGORY")
            selected = self.get_exercise_choices(category, level, num_choices)
            
            selected_exercises[category] = []
            for i, exercise in enumerate(selected, 1):
                if 'duration' in sr:
                    instruction = f"{i}. {exercise}\n   • {sr['sets']} sets x {sr['duration']} hold\n   • Rest 60s between sets\n   • Step-by-step: Stand tall → Hold position → Breathe steadily"
                else:
                    instruction = f"{i}. {exercise}\n   • {sr['sets']} sets x {sr['reps']} reps\n   • Rest 60-90s between sets\n   • Step-by-step: Setup → Execute → Controlled return"
                selected_exercises[category].append(instruction)
        
        return selected_exercises

    def calculate_bmr(self, weight, height, age, gender):
        if gender == 'M':
            return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        else:
            return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    def calculate_tdee(self, bmr, activity_multiplier=1.375):
        return bmr * activity_multiplier

    def calculate_calories(self, user_data):
        bmr = self.calculate_bmr(user_data['current_weight'], user_data['height'], 
                                user_data['age'], user_data['gender'])
        tdee = self.calculate_tdee(bmr)
        
        if user_data['goal_type'] == 'gain':
            calories = tdee + 500
            macros = {'protein': 0.30, 'carbs': 0.50, 'fats': 0.20}
        else:
            calories = tdee - 500
            macros = {'protein': 0.35, 'carbs': 0.40, 'fats': 0.25}
        
        protein_g = (calories * macros['protein']) / 4
        carbs_g = (calories * macros['carbs']) / 4
        fats_g = (calories * macros['fats']) / 9
        
        return {
            'calories': round(calories),
            'protein': round(protein_g),
            'carbs': round(carbs_g),
            'fats': round(fats_g),
            'macros': macros
        }

    def generate_food_suggestions(self, macros):
        suggestions = {}
        for macro, foods in self.foods.items():
            suggestions[macro] = f"• {', '.join(foods[:3])}"
        return suggestions

    def print_plan(self, user_data, nutrition, exercises, foods):
        print("\n" + "="*70)
        print("📊 YOUR CUSTOM PERSONALIZED FITNESS PLAN")
        print("="*70)
        
        print(f"\n👤 PROFILE")
        print(f"   Current: {user_data['current_weight']}kg | Target: {user_data['target_weight']}kg")
        print(f"   Goal: {'GAIN' if user_data['goal_type']=='gain' else 'LOSE'} ({user_data['duration_weeks']}w)")
        print(f"   Level: {user_data['level'].upper()}")
        
        print(f"\n🍽️ DAILY NUTRITION")
        print(f"   Calories: {nutrition['calories']:,} kcal")
        print(f"   Protein: {nutrition['protein']}g ({nutrition['macros']['protein']*100:.0f}%)")
        print(f"   Carbs: {nutrition['carbs']}g ({nutrition['macros']['carbs']*100:.0f}%)")
        print(f"   Fats: {nutrition['fats']}g ({nutrition['macros']['fats']*100:.0f}%)")
        
        print(f"\n🥗 RECOMMENDED FOODS:")
        for macro, suggestion in foods.items():
            pct = nutrition['macros'][macro] * 100
            print(f"   {macro.title()}: {suggestion} ({pct:.0f}%)")
        
        print(f"\n🏋️ YOUR SELECTED EXERCISES ({user_data['level'].upper()})")
        for category, ex_list in exercises.items():
            cat_name = category.replace('_', ' ').title()
            print(f"\n{cat_name}:")
            print("-" * 50)
            for exercise in ex_list:
                print(exercise)
                print()
        
        print("="*70)
        print("✅ PLAN COMPLETE! Follow this for " + str(user_data['duration_weeks']) + " weeks!")
        print("="*70)

def main():
    planner = FitnessPlanner()
    user_data = planner.get_user_input()
    
    nutrition = planner.calculate_calories(user_data)
    foods = planner.generate_food_suggestions(nutrition['macros'])
    
    exercises = planner.select_exercises(user_data)
    
    planner.print_plan(user_data, nutrition, exercises, foods)
    
    again = input("\n🔄 New plan? (y/n): ").lower().strip()
    if again == 'y':
        print("\n" + "="*50 + "\n")
        main()

if __name__ == "__main__":
    main()