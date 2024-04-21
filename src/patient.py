"""
TODO: Implement the Patient class.
Please import and use the config and db config variables.

The attributes for this class should be the same as the columns in the PATIENTS_TABLE.

The Object Arguments should only be name , gender and age.
Rest of the attributes should be set within the class.

-> for id use uuid4 to generate a unique id for each patient.
-> for checkin and checkout use the current date and time.

There should be a method to update the patient's room and ward. validation should be used.(config is given)

Validation should be done for all of the variables in config and db_config.

There should be a method to commit that patient to the database using the api_controller.
"""

import uuid
from datetime import datetime
from doctor import GENDERS
from patient_db_config import API_CONTROLLER_URL
import requests

class Patient:
    def __init__(self, name, gender, age):
        self.id = str(uuid.uuid4())
        self.name = name
        self.gender = gender
        self.age = age
        self.checkin = datetime.now().isoformat()
        self.checkout = None
        self.ward = None
        self.room = None

    def update_room_and_ward(self, ward, room):
        self.ward = ward
        self.room = room

    def commit_to_database(self):
        patient_data = {
            "patient_name": self.name,
            "patient_gender": self.gender,
            "patient_age": self.age,
            "patient_checkin": self.checkin,
            "patient_ward": self.ward,
            "patient_room": self.room
        }

        try:
            response = requests.post(f"{API_CONTROLLER_URL}/patients", json=patient_data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error while committing patient to database:", e)
            return None
