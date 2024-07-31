#!/usr/bin/python3
#import gpiod
#import RPi.GPIO as GPIO
import os
from smbus import SMBus
import time

led2 = 19


#os.system("sudo ip link set eth1 down")
#os.system("sudo ip link set dev eth1 address 04:05:06:01:02:DE")
#os.system("sudo ip link set eth1 up")
def detect_model() -> str:
    with open('/proc/device-tree/model') as f:
        model = f.read()
    return model
    
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
	
	print("MAC address read from 24AA02E48 chip : " + mac_str)
	
	cmd_str = 'sudo ip link set dev eth1 address' + mac_str
	print(cmd_str)
	os.system(cmd_str)

# For Raspberry Pi 5
#chip = gpiod.Chip('gpiochip4')
#led_line = chip.get_line(led2)
#led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
#led_line.set_value(1)

# For Raspberry Pi 4
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(led2,GPIO.OUT)
#GPIO.output(led2,True)
    
print(' ')
print('##########################################')	
print('Raspberry Pi 10Base-T1S skpang.co.uk 07/24')
pi_version = detect_model()
print(pi_version)
if pi_version[13] == '5':
	print("Pi 5 detected")
	os.system("sudo insmod microchip_t1s_pi5.ko")
	os.system("sudo insmod lan865x_t1s_pi5.ko")
	import gpiod
	chip = gpiod.Chip('gpiochip4')
	led_line = chip.get_line(led2)
	led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)
	led_line.set_value(1)
	
elif pi_version[13] == '4':
	print("Pi 4 detected")
	os.system("sudo insmod microchip_t1s_pi4.ko")
	os.system("sudo insmod lan865x_t1s_pi4.ko")
	import RPi.GPIO as GPIO
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(led2,GPIO.OUT)
	GPIO.output(led2,True)
else:	
	print("Unknown version of Raspberry Pi, can't continue.")

ip_str = 'sudo ip addr add dev eth1 192.168.5.100/24'
print(ip_str)
os.system(ip_str)
time.sleep(0.1)
os.system("sudo ip link set eth1 down")

get_mac() # Set MAC address
time.sleep(0.1)

os.system('sudo ip link set eth1 up')
time.sleep(0.1)
os.system('sudo ./ethtool --set-plca-cfg eth1 enable on node-id 0 node-cnt 8 to-tmr 0x20 burst-cnt 0x0 burst-tmr 0x80')
os.system('sudo ./ethtool --get-plca-cfg eth1')