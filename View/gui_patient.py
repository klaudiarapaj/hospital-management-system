from tkinter import *
from tkinter import messagebox, ttk


def add_patient_form(admin, patient_window):
    def save_patient():
        full_name = entry_full_name.get()
        age = entry_age.get()
        gender = gender_var.get()
        contact = entry_contact.get()
        address = entry_address.get()

        if not (full_name and age and gender and contact and address):
            messagebox.showwarning("Incomplete Data", "Please fill out all fields!")
            return

        try:
            admin.add_patient(full_name, int(age), gender, contact, address)
            messagebox.showinfo("Success", f"Patient {full_name} was added successfully!")
            add_patient_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    add_patient_window = Toplevel(patient_window)
    add_patient_window.title("Add Patient")
    add_patient_window.geometry("400x400")
    bg_colour = "#a9ceea"

    add_patient_window.config(bg=bg_colour)

    Label(add_patient_window, text="Full Name:", bg=bg_colour).grid(row=0, column=0, padx=10, pady=10, sticky=W)
    entry_full_name = Entry(add_patient_window, width=30)
    entry_full_name.grid(row=0, column=1, padx=10, pady=10)

    Label(add_patient_window, text="Age:", bg=bg_colour).grid(row=1, column=0, padx=10, pady=10, sticky=W)
    entry_age = Entry(add_patient_window, width=30)
    entry_age.grid(row=1, column=1, padx=10, pady=10)

    Label(add_patient_window, text="Gender:", bg=bg_colour).grid(row=2, column=0, padx=10, pady=10, sticky=W)
    gender_var = StringVar()
    gender_var.set("Male")

    male_radio = Radiobutton(add_patient_window, text="Male", variable=gender_var, value="Male", bg=bg_colour)
    male_radio.grid(row=2, column=1, padx=10, pady=5, sticky=W)

    female_radio = Radiobutton(add_patient_window, text="Female", variable=gender_var, value="Female", bg=bg_colour)
    female_radio.grid(row=2, column=1, padx=80, pady=5, sticky=W)

    Label(add_patient_window, text="Contact:", bg=bg_colour).grid(row=3, column=0, padx=10, pady=10, sticky=W)
    entry_contact = Entry(add_patient_window, width=30)
    entry_contact.grid(row=3, column=1, padx=10, pady=10)

    Label(add_patient_window, text="Address:", bg=bg_colour).grid(row=4, column=0, padx=10, pady=10, sticky=W)
    entry_address = Entry(add_patient_window, width=30)
    entry_address.grid(row=4, column=1, padx=10, pady=10)

    save_button = Button(add_patient_window, text="Save", bg="#164A72", fg="white", width=10, command=save_patient)
    save_button.grid(row=5, columnspan=2, pady=20)

    close_button = Button(add_patient_window, text="Close", bg="#164A72", fg="white", width=10,
                          command=add_patient_window.destroy)
    close_button.grid(row=6, columnspan=2, pady=10)


