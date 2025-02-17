# main class, handles the initial execution to get the system running
from tkinter import *
from Controller.Admin import Admin  # importing the controller which handles all the logic
from admin_login import admin_login_window  # import login window

# initialize the admin instance whihc is the only user of the system
admin = Admin()
admin.load_data()  # load the saved data in the files

# setting up the root window
root = Tk()
root.title("Hospital Management System")  # name of the system
root.state('zoomed')  # full size for better view
bg_colour = "#a9ceea"  # background colour for all windows
headers_colour = "#164A72"  # colour for all buttons
root.configure(bg=bg_colour)  # configuring the background

# login screen pop up before anything else
admin_login_window(admin, root)

admin.save_data()  # when the system exits, the progrem is saved back to the files
