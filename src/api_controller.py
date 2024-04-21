"""Patient API Controller"""

from flask import Flask, request, jsonify
from patient_db import PatientDB
#from patient import Patient

class PatientAPIController:
    def __init__(self):
        self.app = Flask(__name__)
        self.patient_db = PatientDB()
        self.setup_routes()
        self.run()

    def setup_routes(self):
        """
        Sets up the routes for the API endpoints.
        """
        self.app.route("/patients", methods=["GET"])(self.get_patients)
        self.app.route("/patients/<patient_id>", methods=["GET"])(self.get_patient)
        self.app.route("/patients", methods=["POST"])(self.create_patient)
        self.app.route("/patient/<patient_id>", methods=["PUT"])(self.update_patient)
        self.app.route("/patient/<patient_id>", methods=["DELETE"])(self.delete_patient)


    """
    TODO:
    Implement the following methods,
    use the self.patient_db object to interact with the database.

    Every method in this class should return a JSON response with status code
    Status code should be 200 if the operation was successful,
    Status code should be 400 if there was a client error,
    """

    def create_patient(self):
        try:

            data = request.get_json()
            if not data:
                return jsonify({"error": "Missing patient data in request body"}), 400

            patient_id = self.patient_db.insert_patient(data)
            if patient_id == None:
                return jsonify({"error": "Failed to create patient"}), 400

            new_patient = self.patient_db.fetch_patient_id_by_name(data["patient_name"])

            return jsonify(new_patient), 200
            

        except Exception as e:
            print(f"Error creating patient: {e}")
            return jsonify({"error": "Internal server error"}), 500

    def get_patients(self):
        
        try:
            patients = self.patient_db.select_all_patients()
            if patients is not None:
                return jsonify(patients), 200
            else:
                return jsonify({"error": "Failed to retrieve patients."}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def get_patient(self, patient_id):
        
        try:
            patient = self.patient_db.select_patient(patient_id)
            if patient is not None:
                return jsonify(patient), 200
            else:
                return jsonify({"error": "Patient not found."}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def update_patient(self, patient_id):
        
        try:
            update_data = request.json
            affected_rows = self.patient_db.update_patient(patient_id, update_data)
            if affected_rows is not None and affected_rows > 0:
                return jsonify({"message": "Patient updated successfully."}), 200
            else:
                return jsonify({"error": "Failed to update patient."}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def delete_patient(self, patient_id):
        
        try:
            affected_rows = self.patient_db.delete_patient(patient_id)
            if affected_rows is not None and affected_rows > 0:
                return jsonify({"message": "Patient deleted successfully."}), 200
            else:
                return jsonify({"error": "Failed to delete patient."}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def run(self):
        """
        Runs the Flask application.
        """
        self.app.run()


PatientAPIController()
