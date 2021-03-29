import os
import board
import digitalio
import busio
from adafruit_bus_device.spi_device import SPIDevice

# test if enviroment variable is set, if not set BLINKA_FT232H=1 before running
os.environ["BLINKA_FT232H"]

# set interrupt pin high ()
interrupt = digitalio.DigitalInOut(board.C0)
#interrupt.direction = digitalio.Direction.INPUT
#interrupt.direction = digitalio.Direction.OUTPUT
#interrupt.value=True

A_DEVICE_REGISTER = 0x03

with busio.SPI(board.SCK, board.MOSI, board.MISO) as spi_bus:
    cs = digitalio.DigitalInOut(board.C2)
    cs.direction = digitalio.Direction.OUTPUT
    cs.value = False
    device = SPIDevice(spi_bus, cs)

    with device as spi:
        while(True):
            #spi.write(bytes([A_DEVICE_REGISTER]))
            result = bytearray(4)
            spi.readinto(result)
            print(result)
