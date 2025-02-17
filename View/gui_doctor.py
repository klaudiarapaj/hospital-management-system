from tkinter import *
from tkinter import messagebox, ttk


def add_doctor_form(admin, doctor_window):
    def save_doctor():
        full_name = entry_full_name.get()
        specialty = entry_specialty.get()
        contact = entry_contact.get()

        if not (full_name and specialty and contact):
            messagebox.showwarning("Incomplete Data", "Please fill out all fields!")
            return

        try:
            admin.add_doctor(full_name, specialty, contact)
            messagebox.showinfo("Success", f"Doctor {full_name} was added successfully!")
            add_doctor_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    add_doctor_window = Toplevel(doctor_window)
    add_doctor_window.title("Add Doctor")
    add_doctor_window.geometry("400x400")
    bg_colour = "#a9ceea"
    add_doctor_window.config(bg=bg_colour)

    Label(add_doctor_window, text="Full Name:", bg=bg_colour).grid(row=0, column=0, padx=10, pady=10, sticky=W)
    entry_full_name = Entry(add_doctor_window, width=30)
    entry_full_name.grid(row=0, column=1, padx=10, pady=10)

    Label(add_doctor_window, text="Specialty:", bg=bg_colour).grid(row=1, column=0, padx=10, pady=10, sticky=W)
    entry_specialty = Entry(add_doctor_window, width=30)
    entry_specialty.grid(row=1, column=1, padx=10, pady=10)

    Label(add_doctor_window, text="Contact:", bg=bg_colour).grid(row=2, column=0, padx=10, pady=10, sticky=W)
    entry_contact = Entry(add_doctor_window, width=30)
    entry_contact.grid(row=2, column=1, padx=10, pady=10)

    save_button = Button(add_doctor_window, text="Save", bg="#164A72", fg="white", width=10, command=save_doctor)
    save_button.grid(row=3, columnspan=2, pady=20)

    close_button = Button(add_doctor_window, text="Close", bg="#164A72", fg="white", width=10,
                          command=add_doctor_window.destroy)
    close_button.grid(row=4, columnspan=2, pady=10)


def edit_doctor_form(admin, doctor_window):
    def update_doctor_details():
        selected_doctor_id = int(doctor_var.get().split(":")[0])
        updated_details = {
            "full name": entry_full_name.get(),
            "specialty": entry_specialty.cget("text"),
            "contact": entry_contact.get()
        }

        try:
            admin.update_doctor(selected_doctor_id, **updated_details)
            messagebox.showinfo("Success", "Doctor details were updated successfully!")
            edit_doctor_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    edit_doctor_window = Toplevel(doctor_window)
    edit_doctor_window.title("Edit Doctor")
    edit_doctor_window.geometry("400x400")
    bg_colour = "#a9ceea"
    edit_doctor_window.config(bg=bg_colour)

    Label(edit_doctor_window, text="Select Doctor to Edit:", bg=bg_colour).grid(row=0, column=0, padx=10, pady=10,
                                                                                sticky=W)

    doctor_var = StringVar()
    doctor_dropdownlist = ttk.Combobox(edit_doctor_window, textvariable=doctor_var, state="readonly")
    doctor_dropdownlist['values'] = [
        f"{doctor.get_id()}: {doctor.get_full_name()}" for doctor in admin._Admin__doctors
    ]
    doctor_dropdownlist.grid(row=0, column=1, padx=10, pady=10)

    show_button = Button(edit_doctor_window, text="Show Details", command=lambda: show_doctor_details(doctor_var.get()))
    show_button.grid(row=1, columnspan=2, pady=10)

    Label(edit_doctor_window, text="Full Name:", bg=bg_colour).grid(row=2, column=0, padx=10, pady=10, sticky=W)
    entry_full_name = Entry(edit_doctor_window, width=30)
    entry_full_name.grid(row=2, column=1, padx=10, pady=10)

    Label(edit_doctor_window, text="Specialty:", bg=bg_colour).grid(row=3, column=0, padx=10, pady=10, sticky=W)
    entry_specialty = Label(edit_doctor_window, width=25)
    entry_specialty.grid(row=3, column=1, padx=10, pady=10)

    Label(edit_doctor_window, text="Contact:", bg=bg_colour).grid(row=4, column=0, padx=10, pady=10, sticky=W)
    entry_contact = Entry(edit_doctor_window, width=30)
    entry_contact.grid(row=4, column=1, padx=10, pady=10)

    update_button = Button(edit_doctor_window, text="Update", bg="#164A72", fg="white", width=10,
                           command=update_doctor_details)
    update_button.grid(row=5, columnspan=2, pady=20)

    close_button = Button(edit_doctor_window, text="Close", bg="#164A72", fg="white", width=10,
                          command=edit_doctor_window.destroy)
    close_button.grid(row=6, columnspan=2, pady=10)

    def show_doctor_details(doctor_data):
        if doctor_data:
            doctor_id = int(doctor_data.split(":")[0])
            doctor = admin.find_doctor_by_id(doctor_id)
            if doctor:
                entry_full_name.delete(0, END)
                entry_full_name.insert(0, doctor.get_full_name())

                entry_specialty.config(text=doctor.get_specialty())

                entry_contact.delete(0, END)
                entry_contact.insert(0, doctor.get_contact())


