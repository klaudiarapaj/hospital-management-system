# hospital-management-system

The **Hospital Management System** is an application designed to assist with the daily operations of a hospital. This system is intended exclusively for hospital staff—no external users are supported.

## Default Login Credentials

- **Email**: `admin@gmail.com`  
- **Password**: `admin`

## Overview

Once logged in, the user is greeted by a screen with four primary options: **Patients**, **Doctors**, **Appointments**, and **Bills**. Each of these modules has multiple features that integrate with the relevant components.

> ⚠️ All modifications are saved automatically when the system is closed properly. Forcefully terminating the application will result in loss of unsaved changes.

## Architecture

The project follows the **MVC (Model-View-Controller)** architecture:

- **Model**: `Patient`, `Doctor`, `Appointment`, `Billing`  
- **View**: `gui_patient`, `gui_doctor`, `gui_appointment`, `gui_billing`  
- **Controller**: `Admin`

- **Models** define the structure and data of the application.
- **Views** are the graphical interfaces (built with Tkinter) that the user interacts with.
- The **Controller (Admin)** handles all business logic, mediating between models and views.

This modular design simplifies development and maintenance.

## Features

### 1. Patient Management
- Add, edit, or delete patient records with the following details:
  - Full Name  
  - Patient ID  
  - Age  
  - Gender  
  - Address  
  - Contact  
  - Medical Records

### 2. Doctor Management
- Add, edit, or delete doctor details:
  - Full Name  
  - Doctor ID  
  - Specialty  
  - Contact Information  
  - Working Hours

### 3. Appointment Scheduling
- Schedule appointments with details:
  - Date and Time  
  - Patient ID  
  - Doctor ID  
  - Appointment Status (`Scheduled`, `Completed`, `Cancelled`)  
- View, update, cancel, or delete appointments.

### 4. Billing Management
- Generate bills including:
  - Appointment Fees  
  - Procedure/Surgery Fees  
  - Total Payment

### 5. Search and Filter
- Search by:
  - Patients: Name, ID, Contact  
  - Doctors: Name, ID, Specialty  
  - Appointments: ID, Doctor, Patient

### 6. Reports
- Generate reports such as:
  - List of admitted patients  
  - Doctors’ appointments  
  - List of bills

### 7. Data Persistence
- All hospital data is stored in files, ensuring it is preserved across sessions.

### 8. Graphical User Interface (GUI)
- Built with **Tkinter** using:
  - Buttons for navigating modules  
  - Forms and entry fields for data input  
  - Tables/lists for visualizing records

---

**Developed by Klaudia Rapaj for academic purposes.**
