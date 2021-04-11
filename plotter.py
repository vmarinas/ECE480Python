from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np
from matplotlib.animation import FuncAnimation
import pandas as pd

style.use('ggplot')
fig, ax = plt.subplots()
ax.set_xlim(0, 18)
ax.set_ylim(0, 285)
plt.title('Displacement vs. Time')
plt.ylabel('Displacement in microns')
plt.xlabel('Time elapsed in seconds')
plt.plot([0, 2, 4, 6, 8, 10, 12, 14, 16, 18], [0, 0, 57, 57, 114, 114, 171, 171, 228, 228], label="control data")
line1, = ax.plot(0, 0, label="x-displacement")
line2, = ax.plot(0, 0, label="y-displacement")
plt.legend(loc="upper left")

def animate(i):
    data = pd.read_csv('coord_module.csv')
    time = data['time']
    x_displacement = data['x_displacement']
    y_displacement = data['y_displacement']

    line1.set_xdata(time)
    line1.set_ydata(x_displacement)
    line2.set_xdata(time)
    line2.set_ydata(y_displacement)

    return line1, line2,
animation = FuncAnimation(fig, func=animate, frames = np.arange(0,10,0.01), interval=10)
plt.show()





