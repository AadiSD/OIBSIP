import random
import string
import tkinter as tk
from tkinter import ttk

MAX_PASSWORD_LENGTH = 50  # Set the maximum password length

def generate_password(length, use_letters, use_numbers, use_symbols):
    characters = ""

    character_sets = {
        'letters': string.ascii_letters,
        'numbers': string.digits,
        'symbols': string.punctuation
    }

    selected_sets = [name for name, selected in zip(character_sets.keys(), [use_letters, use_numbers, use_symbols]) if selected]

    if not selected_sets:
        return "Error: Please select at least one character type."

    for character_set in selected_sets:
        characters += character_sets[character_set]

    if length < 8:
        return "Error: Password length must be at least 8 characters for security."

    if length > MAX_PASSWORD_LENGTH:
        return f"Error: Password length exceeds the maximum limit of {MAX_PASSWORD_LENGTH} characters."

    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def generate_button_clicked():
    length = int(length_var.get())
    use_letters = letters_var.get()
    use_numbers = numbers_var.get()
    use_symbols = symbols_var.get()

    password = generate_password(length, use_letters, use_numbers, use_symbols)

    result_var.set(f"Generated Password: {password}")

# Create main window
window = tk.Tk()
window.title("Password Generator")

# Set window size and center on screen
window_width = 500
window_height = 300
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Password Length
length_label = ttk.Label(window, text="Password Length:")
length_label.grid(row=0, column=0, padx=10, pady=10)
length_var = tk.StringVar()
length_entry = ttk.Entry(window, textvariable=length_var)
length_entry.grid(row=0, column=1, padx=10, pady=10)

# Character Types
letters_var = tk.BooleanVar()
letters_checkbox = ttk.Checkbutton(window, text="Include Letters", variable=letters_var)
letters_checkbox.grid(row=1, column=0, padx=10, pady=5, sticky="W")

numbers_var = tk.BooleanVar()
numbers_checkbox = ttk.Checkbutton(window, text="Include Numbers", variable=numbers_var)
numbers_checkbox.grid(row=2, column=0, padx=10, pady=5, sticky="W")

symbols_var = tk.BooleanVar()
symbols_checkbox = ttk.Checkbutton(window, text="Include Symbols", variable=symbols_var)
symbols_checkbox.grid(row=3, column=0, padx=10, pady=5, sticky="W")

# Generate Button
generate_button = ttk.Button(window, text="Generate Password", command=generate_button_clicked)
generate_button.grid(row=4, column=0, columnspan=2, pady=10)

# Result
result_var = tk.StringVar()
result_label = ttk.Label(window, textvariable=result_var)
result_label.grid(row=5, column=0, columnspan=2, pady=10)

# Run the GUI
window.mainloop()
