import datetime
import pandas as pd
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


# Suppress FutureWarnings
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Global variables
employees = {'Alex': {'housekeeping': None, 'bfast': None, 'dinner': None},
             'Niicola': {'housekeeping': None, 'bfast': None, 'dinner': None},
             'Wendie': {'housekeeping': None, 'bfast': None, 'dinner': None},
             'Isabel': {'housekeeping': None, 'bfast': None, 'dinner': None},
             'Taylor': {'housekeeping': None, 'bfast': None, 'dinner': None}}


def get_time_of_day():
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "morning"
    elif 12 <= current_hour < 17:
        return "afternoon"
    elif 17 <= current_hour < 20:
        return "evening"
    else:
        return "night"

def greet_user(name):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    time_of_day = get_time_of_day()

    return f"Good {time_of_day}, {name}! Today is {current_date} and the time is {current_time}."

def save_to_excel(name, job_role, sign_in_time, sign_out_time, hours_worked):
    file_path = os.path.join(os.path.expanduser('~'), 'Documents', 'employee_data.xlsx')

    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Check if the file exists; if not, create it with the header
        if not os.path.isfile(file_path):
            df = pd.DataFrame(columns=['Name', 'Job Role', 'Sign In Time', 'Sign Out Time', 'Total Hours Worked'])
            df.to_excel(file_path, index=False)

        df = pd.read_excel(file_path)

        # Append new data to the existing sheet
        new_data = {
            'Name': name,
            'Job Role': job_role,
            'Sign In Time': sign_in_time.strftime('%Y-%m-%d %H:%M:%S') if sign_in_time is not None else None,
            'Sign Out Time': sign_out_time.strftime('%Y-%m-%d %H:%M:%S') if sign_out_time is not None else None,
            'Total Hours Worked': hours_worked
        }
        df = df.append(new_data, ignore_index=True)

        # Save the updated DataFrame to the same sheet
        df.to_excel(file_path, index=False)
        return "Data saved to Excel."
    except Exception as e:
        return f"Error saving data to Excel: {e}"

def sign_in_out_helper(employee_name, job_role, action):
    if employee_name in employees and job_role in employees[employee_name]:
        if employees[employee_name][job_role] is not None:
            # If the user has already signed in
            if action == 'Sign Out':
                # Display confirmation dialog
                confirm = messagebox.askyesno("Confirmation", f"Do you want to sign out {employee_name} from {job_role} duty?")
                if confirm:
                    sign_out_time = datetime.datetime.now()
                    hours_worked = (sign_out_time - employees[employee_name][job_role]['sign_in']).seconds / 3600
                    employees[employee_name][job_role]['sign_out'] = sign_out_time
                    result = f"{employee_name}, you have successfully signed out from {job_role} duty. Total hours worked: {hours_worked:.2f} hours"
                    result += "\n" + save_to_excel(employee_name, job_role, employees[employee_name][job_role]['sign_in'], sign_out_time, hours_worked)
                    result_text.set(result)
                    result_label.config(foreground='green', font=('Helvetica', 12, 'bold'))
                    
                    # Update last sign-out time
                    last_sign_out_time = employees[employee_name][job_role]['sign_out'].strftime('%Y-%m-%d %H:%M:%S')
                    last_time_var.set(f"Last Sign-Out Time: {last_sign_out_time}")
                else:
                    result_text.set("")  # Clear the result text
            else:
                result = f"Welcome back, {employee_name}! You are already signed in for {job_role} duty."
                result_text.set(result)
                result_label.config(foreground='black', font=('Helvetica', 12, 'normal'))

                # Update last sign-in time
                last_sign_in_time = employees[employee_name][job_role]['sign_in'].strftime('%Y-%m-%d %H:%M:%S')
                last_time_var.set(f"Last Sign-In Time: {last_sign_in_time}")
        else:
            # If the user hasn't signed in yet
            sign_in_time = datetime.datetime.now()
            employees[employee_name][job_role] = {'sign_in': sign_in_time, 'sign_out': None}
            result = f"{employee_name}, you have successfully signed in for {job_role} duty."
            result_text.set(result)
            result_label.config(foreground='black', font=('Helvetica', 12, 'normal'))

            # Update last sign-in time
            last_sign_in_time = employees[employee_name][job_role]['sign_in'].strftime('%Y-%m-%d %H:%M:%S')
            last_time_var.set(f"Last Sign-In Time: {last_sign_in_time}")
    else:
        result = "Invalid employee name or job role. Please enter a valid name and job role."
        result_text.set(result)
        result_label.config(foreground='red', font=('Helvetica', 12, 'bold'))

    update_log()
    return result

