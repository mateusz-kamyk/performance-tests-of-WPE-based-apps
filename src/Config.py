import serial

#HDMI GRABBER PORT (/dev/videoX)
HDMI = 4

#DEVICE IP
IP = '10.42.0.251'

###SERIAL CONNECTION
###You have to determine the right port!!! (/dev/ttyUSB)

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate = 115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=0.005
)
