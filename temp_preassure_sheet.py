#!/usr/bin/python
# bmp280.py
# Simple python script to read out the temperature of the
# BMP280 temperature and pressure sensor

import smbus
from time import sleep
import datetime
import time
import datetime
from datetime import date
from openpyxl import load_workbook


# BMP280 I2C address
bmp_addr = 0x77


# Get access to the i2c bus
i2c = smbus.SMBus(1)

# Setup the config register

i2c.write_byte_data(bmp_addr, 0xf5, (0b101<<5))
i2c.write_byte_data(bmp_addr, 0xf4, ((0b101<<5) | (0b111<<2) | (0b11<<0)))

# Sensor is set up and will do a measurement every 1s

dig_T1 = i2c.read_word_data(bmp_addr, 0x88)
dig_T2 = i2c.read_word_data(bmp_addr, 0x8A)
dig_T3 = i2c.read_word_data(bmp_addr, 0x8C)

if(dig_T2 > 32767):
    dig_T2 -= 65536
if(dig_T3 > 32767):
    dig_T3 -= 65536
    
dig_P1 = i2c.read_word_data(bmp_addr, 0x8E)
dig_P2 = i2c.read_word_data(bmp_addr, 0x90)
dig_P3 = i2c.read_word_data(bmp_addr, 0x92)
dig_P4 = i2c.read_word_data(bmp_addr, 0x94)
dig_P5 = i2c.read_word_data(bmp_addr, 0x96)
dig_P6 = i2c.read_word_data(bmp_addr, 0x98)
dig_P7 = i2c.read_word_data(bmp_addr, 0x9A)
dig_P8 = i2c.read_word_data(bmp_addr, 0x9C)
dig_P9 = i2c.read_word_data(bmp_addr, 0x9E)

if(dig_P2 > 32767):
        dig_P2 -= 65536
if(dig_P3 > 32767):
        dig_P3 -= 65536
if(dig_P4 > 32767):
        dig_P4 -= 65536
if(dig_P5 > 32767):
        dig_P5 -= 65536
if(dig_P6 > 32767):
        dig_P6 -= 65536
if(dig_P7 > 32767):
        dig_P7 -= 65536
if(dig_P8 > 32767):
        dig_P8 -= 65536
if(dig_P9 > 32767):
        dig_P9 -= 65536
 


while True:
    
    today = date.today()
    now = datetime.datetime.now().time()
    
# Read the raw temperature
    d1 = i2c.read_byte_data(bmp_addr, 0xfa)
    d2 = i2c.read_byte_data(bmp_addr, 0xfb)
    d3 = i2c.read_byte_data(bmp_addr, 0xfc)
    
    adc_T = ((d1 << 16) | (d2 << 8) | d3) >> 4
    
 # Read the raw preassure   
    d4 = i2c.read_byte_data(bmp_addr, 0xf7)
    d5 = i2c.read_byte_data(bmp_addr, 0xf8)
    d6 = i2c.read_byte_data(bmp_addr, 0xf9)
    
    adc_P = ((d4 << 16) | (d5 << 8) | d6) >> 4


# Calculate temperature
    var1 = ((((adc_T>>3) - (dig_T1<<1))) * (dig_T2)) >> 11;
    var2 = (((((adc_T>>4) - (dig_T1)) * ((adc_T>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14;
    t_fine = var1 + var2;
    T = (t_fine * 5 + 128) >> 8;
    T = T / 100
    
# Calculate preassure
    var1 = (t_fine) - 128000;
    var2 = var1 * var1 * dig_P6;
    var2 = var2 + ((var1 * dig_P5)<<17);
    var2 = var2 + ((dig_P4)<<35);
    var1 = ((var1 * var1 * dig_P3)>>8) + ((var1 * dig_P2)<<12);
    var1 = ((((1)<<47) + var1)) * (dig_P1)>>33;
    
    p = 1048576 - adc_P;
    p = (((p<<31) - var2)*3125)/var1;
    p = int(p);
    var1 = ((dig_P9) * (p>>13) * (p>>13)) >> 25;
    var2 = ((dig_P8) * p) >> 19;
    p = ((p + var1 + var2) >> 8) + ((dig_P7)<<4);
    p = round ((p/256)/100, 1);
 
 
    
    # Save data to /home/ragnar/Documents/weather.xlsx
    # Load the workbook and select the sheet
    wb = load_workbook('/home/ragnar/Documents/weather.xlsx')
    sheet = wb['Sheet1']
    
    # Inform the user!
    print('Adding this data to the spreadsheet')
    print(today)
    print(now)
    print(f"Temperatur: {T} grader Celsius")
    print(f"Tryck: {p:.5} hPa")
    
    #print('{}*C {}hPa'.format(T, p,))
    
    # Append data to the spreadsheet
    row = (today, now, T, p,)
    sheet.append(row)
    
    #Save the workbook
    wb.save('/home/ragnar/Documents/weather.xlsx')
    
    
    sleep(600)
    
    import os
    os.system('clear')

    
#

