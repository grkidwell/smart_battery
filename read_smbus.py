
from smbus2 import SMBus

DEVICE_ADDR=0x0B  #address of the battery

def read_and_scale_register(regname, regaddr):
    def s16(value):   #
        return -(value & 0x8000) | (value & 0x7fff)

    def read_register(regaddr):
        with SMBus(1) as bus:
            bus.write_byte(ADDR,regaddr[0])
            value=bus.read_i2c_block_data(ADDR,regaddr[0],2)
        return value

    def flip_byte_order_2hex(bytearray):
        hexbytearray = ''
        for byte in reversed(bytearray):
            hexbytearray += (format(byte,'x'))
        return s16(int(hexbytearray,16))

    def scale_value(regname,intvalue):
        scalefactor = batreg.scale_dict[regname]
        if regname == 'Temp':
            intvalue = round((intvalue * .1 - 273),2)
        return intvalue*scalefactor

    return scale_value(regname,flip_byte_order_2hex(read_register(regaddr)))

def delay():
    time.sleep(0.2)
    return True

def read_battery_status(batt_addr_dict):
    return {regname: read_and_scale_register(regname, regaddr) for regname, regaddr in batt_addr_dict.items() if delay()}

VOLT=0x09

status = 0x16

reg = 0x19




with SMBus(1) as bus:
    #bus.write_i2c_block_data(DEVICE_ADDR, DMACC1, [register,0x00])
    #value=bus.read_i2c_block_data(DEVICE_ADDR,VOLT,2)
    bus.write_byte(DEVICE_ADDR,reg)
    value=bus.read_i2c_block_data(DEVICE_ADDR,reg,2)
    print(read_battery_status(value))