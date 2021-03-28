import pyautogui as pg
import csv
import keyboard
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np
import timeit

start_time = timeit.default_timer()
print('Collecting data... Press ESC to quit.')
start_x, start_y = pg.position()
with open('coord.csv', 'w+', newline='') as f:
    writer = csv.writer(f)
    while True:
        x, y = pg.position()
        writer.writerow([timeit.default_timer() - start_time, (x - start_x)/1500])
        if keyboard.is_pressed("esc"):
            break

style.use('ggplot')

x,y = np.loadtxt('coord.csv', unpack = True, delimiter = ',')

plt.plot(x,y)

plt.title('Displacement vs. Time')
plt.ylabel('Displacement in inches')
plt.xlabel('Time elapsed in seconds')



plt.show()
