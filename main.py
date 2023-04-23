import os
import requests
from datetime import datetime

TODAY = datetime.today().strftime("%d/%m/%Y")
TIME = datetime.today().strftime("%X")

# nutritionix - change your data 
MY_GENDER = "male"
MY_AGE = 20
MY_HEIGHT_CM = 160.69
MY_WEIGHT_KG = 45

# either remove this and eneter your id's or just add them to enviornment
API_ID = os.environ.get("NUTRITIONIX_API_ID")
API_KEY = os.environ.get("NUTRITIONIX_API_KEY")
# print(API_KEY)
# print(API_ID)

#sheety - enter your auth
AUTH = ""

nutritionix_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheety_endpoint = "https://api.sheety.co/b1aa16d4e46e84e282cbc8eefc14d226/myWorkouts/workouts"

def get_exercise_info():
    exercised = input("enter the exercises you did: ")
    user_params = {
     "query":exercised,
     "gender":MY_GENDER,
     "weight_kg":MY_WEIGHT_KG,
     "height_cm":MY_HEIGHT_CM,
     "age":MY_AGE
    } 

    header = {
    "x-app-id": API_ID,
    "x-app-key": API_KEY,
    }

    response = requests.post(url= nutritionix_endpoint, json= user_params, headers= header)
    response.raise_for_status()
    return response.json()

def enter_in_sheet(data):
    exercise = data['name']
    duration = data['duration_min']
    calories = data['nf_calories']
    params = {
            "workout": {
                "date": TODAY,
                "time": TIME,
                "exercise": exercise,
                "duration": duration,
                "calories": calories,
                }
            }

    header = {
            "Authorization": AUTH 
            }

    response = requests.post(url= sheety_endpoint, json= params, headers= header)
    response.raise_for_status()
    print(response.text)

exercise_data = get_exercise_info()
data = exercise_data["exercises"]

for exercise in data:
    enter_in_sheet(exercise)

