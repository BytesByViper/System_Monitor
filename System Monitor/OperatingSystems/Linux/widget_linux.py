import tkinter as tk
import psutil
from tkinter import Canvas

# Get temperature data

def get_cpu_temp():
    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
        if "coretemp" in temps:
            for entry in temps["coretemp"]:
                if "Physical id 0" in entry.label:
                    return entry.current
                
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            temp_str = f.read().strip()
            temp = int(temp_str) / 1000.0 # Converts from centigrade to celsius
            return temp
    except FileNotFoundError:
        return None
    
# Get CPU and RAM data
    
def get_system_info():
    cpu_percent = psutil.cpu_percent(interval=0.5) # Updates every 0.5 seconds
    ram_percent = psutil.virtual_memory().percent
    cpu_temp = get_cpu_temp()
    return cpu_percent, ram_percent, cpu_temp

# Get Disk usage data
def get_disk_usage():
    disk_usage = psutil.disk_usage('/')
    total_space = disk_usage.total / (1024 ** 3)  # Convert bytes to GB
    used_space = disk_usage.used / (1024 ** 3)
    free_space = disk_usage.free / (1024 ** 3)
    return total_space, used_space, free_space

# Status bars

def draw_loading_bar(canvas, x, y, percent, color, background_color):
    # Circle params
    radius = 50
    width = 20
    start_angle = 90 # TODO mirror
    extent = int((360 / 100) * percent)

    canvas.create_arc(x, y, x + 2 * radius, y + 2 * radius, start=start_angle, extent=extent, outline=color, width=width, style=tk.ARC) # Moving bar
    canvas.create_arc(x, y, x + 2 * radius, y + 2 * radius, start=start_angle + extent, extent=360 - extent, outline=background_color, width=width, style=tk.ARC) # Background for bar

# Updating display

def update_display():
    cpu_percent, ram_percent, cpu_temp = get_system_info()
    total, used, free = get_disk_usage()

    # Change CPU Bar Color Based on Percent

    draw_loading_bar(cpu_canvas, 10, 10, cpu_percent, "#40b9ff", "#1f2131")

    if cpu_percent > 40:
        draw_loading_bar(cpu_canvas, 10, 10, cpu_percent, "#b940ff", "#1f2131")

    if cpu_percent > 70:
        draw_loading_bar(cpu_canvas, 10, 10, cpu_percent, "#ff4096", "#1f2131")

    # Change RAM Bar Color Based on Percent

    draw_loading_bar(ram_canvas, 10, 10, ram_percent, "#40b9ff", "#1f2131")

    if ram_percent > 40:
        draw_loading_bar(ram_canvas, 10, 10, ram_percent, "#b940ff", "#1f2131")

    if ram_percent > 70:
        draw_loading_bar(ram_canvas, 10, 10, ram_percent, "#ff4096", "#1f2131")

    # Change temp Bar Color Based on Temp

    draw_loading_bar(temp_canvas, 10, 10, cpu_temp, "#40b9ff", "#1f2131")

    if cpu_temp > 62:
        draw_loading_bar(temp_canvas, 10, 10, cpu_temp, "#b940ff", "#1f2131")

    if cpu_temp > 76:
        draw_loading_bar(temp_canvas, 10, 10, cpu_temp, "#ff4096", "#1f2131")
        
    # Disk Usage Text
    disk_label.config(text=f"Total space: {total:.2f} GB\nUsed space: {used:.2f} GB\nFree space: {free:.2f} GB")
        
    # Text labels

    cpu_usage_label.config(text=f'CPU\nUsage:\n{cpu_percent}%')
    ram_label.config(text=f'RAM\nUsage:\n{ram_percent}%')
    cpu_label.config(text=f"Temp:\n{cpu_temp}°C")

    root.after(1000, update_display)

# Layout

root = tk.Tk()
root.title("System Monitor")

background = Canvas(root, width=200, height=510, background='#18191A', highlightthickness=0)
background.pack()

# Loading bars

cpu_canvas = Canvas(root, width=300, height=600, highlightthickness=0, bg="#18191A")
cpu_canvas.place(x=40, y=20)

ram_canvas = Canvas(root, width=400, height=400, highlightthickness=0, bg="#18191A")
ram_canvas.place(x=40, y=160)

temp_canvas = Canvas(root, width=400, height=400, highlightthickness=0, bg="#18191A")
temp_canvas.place(x=40, y=300)

# Labels

cpu_usage_label = tk.Label(root, text="", font=("Arial", 10), fg="#40b9ff", bg="#18191A")
cpu_usage_label.place(x=78, y=53)

ram_label = tk.Label(root, text="", font=("Arial", 10), fg="#40b9ff", bg="#18191A")
ram_label.place(x=78, y=191)

cpu_label = tk.Label(root, text="", font=("Arial", 10), fg="#40b9ff", bg="#18191A")
cpu_label.place(x=78, y=340)

# Disk usage label
disk_label = tk.Label(root, text="", font=("Arial", 10), fg="#40b9ff", bg="#18191A")
disk_label.place(x=30, y=440)

update_display()
root.mainloop()