def edit_patient_form(admin, patient_window):
    def update_patient_details():
        selected_patient_id = int(patient_var.get().split(":")[0])
        updated_details = {
            "full name": entry_full_name.get(),
            "age": entry_age.get(),
            "gender": gender_var.get(),
            "contact": entry_contact.get(),
            "address": entry_address.get()
        }

        try:
            admin.update_patient(selected_patient_id, **updated_details)
            messagebox.showinfo("Success", "Patient details were updated successfully!")
            edit_patient_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    edit_patient_window = Toplevel(patient_window)
    edit_patient_window.title("Edit Patient")
    edit_patient_window.geometry("400x400")
    bg_colour = "#a9ceea"
    edit_patient_window.config(bg=bg_colour)

    Label(edit_patient_window, text="Select Patient to Edit:", bg=bg_colour).grid(row=0, column=0, padx=10, pady=10,
                                                                                  sticky=W)
    patient_var = StringVar()
    patient_dropdownlist = ttk.Combobox(edit_patient_window, textvariable=patient_var, state="readonly")
    patient_dropdownlist['values'] = [
        f"{patient.get_id()}: {patient.get_full_name()}" for patient in admin._Admin__patients
    ]
    patient_dropdownlist.grid(row=0, column=1, padx=10, pady=10)

    show_button = Button(edit_patient_window, text="Show Details",
                         command=lambda: show_patient_details(patient_var.get()))
    show_button.grid(row=1, columnspan=2, pady=10)

    Label(edit_patient_window, text="Full Name:", bg=bg_colour).grid(row=2, column=0, padx=10, pady=10, sticky=W)
    entry_full_name = Entry(edit_patient_window, width=30)
    entry_full_name.grid(row=2, column=1, padx=10, pady=10)

    Label(edit_patient_window, text="Age:", bg=bg_colour).grid(row=3, column=0, padx=10, pady=10, sticky=W)
    entry_age = Entry(edit_patient_window, width=30)
    entry_age.grid(row=3, column=1, padx=10, pady=10)

    Label(edit_patient_window, text="Gender:", bg=bg_colour).grid(row=4, column=0, padx=10, pady=10, sticky=W)
    gender_var = StringVar()

    male_radio = Radiobutton(edit_patient_window, text="Male", variable=gender_var, value="Male", bg=bg_colour)
    male_radio.grid(row=4, column=1, padx=10, pady=5, sticky=W)

    female_radio = Radiobutton(edit_patient_window, text="Female", variable=gender_var, value="Female", bg=bg_colour)
    female_radio.grid(row=4, column=1, padx=80, pady=5, sticky=W)

    Label(edit_patient_window, text="Contact:", bg=bg_colour).grid(row=5, column=0, padx=10, pady=10, sticky=W)
    entry_contact = Entry(edit_patient_window, width=30)
    entry_contact.grid(row=5, column=1, padx=10, pady=10)

    Label(edit_patient_window, text="Address:", bg=bg_colour).grid(row=6, column=0, padx=10, pady=10, sticky=W)
    entry_address = Entry(edit_patient_window, width=30)
    entry_address.grid(row=6, column=1, padx=10, pady=10)

    update_button = Button(edit_patient_window, text="Update", bg="#164A72", fg="white", width=10,
                           command=update_patient_details)
    update_button.grid(row=7, columnspan=2, pady=20)

    close_button = Button(edit_patient_window, text="Close", bg="#164A72", fg="white", width=10,
                          command=edit_patient_window.destroy)
    close_button.grid(row=8, columnspan=2, pady=10)

    def show_patient_details(patient_data):
        if patient_data:
            patient_id = int(patient_data.split(":")[0])
            patient = admin.find_patient_by_id(patient_id)
            if patient:
                entry_full_name.delete(0, END)
                entry_full_name.insert(0, patient.get_full_name())

                entry_age.delete(0, END)
                entry_age.insert(0, patient.get_age())

                gender_var.set(patient.get_gender())

                entry_contact.delete(0, END)
                entry_contact.insert(0, patient.get_contact())

                entry_address.delete(0, END)
                entry_address.insert(0, patient.get_address())


def delete_patient_form(admin, patient_window):
    def delete_patient():
        selected_patient_id = int(patient_var.get().split(":")[0])
        patient = admin.find_patient_by_id(selected_patient_id)

        if patient:
            admin.delete_patient(selected_patient_id)
            messagebox.showinfo("Success", f"Patient {patient.get_full_name()} was deleted!")
            delete_patient_window.destroy()
        else:
            messagebox.showerror("Error", "Patient not found!")

    delete_patient_window = Toplevel(patient_window)
    delete_patient_window.title("Delete Patient")
    delete_patient_window.geometry("400x400")
    bg_colour = "#a9ceea"

    delete_patient_window.config(bg=bg_colour)

    Label(delete_patient_window, text="Select Patient to Delete:", bg=bg_colour).grid(row=0, column=0, padx=10, pady=20,
                                                                                      sticky=W)

    patient_var = StringVar()

    patient_dropdownlist = ttk.Combobox(delete_patient_window, textvariable=patient_var, state="readonly")
    patient_dropdownlist['values'] = [
        f"{patient.get_id()}: {patient.get_full_name()}" for patient in admin._Admin__patients
    ]
    patient_dropdownlist.grid(row=0, column=1, padx=10, pady=20)

    delete_button = Button(delete_patient_window, text="Delete Patient", bg="red", fg="white", width=20,
                           command=delete_patient)
    delete_button.grid(row=1, columnspan=2, pady=10)

    close_button = Button(delete_patient_window, text="Close", bg="#164A72", fg="white", width=20,
                          command=delete_patient_window.destroy)
    close_button.grid(row=2, columnspan=2, pady=10)


