import random
import tkinter as Tk
from itertools import count
import time
import threading

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.style.use('fivethirtyeight')
# values for first graph
x_vals = []
y_vals = []
# values for second graph
y_vals2 = []

index = count()
index2 = count()

ani = None

fig, ax = plt.subplots()

def genValues1():
    while True:
        x_vals.append(next(index))
        y_vals.append(random.randint(0, 5))
        print("generar data")
        time.sleep(1)

def animate(i):
    # Generate values
    #x_vals.append(next(index))
    #y_vals.append(random.randint(0, 5))
    #y_vals2.append(random.randint(0, 5))
    # Get all axes of figure
    # Clear current data
    ax.cla()
    # Plot new data
    ax.plot(x_vals, y_vals)


thread = threading.Thread(target=genValues1, daemon=True)
thread.start()

def on_closing(root):
    root.quit()

def borrar():
    ax.clear()
    x_vals.clear()
    y_vals.clear()
    ax.plot(x_vals, y_vals)
    fig.canvas.draw_idle()

# GUI
root = Tk.Tk()
root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
label = Tk.Label(root, text="Realtime Animated Graphs").grid(column=0, row=0)

# graph 1
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=0, row=1)
# Create two subplots in row 1 and column 1, 2
ani = FuncAnimation(fig, animate, interval=1000, blit=False, cache_frame_data=False)
button = Tk.Button(root, text="Start", command=ani.resume).grid(column=0, row=2)
button2 = Tk.Button(root, text="Stop", command=ani.pause).grid(column=1, row=2)
button3 = Tk.Button(root, text="Clear", command=lambda: borrar()).grid(column=2, row=2)
Tk.mainloop()