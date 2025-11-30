import tkinter as tk
import calendar
from datetime import date
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO

# ----------------------------
# Setup
# ----------------------------
today = date.today()
year, month, day = today.year, today.month, today.day

# LED Setup
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

# I2C Setup for ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# FSR on channel 0 (A0)
chan = AnalogIn(ads, 0)
THRESHOLD = 100  # Adjust after testing FSR

# Calendar settings
calendar.setfirstweekday(calendar.SUNDAY)

# ----------------------------
# Tkinter setup
# ----------------------------
root = tk.Tk()
root.title("Calendar UI")
screen_width = 480
screen_height = 320
root.geometry(f"{screen_width}x{screen_height}")
root.resizable(False, False)
root.configure(bg="white")

current_view = "calendar"

# Container frame
container = tk.Frame(root, bg="white")
container.grid(row=0, column=0, sticky="nsew")
container.rowconfigure(0, weight=1)
container.columnconfigure(0, weight=1)

# ----------------------------
# Calendar Frame
# ----------------------------
calendar_frame = tk.Frame(container, bg="white")
calendar_frame.grid(row=0, column=0, sticky="nsew")
calendar_frame.columnconfigure(0, weight=0)
calendar_frame.columnconfigure(1, weight=1)
calendar_frame.rowconfigure(0, weight=1)

# Left panel
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

# Right panel
right = tk.Frame(calendar_frame, bg="white")
right.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
cols, rows = 7, 7
for i in range(cols):
    right.columnconfigure(i, weight=1)
for i in range(rows):
    right.rowconfigure(i, weight=1)

days = ["S", "M", "T", "W", "TH", "F", "S"]
colors = ["red", "gray", "gray", "gray", "gray", "gray", "red"]

# Headers
for i, d in enumerate(days):
    tk.Label(right, text=d, fg=colors[i], bg="white",
             font=("Arial", max(int(screen_width*0.02), 10), "bold")).grid(row=0, column=i, sticky="nsew", pady=(0,2))

month_layout = calendar.monthcalendar(year, month)
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

# ----------------------------
# Smile Frame
# ----------------------------
smile_frame = tk.Frame(container, bg="white")
smile_frame.rowconfigure(0, weight=1)
smile_frame.columnconfigure(0, weight=1)

canvas = tk.Canvas(smile_frame, bg="white", highlightthickness=0)
canvas.grid(row=0, column=0, sticky="nsew")

def draw_smile():
    canvas.delete("all")
    w = canvas.winfo_width()
    h = canvas.winfo_height()
    if w <= 1 or h <= 1:
        canvas.after(100, draw_smile)
        return
    size = min(w,h)*0.6
    cx, cy = w//2, h//2
    canvas.create_oval(cx-size//2, cy-size//2, cx+size//2, cy+size//2, fill="#FFD700", outline="black", width=3)
    eye_y = cy - size//6
    eye_offset = size//5
    eye_size = size//12
    canvas.create_oval(cx-eye_offset-eye_size, eye_y-eye_size, cx-eye_offset+eye_size, eye_y+eye_size, fill="black")
    canvas.create_oval(cx+eye_offset-eye_size, eye_y-eye_size, cx+eye_offset+eye_size, eye_y+eye_size, fill="black")
    mouth_y = cy + size//8
    mouth_width = size//3
    canvas.create_arc(cx-mouth_width, mouth_y-size//8, cx+mouth_width, mouth_y+size//4,
                      start=0, extent=-180, style=tk.ARC, width=3)

canvas.bind("<Configure>", lambda e: draw_smile())
canvas.bind("<Double-Button-1>", lambda e: show_smile())

# ----------------------------
# View switching functions
# ----------------------------
def show_calendar():
    global current_view
    current_view = "calendar"
    smile_frame.grid_remove()
    calendar_frame.grid(row=0, column=0, sticky="nsew")
    root.title("Calendar UI - Press 'b' for smile")

def show_smile(event=None):
    global current_view
    current_view = "smile"
    calendar_frame.grid_remove()
    smile_frame.grid(row=0, column=0, sticky="nsew")
    draw_smile()
    root.title("Smile View - Press 'a' for calendar")

def switch_view(event):
    key = event.char.lower()
    if key == 'a':
        show_calendar()
    elif key == 'b':
        show_smile()
    elif key == 'q':
        root.destroy()

root.bind('<Key>', switch_view)

# Start with calendar view
show_calendar()

# ----------------------------
# FSR polling using after()
# ----------------------------
timesClicked = 0
isClicking = False

def poll_fsr():
    global timesClicked, isClicking
    fsr_value = chan.value
    if fsr_value > THRESHOLD and not isClicking:
        isClicking = True
        timesClicked += 1
        if timesClicked == 2:
            print("Sekai is awake, say a command")
            GPIO.output(LED_PIN, GPIO.HIGH)
            timesClicked = 0
            root.after(5000, lambda: GPIO.output(LED_PIN, GPIO.LOW))
            print("Sekai stopped listening")
    else:
        isClicking = False
        GPIO.output(LED_PIN, GPIO.LOW)
    root.after(100, poll_fsr)

poll_fsr()  # start polling

# Run Tkinter main loop
try:
    root.mainloop()
finally:
    GPIO.cleanup()
