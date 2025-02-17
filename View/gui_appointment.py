from tkinter import *
from tkinter import ttk, messagebox


def schedule_appointment_form(admin, appointment_window):
    # Create a new window for scheduling the appointment
    appointment_form = Toplevel(appointment_window)
    appointment_form.title("Schedule Appointment")
    appointment_form.geometry("500x400")  # Adjust as necessary
    appointment_form.config(bg="#a9ceea")

    # Patient dropdown
    Label(appointment_form, text="Select Patient:", bg="#a9ceea").grid(row=0, column=0, padx=10, pady=10)
    patients = [patient.get_full_name() for patient in admin._Admin__patients]
    patient_dropdown = ttk.Combobox(appointment_form, values=patients)
    patient_dropdown.grid(row=0, column=1, padx=10, pady=10)

    # Doctor dropdown
    Label(appointment_form, text="Select Doctor:", bg="#a9ceea").grid(row=1, column=0, padx=10, pady=10)
    doctors = [doctor.get_full_name() for doctor in admin._Admin__doctors]
    doctor_dropdown = ttk.Combobox(appointment_form, values=doctors)
    doctor_dropdown.grid(row=1, column=1, padx=10, pady=10)

    # Day dropdown
    Label(appointment_form, text="Select Day:", bg="#a9ceea").grid(row=2, column=0, padx=10, pady=10)
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    day_dropdown = ttk.Combobox(appointment_form, values=days)
    day_dropdown.grid(row=2, column=1, padx=10, pady=10)

    # Time slot dropdown (list from 8 AM to 6 PM)
    Label(appointment_form, text="Select Time Slot:", bg="#a9ceea").grid(row=3, column=0, padx=10, pady=10)
    time_slots = [f"{hour}:00-{hour + 1}:00" for hour in range(8, 19)]  # Available slots from 8:00-9:00 to 4:00-5:00
    time_slot_dropdown = ttk.Combobox(appointment_form, values=time_slots)
    time_slot_dropdown.grid(row=3, column=1, padx=10, pady=10)

    # Schedule Appointment button
    def schedule_appointment_action():
        patient_name = patient_dropdown.get()
        doctor_name = doctor_dropdown.get()
        day = day_dropdown.get()
        time_slot = time_slot_dropdown.get()

        if not all([patient_name, doctor_name, day, time_slot]):
            messagebox.showerror("Error", "Please fill all fields.")
            return

        patient = None
        for p in admin._Admin__patients:
            if p.get_full_name() == patient_name:
                patient = p
                break  # Exit the loop once the patient is found

        # For doctor lookup
        doctor = None
        for d in admin._Admin__doctors:
            if d.get_full_name() == doctor_name:
                doctor = d
                break

        if patient and doctor:
            # Check if doctor is available for the chosen day and time
            available_slots = doctor.get_available_timeslots(day)
            if time_slot not in available_slots:
                messagebox.showerror("Error", f"Dr. {doctor_name} is not available on {day} at {time_slot}.")
                return

            # If the doctor is available, schedule the appointment
            success = admin.schedule_appointment(patient, doctor, day, time_slot)
            if success:
                messagebox.showinfo("Success",
                                    f"Appointment scheduled for {patient_name} with Dr. {doctor_name} on {day} at {time_slot}.")
                appointment_form.destroy()
        else:
            messagebox.showerror("Error", "Patient or Doctor not found.")

    schedule_button = Button(appointment_form, text="Schedule Appointment", bg="#164A72", fg="#a9ceea",
                             font=("Helvetica", 10), command=schedule_appointment_action)
    schedule_button.grid(row=4, column=0, columnspan=2, pady=20)

    # Close button
    close_button = Button(appointment_form, text="Close", bg="#164A72", fg="#a9ceea", font=("Helvetica", 10),
                          command=appointment_form.destroy)
    close_button.grid(row=5, column=0, columnspan=2, pady=10)


