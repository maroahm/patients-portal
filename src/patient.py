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
from config import GENDERS, WARD_NUMBERS, ROOM_NUMBERS,API_CONTROLLER_URL
#from patient_db_config import API_CONTROLLER_URL
import requests
from itertools import chain

class Patient:
    def __init__(self, name, gender, age):
        self.id = str(uuid.uuid4())
        self.name = name
        if gender not in  GENDERS:
            raise ValueError("Gender must be valid")
        else:
            self.gender = gender
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be Valid")
        else:
            self.age = age
        self.checkin = datetime.now().isoformat()
        self.checkout = None
        self.ward = None
        self.room = None


    def get_id(self):
        print(self.id)
        return self.id
    def get_name(self):
        return self.name
    def get_age(self):
        return self.age
    def get_ward(self):
        return self.ward
    def get_room(self):
        return self.room

    def set_room(self, room_number):
            rooms = list(ROOM_NUMBERS.values())
            flatten = list(chain.from_iterable(rooms))
            if not flatten.__contains__(str(room_number)):
                raise ValueError(f"Invalid room number: {room_number}")
            else:
                self.room = str(room_number)

    def set_ward(self, ward_number):
        if not WARD_NUMBERS.__contains__(ward_number):
            raise ValueError("room should be valid")
        else :
            self.ward = str(ward_number)
    
    def _get_patient_by_id(uri, id):
        uri = f"{API_CONTROLLER_URL}/patients/{id}"
        response = requests.get(uri)
        return response.json()

    def commit(self):
        patient_data = {
            "patient_id": self.id,
            "patient_name": self.name,
            "patient_age": self.age,
            "patient_gender": self.gender,
            "patient_checkin": self.checkin,
            "patient_checkout": self.checkout,
            "patient_ward": self.ward,
            "patient_room": self.room,
        }
        
        get = f"{API_CONTROLLER_URL}/patients"
        put = f"{API_CONTROLLER_URL}/patient/{self.id}"
        response = requests.get(get).json()
        ids = [patient['id'] for patient in response if patient['id'] == self.id]
        
        if self.patient_id in ids:
            response = requests.put(put, json=patient_data)
            if response.status_code == 200:
                print("patient commited to database")
            else:
                print("patient was not commited")

        else:
            response = requests.post(get, json=patient_data)
            if response.status_code == 200:
                print("patient commited to databasel")
            else:
                print("patient was not commited")
        
        