def display_patients_form(admin, patient_window):
    display_window = Toplevel(patient_window)
    display_window.title("Display Patients")
    display_window.geometry("900x400")
    bg_colour = "#a9ceea"
    display_window.config(bg=bg_colour)

    columns = ("ID", "Full Name", "Age", "Gender", "Contact", "Address")
    patient_tree = ttk.Treeview(display_window, columns=columns, show="headings")

    # Define column headings and their width
    patient_tree.heading("ID", text="ID", anchor=W)
    patient_tree.heading("Full Name", text="Full Name", anchor=W)
    patient_tree.heading("Age", text="Age", anchor=W)
    patient_tree.heading("Gender", text="Gender", anchor=W)
    patient_tree.heading("Contact", text="Contact", anchor=W)
    patient_tree.heading("Address", text="Address", anchor=W)

    patient_tree.column("ID", width=50, anchor=W)
    patient_tree.column("Full Name", width=200, anchor=W)
    patient_tree.column("Age", width=50, anchor=W)
    patient_tree.column("Gender", width=75, anchor=W)
    patient_tree.column("Contact", width=150, anchor=W)
    patient_tree.column("Address", width=250, anchor=W)

    for patient in admin._Admin__patients:
        patient_tree.insert("", "end", values=(
            patient.get_id(),
            patient.get_full_name(),
            patient.get_age(),
            patient.get_gender(),
            patient.get_contact(),
            patient.get_address()
        ))

    # Scrollbar for the treeview
    scrollbar = Scrollbar(display_window, orient="vertical", command=patient_tree.yview)
    patient_tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    patient_tree.grid(row=0, column=0, padx=10, pady=10)

    close_button = Button(display_window, text="Close", bg="#164A72", fg="white", width=20,
                          command=display_window.destroy)
    close_button.grid(row=1, columnspan=2, pady=20)


def display_appointments_form(admin, patient_window):
    display_window = Toplevel(patient_window)
    display_window.title("Display Appointments")
    display_window.geometry("800x400")
    bg_colour = "#a9ceea"
    display_window.config(bg=bg_colour)

    # Define columns for appointments
    columns = ("Patient ID", "Full Name", "Appointment Day", "Time Slot", "Doctor")

    # Create the treeview to display appointments
    appointment_tree = ttk.Treeview(display_window, columns=columns, show="headings")

    # Define column headings and their width
    appointment_tree.heading("Patient ID", text="Patient ID", anchor=W)
    appointment_tree.heading("Full Name", text="Full Name", anchor=W)
    appointment_tree.heading("Appointment Day", text="Appointment Day", anchor=W)
    appointment_tree.heading("Time Slot", text="Time Slot", anchor=W)
    appointment_tree.heading("Doctor", text="Doctor", anchor=W)

    appointment_tree.column("Patient ID", width=75, anchor=W)
    appointment_tree.column("Full Name", width=200, anchor=W)
    appointment_tree.column("Appointment Day", width=110, anchor=W)
    appointment_tree.column("Time Slot", width=100, anchor=W)
    appointment_tree.column("Doctor", width=150, anchor=W)

    # Insert appointments data into the Treeview
    for patient in admin._Admin__patients:
        for appointment in patient.get_appointments():
            appointment_tree.insert("", "end", values=(
                patient.get_id(),
                patient.get_full_name(),
                appointment["Day"],
                appointment["Time slot"],
                appointment["Doctor"].get_full_name()
            ))

    # Scrollbar for the treeview
    scrollbar = Scrollbar(display_window, orient="vertical", command=appointment_tree.yview)
    appointment_tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    appointment_tree.grid(row=0, column=0, padx=10, pady=10)

    # Close button to close the appointment display window
    close_button = Button(display_window, text="Close", bg="#164A72", fg="white", width=20,
                          command=display_window.destroy)
    close_button.grid(row=1, columnspan=2, pady=20)


def display_medical_history_form(admin, patient_window):
    display_window = Toplevel(patient_window)
    display_window.title("View Medical History")
    display_window.geometry("800x400")
    bg_colour = "#a9ceea"
    display_window.config(bg=bg_colour)

    # Define columns for medical history
    columns = ("Patient ID", "Full Name", "Medical Record")

    # Create the treeview to display medical records
    medical_history_tree = ttk.Treeview(display_window, columns=columns, show="headings")

    # Define column headings and their width
    medical_history_tree.heading("Patient ID", text="Patient ID", anchor=W)
    medical_history_tree.heading("Full Name", text="Full Name", anchor=W)
    medical_history_tree.heading("Medical Record", text="Medical Record", anchor=W)

    medical_history_tree.column("Patient ID", width=75, anchor=W)
    medical_history_tree.column("Full Name", width=200, anchor=W)
    medical_history_tree.column("Medical Record", width=350, anchor=W)

    # Insert medical records data into the Treeview
    for patient in admin._Admin__patients:
        for medical_record in patient._Patient__medical_records:  # Access private attribute to get medical records
            medical_history_tree.insert("", "end", values=(
                patient.get_id(),
                patient.get_full_name(),
                medical_record
            ))

    # Scrollbar for the treeview
    scrollbar = Scrollbar(display_window, orient="vertical", command=medical_history_tree.yview)
    medical_history_tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    medical_history_tree.grid(row=0, column=0, padx=10, pady=10)

    # Close button to close the medical history display window
    close_button = Button(display_window, text="Close", bg="#164A72", fg="white", width=20,
                          command=display_window.destroy)
    close_button.grid(row=1, columnspan=2, pady=20)


