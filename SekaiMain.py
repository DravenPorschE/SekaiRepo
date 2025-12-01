import tkinter as tk
from tkinter import PhotoImage
import calendar
from datetime import date
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
import threading
import random
import os

today = date.today()
year = today.year
month = today.month
day = today.day

timesClicked = 0
isClicking = False

# ----------------------------
# LED Setup
# ----------------------------
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# ----------------------------
# I2C Setup for ADS1115
# ----------------------------
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# ----------------------------
# FSR on channel 0 (A0)
# ----------------------------
chan = AnalogIn(ads, 0)

# ----------------------------
# Threshold to detect touch
# ----------------------------
THRESHOLD = 100

calendar.setfirstweekday(calendar.SUNDAY)

root = tk.Tk()
root.title("Calendar UI")

# Set fixed screen size
screen_width = 480
screen_height = 320
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, False)
root.configure(bg="white")

# Current view state
current_view = "calendar"

# GRID SETUP
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

# Container for all views
container = tk.Frame(root, bg="white")
container.grid(row=0, column=0, sticky="nsew")
container.rowconfigure(0, weight=1)
container.columnconfigure(0, weight=1)

# CALENDAR VIEW FRAME
calendar_frame = tk.Frame(container, bg="white")
calendar_frame.grid(row=0, column=0, sticky="nsew")
calendar_frame.columnconfigure(0, weight=0)
calendar_frame.columnconfigure(1, weight=1)
calendar_frame.rowconfigure(0, weight=1)

# SMILING FIGURE VIEW FRAME
smile_frame = tk.Frame(container, bg="white")
smile_frame.rowconfigure(0, weight=1)
smile_frame.columnconfigure(0, weight=1)

# WEATHER VIEW FRAME
weather_frame = tk.Frame(container, bg="white")
weather_frame.rowconfigure(0, weight=1)
weather_frame.columnconfigure(0, weight=1)
weather_frame.columnconfigure(1, weight=1)

# Create smiling figure using canvas
canvas = tk.Canvas(smile_frame, bg="white", highlightthickness=0)
canvas.grid(row=0, column=0, sticky="nsew")

def draw_smile():
    canvas.delete("all")
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    
    if w <= 1 or h <= 1:
        canvas.after(100, draw_smile)
        return
    
    size = min(w, h) * 0.6
    cx, cy = w // 2, h // 2
    
    # Face circle (yellow)
    canvas.create_oval(cx - size//2, cy - size//2, cx + size//2, cy + size//2, 
                      fill="#FFD700", outline="black", width=3)
    
    # Eyes
    eye_y = cy - size//6
    eye_offset = size//5
    eye_size = size//12
    # Left eye
    canvas.create_oval(cx - eye_offset - eye_size, eye_y - eye_size,
                      cx - eye_offset + eye_size, eye_y + eye_size,
                      fill="black")
    # Right eye
    canvas.create_oval(cx + eye_offset - eye_size, eye_y - eye_size,
                      cx + eye_offset + eye_size, eye_y + eye_size,
                      fill="black")
    
    # Smile (arc)
    mouth_y = cy + size//8
    mouth_width = size//3
    canvas.create_arc(cx - mouth_width, mouth_y - size//8,
                     cx + mouth_width, mouth_y + size//4,
                     start=0, extent=-180, style=tk.ARC, width=3)

canvas.bind("<Configure>", lambda e: draw_smile())

# Weather data (test data matching your image)
weather_data = {
    "current": {
        "day": "Monday",
        "time": "1:40pm",
        "temp": "34 C",
        "location": "Lipa City",
        "icon": "partly_cloudy_weather.png"
    },
    "forecast": [
        {"day": "Tuesday", "time": "1:40pm", "temp": "37C", "icon": "partly_cloudy_weather.png"},
        {"day": "Wednesday", "time": "1:40pm", "temp": "37C", "icon": "sunny_weather.png"},
        {"day": "Thursday", "time": "1:40pm", "temp": "37C", "icon": "thunderstorm_weather.png"},
        {"day": "Friday", "time": "1:40pm", "temp": "37C", "icon": "cloudy_weather.png"}
    ]
}

# Function to load weather icon
def load_weather_icon(icon_name, size=(80, 80)):
    try:
        from PIL import Image, ImageTk
        img_path = os.path.join("weather_assets", icon_name)
        img = Image.open(img_path)
        img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading icon {icon_name}: {e}")
        return None