def complete_appointment_form(admin, appointment_window):
    def mark_appointment_completed():
        selected_appointment_text = appointment_var.get()
        if not selected_appointment_text:
            messagebox.showerror("Error", "Please select an appointment to mark as completed.")
            return

        # Extracting appointment details from the dropdown text
        appointment_id = int(selected_appointment_text.split(":")[0])
        selected_appointment = next((appt for appt in admin._Admin__appointments if appt.get_id() == appointment_id),
                                    None)

        if selected_appointment:
            doctor = selected_appointment.get_doctor()
            patient = selected_appointment.get_patient()
            day = selected_appointment.get_day()
            time_slot = selected_appointment.get_time_slot()

            # Call admin's method for completing the appointment
            admin.completed_appointment(patient, doctor, day, time_slot)
            messagebox.showinfo("Success", f"Appointment {appointment_id} marked as Completed!")
            edit_appointment_window.destroy()
        else:
            messagebox.showerror("Error", f"No appointment found with ID {appointment_id}")

    edit_appointment_window = Toplevel(appointment_window)
    edit_appointment_window.title("Edit Appointment")
    edit_appointment_window.geometry("400x200")
    bg_colour = "#a9ceea"
    edit_appointment_window.config(bg=bg_colour)

    Label(edit_appointment_window, text="Select Appointment:", bg=bg_colour).grid(row=0, column=0, padx=10, pady=10,
                                                                                  sticky=W)

    appointment_var = StringVar()
    appointment_dropdownlist = ttk.Combobox(edit_appointment_window, textvariable=appointment_var, state="readonly")
    # Populate dropdown list with current appointments
    appointment_dropdownlist['values'] = [
        f"{appt.get_id()}: {appt.get_patient().get_full_name()} with {appt.get_doctor().get_full_name()} on {appt.get_day()} at {appt.get_time_slot()}"
        for appt in admin._Admin__appointments
    ]
    appointment_dropdownlist.grid(row=0, column=1, padx=10, pady=10)

    mark_button = Button(edit_appointment_window, text="Mark as Completed", bg="#28a745", fg="white", width=20,
                         command=mark_appointment_completed)
    mark_button.grid(row=1, columnspan=2, pady=20)

    close_button = Button(edit_appointment_window, text="Close", bg="#164A72", fg="white", width=20,
                          command=edit_appointment_window.destroy)
    close_button.grid(row=2, columnspan=2, pady=10)


def cancel_appointment_form(admin, appointment_window):
    def refresh_appointment_list():
        """Refresh the dropdown list with updated appointments."""
        appointment_dropdownlist['values'] = [
            f"{appt.get_id()}: {appt.get_patient().get_full_name()} with {appt.get_doctor().get_full_name()} on {appt.get_day()} at {appt.get_time_slot()}"
            for appt in admin._Admin__appointments
        ]
        appointment_var.set("")  # Clear the selection

    def mark_appointment_cancelled():
        """Cancel the selected appointment."""
        selected_appointment_text = appointment_var.get()
        if not selected_appointment_text:
            messagebox.showerror("Error", "Please select an appointment to cancel.")
            return

        selected_appointment_id = int(selected_appointment_text.split(":")[0])
        selected_appointment = next(
            (appt for appt in admin._Admin__appointments if appt.get_id() == selected_appointment_id), None)

        if selected_appointment:
            doctor = selected_appointment.get_doctor()
            patient = selected_appointment.get_patient()
            day = selected_appointment.get_day()
            time_slot = selected_appointment.get_time_slot()

            # Call admin's method to cancel the appointment
            admin.cancel_appointment(patient, doctor, day, time_slot)

            messagebox.showinfo("Success", f"Appointment {selected_appointment_id} canceled!")
            refresh_appointment_list()
        else:
            messagebox.showerror("Error", f"No appointment found with ID {selected_appointment_id}")

    cancel_appointment_window = Toplevel(appointment_window)
    cancel_appointment_window.title("Cancel Appointment")
    cancel_appointment_window.geometry("400x200")
    bg_colour = "#a9ceea"
    cancel_appointment_window.config(bg=bg_colour)

    Label(cancel_appointment_window, text="Select Appointment:", bg=bg_colour).grid(row=0, column=0, padx=10, pady=10,
                                                                                    sticky=W)

    appointment_var = StringVar()
    appointment_dropdownlist = ttk.Combobox(cancel_appointment_window, textvariable=appointment_var, state="readonly",
                                            width=30)
    refresh_appointment_list()  # Populate the dropdown with current appointments
    appointment_dropdownlist.grid(row=0, column=1, padx=10, pady=10)

    cancel_button = Button(cancel_appointment_window, text="Mark as Cancelled", bg="red", fg="white", width=20,
                           command=mark_appointment_cancelled)
    cancel_button.grid(row=1, columnspan=2, pady=20)

    close_button = Button(cancel_appointment_window, text="Close", bg="#164A72", fg="white", width=20,
                          command=cancel_appointment_window.destroy)
    close_button.grid(row=2, columnspan=2, pady=10)


