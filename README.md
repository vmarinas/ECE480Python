# Low Cost Python DIC Module Code
## Installation and Setup
1. [project uses pycharm, download here if you do not have it](https://www.jetbrains.com/pycharm/)
3. [setup for ft232h usb bridge with circuitpy](https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h)
4. [post install checks](https://learn.adafruit.com/circuitpython-on-any-computer-with-ft232h/troubleshooting)
5. [create a new virtual enviroment in pycharm if existing does not work](https://www.jetbrains.com/help/pycharm/creating-virtual-environment.html)
6. [install missing packages for your enviroment/interpreter](https://www.jetbrains.com/help/pycharm/installing-uninstalling-and-upgrading-packages.html#interpreter-settings)
    * Adafruit-Blinka	6.4.1
    * Adafruit-PlatformDetect	3.4.1
    * Adafruit-PureIO	1.1.8
    * MouseInfo	0.1.3
    * Pillow	8.1.2
    * PyAutoGUI	0.9.52
    * PyGetWindow	0.0.9
    * PyMsgBox	1.0.9
    * PyRect	0.1.4
    * PyScreeze	0.1.26
    * PyTweening	1.0.3
    * adafruit-circuitpython-busdevice	5.0.6
    * cycler	0.10.0
    * keyboard	0.13.5
    * kiwisolver	1.3.1
    * matplotlib	3.3.4
    * numpy	1.20.1
    * pandas	1.2.4
    * pip	21.0.1
    * pyftdi	0.52.9
    * pyparsing	2.4.7
    * pyperclip	1.8.2
    * pyserial	3.5
    * python-dateutil	2.8.1
    * pytz	2021.1
    * pyusb	1.1.1
    * setuptools	54.1.2
    * six	1.15.0

### Files
1. CoordModule.txt is the csv logfile
2. Module.py is the main file
3. Plotter contains realtime plotting code
4. Test.py - post install check test

#### Running Code
   * Terminates and graphs when you hit escape button
   * To run realtime plotter and module.py run in terminal
   ```
    set BLINKA_FT232H=1
    start python module.py & start python plotter.py
   ```
   * Windows requires use of zadig every time usb port is changed as windows automatically overwrites driver
   ** this is not required for linux and osx
   * To run static plot/graph on escape (plot without launching the seperate realtime plotting file) comment out plotting code in module.py and add in required imports from plotter.py(matplotlib, pandas, numpy)

##### Datasheets
   * [XY displacement sensor](https://d3s5r33r268y59.cloudfront.net/datasheets/9604/2017-05-07-18-19-11/PMS0058-PMW3360DM-T2QU-DS-R1.50-26092016._20161202173741.pdf)
   `ALL REGISTER ADDRESSES ARE ON PAGE 29 IN A TABLE. REFERENCE THIS`
   * [adafruit USB-SPI bus](https://www.adafruit.com/product/2264?gclid=Cj0KCQiAs5eCBhCBARIsAEhk4r4Gve8tj7aJNjhQgQO9qX7yfBwBulwKgRsjbuX3YjJ2OURq-_z2lv0aAmEMEALw_wcB)
   * [FT232H](https://ftdichip.com/wp-content/uploads/2020/07/DS_FT232H.pdf)
