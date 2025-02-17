# appointment class to handle appointment instances
import os


class Appointment:
    ID_FILE = "appointment_id.txt"  # keeps track of the latest id created in order to have incremental unique ids

    # all attributes of instances are private
    def __init__(self, patient, doctor, day, time_slot,
                 status="Scheduled"):  # the constructor and its necessary attributes, the status is Scheduled by defaulted
        self.__id = self.load_appointment_id()  # load the highest existing Id and set it to the instance id
        self.save_appointment_id(self.__id + 1)  # increment the id and save it for the next instance to be created
        self.__patient = patient
        self.__doctor = doctor
        self.__day = day
        self.__time_slot = time_slot
        self.__status = status

    def load_appointment_id(cls):  # load the id file
        if os.path.exists(cls.ID_FILE):  # check if it exists
            with open(cls.ID_FILE, "r") as file:
                return int(file.read().strip())  # return the id found
        else:
            return 1  # if the file doesn't exist with start with the ids from 1

    def save_appointment_id(cls, new_id):  # save the most recent id increment
        with open(cls.ID_FILE, "w") as file:
            file.write(str(new_id))  # write the id to the file

    # getters and setters for all attributes
    def get_id(self):
        return self.__id

    def get_patient(self):
        return self.__patient

    def get_doctor(self):
        return self.__doctor

    def get_day(self):
        return self.__day

    def get_time_slot(self):
        return self.__time_slot

    def get_status(self):
        return self.__status

    def set_status(self, status):
        self.__status = status

    def set_time_slot(self, time_slot):
        self.__time_slot = time_slot

    def set_day(self, day):
        self.__day = day
