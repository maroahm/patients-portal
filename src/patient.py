from datetime import datetime
import uuid
import requests
from itertools import chain
from config import GENDERS, WARD_NUMBERS, ROOM_NUMBERS ,API_CONTROLLER_URL


class Patient:
    def __init__(self, name,gender,age):
        self.patient_id = str(uuid.uuid4())
        self.patient_name = name
        if gender not in  GENDERS:
            raise ValueError("Gender must be valid")
        else:
            self.patient_gender = gender
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be Valid")
        else:
            self.patient_age = age
        self.patient_checkin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.patient_checkout = None
        self.patient_ward = None
        self.patient_room = None

    def get_room(self):
            return str(self.patient_room)
    
    def get_ward(self):
        return str(self.patient_ward)
    
    def get_id(self):
        return self.patient_id
    
    def get_name(self):
        return self.patient_name
    
    def get_age(self):

        return str(self.patient_age)
    def get_gender(self):
        return self.patient_gender
    
    

    def set_room(self, number):
        rooms = list(ROOM_NUMBERS.values())
        all_rooms = list(chain.from_iterable(rooms))
        if not all_rooms.__contains__(str(number)):
            raise ValueError(f"Invalid room number: {number}")
        else:
            self.patient_room = str(number)
        
            

    def set_ward(self, number):
        if not WARD_NUMBERS.__contains__(number):
            raise ValueError(f"Invalid ward number: {number}")
        else :
            self.patient_ward = str(number)
    
    def _get_patient_by_id(uri, id):
        uri = f"{API_CONTROLLER_URL}/patients/{id}"
        response = requests.get(uri)
        return response.json()

    def commit(self):
        patient_data = {
            "patient_id": self.patient_id,
            "patient_name": self.patient_name,
            "patient_age": self.patient_age,
            "patient_gender": self.patient_gender,
            "patient_checkin": self.patient_checkin,
            "patient_checkout": self.patient_checkout,
            "patient_ward": self.patient_ward,
            "patient_room": self.patient_room,
        }
        
        response = requests.get(f"{API_CONTROLLER_URL}/patients").json()
        ids = [patient['patient_id'] for patient in response if patient['patient_id'] == self.patient_id]
        
        if self.patient_id in ids:
            response = requests.put(f"{API_CONTROLLER_URL}/patient/{self.patient_id}", json=patient_data)
            if response.status_code == 200:
                print("patient Added")
            else:
                print("Commiting failed")

        else:
            response = requests.post(f"{API_CONTROLLER_URL}/patients", json=patient_data)
            if response.status_code == 200:
                print("patient Added")
            else:
                print("Commiting failed")
        
       
