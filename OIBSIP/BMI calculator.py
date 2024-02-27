import tkinter as tk
from tkinter import ttk

def validate_input(action, value_if_allowed):
    return value_if_allowed.replace('.', '', 1).isdigit()

def calculate_bmi():
    weight_str = weight_entry.get()
    height_str = height_entry.get()

    if not weight_str or not height_str:
        result_label.config(text="Please enter both weight and height.")
        return

    weight = float(weight_str)
    height = float(height_str)

    if weight <= 0 or height <= 0:
        result_label.config(text="Weight and height must be positive values.")
        return

    bmi = weight / (height ** 2)
    if not (10 < bmi < 60):
        result_label.config(text="Invalid BMI value calculated.")
        return

    category = classify_bmi(bmi)
    result_label.config(text=f"Your BMI is: {bmi:.2f}\nCategory: {category}")

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obese"

# Create the main window
root = tk.Tk()
root.title("BMI Calculator")

# Set window size and center it on the screen
window_width = 300
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Create and place widgets
weight_label = ttk.Label(root, text="Enter weight (kg):")
weight_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

validate_weight = root.register(validate_input)
weight_entry = ttk.Entry(root, validate="key", validatecommand=(validate_weight, "%d", "%P"))
weight_entry.grid(row=0, column=1, padx=10, pady=10)

height_label = ttk.Label(root, text="Enter height (m):")
height_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

validate_height = root.register(validate_input)
height_entry = ttk.Entry(root, validate="key", validatecommand=(validate_height, "%d", "%P"))
height_entry.grid(row=1, column=1, padx=10, pady=10)

calculate_button = ttk.Button(root, text="Calculate BMI", command=calculate_bmi)
calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

result_label = ttk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=2, pady=10)

# Run the GUI loop
root.mainloop()
