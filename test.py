import usb
import usb.util
dev = usb.core.find(idVendor=0x0403, idProduct=0x6014)
print(dev)