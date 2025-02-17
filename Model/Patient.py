# patient class to handle patient instances

import os


class Patient:
    ID_FILE = "patient_id.txt"  # keeps track of the latest id created in order to have incremental unique ids

    def __init__(self, full_name, age, gender, contact, address):  # the constructor and its necessary attributes
        self.__id = self.load_patient_id()  # load the highest existing Id and set it to the instance id
        self.save_patient_id(self.__id + 1)  # increment the id and save it for the next instance to be created
        self.__full_name = full_name
        self.__age = age
        self.__gender = gender
        self.__contact = contact
        self.__address = address
        self.__medical_records = {}  # dictionary of medical records
        self.__appointments = []  # list of appointments

    def load_patient_id(cls):  # load the id file
        if os.path.exists(cls.ID_FILE):  # check if it exists
            with open(cls.ID_FILE, "r") as file:
                return int(file.read().strip())  # return the id found
        else:
            return 1  # if the file doesn't exist with start with the ids from 1

    def save_patient_id(cls, new_id):  # save the most recent id increment
        with open(cls.ID_FILE, "w") as file:
            file.write(str(new_id))  # write the id to the file

    # getters and setters for all attributes
    def get_id(self):
        return self.__id

    def get_full_name(self):
        return self.__full_name

    def get_age(self):
        return self.__age

    def get_gender(self):
        return self.__gender

    def get_contact(self):
        return self.__contact

    def get_address(self):
        return self.__address

    def get_appointments(self):
        return self.__appointments

    def get_medical_records(self):
        return self.__medical_records

    def set_full_name(self, full_name):
        self.__full_name = full_name

    def set_age(self, age):
        self.__age = age

    def set_gender(self, gender):
        self.__gender = gender

    def set_contact(self, contact):
        self.__contact = contact

    def set_address(self, address):
        self.__address = address

    # method to add medical records to a patient's profile
    def add_medical_record(self, diagnosis, treatment, date):
        medical_record = {  # dictionary is composed of 3 main parts to keep track of
            "Diagnosis": diagnosis,
            "Treatment": treatment,
            "Date": date
        }
        self.__medical_records.append(medical_record)  # add the medical record to the dictionary

    def add_appointment(self, day, time_slot, doctor):  # method to add appointment to the patient's profile
        self.__appointments.append({"Day": day, "Time slot": time_slot, "Doctor": doctor})
