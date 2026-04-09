import matplotlib.pyplot as plt
import numpy as np

class User:
    def initialize(self, input_desire_weight, input_duration):
        weight_goal_kg = input_desire_weight
        goal_duration = input_duration

        return weight_goal_kg, goal_duration

    def info(self, user_height, user_weight):
        height = user_height
        weight = user_weight
        
        return height, weight
    

target_weight_data = input("Set Your Target Weight (KG): ")
target_duration_data = input("Enter Your Target Timeframe (Weeks): ")

user_height_cm = input("Enter your height in cm: ")
user_weight_kg = input("Enter your current weight in kg: ")

user = User()
print(user.initialize(target_weight_data, target_duration_data))
print(user.info(user_height_cm, user_weight_kg))
