import threading
import itertools
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time


iterador = itertools.count()


x = []
y = []

fig, ax = plt.subplots()

def modificarVector():
    try:
        while True:
            x.append(next(iterador))
            y.append(random.randint(0,5))
            print("se cambian los vectores\n {},{}", x,y)
            time.sleep(0.5)
    except:
        pass


def animate(i):
    ax.cla()
    ax.plot(x,y)



changeThread = threading.Thread(target=modificarVector, daemon=True)
changeThread.start()

ani = FuncAnimation(fig, animate, interval = 1000, blit=False)
plt.show()





