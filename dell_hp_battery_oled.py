# author: Gary Kidwell
# modified from 'dellbaten.py' program authored by Anthony Alonzo

import time
import battery_registers as batreg
from smbus2 import SMBus
import subprocess
import time, os
import pioled
import RPi.GPIO as GPIO

ADDR = 0X0B #Address of the battery

button = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(button, GPIO.IN,GPIO.PUD_UP)

def button_pressed(channel):
    print("shutting down")
    pioled.display_textlines(["Shutting Down  "])
    os.system("sudo shutdown -h now")
    time.sleep(5)

#button state is interrupt driven and is not polled.
GPIO.add_event_detect(button, GPIO.FALLING,callback=button_pressed,bouncetime=200)

def get_ip_address():
    cmd = "hostname -I | cut -d\' \' -f1"
    return subprocess.check_output(cmd, shell=True).decode("utf-8").rstrip()

def read_register(regaddr,bytecount=2):
    with SMBus(1) as bus:
        bus.write_byte(ADDR,regaddr[0])
        value=bus.read_i2c_block_data(ADDR,regaddr[0],bytecount)
    return value

def enable_dell_battery():
    with SMBus(1) as bus:
        bus.write_i2c_block_data(ADDR,0x00,[0x08,0x00   ])
        value=read_register(batreg.dell_bat_enable['manufacturer access'])
        value=read_register(batreg.dell_bat_enable['manufacturer access'])
        value=read_register(batreg.dell_bat_enable['battery mode'])

def read_and_scale_register(regname, regaddr):
    def s16(value):   #
        return -(value & 0x8000) | (value & 0x7fff)

    def flip_byte_order_2hex(bytearray):
        hexbytearray = ''
        for byte in reversed(bytearray):
            hexbytearray += (format(byte,'x'))
        return s16(int(hexbytearray,16))

    def scale_value(regname,intvalue):
        scalefactor = batreg.scale_dict[regname]
        if regname == 'Temp':
            value = round((intvalue * .1 - 273),2)*scalefactor
        else:
            value = round(intvalue*scalefactor, 3)
        return value

    return scale_value(regname,flip_byte_order_2hex(read_register(regaddr)))

def delay():
    time.sleep(0.2)
    return True

def read_battery_status(batt_addr_dict):
    return {regname: read_and_scale_register(regname, regaddr) for regname, regaddr in batt_addr_dict.items() if delay()}


def main():
    print("starting program")
    pioled.display_textlines(["Starting Up"])
    time.sleep(2)

    while True:
        try:
            enable_dell_battery()
            batt_status_dict = read_battery_status(batreg.abrev_addr_dict)
            print(batt_status_dict)
            print()
            pioled.display_textlines(["Voltage: "+str(batt_status_dict['Volt'])+"   SOC: "+str(batt_status_dict['SOC'])+"%",
                                      "Current: "+str(str(batt_status_dict['Curr']))+"   Temp: "+str(batt_status_dict['Temp'])+"C",
                                      "IP:"+get_ip_address()+ " batterypi"])
        except:
            print("if first you don't succeed.....")
            pioled.display_textlines(["IO Error", "Check I2C wires"])
        time.sleep(1)

if __name__ =="__main__":
    main()