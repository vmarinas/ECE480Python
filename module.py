import os
import board
import digitalio
import busio
#from adafruit_bus_device.spi_device import SPIDevice

# test if enviroment variable is set, if not set BLINKA_FT232H=1 before running
os.environ["BLINKA_FT232H"]

# set interrupt pin high ()
interrupt = digitalio.DigitalInOut(board.C0)
interrupt.direction = digitalio.Direction.INPUT
# interrupt.direction = digitalio.Direction.OUTPUT
# interrupt.value=True

with busio.SPI(board.SCK, board.MOSI, board.MISO) as spi_bus:
#    cs = digitalio.DigitalInOut(board.D3)
#    device = SPIDevice(spi_bus, cs)