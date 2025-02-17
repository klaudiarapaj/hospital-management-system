# admin login is prompted when the program executes
from tkinter import *
from tkinter import messagebox


def verify_login(admin, email_entry, password_entry, login_window,
                 root):  # validates the login credentials before logging in
    email = email_entry.get()  # get the email and password from the entries
    password = password_entry.get()

    if admin.validate_admin(email,
                            password):  # validating the email and password ensuring they match the required values
        login_window.destroy()  # closing the login window once they are logged in
        main_screen(root, admin)  # showing the main screen menu
    else:
        messagebox.showerror("Error", "Invalid login credentials, please try again.")


def admin_login_window(admin, root):  # the login window prompted to the user
    login_window = Toplevel()
    login_window.title("Login")
    login_window.geometry("400x250")
    login_window.configure(bg="#a9ceea")

    # input the email field
    Label(login_window, text="Email:", bg="#a9ceea").grid(row=0, column=0, padx=10, pady=10, sticky=W)
    email_entry = Entry(login_window, width=30)
    email_entry.grid(row=0, column=1, padx=10, pady=10)

    # input the password field
    Label(login_window, text="Password:", bg="#a9ceea").grid(row=1, column=0, padx=10, pady=10, sticky=W)
    password_entry = Entry(login_window, width=30, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    # button to login, calling the verify login function
    login_button = Button(login_window, text="Login", bg="#164A72", fg="white", width=10,
                          command=lambda: verify_login(admin, email_entry, password_entry, login_window, root))
    login_button.grid(row=2, columnspan=2, pady=20)

    close_button = Button(login_window, text="Close", bg="#164A72", fg="white", width=10, command=login_window.quit)
    close_button.grid(row=3, columnspan=2, pady=10)

    login_window.mainloop()


def main_screen(root, admin):  # the main screen of the program
    from View import gui_appointment, gui_billing, gui_doctor, gui_patient

    # initalize the window
    root.title("Hospital Management System")
    root.state('zoomed')
    bg_colour = "#a9ceea"
    headers_colour = "#164A72"
    root.configure(bg=bg_colour)

    welcome = Label(root, text="Welcome to the System!", fg=headers_colour)
    welcome.config(bg=bg_colour)
    welcome.config(font=("Helvetica", 20, "bold"))
    welcome.grid(row=0, column=0, columnspan=4, padx=500, pady=50)

    # buttons for the main functionalities and components
    patients = Button(root, text="Patients", bg=headers_colour, fg=bg_colour, font=("Helvetica", 15), height=2,
                      width=20, command=lambda: gui_patient.patients_window(admin))
    doctors = Button(root, text="Doctors", bg=headers_colour, fg=bg_colour, font=("Helvetica", 15), height=2, width=20,
                     command=lambda: gui_doctor.doctors_window(admin))
    appointments = Button(root, text="Appointments", bg=headers_colour, fg=bg_colour, font=("Helvetica", 15), height=2,
                          width=20, command=lambda: gui_appointment.appointments_window(admin))
    bills = Button(root, text="Bills", bg=headers_colour, fg=bg_colour, font=("Helvetica", 15), height=2, width=20,
                   command=lambda: gui_billing.bills_window(admin))
    exit_menu = Button(root, text="Exit", bg=headers_colour, fg=bg_colour, font=("Helvetica", 10), height=1, width=15,
                       command=root.quit)

    # grid layouts for the buttons
    patients.grid(row=1, column=0, padx=200, pady=50)
    doctors.grid(row=1, column=1)
    appointments.grid(row=2, column=0)
    bills.grid(row=2, column=1)
    exit_menu.grid(row=3, column=0, columnspan=4, pady=200)

    root.mainloop()
