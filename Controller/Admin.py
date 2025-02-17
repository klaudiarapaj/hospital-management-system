# admin class, acts as a controller to handle the logic related to any interaction between the admin and the GUI
import os
import pickle  # handling the files with pickle so that it is serialized and secure data

# importing all models which the system has and which the admin can modify
from Model.Appointment import Appointment
from Model.Billing import Billing
from Model.Doctor import Doctor
from Model.Patient import Patient


class Admin:  # the class has 4 lists to handle the information for each big component
    __patients = []
    __doctors = []
    __appointments = []
    __bills = []

    def __init__(self):  # the initializer for the class handles only the logic information
        self.admin_email = "admin@gmail.com"  # default admin email
        self.admin_password = "admin"  # default password
        # the login information will be validated based on these
        # the credentials remain the same within the system because they are shared with the staff

    @staticmethod
    def load_data():  # static methods to handle the pickled files
        if os.path.exists("../patients.pkl"):  # relative path of the file
            with open("../patients.pkl", "rb") as patient_file:  # opening the file of read
                Admin.__patients = pickle.load(patient_file)  # loading the file into the admin's dedicated list
        else:
            Admin.__patients = []

        if os.path.exists("../doctors.pkl"):
            with open("../doctors.pkl", "rb") as doctor_file:
                Admin.__doctors = pickle.load(doctor_file)  # loading the file into the admin's dedicated list
        else:
            Admin.__doctors = []

        if os.path.exists("../appointments.pkl"):
            with open("../appointments.pkl", "rb") as appointment_file:
                Admin.__appointments = pickle.load(appointment_file)  # loading the file into the admin's dedicated list
        else:
            Admin.__appointments = []

        if os.path.exists("../bills.pkl"):
            with open("../bills.pkl", "rb") as bill_file:
                Admin.__bills = pickle.load(bill_file)  # loading the file into the admin's dedicated list
        else:
            Admin.__bills = []

        print("Data was loaded.")  # printed in the console to ensure everything was loaded

    @staticmethod
    def save_data():  # before exiting the program the progress is saved back to the files
        with open("../patients.pkl", "wb") as patient_file:  # open the file to write
            pickle.dump(Admin.__patients, patient_file)  # file gets updated with the latest state of the list

        with open("../doctors.pkl", "wb") as doctor_file:
            pickle.dump(Admin.__doctors, doctor_file)  # file gets updated with the latest state of the list

        with open("../appointments.pkl", "wb") as appointment_file:
            pickle.dump(Admin.__appointments, appointment_file)  # file gets updated with the latest state of the list

        with open("../bills.pkl", "wb") as bill_file:
            pickle.dump(Admin.__bills, bill_file)  # file gets updated with the latest state of the list

        print("Data has been saved.")  # printed in the console to ensure everything was saved

    # Patients logic handling
    def add_patient(self, full_name, age, gender, contact, address):
        if self.find_patient(full_name, gender, contact):
            print(f"Patient {full_name} exists.")
            return

        new_patient = Patient(full_name, age, gender, contact, address)
        self.__patients.append(new_patient)

    def find_patient(self, full_name, gender, contact):
        for patient in self.__patients:
            if patient.get_full_name() == full_name and patient.get_gender() == gender and patient.get_contact() == contact:
                return patient
            else:
                return None

    def update_patient(self, id, **kwargs):
        patient = self.find_patient_by_id(id)  # Look for the patient by ID
        if patient:
            if "full name" in kwargs:
                patient.set_full_name(kwargs["full name"])
            if "age" in kwargs:
                patient.set_age(kwargs["age"])
            if "gender" in kwargs:
                patient.set_gender(kwargs["gender"])
            if "contact" in kwargs:
                patient.set_contact(kwargs["contact"])
            if "address" in kwargs:
                patient.set_address(kwargs["address"])  # Fixed the wrong method call

        else:
            print(f"Patient with ID {id} doesn't exist.")

    def find_patient_by_id(self, id):
        for patient in self.__patients:
            if patient.get_id() == id:
                return patient
        else:
            return None

    def delete_patient(self, id):
        patient = self.find_patient_by_id(id)

        if patient:
            self.__patients.remove(patient)
        else:
            print(f"Patient with ID {id} doesn't exist.")

    def display_patients(self):
        print("Patients List:")
        for patient in self.__patients:
            print(f"ID: {patient.get_id()}, Full Name: {patient.get_full_name()}, "
                  f"Age: {patient.get_age()}, Gender: {patient.get_gender()}, Address: "
                  f"{patient.get_address()}, Contact: {patient.get_contact()}")

    # doctors
    def add_doctor(self, full_name, specialty, contact):
        if self.find_doctor(full_name, specialty, contact):
            print(f"Doctor {full_name} exists.")
            return

        new_doctor = Doctor(full_name, specialty, contact)
        self.__doctors.append(new_doctor)

    def find_doctor(self, full_name, specialty, contact):
        for doctor in self.__doctors:
            if doctor.get_full_name() == full_name and doctor.get_specialty() == specialty and doctor.get_contact() == contact:
                return doctor
            else:
                return None

    def update_doctor(self, id, **kwargs):
        doctor = self.find_doctor_by_id(id)
        if doctor:
            if "full name" in kwargs:
                doctor.set_full_name(kwargs["full name"])
            if "specialty" in kwargs:
                doctor.set_speciality(kwargs["specialty"])
            if "contact" in kwargs:
                doctor.set_contact(kwargs["contact"])
        else:
            print(f"Doctor with ID {id} doesn't exist.")

    def find_doctor_by_id(self, id):
        for doctor in self.__doctors:
            if doctor.get_id() == id:
                return doctor
        else:
            return None

    def delete_doctor(self, id):
        doctor = self.find_doctor_by_id(id)

        if doctor:
            self.__doctors.remove(doctor)
        else:
            print(f"Doctor with ID {id} doesn't exist.")

    def display_doctors(self):
        print("Doctors List:")
        for doctor in self.__doctors:
            print(f"ID: {doctor.get_id()}, Full Name: {doctor.get_full_name()}, "
                  f"Specialty: {doctor.get_specialty()}, Contact: {doctor.get_contact()}")

    # appointments
    def schedule_appointment(self, patient, doctor, day, time_slot):
        if doctor not in self.__doctors:
            print(f"Doctor {doctor.get_full_name()} doesn't exist.")
            return False
        if patient not in self.__patients:
            print(f"Patient {patient.get_full_name()} doesn't exist.")
            return False
        if not doctor.is_available(day, time_slot):
            print(f"Doctor {doctor.get_full_name()} is not available on {day} at {time_slot}.")
            return False

        if doctor.book_appointment(day, time_slot, patient):
            new_appointment = Appointment(patient, doctor, day, time_slot)
            self.__appointments.append(new_appointment)
            print(f"Appointment scheduled successfully for {patient.get_full_name()} with {doctor.get_full_name()}.")
            return True

        print("Failed to schedule the appointment.")
        return False

    # Cancel an appointment
    def cancel_appointment(self, patient, doctor, day, time_slot):
        appointment = self.find_appointment(doctor, patient, day, time_slot)
        if appointment:
            appointment.set_status("Cancelled")
            doctor.cancel_appointment(day, time_slot, patient)
            print(f"Appointment on {appointment.get_day()} at {appointment.get_time_slot()} canceled successfully.")
        else:
            print("Appointment not found.")

    # Find an appointment
    def find_appointment(self, doctor, patient, day, time_slot):
        for appointment in self.__appointments:
            if (appointment.get_doctor() == doctor
                    and appointment.get_patient() == patient
                    and appointment.get_day() == day
                    and appointment.get_time_slot() == time_slot):
                return appointment
        return None

    # Mark an appointment as completed
    def completed_appointment(self, patient, doctor, day, time_slot):
        appointment = self.find_appointment(doctor, patient, day, time_slot)
        if appointment:
            appointment.set_status("Completed")
            doctor.complete_appointment(day, time_slot, patient)
            print(f"Appointment on {day} at {time_slot} marked as completed.")
        else:
            print(f"No appointment was found for {patient.get_full_name()} with {doctor.get_full_name()}.")

    # In Admin class:
    def delete_appointment(self, doctor, patient, day, time_slot):
        appointment = self.find_appointment(doctor, patient, day, time_slot)
        if appointment:
            # Remove the appointment using the method from the doctor class
            doctor.delete_appointment(appointment.get_day(), appointment.get_time_slot(), appointment.get_patient())
            self.__appointments.remove(appointment)
            return True
        print("Appointment not found.")
        return False

    # Reset working hours after checking pending appointments
    def reset_doctor_working_hours(self, doctor):
        if doctor.has_pending_appointments():
            print(f"Cannot reset working hours for Dr. {doctor.get_full_name()} as there are scheduled appointments.")
            return False
        doctor.reset_working_hours()
        print(f"Working hours and appointments reset for Dr. {doctor.get_full_name()}.")
        return True

    def display_appointments(self):
        return self.__appointments

    # bills
    def add_bill(self, patient, appointment_fee, procedures):
        if patient not in self.__patients:
            print(f"Patient {patient.get_full_name} was not found.")

        new_bill = Billing(patient, appointment_fee, procedures)
        self.__bills.append(new_bill)

    def validate_admin(self, email, password):
        return email == self.admin_email and password == self.admin_password