def delete_doctor_form(admin, doctor_window):
    def delete_doctor():
        selected_doctor_id = int(doctor_var.get().split(":")[0])
        doctor = admin.find_doctor_by_id(selected_doctor_id)

        if doctor:
            admin.delete_doctor(selected_doctor_id)
            messagebox.showinfo("Success", f"Doctor {doctor.get_full_name()} was deleted!")
            delete_doctor_window.destroy()
        else:
            messagebox.showerror("Error", "Doctor not found!")

    delete_doctor_window = Toplevel(doctor_window)
    delete_doctor_window.title("Delete Doctor")
    delete_doctor_window.geometry("400x400")
    bg_colour = "#a9ceea"
    delete_doctor_window.config(bg=bg_colour)

    Label(delete_doctor_window, text="Select Doctor to Delete:", bg=bg_colour).grid(row=0, column=0, padx=10, pady=20,
                                                                                    sticky=W)
    doctor_var = StringVar()

    doctor_dropdownlist = ttk.Combobox(delete_doctor_window, textvariable=doctor_var, state="readonly")
    doctor_dropdownlist['values'] = [
        f"{doctor.get_id()}: {doctor.get_full_name()}" for doctor in admin._Admin__doctors
    ]
    doctor_dropdownlist.grid(row=0, column=1, padx=10, pady=20)

    delete_button = Button(delete_doctor_window, text="Delete Doctor", bg="red", fg="white", width=20,
                           command=delete_doctor)
    delete_button.grid(row=1, columnspan=2, pady=10)

    close_button = Button(delete_doctor_window, text="Close", bg="#164A72", fg="white", width=20,
                          command=delete_doctor_window.destroy)
    close_button.grid(row=2, columnspan=2, pady=10)


def display_doctors_form(admin, doctor_window):
    display_window = Toplevel(doctor_window)
    display_window.title("Display Doctors")
    display_window.geometry("600x400")
    bg_colour = "#a9ceea"
    display_window.config(bg=bg_colour)

    columns = ("ID", "Full Name", "Specialty", "Contact")
    doctor_tree = ttk.Treeview(display_window, columns=columns, show="headings")

    # Define column headings and their width
    doctor_tree.heading("ID", text="ID", anchor=W)
    doctor_tree.heading("Full Name", text="Full Name", anchor=W)
    doctor_tree.heading("Specialty", text="Specialty", anchor=W)
    doctor_tree.heading("Contact", text="Contact", anchor=W)

    doctor_tree.column("ID", width=50, anchor=W)
    doctor_tree.column("Full Name", width=200, anchor=W)
    doctor_tree.column("Specialty", width=150, anchor=W)
    doctor_tree.column("Contact", width=150, anchor=W)

    for doctor in admin._Admin__doctors:
        doctor_tree.insert("", "end", values=(
            doctor.get_id(),
            doctor.get_full_name(),
            doctor.get_specialty(),
            doctor.get_contact()
        ))

    # Scrollbar for the treeview
    scrollbar = Scrollbar(display_window, orient="vertical", command=doctor_tree.yview)
    doctor_tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(row=0, column=1, sticky='ns')

    doctor_tree.grid(row=0, column=0, padx=10, pady=10)

    close_button = Button(display_window, text="Close", bg="#164A72", fg="white", width=20,
                          command=display_window.destroy)
    close_button.grid(row=1, columnspan=2, pady=20)