def delete_appointment_form(admin, appointment_window):
    # This function creates a window to delete appointments.
    delete_appointment_window = Toplevel(appointment_window)
    delete_appointment_window.title("Delete Appointment")
    delete_appointment_window.geometry("400x200")  # Adjusted window size for simplicity
    bg_colour = "#a9ceea"
    delete_appointment_window.config(bg=bg_colour)

    Label(delete_appointment_window, text="Select Appointment:", bg=bg_colour).grid(row=0, column=0, padx=10, pady=10,
                                                                                    sticky=W)

    appointment_var = StringVar()
    appointment_dropdownlist = ttk.Combobox(delete_appointment_window, textvariable=appointment_var, state="readonly")
    # Populate the dropdown with appointment details
    appointment_dropdownlist['values'] = [
        f"{appt.get_id()}: {appt.get_patient().get_full_name()} with {appt.get_doctor().get_full_name()} on {appt.get_day()} at {appt.get_time_slot()}"
        for appt in admin._Admin__appointments
    ]
    appointment_dropdownlist.grid(row=0, column=1, padx=10, pady=10)

    # Define a function to delete the selected appointment
    def delete_appointment_completed():
        selected_appointment_text = appointment_var.get()

        if selected_appointment_text:
            # Extract relevant information from the combobox text
            appointment_id = int(selected_appointment_text.split(":")[0])  # Extracting the ID number from the string
            selected_appointment = None

            # Find the appointment object based on the extracted ID
            for appt in admin._Admin__appointments:
                if appt.get_id() == appointment_id:
                    selected_appointment = appt
                    break

            if selected_appointment:
                doctor = selected_appointment.get_doctor()
                patient = selected_appointment.get_patient()
                day = selected_appointment.get_day()
                time_slot = selected_appointment.get_time_slot()

                admin.delete_appointment(doctor, patient, day, time_slot)
                messagebox.showinfo("Success", f"Appointment was deleted!")


                # Close the deletion window after success
                delete_appointment_window.destroy()
            else:
                print("Appointment not found!")  # This handles the case where the appointment ID was invalid
        else:
            print("No appointment selected!")  # Handle if no appointment was selected

    # Button to delete the selected appointment
    delete_button = Button(delete_appointment_window, text="Delete", bg="red", fg="white", width=20,
                           command=delete_appointment_completed)
    delete_button.grid(row=1, columnspan=2, pady=20)

    # Button to close the form
    close_button = Button(delete_appointment_window, text="Close", bg="#164A72", fg="white", width=20,
                          command=delete_appointment_window.destroy)
    close_button.grid(row=2, columnspan=2, pady=10)


