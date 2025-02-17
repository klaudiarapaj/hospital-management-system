from tkinter import *
from tkinter import messagebox, ttk


def generate_bill_form(admin, bills_window):
    def calculate_total():
        # Calculate the total amount
        try:
            appointment_fee = float(entry_appointment_fee.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid appointment fee.")
            return

        try:
            procedures = [
                (procedure.split(":")[0].strip(), float(procedure.split(":")[1].strip()))
                for procedure in text_procedures.get("1.0", END).strip().split("\n") if procedure
            ]
        except (IndexError, ValueError):
            messagebox.showerror("Error", "Ensure procedures are in 'Procedure Name: Charge' format.")
            return

        total = appointment_fee + sum(charge for _, charge in procedures)
        label_total.config(text=f"Total: ${total:.2f}")

    def save_bill():
        # Save the bill
        try:
            appointment_fee = float(entry_appointment_fee.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid appointment fee.")
            return

        try:
            procedures = [
                (procedure.split(":")[0].strip(), float(procedure.split(":")[1].strip()))
                for procedure in text_procedures.get("1.0", END).strip().split("\n") if procedure
            ]
        except (IndexError, ValueError):
            messagebox.showerror("Error", "Ensure procedures are in 'Procedure Name: Charge' format.")
            return

        patient_name = patient_dropdown.get()
        if not patient_name:
            messagebox.showerror("Error", "Please select a patient.")
            return

        patient = next((p for p in admin._Admin__patients if p.get_full_name() == patient_name), None)
        if not patient:
            messagebox.showerror("Error", "Selected patient not found.")
            return

        try:
            admin.add_bill(patient, appointment_fee, procedures)
            messagebox.showinfo("Success", f"Bill generated and saved for {patient_name}.")
            generate_bill_form.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    # Create the billing form
    generate_bill_form = Toplevel(bills_window)
    generate_bill_form.title("Generate Bill")
    generate_bill_form.geometry("600x500")
    bg_colour = "#a9ceea"
    generate_bill_form.config(bg=bg_colour)

    Label(generate_bill_form, text="Select Patient:", bg=bg_colour).grid(row=0, column=0, padx=10, pady=10)
    patients = [patient.get_full_name() for patient in admin._Admin__patients]
    patient_dropdown = ttk.Combobox(generate_bill_form, values=patients)
    patient_dropdown.grid(row=0, column=1, padx=10, pady=10)

    Label(generate_bill_form, text="Appointment Fee:", bg=bg_colour).grid(row=1, column=0, padx=10, pady=10)
    entry_appointment_fee = Entry(generate_bill_form, width=23)
    entry_appointment_fee.grid(row=1, column=1, padx=10, pady=10)

    Label(generate_bill_form, text="Procedures (name:charge):", bg=bg_colour).grid(row=2, column=0, padx=10, pady=10)
    text_procedures = Text(generate_bill_form, height=10, width=40)
    text_procedures.grid(row=2, column=1, padx=10, pady=10)

    label_total = Label(generate_bill_form, text="Total: $0.00", bg=bg_colour, font=("Helvetica", 12))
    label_total.grid(row=3, column=1, columnspan=1, pady=20)

    calculate_button = Button(generate_bill_form, text="Calculate", bg="#28a745", fg="white", width=15,
                              command=calculate_total)
    calculate_button.grid(row=3, column=0, pady=10, padx=10)

    save_button = Button(generate_bill_form, text="Save", bg="#164A72", fg="white", width=15, command=save_bill)
    save_button.grid(row=4, column=0, pady=10, padx=10)

    close_button = Button(generate_bill_form, text="Close", bg="#FF5733", fg="white", width=15,
                          command=generate_bill_form.destroy)
    close_button.grid(row=5, column=0, pady=20)

def display_bills_form(admin, bills_window):
    display_window = Toplevel(bills_window)
    display_window.title("View All Bills")
    display_window.geometry("800x400")
    display_window.config(bg="#a9ceea")

    # Define columns for the display
    columns = ("Bill ID", "Patient Name", "Appointment Fee", "Procedures", "Total Amount")

    # Create a treeview to display bills
    bill_tree = ttk.Treeview(display_window, columns=columns, show="headings")

    # Define column headings and their width
    bill_tree.heading("Bill ID", text="Bill ID", anchor=W)
    bill_tree.heading("Patient Name", text="Patient Name", anchor=W)
    bill_tree.heading("Appointment Fee", text="Appointment Fee", anchor=W)
    bill_tree.heading("Procedures", text="Procedures", anchor=W)
    bill_tree.heading("Total Amount", text="Total Amount", anchor=W)

    bill_tree.column("Bill ID", width=75, anchor=W)
    bill_tree.column("Patient Name", width=200, anchor=W)
    bill_tree.column("Appointment Fee", width=100, anchor=W)
    bill_tree.column("Procedures", width=200, anchor=W)
    bill_tree.column("Total Amount", width=100, anchor=W)

    bill_tree.grid(row=1, column=0, padx=10, pady=20)

    # Populate treeview with bills data
    for bill in admin._Admin__bills:
        bill.calculate_total()  # Ensure total is updated

        procedures_str = ", ".join([f"{procedure}: ${charge:.2f}" for procedure, charge in bill.get_procedures()])

        bill_tree.insert("", "end", values=(
            bill.get_id(),
            bill.get_patient().get_full_name(),
            f"${bill.get_appointment_fee():.2f}",
            procedures_str,
            f"${bill.get_total_amount():.2f}"
        ))

    # Close button for the display window
    Button(display_window, text="Close", bg="#164A72", fg="white", width=10, command=display_window.destroy).grid(
        row=2, columnspan=5, pady=20)

def search_bill_form(admin, bills_window):
    def search_bill():
        # Get the search text (lowercased for case-insensitive search)
        search_text = entry_search.get().lower()

        # Filter bills based on Patient's full name or Bill ID match
        matching_bills = [
            bill for bill in admin._Admin__bills if
            search_text in bill.get_patient().get_full_name().lower() or search_text in str(bill.get_id())
        ]

        if matching_bills:
            # Create a new window to display results
            result_window = Toplevel(bills_window)
            result_window.title("Search Results")
            result_window.geometry("1000x500")  # Increased window size
            result_window.config(bg="#a9ceea")

            Label(result_window, text="Search Results:", bg="#a9ceea", font=("Helvetica", 14, 'bold')).grid(row=0, column=0,
                                                                                                            padx=10, pady=10, sticky=W)
            row = 1

            # Iterate over matching bills to display full details
            for bill in matching_bills:
                bill.calculate_total()  # Ensure the total is up to date
                bill_details = f"""
Bill ID: {bill.get_id()}
Patient Name: {bill.get_patient().get_full_name()}
Appointment Fee: ${bill.get_appointment_fee():.2f}
Procedures:
"""
                for procedure, charge in bill.get_procedures():
                    bill_details += f"  - {procedure}: ${charge:.2f}\n"

                bill_details += f"Total Amount: ${bill.get_total_amount():.2f}"

                # Display the detailed information
                Label(result_window, text=bill_details, bg="#a9ceea", justify=LEFT, font=("Helvetica", 10)).grid(
                    row=row, column=0, padx=10, pady=5, sticky=W)
                row += 1

            # Close button for results window
            Button(result_window, text="Close", bg="#164A72", fg="white", width=10, command=result_window.destroy).grid(
                row=row, column=0, pady=20)

        else:
            messagebox.showinfo("No Results", "No bills found matching the search criteria.")

    # Create the search window to take input for search
    search_window = Toplevel(bills_window)
    search_window.title("Search Bill")
    search_window.geometry("300x200")
    search_window.config(bg="#a9ceea")

    Label(search_window, text="Enter Bill ID or Patient Name to search:", bg="#a9ceea").grid(row=0, column=0, padx=10, pady=10, sticky=W)

    entry_search = Entry(search_window, width=30)
    entry_search.grid(row=1, column=0, padx=10, pady=10)

    Button(search_window, text="Search", bg="#164A72", fg="white", width=10, command=search_bill).grid(row=2, columnspan=2, pady=20)
    Button(search_window, text="Close", bg="#164A72", fg="white", width=10, command=search_window.destroy).grid(row=3, columnspan=2, pady=10)

def bills_window(admin):

    bills_window = Toplevel()
    bills_window.title("Patients")
    bills_window.state('zoomed')
    bg_colour = "#a9ceea"
    headers_colour = "#164A72"
    bills_window.config(bg=bg_colour)

    generate_bill = Button(bills_window, text="Generate Bill", bg=headers_colour, fg=bg_colour, font=("Helvetica", 10), height=2, width=20, command=lambda:generate_bill_form(admin, bills_window))
    display_bills = Button(bills_window, text="Display Bills", bg=headers_colour, fg=bg_colour, font=("Helvetica", 10), height=2, width=20, command=lambda:display_bills_form(admin, bills_window))
    search_bills = Button(bills_window, text="Search Bills", bg=headers_colour, fg=bg_colour, font=("Helvetica", 10), height=2, width=20, command=lambda:search_bill_form(admin, bills_window))
    exit_menu= Button(bills_window, text="Exit", bg=headers_colour, fg=bg_colour, font=("Helvetica", 10), height=1, width=5, command=bills_window.destroy)

    generate_bill.grid(row=1, column=0, padx=550, pady=50)
    display_bills.grid(row=2, column=0, padx=100, pady=50)
    search_bills.grid(row=3, column=0, padx=100, pady=50)
    exit_menu.grid(row=4, column=0, padx=100, pady=160)