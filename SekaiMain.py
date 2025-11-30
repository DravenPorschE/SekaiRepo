import tkinter as tk
import calendar
from datetime import date

today = date.today()
year = today.year
month = today.month
day = today.day

calendar.setfirstweekday(calendar.SUNDAY)

root = tk.Tk()
root.title("Calendar UI")
root.geometry("600x400")
root.resizable(False, False)
root.configure(bg="white")

# GRID SETUP
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

main = tk.Frame(root, bg="white")
main.grid(row=0, column=0, sticky="nsew")
main.columnconfigure(0, weight=0)  # Fixed width for left panel
main.columnconfigure(1, weight=1)  # Expandable right panel
main.rowconfigure(0, weight=1)

# LEFT PANEL
left = tk.Frame(main, bg="white", highlightbackground="black", highlightthickness=2, width=180)
left.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
left.grid_propagate(False)  # Prevent shrinking

left.rowconfigure(0, weight=1)
left.rowconfigure(1, weight=4)
left.rowconfigure(2, weight=1)
left.columnconfigure(0, weight=1)

weekday_name = today.strftime("%A")
header = tk.Label(left, text=weekday_name, bg="#27ae60", fg="white",
                  font=("Arial", 16, "bold"))
header.grid(row=0, column=0, sticky="nsew")

day_label = tk.Label(left, text=str(day), bg="white", fg="black",
                     font=("Arial", 72, "bold"))
day_label.grid(row=1, column=0, sticky="nsew")

year_label = tk.Label(left, text=str(year), bg="white", fg="red",
                      font=("Arial", 20, "bold"))
year_label.grid(row=2, column=0, sticky="nsew")

# RIGHT PANEL
right = tk.Frame(main, bg="white")
right.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# Spread evenly
for i in range(7):
    right.columnconfigure(i, weight=1, minsize=50)
for i in range(7):
    right.rowconfigure(i, weight=1, minsize=40)

days = ["S", "M", "T", "W", "TH", "F", "S"]
colors = ["red", "gray", "gray", "gray", "gray", "gray", "red"]

# Headers
for i, d in enumerate(days):
    tk.Label(right, text=d, fg=colors[i], bg="white",
             font=("Arial", 14, "bold")).grid(row=0, column=i, sticky="nsew", pady=(0, 5))

month_layout = calendar.monthcalendar(year, month)

# Calendar numbers
row_start = 1
for r, week in enumerate(month_layout):
    for c, num in enumerate(week):
        if num == 0:
            tk.Label(right, text="", bg="white").grid(row=row_start+r, column=c, sticky="nsew")
        elif num == day:
            frame = tk.Frame(right, bg="white", highlightbackground="#27ae60", highlightthickness=2)
            frame.grid(row=row_start+r, column=c, sticky="nsew", padx=3, pady=3)
            tk.Label(frame, text=str(num), bg="white", font=("Arial", 14, "bold")).pack(expand=True)
        else:
            tk.Label(right, text=str(num), bg="white", font=("Arial", 14, "bold")).grid(
                row=row_start+r, column=c, sticky="nsew", padx=3, pady=3
            )

root.mainloop()