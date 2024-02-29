import tkinter as tk
from tkinter import ttk
import requests

API_KEY = "a601e7ffa249fa166013d241e59eb7c4"

def get_weather(api_key, location):
    if not location:
        result_var.set("Error: Please enter a location.")
        return

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'  
    }

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if response.status_code == 200:
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            weather_condition = data['weather'][0]['description']

            result_var.set(f"Weather in {location}:\n"
                           f"Temperature: {temperature}°C\n"
                           f"Humidity: {humidity}%\n"
                           f"Weather Condition: {weather_condition}")
        else:
            result_var.set(f"Error: Unable to fetch weather data. {data.get('message', 'Unknown error')}")
    except Exception as e:
        result_var.set(f"Error: {e}")

def get_weather_button_clicked():
    location = location_entry.get()
    get_weather(API_KEY, location)

# Create main window
window = tk.Tk()
window.title("Weather App")

window_width = 400
window_height = 300
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Location
location_label = ttk.Label(window, text="Enter the location (city or ZIP code):")
location_label.grid(row=0, column=0, padx=10, pady=10)
location_var = tk.StringVar()
location_entry = ttk.Entry(window, textvariable=location_var)
location_entry.grid(row=0, column=1, padx=10, pady=10)

# Get Weather Button
get_weather_button = ttk.Button(window, text="Get Weather", command=get_weather_button_clicked)
get_weather_button.grid(row=1, column=0, columnspan=2, pady=10)

# Result
result_var = tk.StringVar()
result_label = ttk.Label(window, textvariable=result_var, wraplength=300, justify="left")
result_label.grid(row=2, column=0, columnspan=2, pady=10)

# Run the GUI
window.mainloop()
