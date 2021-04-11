import os
import board
import digitalio
import busio
import csv
import keyboard
import timeit
from time import sleep

# test if environment variable is set, if not set BLINKA_FT232H=1 before running
os.environ["BLINKA_FT232H"]

# Params: val = value in counts, resolution: sensor resolution in cpi
# Returns value in microns
def ConvertCountsToMicrons(val, resolution):
    return val / resolution * 25400


# DigitalInOut: Digital pin support. Define Motion/Interrupt, Reset, and Chip Select pins on motion sensor
# # w/ pins on breakout board. Defaults to input.
# Motion/Interrupt: signals the breakout board when motion has occurred. Active low
interrupt = digitalio.DigitalInOut(board.C0)
# Reset: chip reset. Active low
rst = digitalio.DigitalInOut(board.C1)
# Chip select (active low)
chip_select = digitalio.DigitalInOut(board.C2)

# Change direction of pins (input or output)
interrupt.direction = digitalio.Direction.OUTPUT
rst.direction = digitalio.Direction.OUTPUT
chip_select.direction = digitalio.Direction.OUTPUT

# Reset motion sensor
rst.value = True
sleep(.001)
rst.value = False
sleep(.050)
chip_select.value = True

# busio: Hardware accelerated external bus access, use for write and readinto
spi = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI)

# Marks the start time of the code
start_time = timeit.default_timer()
# Marks the origin of the module
x_pos = 0
y_pos = 0

# List of register values on the motion sensor
REGISTER_CONFIG1 = 0x0F  # sensor resolution in cpi
REGISTER_MOTION = 0x02  # used to determine if motion has occurred since the last time it was read
REGISTER_DELTA_X_L = 0x03  # X movement in counts since last report, lower 8 bits
REGISTER_DELTA_X_H = 0x04  # X movement in counts since last report, upper 8 bits
REGISTER_DELTA_Y_L = 0x05  # Y movement in counts since last report, lower 8 bits
REGISTER_DELTA_Y_H = 0x06  # Y movement in counts since last report, upper 8 bits

# Set motion sensor resolution to 12000cpi, default 5000 cpi
# | 0x80 sets MSB to 1, required for write operations
# 0x77 sets resolution 12000cpi as denoted by data sheet
spi.write(bytes([REGISTER_CONFIG1 | 0x80, 0x77]))

# TODO: double check float precision in the registers

fieldnames = ["time", "x_displacement", "y_displacement"]

# Overwrite new or existing csv file
with open('coord_module.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

while True:
    # Pass until SPI device is locked
    while not spi.try_lock():
        pass
    # Configure the SPI bus
    # baudrate: serial port clock frequency in Hz
    # phase: edge of the clock that data is captured. First edge = 0, second edge = 1
    # polarity: the base state of clock line
    spi.configure(baudrate=2000000, phase=0, polarity=0)
    # Active serial port
    chip_select.value = False

    # Each result will hold one byte of data read from their corresponding motion registers
    result_motion = bytearray(1) # Motion
    result_x_l = bytearray(1)  # Delta_X_L
    result_x_h = bytearray(1)  # Delta_X_H
    result_y_l = bytearray(1)  # Delta_Y_L
    result_y_h = bytearray(1)  # Delta_Y_H

    # Start procedure to read motion register data
    # Write any value to the Motion register
    spi.write(bytes([REGISTER_MOTION | 0x80, 0x01]))
    # Read the Motion register. This freezes the Delta X/Y register values
    spi.write(bytes([REGISTER_MOTION & 0x7f]))
    spi.readinto(result_motion)

    # Read the Delta_X_L register. Store byte
    spi.write(bytes([REGISTER_DELTA_X_L & 0x7f]))
    spi.readinto(result_x_l)
    # Read the Delta_X_H register. Store byte
    spi.write(bytes([REGISTER_DELTA_X_H & 0x7f]))
    spi.readinto(result_x_h)
    # Read the Delta_Y_L register. Store byte
    spi.write(bytes([REGISTER_DELTA_Y_L & 0x7f]))
    spi.readinto(result_y_l)
    # Read the Delta_Y_H register. Store byte
    spi.write(bytes([REGISTER_DELTA_Y_H & 0x7f]))
    spi.readinto(result_y_h)

    # Transactions complete
    chip_select.value = True
    spi.unlock()

    # Combine LOWORD and HIWORD bytes into a single array
    x = bytearray(2)
    y = bytearray(2)
    x = result_x_h + result_x_l
    y = result_y_h + result_y_l

    # Convert bytes to a count value
    x_pos += int.from_bytes(x, byteorder='little', signed=True)
    y_pos += int.from_bytes(y, byteorder='little', signed=True)

    # Write new row in the csv file. Time elapsed, x-displacement in microns, y-displacement in microns
    with open('coord_module.csv', 'a') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        info = {
            "time": timeit.default_timer() - start_time,
            "x_displacement": ConvertCountsToMicrons(x_pos, 1000000),
            "y_displacement": ConvertCountsToMicrons(y_pos, 1000000)
        }
        writer.writerow(info)

    # print count values being read from the Delta_X and Delta_Y registers
    print(int.from_bytes(x, byteorder='little', signed=True), int.from_bytes(y, byteorder='little', signed=True))

    # Press ESC key to break loop
    if keyboard.is_pressed("esc"):
        break
'''
# Old plotting code
# Plot the captured data
style.use('ggplot')

time, x_displacement, y_displacement = np.loadtxt('coord_module.csv', unpack = True, delimiter = ',')

plt.plot(time, x_displacement, label = "x displacement")
plt.plot(time, y_displacement, label = "y displacement")

# Plotting control data
# Procedure:
# 1) Start code. Wait two seconds.
# 2) Move the dial of the motion stage a 1/4 revolution for two seconds. Then wait for two seconds.
# 3) Repeat step 2 for one revolution
plt.plot([0, 2, 4, 6, 8, 10, 12, 14, 16, 18], [0, 0, 57, 57, 114, 114, 171, 171, 228, 228], label="control data")

plt.title('Displacement vs. Time')
plt.ylabel('Displacement in microns')
plt.xlabel('Time elapsed in seconds')
plt.legend()
plt.show()
'''