def display_working_hours_form(admin, doctor_window):
    def show_working_hours():
        # Clear the treeview first
        for row in working_hours_tree.get_children():
            working_hours_tree.delete(row)

        # Check if a specific doctor is selected
        if doctor_var.get():
            selected_doctor_id = int(doctor_var.get().split(":")[0])
            doctor = admin.find_doctor_by_id(selected_doctor_id)

            if doctor:
                working_hours = "; ".join(
                    [f"{day}: {', '.join(slots)}" for day, slots in doctor.get_working_hours().items()])
                working_hours_tree.insert("", "end", values=(
                    doctor.get_id(),
                    doctor.get_full_name(),
                    working_hours
                ))
        else:
            # Show all doctors' working hours
            for doctor in admin._Admin__doctors:
                working_hours = "; ".join(
                    [f"{day}: {', '.join(slots)}" for day, slots in doctor.get_working_hours().items()])
                working_hours_tree.insert("", "end", values=(
                    doctor.get_id(),
                    doctor.get_full_name(),
                    working_hours
                ))

    # Create the display window
    display_window = Toplevel(doctor_window)
    display_window.title("View Doctor Working Hours")
    display_window.geometry("800x500")
    bg_colour = "#a9ceea"
    display_window.config(bg=bg_colour)

    # Dropdown for selecting a doctor
    Label(display_window, text="Select Doctor (Leave blank to view all):", bg=bg_colour).grid(row=0, column=0, padx=10,
                                                                                              pady=10, sticky=W)
    doctor_var = StringVar()

    doctor_dropdownlist = ttk.Combobox(display_window, textvariable=doctor_var, state="normal", width=50)
    doctor_dropdownlist['values'] = [
        f"{doctor.get_id()}: {doctor.get_full_name()}" for doctor in admin._Admin__doctors
    ]
    doctor_dropdownlist.grid(row=0, column=1, padx=10, pady=10)

    # Button to show working hours
    show_button = Button(display_window, text="Show Working Hours", bg="#164A72", fg="white", width=20,
                         command=show_working_hours)
    show_button.grid(row=0, column=2, padx=10, pady=10)

    # Frame for the Treeview and its scrollbars
    frame = Frame(display_window, bg=bg_colour)
    frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

    # Define columns for working hours
    columns = ("Doctor ID", "Full Name", "Working Hours")

    # Create the treeview to display working hours
    working_hours_tree = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")

    # Define column headings and their width
    working_hours_tree.heading("Doctor ID", text="Doctor ID", anchor=W)
    working_hours_tree.heading("Full Name", text="Full Name", anchor=W)
    working_hours_tree.heading("Working Hours", text="Working Hours", anchor=W)

    working_hours_tree.column("Doctor ID", width=75, anchor=W)
    working_hours_tree.column("Full Name", width=200, anchor=W)
    working_hours_tree.column("Working Hours", width=500, anchor=W)

    # Add scrollbars
    scrollbary = Scrollbar(frame, orient="vertical", command=working_hours_tree.yview)
    scrollbarx = Scrollbar(frame, orient="horizontal", command=working_hours_tree.xview)

    working_hours_tree.configure(yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)

    # Pack Treeview and scrollbars
    working_hours_tree.grid(row=0, column=0, sticky="nsew")
    scrollbary.grid(row=0, column=1, sticky="ns")
    scrollbarx.grid(row=1, column=0, sticky="ew")

    # Configure resizing
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Close button
    close_button = Button(display_window, text="Close", bg="#164A72", fg="white", width=20,
                          command=display_window.destroy)
    close_button.grid(row=2, column=0, columnspan=3, pady=20)

    # Show all doctors' working hours by default when the window is opened
    show_working_hours()