def add_medical_history_form(admin, patient_window):
    def add_medical_history():
        # Getting the selected patient
        selected_patient_id = int(patient_var.get().split(":")[0])
        diagnosis = entry_diagnosis.get()
        treatment = entry_treatment.get()
        date_of_visit = entry_date_of_visit.get()

        # Check for empty fields
        if not diagnosis or not treatment or not date_of_visit:
            messagebox.showerror("Error", "All fields must be filled out!")
            return

        try:
            # Finding the selected patient using ID
            patient = next((p for p in admin._Admin__patients if p.get_id() == selected_patient_id), None)
            if patient:
                # Add medical history
                patient.add_medical_record(diagnosis, treatment, date_of_visit)
                messagebox.showinfo("Success", "Medical history added successfully!")
                add_medical_history_window.destroy()
            else:
                messagebox.showerror("Error", "Patient not found.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Creating the add medical history form window
    add_medical_history_window = Toplevel(patient_window)
    add_medical_history_window.title("Add Medical History")
    add_medical_history_window.geometry("400x400")
    bg_colour = "#a9ceea"
    add_medical_history_window.config(bg=bg_colour)

    # Step 1: Select Patient dropdown
    Label(add_medical_history_window, text="Select Patient:", bg=bg_colour).grid(row=0, column=0, padx=10, pady=10,
                                                                                 sticky=W)
    patient_var = StringVar()
    patient_dropdownlist = ttk.Combobox(add_medical_history_window, textvariable=patient_var, state="readonly")
    patient_dropdownlist['values'] = [
        f"{patient.get_id()}: {patient.get_full_name()}" for patient in admin._Admin__patients
    ]
    patient_dropdownlist.grid(row=0, column=1, padx=10, pady=10)

    # Step 2: Medical history input fields
    Label(add_medical_history_window, text="Diagnosis:", bg=bg_colour).grid(row=1, column=0, padx=10, pady=10, sticky=W)
    entry_diagnosis = Entry(add_medical_history_window, width=30)
    entry_diagnosis.grid(row=1, column=1, padx=10, pady=10)

    Label(add_medical_history_window, text="Treatment:", bg=bg_colour).grid(row=2, column=0, padx=10, pady=10, sticky=W)
    entry_treatment = Entry(add_medical_history_window, width=30)
    entry_treatment.grid(row=2, column=1, padx=10, pady=10)

    Label(add_medical_history_window, text="Date of Visit (YYYY-MM-DD):", bg=bg_colour).grid(row=3, column=0, padx=10,
                                                                                             pady=10, sticky=W)
    entry_date_of_visit = Entry(add_medical_history_window, width=30)
    entry_date_of_visit.grid(row=3, column=1, padx=10, pady=10)

    # Step 3: Add Medical History button
    add_button = Button(add_medical_history_window, text="Add Medical History", bg="#164A72", fg="white", width=20,
                        command=add_medical_history)
    add_button.grid(row=4, columnspan=2, pady=20)

    close_button = Button(add_medical_history_window, text="Close", bg="#164A72", fg="white", width=10,
                          command=add_medical_history_window.destroy)
    close_button.grid(row=5, columnspan=2, pady=10)


def search_patient_form(admin, patient_window):
    def search_patient():
        # Get the search text (lowercased for case-insensitive search)
        search_text = entry_search.get().lower()

        # Filter patients based on ID or Full Name match
        matching_patients = [
            patient for patient in admin._Admin__patients if
            search_text in patient.get_full_name().lower() or search_text in str(patient.get_id())
        ]

        if matching_patients:
            # Create a new window to display results
            result_window = Toplevel(patient_window)
            result_window.title("Search Results")
            result_window.geometry("600x500")
            result_window.config(bg="#a9ceea")

            Label(result_window, text="Search Results:", bg="#a9ceea", font=("Helvetica", 14, 'bold')).grid(row=0,
                                                                                                            column=0,
                                                                                                            padx=10,
                                                                                                            pady=10,
                                                                                                            sticky=W)
            row = 1

            # Iterate over matching patients to display full details
            for patient in matching_patients:
                patient_details = f"""
ID: {patient.get_id()}
Full Name: {patient.get_full_name()}
Age: {patient.get_age()}
Gender: {patient.get_gender()}
Contact: {patient.get_contact()}
Address: {patient.get_address()}

Medical Records:
"""
                # Add each medical record to the details
                for record in patient.get_medical_records():
                    patient_details += f"Diagnosis: {record['Diagnosis']}\n"
                    patient_details += f"Treatment: {record['Treatment']}\n"
                    patient_details += f"Date of Visit: {record['Date']}\n"

                # Displaying the detailed information
                Label(result_window, text=patient_details, bg="#a9ceea", justify=LEFT, font=("Helvetica", 10)).grid(
                    row=row, column=0, padx=10, pady=5, sticky=W)
                row += 1

            # Close button for results window
            Button(result_window, text="Close", bg="#164A72", fg="white", width=10, command=result_window.destroy).grid(
                row=row, column=0, pady=20)

        else:
            messagebox.showinfo("No Results", "No patients found matching the search criteria.")

    # Create the search window to take input for search
    search_window = Toplevel(patient_window)
    search_window.title("Search Patient")
    search_window.geometry("400x250")
    search_window.config(bg="#a9ceea")

    Label(search_window, text="Enter ID or Full Name to search:", bg="#a9ceea").grid(row=0, column=0, padx=10, pady=10,
                                                                                     sticky=W)

    entry_search = Entry(search_window, width=30)
    entry_search.grid(row=1, column=0, padx=10, pady=10)

    Button(search_window, text="Search", bg="#164A72", fg="white", width=10, command=search_patient).grid(row=2,
                                                                                                          columnspan=2,
                                                                                                          pady=20)
    Button(search_window, text="Close", bg="#164A72", fg="white", width=10, command=search_window.destroy).grid(row=3,
                                                                                                                columnspan=2,
                                                                                                                pady=10)

def patients_window(admin):
    patient_window = Toplevel()
    patient_window.title("Patients")
    patient_window.state('zoomed')
    bg_colour = "#a9ceea"
    headers_colour = "#164A72"
    patient_window.config(bg=bg_colour)

    add_patient = Button(patient_window, text="Add Patient", bg=headers_colour, fg=bg_colour, font=("Helvetica", 10),
                         height=1, width=20, command=lambda: add_patient_form(admin, patient_window))
    edit_patient = Button(patient_window, text="Edit Patient", bg=headers_colour, fg=bg_colour, font=("Helvetica", 10),
                          height=1, width=20, command=lambda: edit_patient_form(admin, patient_window))
    delete_patient = Button(patient_window, text="Delete Patient", bg=headers_colour, fg=bg_colour,
                            font=("Helvetica", 10), height=1, width=20,
                            command=lambda: delete_patient_form(admin, patient_window))
    display_patients = Button(patient_window, text="Display Patients", bg=headers_colour, fg=bg_colour,
                              font=("Helvetica", 10), height=1, width=20,
                              command=lambda: display_patients_form(admin, patient_window))
    view_appointments = Button(patient_window, text="View Appointments", bg=headers_colour, fg=bg_colour,
                                  font=("Helvetica", 10), height=1, width=20,
                                  command=lambda: display_appointments_form(admin, patient_window))
    search_patient = Button(patient_window, text="Search Patients", bg=headers_colour, fg=bg_colour,
                            font=("Helvetica", 10), height=1, width=20, command=lambda: search_patient_form(admin, patient_window))
    view_medical_history = Button(patient_window, text="View Medical History", bg=headers_colour, fg=bg_colour,
                                  font=("Helvetica", 10), height=1, width=20,
                                  command=lambda: display_medical_history_form(admin, patient_window))
    add_medical_history = Button(patient_window, text="Add Medical History", bg=headers_colour, fg=bg_colour,
                                 font=("Helvetica", 10), height=1, width=20,
                                 command=lambda: add_medical_history_form(admin, patient_window))
    exit_menu = Button(patient_window, text="Exit", bg=headers_colour, fg=bg_colour, font=("Helvetica", 10), height=1,
                       width=5, command=patient_window.destroy)

    add_patient.grid(row=1, column=0, padx=550, pady=20)
    edit_patient.grid(row=2, column=0, padx=100, pady=20)
    delete_patient.grid(row=3, column=0, padx=100, pady=20)
    display_patients.grid(row=4, column=0, padx=100, pady=20)
    view_appointments.grid(row=5, column=0, padx=100, pady=20)
    view_medical_history.grid(row=6, column=0, padx=100, pady=20)
    add_medical_history.grid(row=7, column=0, padx=100, pady=20)
    search_patient.grid(row=8, column=0, padx=100, pady=20)
    exit_menu.grid(row=9, column=0, padx=100, pady=50)