# Build weather view
def build_weather_view():
    # Left panel - Current weather
    left_weather = tk.Frame(weather_frame, bg="#f0f0f0", highlightbackground="gray", highlightthickness=1)
    left_weather.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    # Day and time
    tk.Label(left_weather, text=f"{weather_data['current']['day']} {weather_data['current']['time']}", 
             bg="#f0f0f0", font=("Arial", 14), anchor="w").pack(pady=(10, 5), padx=10, fill="x")
    
    # Weather icon
    icon_current = load_weather_icon(weather_data['current']['icon'], (120, 120))
    if icon_current:
        icon_label = tk.Label(left_weather, image=icon_current, bg="#f0f0f0")
        icon_label.image = icon_current  # Keep reference
        icon_label.pack(pady=10)
    
    # Temperature
    tk.Label(left_weather, text=weather_data['current']['temp'], 
             bg="#f0f0f0", font=("Arial", 32, "bold")).pack(pady=5)
    
    # Location
    tk.Label(left_weather, text=weather_data['current']['location'], 
             bg="#f0f0f0", font=("Arial", 16)).pack(pady=(5, 10))
    
    # Right panel - Forecast
    right_weather = tk.Frame(weather_frame, bg="white")
    right_weather.grid(row=0, column=1, sticky="nsew", padx=(0, 10), pady=10)
    
    for idx, forecast in enumerate(weather_data['forecast']):
        forecast_card = tk.Frame(right_weather, bg="#f0f0f0", highlightbackground="gray", highlightthickness=1)
        forecast_card.pack(fill="x", pady=5, padx=5)
        
        # Create inner frame for icon and text
        inner = tk.Frame(forecast_card, bg="#f0f0f0")
        inner.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Icon on the left
        icon = load_weather_icon(forecast['icon'], (40, 40))
        if icon:
            icon_lbl = tk.Label(inner, image=icon, bg="#f0f0f0")
            icon_lbl.image = icon  # Keep reference
            icon_lbl.pack(side="left", padx=(0, 10))
        
        # Text on the right
        text_frame = tk.Frame(inner, bg="#f0f0f0")
        text_frame.pack(side="left", fill="both", expand=True)
        
        tk.Label(text_frame, text=forecast['day'], bg="#f0f0f0", 
                font=("Arial", 12, "bold"), anchor="w").pack(fill="x")
        tk.Label(text_frame, text=f"{forecast['time']} - {forecast['temp']}", 
                bg="#f0f0f0", font=("Arial", 10), anchor="w").pack(fill="x")

# LEFT PANEL (Calendar view)
left_width = int(screen_width * 0.35)
left = tk.Frame(calendar_frame, bg="white", highlightbackground="black", highlightthickness=2, width=left_width)
left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
left.grid_propagate(False)

left.rowconfigure(0, weight=1)
left.rowconfigure(1, weight=4)
left.rowconfigure(2, weight=1)
left.columnconfigure(0, weight=1)

weekday_name = today.strftime("%A")
header = tk.Label(left, text=weekday_name, bg="#27ae60", fg="white",
                  font=("Arial", max(int(left_width*0.08), 12), "bold"))
header.grid(row=0, column=0, sticky="nsew")

day_label = tk.Label(left, text=str(day), bg="white", fg="black",
                     font=("Arial", max(int(left_width*0.3), 36), "bold"))
day_label.grid(row=1, column=0, sticky="nsew")

year_label = tk.Label(left, text=str(year), bg="white", fg="red",
                      font=("Arial", max(int(left_width*0.07), 14), "bold"))
year_label.grid(row=2, column=0, sticky="nsew")

# RIGHT PANEL (Calendar view)
right = tk.Frame(calendar_frame, bg="white")
right.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

cols = 7
rows = 7
for i in range(cols):
    right.columnconfigure(i, weight=1)
for i in range(rows):
    right.rowconfigure(i, weight=1)

days = ["S", "M", "T", "W", "TH", "F", "S"]
colors = ["red", "gray", "gray", "gray", "gray", "gray", "red"]

# Headers
for i, d in enumerate(days):
    tk.Label(right, text=d, fg=colors[i], bg="white",
             font=("Arial", max(int(screen_width*0.02), 10), "bold")).grid(row=0, column=i, sticky="nsew", pady=(0, 2))