# Function to set working hours for a doctor
def set_working_hours_form(admin, doctor_window):
    set_hours_window = Toplevel(doctor_window)
    set_hours_window.title("Set Doctor Working Hours")
    set_hours_window.geometry("1200x600")
    bg_colour = "#a9ceea"
    set_hours_window.config(bg=bg_colour)

    Label(set_hours_window, text="Select Doctor:", bg=bg_colour, font=("Helvetica", 10)).grid(row=0, column=0, padx=10,
                                                                                              pady=10, sticky="w")

    doctor_names = [f"{doctor.get_id()}: {doctor.get_full_name()}" for doctor in admin._Admin__doctors]
    selected_doctor = StringVar(set_hours_window)
    selected_doctor.set('')

    doctor_dropdownlist = ttk.Combobox(set_hours_window, textvariable=selected_doctor, state="normal", width=50)
    doctor_dropdownlist['values'] = doctor_names
    doctor_dropdownlist.grid(row=0, column=1, padx=10, pady=10, sticky="w", columnspan=2)

    Label(set_hours_window, text="Select Time Slots:", bg=bg_colour, font=("Helvetica", 10)).grid(row=1, column=0,
                                                                                                  columnspan=1, padx=5)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    times = [f"{hour}:00-{hour + 1}:00" for hour in range(8, 18)]

    day_slot_vars = {day: {time: IntVar() for time in times} for day in days}

    for row in range(len(days) + 2):
        set_hours_window.grid_rowconfigure(row, weight=1, minsize=20)

    for col in range(len(times)):
        set_hours_window.grid_columnconfigure(col + 1, weight=1, minsize=50)

    for row, day in enumerate(days, start=2):
        Label(set_hours_window, text=day, bg=bg_colour, font=("Helvetica", 10)).grid(row=row, column=0, padx=5, pady=5,
                                                                                     sticky="w")
        for col, time in enumerate(times):
            checkbox = Checkbutton(set_hours_window, text=time, bg=bg_colour, variable=day_slot_vars[day][time])
            checkbox.grid(row=row, column=col + 1, padx=5, pady=2, sticky="w")

    def save_working_hours():
        doctor_data = selected_doctor.get()
        if not doctor_data:
            messagebox.showerror("Error", "Please select a doctor.")
            return

        doctor_id = int(doctor_data.split(":")[0])
        selected_working_hours = {day: [] for day in days}

        for day, slots in day_slot_vars.items():
            for time, var in slots.items():
                if var.get():
                    selected_working_hours[day].append(time)

        for doctor in admin._Admin__doctors:
            if doctor.get_id() == doctor_id:
                try:
                    doctor.set_working_hours(selected_working_hours)
                    messagebox.showinfo("Success", f"Working hours updated for Dr. {doctor.get_full_name()}")
                    set_hours_window.destroy()
                except ValueError as e:
                    messagebox.showerror("Error", str(e))
                return

        messagebox.showerror("Error", "Doctor not found.")

    set_button = Button(set_hours_window, text="Set", bg="#164A72", fg="white", width=15, command=save_working_hours)
    set_button.grid(row=len(days) + 3, column=0, columnspan=2, pady=20)

    close_button = Button(set_hours_window, text="Close", bg="#164A72", fg="white", width=15,
                          command=set_hours_window.destroy)
    close_button.grid(row=len(days) + 3, column=2, columnspan=2, pady=20)


def reset_working_hours_form(admin, doctor_window):
    reset_hours_window = Toplevel(doctor_window)
    reset_hours_window.title("Reset Doctor Working Hours")
    reset_hours_window.geometry("400x200")  # Same geometry size as delete_doctor_form
    bg_colour = "#a9ceea"  # Matching background color for consistency
    reset_hours_window.config(bg=bg_colour)

    # Label to prompt the user to select a doctor
    Label(reset_hours_window, text="Select Doctor to Reset Hours:", bg=bg_colour, font=("Helvetica", 10)).grid(
        row=0, column=0, padx=10, pady=20, sticky="w"
    )

    doctor_names = [f"{doctor.get_id()}: {doctor.get_full_name()}" for doctor in admin._Admin__doctors]
    selected_doctor = StringVar(reset_hours_window)
    selected_doctor.set('')  # Default empty selection

    # Dropdown for selecting a doctor
    doctor_dropdownlist = ttk.Combobox(reset_hours_window, textvariable=selected_doctor, state="normal", width=20)
    doctor_dropdownlist['values'] = doctor_names
    doctor_dropdownlist.grid(row=0, column=1, padx=10, pady=20)

    # Function to reset working hours
    def reset_working_hours():
        doctor_data = selected_doctor.get()
        if not doctor_data:
            messagebox.showerror("Error", "Please select a doctor.")
            return

        doctor_id = int(doctor_data.split(":")[0])

        doctor = next((doc for doc in admin._Admin__doctors if doc.get_id() == doctor_id), None)

        if not doctor:
            messagebox.showerror("Error", "Doctor not found.")
            return

        try:
            doctor.reset_working_hours()
            messagebox.showinfo("Success", f"Working hours reset for Dr. {doctor.get_full_name()}.")
            reset_hours_window.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    # Reset Button with the same style as Delete Doctor window
    reset_button = Button(
        reset_hours_window, text="Reset", bg="red", fg="white", width=15, font=("Helvetica", 10),
        command=reset_working_hours
    )
    reset_button.grid(row=1, columnspan=2, pady=20)

    # Close Button with the same style as Delete Doctor window
    close_button = Button(
        reset_hours_window, text="Close", bg="#164A72", fg="white", width=15, font=("Helvetica", 10),
        command=reset_hours_window.destroy
    )
    close_button.grid(row=2, columnspan=2, pady=10)

