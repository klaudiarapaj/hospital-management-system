# doctor class to handle doctor instances

import os

from Model.Appointment import Appointment


class Doctor:
    ID_FILE = "doctor_id.txt"  # keeps track of the latest id created in order to have incremental unique ids

    def __init__(self, full_name, specialty, contact):  # the constructor and its necessary attributes
        self.__id = self.load_doctor_id()  # load the highest existing Id and set it to the instance id
        self.save_doctor_id(self.__id + 1)  # increment the id and save it for the next instance to be created
        self.__full_name = full_name
        self.__specialty = specialty
        self.__contact = contact
        self.__working_hours = {  # default structure of the dictionary, each key holds a list of working hours
            "Monday": [],
            "Tuesday": [],
            "Wednesday": [],
            "Thursday": [],
            "Friday": []
        }
        self.__appointments = [] #store appointements objects in a list
        self.__is_working_hours_set = False  # To track if working hours are already set

    def load_doctor_id(cls):  # load the id file
        if os.path.exists(cls.ID_FILE):  # check if it exists
            with open(cls.ID_FILE, "r") as file:
                return int(file.read().strip())  # return the id found
        else:
            return 1  # if the file doesn't exist with start with the ids from 1

    def save_doctor_id(cls, new_id):  # save the most recent id increment
        with open(cls.ID_FILE, "w") as file:
            file.write(str(new_id))  # write the id to the file

    # getters and setters for all attributes

    def get_id(self):
        return self.__id

    def get_full_name(self):
        return self.__full_name

    def get_specialty(self):
        return self.__specialty

    def get_contact(self):
        return self.__contact

    def get_working_hours(self):
        return self.__working_hours

    def get_appointments(self):
        return self.__appointments

    def set_full_name(self, full_name):
        self.__full_name = full_name

    def set_specialty(self, specialty):
        self.__specialty = specialty

    def set_contact(self, contact):
        self.__contact = contact

    def has_pending_appointments(self):
        # Checks if there are any scheduled appointments
        return any(app.get_status() == "Scheduled" for app in self.__appointments)

    def reset_working_hours(self):
        if self.has_pending_appointments():
            raise ValueError("Cannot reset working hours with pending appointments.")
        for day in self.__working_hours:
            self.__working_hours[day] = []
        self.__appointments.clear()
        self.__is_working_hours_set = False

    def set_working_hours(self, working_hours):
        if self.__is_working_hours_set:
            raise ValueError("Working hours already set. Reset them to update.")
        for day, hours in working_hours.items():
            if day in self.__working_hours:
                self.__working_hours[day] = hours
        self.__is_working_hours_set = True

        # Appointment management

    def book_appointment(self, day, time_slot, patient):
        if day in self.__working_hours and time_slot in self.__working_hours[day]:
            self.__working_hours[day].remove(time_slot)  # Remove the time slot from available working hours
            # Create an Appointment object and store it in __appointments
            appointment = Appointment(patient, self, day, time_slot)
            self.__appointments.append(appointment)
            return True
        return False

    def complete_appointment(self, day, time_slot, patient):
        # Search for the appointment and mark it as completed
        for appointment in self.__appointments:
            if appointment.get_day() == day and appointment.get_time_slot() == time_slot and appointment.get_patient() == patient:
                appointment.set_status("Completed")
                return True
        return False

    def cancel_appointment(self, day, time_slot, patient):
        print(self.__appointments)
        # Search for the appointment and cancel it
        for appointment in self.__appointments:
            if appointment.get_day() == day and appointment.get_time_slot() == time_slot and appointment.get_patient() == patient:
                appointment.set_status("Canceled")
                return True
        return False

    # Modify delete_appointment to take Appointment object directly.
    def delete_appointment(self, day, time_slot, patient):
        for appointment in self.__appointments:
            if appointment.get_day() == day and appointment.get_time_slot() == time_slot and appointment.get_patient() == patient:
                self.__appointments.remove(appointment)
                print(f"Appointment with {patient.get_full_name()} on {day} at {time_slot} has been removed.")
                return True
        print(f"No matching appointment found for {patient.get_full_name()} on {day} at {time_slot}.")
        return False

    def get_available_timeslots(self, day):
        if day not in self.__working_hours:
            return []
        return self.__working_hours[day]

    def is_available(self, day, time_slot):
        return day in self.__working_hours and time_slot in self.get_available_timeslots(day)