def display_appointments_form(admin, patient_window):
    display_window = Toplevel(patient_window)
    display_window.title("View Appointments")
    display_window.geometry("800x400")
    bg_colour = "#a9ceea"
    display_window.config(bg=bg_colour)

    # Define columns for appointments (including Appointment ID and Status)
    columns = ("Appointment ID", "Patient Name", "Appointment Day", "Time Slot", "Doctor", "Status")

    # Create the treeview to display appointments
    appointment_tree = ttk.Treeview(display_window, columns=columns, show="headings")

    # Define column headings and their width
    appointment_tree.heading("Appointment ID", text="Appointment ID", anchor=W)
    appointment_tree.heading("Patient Name", text="Patient Name", anchor=W)
    appointment_tree.heading("Appointment Day", text="Appointment Day", anchor=W)
    appointment_tree.heading("Time Slot", text="Time Slot", anchor=W)
    appointment_tree.heading("Doctor", text="Doctor", anchor=W)
    appointment_tree.heading("Status", text="Status", anchor=W)


    appointment_tree.column("Appointment ID", width=100, anchor=W)
    appointment_tree.column("Patient Name", width=200, anchor=W)
    appointment_tree.column("Appointment Day", width=120, anchor=W)
    appointment_tree.column("Time Slot", width=100, anchor=W)
    appointment_tree.column("Doctor", width=150, anchor=W)
    appointment_tree.column("Status", width=100, anchor=W)

    # Insert appointments data into the Treeview
    for appointment in admin._Admin__appointments:  # Loop through all appointments
        patient = appointment.get_patient()
        doctor = appointment.get_doctor()

        appointment_tree.insert("", "end", values=(
            appointment.get_id(),                              # Appointment ID
            patient.get_full_name(),                           # Patient Name
            appointment.get_day(),                             # Appointment Day
            appointment.get_time_slot(),                       # Time Slot
            doctor.get_full_name(),                           # Doctor Name
            appointment.get_status()                          # Status (Scheduled, Completed, or Cancelled)
        ))

    # Scrollbar for the treeview
    scrollbar = Scrollbar(display_window, orient="vertical", command=appointment_tree.yview)
    appointment_tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    # Place the treeview in the grid
    appointment_tree.grid(row=0, column=0, padx=10, pady=10)

    # Close button to close the appointment display window
    close_button = Button(display_window, text="Close", bg="#164A72", fg="white", width=20,
                          command=display_window.destroy)
    close_button.grid(row=1, columnspan=2, pady=20)


def search_appointment_form(admin, appointment_window):
    def search_appointment():
        # Get the search text (lowercased for case-insensitive search)
        search_text = entry_search.get().lower()

        # Filter appointments based on appointment ID, patient name, or doctor name
        matching_appointments = [
            appointment for appointment in admin._Admin__appointments if
            search_text in str(appointment.get_id()) or  # Searching in Appointment ID
            search_text in appointment.get_patient().get_full_name().lower() or  # Searching in Patient's Name
            search_text in appointment.get_doctor().get_full_name().lower()  # Searching in Doctor's Name
        ]

        if matching_appointments:
            # Create a new window to display the results
            result_window = Toplevel(appointment_window)
            result_window.title("Search Results")
            result_window.geometry("700x500")  # Adjust as needed
            result_window.config(bg="#a9ceea")

            Label(result_window, text="Search Results:", bg="#a9ceea", font=("Helvetica", 14, 'bold')).grid(
                row=0, column=0, padx=10, pady=10, sticky=W)

            row = 1  # Initialize row index for displaying results

            for appointment in matching_appointments:
                # Compile appointment details
                appointment_details = f"""
Appointment ID: {appointment.get_id()}
Patient Name: {appointment.get_patient().get_full_name()}
Doctor Name: {appointment.get_doctor().get_full_name()}
Appointment Day: {appointment.get_day()}
Time Slot: {appointment.get_time_slot()}
Status: {appointment.get_status()}
"""

                # Display appointment details in a Label widget
                Label(
                    result_window,
                    text=appointment_details,
                    bg="#a9ceea",
                    font=("Helvetica", 10),
                    justify=LEFT,
                ).grid(row=row, column=0, padx=10, pady=5, sticky=W)
                row += 1  # Increment row for next appointment

            # Close button for the results window
            Button(result_window, text="Close", bg="#164A72", fg="white", command=result_window.destroy).grid(
                row=row, column=0, pady=20
            )

        else:
            messagebox.showinfo("No Results", "No appointments found matching the search criteria.")

    # Create the search window to take input for search
    search_window = Toplevel(appointment_window)
    search_window.title("Search Appointment")
    search_window.geometry("400x250")
    search_window.config(bg="#a9ceea")

    Label(search_window, text="Enter Appointment ID, Patient Name, or Doctor Name:", bg="#a9ceea").grid(
        row=0, column=0, padx=10, pady=10, sticky=W)

    # Entry widget for taking search input
    entry_search = Entry(search_window, width=30)
    entry_search.grid(row=1, column=0, padx=10, pady=10)

    # Search button
    Button(search_window, text="Search", bg="#164A72", fg="white", width=10, command=search_appointment).grid(
        row=2, columnspan=2, pady=20
    )

    # Close button to close the search window
    Button(search_window, text="Close", bg="#164A72", fg="white", width=10, command=search_window.destroy).grid(
        row=3, columnspan=2, pady=10
    )


