# billing class to handle bill instances

import os


class Billing:
    ID_FILE = "bill_id.txt"  # keeps track of the latest id created in order to have incremental unique ids

    # all attributes of instances are private
    def __init__(self, patient, appointment_fee, procedures):  # the constructor and its necessary attributes
        self.__id = self.load_bill_id()  # load the highest existing Id and set it to the instance id
        self.save_bill_id(self.__id + 1)  # increment the id and save it for the next instance to be created
        self.__patient = patient
        self.__appointment_fee = appointment_fee if appointment_fee else 0  # will be used to calculate total, default is 0 unless specified
        self.__procedures = procedures if procedures else []  # will store the values of the procedures if set, otherwise its empty
        self.__total_amount = 0.0  # total amount 0 by default

    def load_bill_id(cls):  # load the id file
        if os.path.exists(cls.ID_FILE):  # check if it exists
            with open(cls.ID_FILE, "r") as file:
                return int(file.read().strip())  # return the id found
        else:
            return 1  # if the file doesn't exist with start with the ids from 1

    def save_bill_id(cls, new_id):  # save the most recent id increment
        with open(cls.ID_FILE, "w") as file:
            file.write(str(new_id))  # write the id to the file

    def get_id(self):
        return self.__id

    def get_patient(self):
        return self.__patient

    def get_appointment_fee(self):
        return self.__appointment_fee

    def get_procedures(self):
        return self.__procedures

    def get_total_amount(self):
        return self.__total_amount

    def calculate_total(self):  # function to calculate the total of a bill
        procedures_total = 0

        for procedure in self.__procedures:  # go through all procedures
            procedure_name, charge = procedure  # each has a name and a price fee
            procedures_total += charge  # calculate the total for the procedures
            self.__total_amount = self.__appointment_fee + procedures_total  # generate the total amount
