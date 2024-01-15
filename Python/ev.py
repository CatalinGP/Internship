import tkinter as tk


def calculate_vehicle_range(battery_level_percentage):
    total_battery_capacity = 62  # in kWh
    energy_consumption_rate = 15.6  # kWh per 100 km
    current_battery_capacity = (battery_level_percentage / 100) * total_battery_capacity
    available_range = (current_battery_capacity / energy_consumption_rate) * 100  # in km
    return available_range


def on_slider_move(event):
    battery_level = slider.get()
    estimated_range = calculate_vehicle_range(battery_level)
    result_label.config(text=f"Estimated Available Range: {estimated_range:.2f} km")


window = tk.Tk()
window.title("Vehicle Range Calculator")

window_width, window_height = 400, 100
window.resizable(False, False)

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

center_x = int((screen_width / 2) - (window_width / 2))
center_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

slider = tk.Scale(window, from_=0, to=100, orient='horizontal', command=on_slider_move)
slider.pack()

result_label = tk.Label(window, text="Estimated Available Range: ")
result_label.pack()

window.mainloop()