def appointments_window(admin):
    appointment_window = Toplevel()
    appointment_window.title("Appointments")
    appointment_window.state('zoomed')
    bg_colour = "#a9ceea"
    headers_colour = "#164A72"
    appointment_window.config(bg=bg_colour)

    schedule_appointment = Button(appointment_window, text="Schedule Appointment", bg=headers_colour, fg=bg_colour,
                                  font=("Helvetica", 10), height=2, width=20,
                                  command=lambda: schedule_appointment_form(admin, appointment_window))
    update_appointment = Button(appointment_window, text="Update Appointment", bg=headers_colour, fg=bg_colour,
                                font=("Helvetica", 10), height=2, width=20,
                                command=lambda: complete_appointment_form(admin, appointment_window))
    cancel_appointment = Button(appointment_window, text="Cancel Appointment", bg=headers_colour, fg=bg_colour,
                                font=("Helvetica", 10), height=2, width=20,
                                command=lambda: cancel_appointment_form(admin, appointment_window))
    delete_appointment = Button(appointment_window, text="Delete Appointment", bg=headers_colour, fg=bg_colour,
                                font=("Helvetica", 10), height=2, width=20,
                                command=lambda: delete_appointment_form(admin, appointment_window))
    display_appointments = Button(appointment_window, text="View Appointments", bg=headers_colour, fg=bg_colour,
                                  font=("Helvetica", 10), height=2, width=20,
                                  command=lambda: display_appointments_form(admin, appointment_window))
    search_appointment = Button(appointment_window, text="Search Appointments", bg=headers_colour, fg=bg_colour,
                                font=("Helvetica", 10), height=2, width=20,
                                command=lambda: search_appointment_form(admin, appointment_window))
    exit_menu = Button(appointment_window, text="Exit", bg=headers_colour, fg=bg_colour, font=("Helvetica", 10),
                       height=1, width=5, command=appointment_window.destroy)

    schedule_appointment.grid(row=1, column=0, padx=550, pady=20)
    update_appointment.grid(row=2, column=0, padx=100, pady=20)
    cancel_appointment.grid(row=3, column=0, padx=100, pady=20)
    delete_appointment.grid(row=4, column=0, padx=100, pady=20)
    display_appointments.grid(row=5, column=0, padx=100, pady=20)
    search_appointment.grid(row=6, column=0, padx=100, pady=20)
    exit_menu.grid(row=7, column=0, padx=100, pady=100)