def update_log():
    log_text.delete(1.0, tk.END)
    for employee_name, duties in employees.items():
        for job_role, times in duties.items():
            if times:
                log_text.insert(tk.END, f"{employee_name} - {job_role} duty: ")
                log_text.insert(tk.END, f"Sign In Time: {times['sign_in'].strftime('%Y-%m-%d %H:%M:%S')}, ")
                if times['sign_out']:
                    log_text.insert(tk.END, f"Sign Out Time: {times['sign_out'].strftime('%Y-%m-%d %H:%M:%S')}\n")
                else:
                    log_text.insert(tk.END, "Not signed out yet\n")
                log_text.insert(tk.END, "\n")

def update_clock():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    clock_label.config(text=f"Current Time: {current_time}\nCurrent Date: {current_date}")
    root.after(1000, update_clock)

def clear_log():
    log_text.delete(1.0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Employee Sign-In/Sign-Out System")

style = ttk.Style()
style.theme_use("clam")  # Use the "clam" theme

# Additional styling options if needed
style.configure("TFrame", background="white")
style.configure("TLabel", background="white", foreground="black", font=('Helvetica', 12))
style.configure("TButton", background="green", foreground="red", font=('Helvetica', 12))


# Clock Label
clock_label = ttk.Label(root, text="")
clock_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="ew")

# Employee Section
employee_frame = ttk.LabelFrame(root, text="Employee Details", style="TFrame")
employee_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Last Sign-In/Sign-Out Time
last_time_label = ttk.Label(employee_frame, text="Last Sign-In/Out Time:", style="TLabel")
last_time_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
last_time_var = tk.StringVar()
last_time_display = ttk.Label(employee_frame, textvariable=last_time_var, style="TLabel")
last_time_display.grid(row=3, column=1, padx=10, pady=5, sticky="w")

# Employee Name Dropdown
name_label = ttk.Label(employee_frame, text="Employee Name:", style="TLabel")
name_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
name_var = tk.StringVar()
name_combobox = ttk.Combobox(employee_frame, textvariable=name_var, values=list(employees.keys()), state="readonly", font=('Helvetica', 12))
name_combobox.grid(row=4, column=1, padx=10, pady=5, sticky="w")

# Job Role Dropdown
job_role_label = ttk.Label(employee_frame, text="Job Role:", style="TLabel")
job_role_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
job_role_var = tk.StringVar()
job_role_combobox = ttk.Combobox(employee_frame, textvariable=job_role_var, values=['housekeeping', 'bfast', 'dinner'], state="readonly", font=('Helvetica', 12))
job_role_combobox.grid(row=5, column=1, padx=10, pady=5, sticky="w")

# Action (Sign In/Sign Out) Dropdown
action_label = ttk.Label(employee_frame, text="Action:", style="TLabel")
action_label.grid(row=6, column=0, padx=10, pady=5, sticky="w")
action_var = tk.StringVar()
action_var.set("Sign In")
action_menu = ttk.Combobox(employee_frame, textvariable=action_var, values=["Sign In", "Sign Out"], state="readonly", font=('Helvetica', 12))
action_menu.grid(row=6, column=1, padx=10, pady=5, sticky="w")

# Submit Button
submit_button = ttk.Button(employee_frame, text="Submit", command=lambda: sign_in_out_helper(name_var.get(), job_role_var.get(), action_var.get()), style="TButton")
submit_button.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

# Log Section
log_frame = ttk.LabelFrame(root, text="Log", style="TFrame")
log_frame.grid(row=8, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Log Display
log_text = tk.Text(log_frame, height=10, width=40, wrap=tk.WORD)
log_text.grid(row=0, column=0, pady=5, padx=10, sticky="w")

# Clear Log Button
clear_log_button = ttk.Button(log_frame, text="Clear Log", command=clear_log, style="TButton")
clear_log_button.grid(row=1, column=0, pady=5, padx=10, sticky="w")

# Result
result_text = tk.StringVar()
result_label = ttk.Label(root, textvariable=result_text, wraplength=400, foreground='black', font=('Helvetica', 12, 'normal'))
result_label.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# Initialize Clock and Log
update_clock()
update_log()

root.mainloop()
