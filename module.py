import os
import board
import digitalio
import busio
from adafruit_bus_device.spi_device import SPIDevice
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

# with busio.SPI(board.SCLK, board.MOSI, board.MISO) as spi_bus:
#     #    cs = digitalio.DigitalInOut(board.D3)
#     device = SPIDevice(spi_bus, digitalio.DigitalInOut(board.C2))
#
#     with device as spi:
#         while(True):
#             spi.write(bytes([REGISTER_DELTA_L,0x01]))
#             result = bytearray(1)
#             spi.readinto(result)
#             # result = spi.read()
#             print(result)
#             break

spi = busio.SPI(board.SCK, MISO=board.MISO, MOSI=board.MOSI)

while True:
    while not spi.try_lock():
         pass
    spi.configure(baudrate=2000000, phase=0, polarity=0)
    sleep(.001)
    chip_select.value = False
    sleep(.001)
    result = bytearray(1)
    resultt = bytearray(1)
    sleep(.001)
    # & 0x7y sets MSB to 0
    spi.write(bytes([0x03 & 0x7f]))
    sleep(.0001)
    spi.readinto(result)
    sleep(.0001)
    spi.write(bytes([0x04 & 0x7f]))
    sleep(.0001)
    spi.readinto(resultt)
    sleep(.001)
    chip_select.value = True
    sleep(.001)
    spi.unlock()
    print(result)
    print(resultt)
