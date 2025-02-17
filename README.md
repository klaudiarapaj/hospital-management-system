# hospital-management-system

The hospital management system is an application aimed to assist the daily operations in a hospital. This system is solely for the staff of the hospital and no external users.

To log in to the system use the default login credentials:
Email: admin@gmail.com
Password: admin

Once logged in you will be greeted by a screen with 4 buttons: Patients, Doctors, Appointments and Bills. Each of these have several functionalities of their own, which incorporate with the related components.

Any modification to the system, is automatically saved after exiting the system. Breaking the execution will not save the progress made.

The project is structured according to the MVC principles.

Model: Patient, Doctor, Appointment, Billing
View: gui_patient, gui_doctor, gui_appointment, gui_billing
Controller: Admin

The models are the main components of which the project is consisted of. They are responsible of defining the object structure. The views are what the user sees and interacts with. They are developed using the built-in GUI Tk. They communicate with the controller which is the Admin. Admin handles all the logic and receives commands from the view, which it processes and then calls the model, to eventually pass the result back to the view and display to the user. This structure is self-explanatory and easier to work with.

Features:
1.	Patient Management:
o	Add, edit or delete patient records with details such as:
 Full Name
	Patient ID
	Age
	Gender
	Address
	Contact
	Medical Records
3.	Doctor Management:
Add, edit, or delete doctor details such as:
	Full Name
	Doctor ID
	Specialty
	Contact Information
	Working hours
5.	Appointment Scheduling:
o	Schedule appointments for patients with doctors with details such as:
	Date and time
	Patient ID
	Doctor ID
	Appointment Status (Scheduled/Completed/Cancelled).
o	View, update, cancel or delete appointments.
7.	Billing Management:
o	Generate bills for patients including:
	Appointment fees.
	Procedures/surgeries conducted fees.
	Total payment.
9.	Search and Filter functionalities:
o	Search for patients by name, ID, or contact information.
o	Search for doctors by name, ID, or specialty.
o	Search appointments by ID, doctor, patient
12.	Reports:
o	Generate reports like:
	List of admitted patients.
	Doctors’ appointments.
	List of bills
13.	Data Persistence:
o	Store all hospital data in files to ensure data is preserved across sessions.
14.	Graphical User Interface (GUI):
o	Use Tkinter to create a user-friendly interface with widgets like buttons for managing patients, doctors and appointments. Forms and entry fields for entering or updating data. Tables or lists to visualize patient, doctor, appointment records and bills.

Developed by Klaudia Rapaj for academical purposes