def display_appointments_form(admin, doctor_window):
    display_window = Toplevel(doctor_window)
    display_window.title("View Appointments")
    display_window.geometry("800x400")
    bg_colour = "#a9ceea"
    display_window.config(bg=bg_colour)

    # Define columns for appointments
    columns = ("Doctor ID", "Full Name", "Appointment Day", "Time Slot", "Patient", "Status")

    # Create the treeview to display appointments
    appointment_tree = ttk.Treeview(display_window, columns=columns, show="headings")

    # Define column headings and their width
    appointment_tree.heading("Doctor ID", text="Doctor ID", anchor=W)
    appointment_tree.heading("Full Name", text="Full Name", anchor=W)
    appointment_tree.heading("Appointment Day", text="Appointment Day", anchor=W)
    appointment_tree.heading("Time Slot", text="Time Slot", anchor=W)
    appointment_tree.heading("Patient", text="Patient", anchor=W)
    appointment_tree.heading("Status", text="Status", anchor=W)

    appointment_tree.column("Doctor ID", width=75, anchor=W)
    appointment_tree.column("Full Name", width=200, anchor=W)
    appointment_tree.column("Appointment Day", width=110, anchor=W)
    appointment_tree.column("Time Slot", width=100, anchor=W)
    appointment_tree.column("Patient", width=150, anchor=W)
    appointment_tree.column("Status", width=150, anchor=W)

    # Insert appointments data into the Treeview
    for doctor in admin._Admin__doctors:
        for appointment in doctor.get_appointments():
            # Remove canceled appointments completely from the list
            appointment_tree.insert("", "end", values=(
                doctor.get_id(),
                doctor.get_full_name(),
                appointment.get_day(),
                appointment.get_time_slot(),
                appointment.get_patient().get_full_name(),
                appointment.get_status()
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

def search_doctor_form(admin, doctor_window):
    def search_doctor():
        # Get the search text (lowercased for case-insensitive search)
        search_text = entry_search.get().lower()

        # Filter doctors based on ID or Full Name match
        matching_doctors = [
            doctor for doctor in admin._Admin__doctors if
            search_text in doctor.get_full_name().lower() or search_text in str(doctor.get_id())
        ]

        if matching_doctors:
            # Create a new window to display results
            result_window = Toplevel(doctor_window)
            result_window.title("Search Results")
            result_window.geometry("1000x500")  # Increased window size
            result_window.config(bg="#a9ceea")

            Label(result_window, text="Search Results:", bg="#a9ceea", font=("Helvetica", 14, 'bold')).grid(row=0,
                                                                                                            column=0,
                                                                                                            padx=10,
                                                                                                            pady=10,
                                                                                                            sticky=W)
            row = 1

            # Iterate over matching doctors to display full details
            for doctor in matching_doctors:
                doctor_details = f"""
ID: {doctor.get_id()}
Full Name: {doctor.get_full_name()}
Specialty: {doctor.get_specialty()}
Contact: {doctor.get_contact()}
Working Hours: {doctor.get_working_hours()}
"""

                # Display the detailed information
                Label(result_window, text=doctor_details, bg="#a9ceea", justify=LEFT, font=("Helvetica", 10)).grid(
                    row=row, column=0, padx=10, pady=5, sticky=W)
                row += 1

            # Close button for results window
            Button(result_window, text="Close", bg="#164A72", fg="white", width=10, command=result_window.destroy).grid(
                row=row, column=0, pady=20)

        else:
            messagebox.showinfo("No Results", "No doctors found matching the search criteria.")

    # Create the search window to take input for search
    search_window = Toplevel(doctor_window)
    search_window.title("Search Doctor")
    search_window.geometry("250x250")
    search_window.config(bg="#a9ceea")

    Label(search_window, text="Enter ID or Full Name to search:", bg="#a9ceea").grid(row=0, column=0, padx=10, pady=10,
                                                                                     sticky=W)

    entry_search = Entry(search_window, width=30)
    entry_search.grid(row=1, column=0, padx=10, pady=10)

    Button(search_window, text="Search", bg="#164A72", fg="white", width=10, command=search_doctor).grid(row=2,
                                                                                                         columnspan=2,
                                                                                                         pady=20)
    Button(search_window, text="Close", bg="#164A72", fg="white", width=10, command=search_window.destroy).grid(row=3,
                                                                                                                columnspan=2,
                                                                                                                pady=10)


def doctors_window(admin):
    doctor_window = Toplevel()
    doctor_window.title("Doctors")
    doctor_window.state('zoomed')
    bg_colour = "#a9ceea"
    headers_colour = "#164A72"
    doctor_window.config(bg=bg_colour)

    add_doctor = Button(doctor_window, text="Add Doctor", bg=headers_colour, fg=bg_colour, font=("Helvetica", 10),
                        height=1, width=20, command=lambda: add_doctor_form(admin, doctor_window))
    edit_doctor = Button(doctor_window, text="Edit Doctor", bg=headers_colour, fg=bg_colour, font=("Helvetica", 10),
                         height=1, width=20, command=lambda: edit_doctor_form(admin, doctor_window))
    delete_doctor = Button(doctor_window, text="Delete Doctor", bg=headers_colour, fg=bg_colour, font=("Helvetica", 10),
                           height=1, width=20, command=lambda: delete_doctor_form(admin, doctor_window))
    display_doctors = Button(doctor_window, text="Display Doctors", bg=headers_colour, fg=bg_colour,
                             font=("Helvetica", 10), height=1, width=20,
                             command=lambda: display_doctors_form(admin, doctor_window))
    doctors_working_hours = Button(doctor_window, text="View Working Hours", bg=headers_colour, fg=bg_colour,
                                   font=("Helvetica", 10), height=1, width=20,
                                   command=lambda: display_working_hours_form(admin, doctor_window))
    set_working_hours = Button(doctor_window, text="Set Working Hours", bg=headers_colour, fg=bg_colour,
                               font=("Helvetica", 10), height=1, width=20,
                               command=lambda: set_working_hours_form(admin, doctor_window))
    reset_working_hours = Button(doctor_window, text="Reset Working Hours", bg=headers_colour, fg=bg_colour,
                               font=("Helvetica", 10), height=1, width=20,
                               command=lambda: reset_working_hours_form(admin, doctor_window))
    view_appointments = Button(doctor_window, text="View Appointments", bg=headers_colour, fg=bg_colour,
                               font=("Helvetica", 10), height=1, width=20,
                               command=lambda: display_appointments_form(admin, doctor_window))
    search_doctor = Button(doctor_window, text="Search Doctors", bg=headers_colour, fg=bg_colour,
                           font=("Helvetica", 10), height=1, width=20,
                           command=lambda: search_doctor_form(admin, doctor_window))
    exit_menu = Button(doctor_window, text="Exit", bg=headers_colour, fg=bg_colour, font=("Helvetica", 9), height=1,
                       width=5, command=doctor_window.destroy)

    add_doctor.grid(row=1, column=0, padx=550, pady=20)
    edit_doctor.grid(row=2, column=0, padx=100, pady=20)
    delete_doctor.grid(row=3, column=0, padx=100, pady=20)
    display_doctors.grid(row=4, column=0, padx=100, pady=20)
    doctors_working_hours.grid(row=5, column=0, padx=100, pady=20)
    set_working_hours.grid(row=6, column=0, padx=100, pady=20)
    reset_working_hours.grid(row=7, column=0, padx=100, pady=20)
    view_appointments.grid(row=8, column=0, padx=100, pady=20)
    search_doctor.grid(row=9, column=0, padx=100, pady=20)
    exit_menu.grid(row=10, column=0, padx=100, pady=15)