month_layout = calendar.monthcalendar(year, month)

# Calendar numbers
row_start = 1
for r, week in enumerate(month_layout):
    for c, num in enumerate(week):
        if num == 0:
            tk.Label(right, text="", bg="white").grid(row=row_start+r, column=c, sticky="nsew")
        elif num == day:
            frame = tk.Frame(right, bg="white", highlightbackground="#27ae60", highlightthickness=1)
            frame.grid(row=row_start+r, column=c, sticky="nsew", padx=1, pady=1)
            tk.Label(frame, text=str(num), bg="white", font=("Arial", max(int(screen_width*0.02), 10), "bold")).pack(expand=True)
        else:
            tk.Label(right, text=str(num), bg="white", font=("Arial", max(int(screen_width*0.02), 10), "bold")).grid(
                row=row_start+r, column=c, sticky="nsew", padx=1, pady=1
            )

# Build weather view
build_weather_view()

# View switching functions
def show_calendar():
    global current_view
    current_view = "calendar"
    smile_frame.grid_remove()
    weather_frame.grid_remove()
    calendar_frame.grid(row=0, column=0, sticky="nsew")
    root.title("Calendar UI")

def show_smile():
    global current_view
    current_view = "smile"
    calendar_frame.grid_remove()
    weather_frame.grid_remove()
    smile_frame.grid(row=0, column=0, sticky="nsew")
    set_mood("happy")  # Default to happy when showing smile
    root.title("Sekai is listening...")

def show_weather():
    global current_view
    current_view = "weather"
    calendar_frame.grid_remove()
    smile_frame.grid_remove()
    weather_frame.grid(row=0, column=0, sticky="nsew")
    root.title("Weather")

def switch_view(event):
    key = event.char.lower()
    if key == 'a':
        show_calendar()
    elif key == 'b':
        show_smile()
    elif key == 'c':
        show_weather()
    elif key == 'q':
        cleanup_and_quit()

def cleanup_and_quit():
    GPIO.cleanup()
    root.destroy()

# Bind keys
root.bind('<Key>', switch_view)

# FSR monitoring function
def monitor_fsr():
    global timesClicked, isClicking
    
    while True:
        try:
            fsr_value = chan.value

            if fsr_value > THRESHOLD and not isClicking:
                isClicking = True
                timesClicked += 1
                
                if timesClicked == 2:
                    print("Sekai is awake, say a command")

                    # Determine emotion
                    emotion = random.choices(
                        ["happy", "angry"],
                        weights=[9, 1]
                    )[0]

                    # Switch to smile view first
                    if current_view != "smile":
                        root.after(0, show_smile)
                    
                    # Set the mood based on emotion
                    root.after(100, lambda e=emotion: set_mood(e))
                    
                    # Turn on LED
                    GPIO.output(LED_PIN, GPIO.HIGH)
                    timesClicked = 0

                    if emotion == "happy":
                        audio_folder = "voices_happy"
                        print("Sekai is happy!")
                    else:
                        audio_folder = "voices_angry"
                        print("Sekai is angry!")

                    # Pick a random file inside that folder
                    files = os.listdir(audio_folder)
                    audioToPlay = os.path.join(audio_folder, random.choice(files))

                    # Play through USB headphones
                    os.system(f"aplay -D plughw:1,0 {audioToPlay}")
                    
                    # Wait 5 seconds then turn off LED (but keep smile)
                    time.sleep(5)
                    GPIO.output(LED_PIN, GPIO.LOW)
                    print("Sekai stopped listening")
                    isClicking = False
            else:
                isClicking = False
                GPIO.output(LED_PIN, GPIO.LOW)

            time.sleep(0.1)
            
        except Exception as e:
            print(f"FSR Error: {e}")
            time.sleep(0.1)

# Start FSR monitoring in separate thread
fsr_thread = threading.Thread(target=monitor_fsr, daemon=True)
fsr_thread.start()

# Start inactivity checker
check_inactivity()

# Start with weather view to test the design
show_weather()

# Handle window close
root.protocol("WM_DELETE_WINDOW", cleanup_and_quit)

try:
    root.mainloop()
except KeyboardInterrupt:
    cleanup_and_quit()