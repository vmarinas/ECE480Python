import os
import board
import digitalio
import busio
import csv
import keyboard
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np
import timeit
from time import sleep

# test if enviroment variable is set, if not set BLINKA_FT232H=1 before running
os.environ["BLINKA_FT232H"]

# set interrupt pin high ()
interrupt = digitalio.DigitalInOut(board.C0)
rst = digitalio.DigitalInOut(board.C1)
chip_select = digitalio.DigitalInOut(board.C2)

interrupt.direction = digitalio.Direction.OUTPUT
rst.direction = digitalio.Direction.OUTPUT
chip_select.direction = digitalio.Direction.OUTPUT

# rst.value=False
rst.value=True
sleep(.001)
rst.value=False
sleep(.050)
REGISTER_DELTA_L = 0x00
chip_select.value = True

spi = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# marks the start time of the code
start_time = timeit.default_timer()
# marks the origin of the module
x_pos = 0
y_pos = 0

# set res 12000cpi, default seems to have x y res different
        # | 0x80 sets MSB to 1 for write operations
        # 0x77 denotes full 12000cpi
spi.write(bytes([0x0F | 0x80, 0x77]))

# TODO: double check float precision in the registers
with open('coord_module.csv', 'w+', newline='') as f:
    writer = csv.writer(f)
    while True:
        row = [timeit.default_timer() - start_time, (x_pos) / 1000000, (y_pos) / 1000000]
        while not spi.try_lock():
             pass
        spi.configure(baudrate=2000000, phase=0, polarity=0)
        chip_select.value = False

        # Delta_X LOWORD, lower 2 bytes
        result_x_l = bytearray(1)
        # Delta_X HIWORD, upper 2 bytes
        result_x_h = bytearray(1)
        # Delta_Y LOWORD, lower 2 bytes
        result_y_l = bytearray(1)
        # Delta_Y HIWORD, upper 2 bytes
        result_y_h = bytearray(1)

        # set and read motion bit to freeze values for read
        spi.write(bytes([0x02 | 0x80, 0x01]))
        spi.write(bytes([0x02 & 0x7f]))
        spi.readinto(result_x_l)

        # & 0x7y sets MSB to 0 for read operations
        # read x_l, x_h, y_l, y_h registers
        spi.write(bytes([0x03 & 0x7f]))
        spi.readinto(result_x_l)
        spi.write(bytes([0x04 & 0x7f]))
        spi.readinto(result_x_h)
        spi.write(bytes([0x05 & 0x7f]))
        spi.readinto(result_y_l)
        spi.write(bytes([0x06 & 0x7f]))
        spi.readinto(result_y_h)

        chip_select.value = True
        spi.unlock()

        x=bytearray(2)
        y=bytearray(2)
        x=result_x_h+result_x_l
        y=result_y_h+result_y_l
        x_pos+=int.from_bytes(x,byteorder='little',signed=True)
        y_pos += int.from_bytes(y, byteorder='little', signed=True)

        writer.writerow(row)

        # print count values being read from the Delta_X and Delta_Y registers
        print(int.from_bytes(x,byteorder='little',signed=True),int.from_bytes(y,byteorder='little',signed=True))

        if keyboard.is_pressed("esc"):
            break
    # print(x.decode('utf-16le'),y.decode('utf-16le'))
    # print(resultt)

# todo: make live updating graph
style.use('ggplot')

time,x_displacement,y_displacement = np.loadtxt('coord_module.csv', unpack = True, delimiter = ',')

plt.plot(time, x_displacement, label = "x displacement")
plt.plot(time, y_displacement, label = "y displacement")

# Plotting control data
# Procedure:
# 1) Start code. Wait two seconds.
# 2) Move the dial of the motion stage a 1/4 revolution for two seconds. Then wait for two seconds.
# 3) Repeat step 2 for one revolution
plt.plot([2,4,6,8,10,12,14,16,18],[0,0.00224409,0.00224409,0.00448819, 0.00448819, 0.00673228, 0.00673228, 0.00897638, 0.00897638], label="control data")
# Backup Procedure:
# 1) Start code. Wait two seconds.
# 2) Move the dial of the motion stage a 1/2 revolution for two seconds. Then wait for two seconds.
# 3) Repeat step 2 for one revolution
#plt.plot([0,2,4,6,8,10,12,14,16,18],[0,0,0.00448819,0.00448819,0.00897638, 0.00897638, 0.0134646, 0.0134646, 0.0179528, 0.0179528], label="control data")

plt.title('Displacement vs. Time')
plt.ylabel('Displacement in inches')
plt.xlabel('Time elapsed in seconds')
plt.legend()
plt.show()
