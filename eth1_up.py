#!/usr/bin/python3
import gpiod
#import RPi.GPIO as GPIO
import os
from smbus import SMBus
import time

led2 = 19


#os.system("sudo ip link set eth1 down")
#os.system("sudo ip link set dev eth1 address 04:05:06:01:02:DE")
#os.system("sudo ip link set eth1 up")

def get_mac():
	mac_str = ' '
	i2cbus = SMBus(1)  # Create a new I2C bus
	i2caddress = 0x50  # Address of device
	i2cbus.write_byte(i2caddress,0xfa)
	a = 0
	a = i2cbus.read_byte(i2caddress)
	mac_str = mac_str + f'{a:x}' + ':'
	
	a = i2cbus.read_byte(i2caddress)
	mac_str = mac_str + f'{a:x}' + ':'

	a = i2cbus.read_byte(i2caddress)
	mac_str = mac_str + f'{a:x}' + ':'

	a = i2cbus.read_byte(i2caddress)
	mac_str = mac_str + f'{a:x}' + ':'

	a = i2cbus.read_byte(i2caddress)
	mac_str = mac_str + f'{a:x}' + ':'
	
	a = i2cbus.read_byte(i2caddress)
	mac_str = mac_str + f'{a:x}' 					
	
	print("MAC address " + mac_str)
	
	cmd_str = 'sudo ip link set dev eth1 address' + mac_str
	print(cmd_str)
	os.system(cmd_str)

# For Raspberry Pi 5
chip = gpiod.Chip('gpiochip4')
led_line = chip.get_line(led2)
led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
led_line.set_value(1)

# For Raspberry Pi 4
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(led2,GPIO.OUT)
#GPIO.output(led2,True)
    
print(' ')
print('##########################################')	
print('Raspberry Pi 10Base-T1S skpang.co.uk 06/24')

os.system("sudo insmod microchip_t1s.ko")
os.system("sudo insmod lan865x_t1s.ko")
#os.system("sudo ip link set eth1 down")

os.system("sudo ip addr add dev eth1 192.168.5.100/24")
get_mac() # Set MAC address
os.system('sudo ip link set eth1 up')

