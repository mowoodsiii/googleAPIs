#!/usr/bin/python
# Example using a character LCD connected to a Raspberry Pi or BeagleBone Black.
import time

import Adafruit_CharLCD as LCD

# LCD Pinout
# Vss | Vdd | Vo  | RS  | R/W | E   | DB0 | DB1 | DB2 | DB3 | DB4 | DB5 | DB6 | DB7 | A   | K   
# GND | 5V  | POT | YEL | GND | GRN | -   | -   | -   | -   | BL1 | BL2 | ORG | WHT | 5V  | GND

# Pi Pinout
# 5V  | 5V  | GND | G14 | G15 | G18 | GND | G23 | G24 | GND | G25 | G8  | ...
# -   | 5V  | GND | WHT | ORG | BL2 | GND | BL1 | GRN | GND | YEL | -   | ...

# Raspberry Pi pin configuration:
lcd_rs        = 25#27  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 24#22
lcd_d4        = 23#25
lcd_d5        = 18#24
lcd_d6        = 15#23
lcd_d7        = 14#18
lcd_backlight = 4

# BeagleBone Black configuration:
# lcd_rs        = 'P8_8'
# lcd_en        = 'P8_10'
# lcd_d4        = 'P8_18'
# lcd_d5        = 'P8_16'
# lcd_d6        = 'P8_14'
# lcd_d7        = 'P8_12'
# lcd_backlight = 'P8_7'

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

# Alternatively specify a 20x4 LCD.
# lcd_columns = 20
# lcd_rows    = 4

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

# Print a two line message
lcd.message('Hello\nworld!')

# Wait 5 seconds
time.sleep(5.0)

# Demo showing the cursor.
lcd.clear()
lcd.show_cursor(True)
lcd.message('Show cursor')

time.sleep(5.0)

# Demo showing the blinking cursor.
lcd.clear()
lcd.blink(True)
lcd.message('Blink cursor')

time.sleep(5.0)

# Stop blinking and showing cursor.
lcd.show_cursor(False)
lcd.blink(False)

# Demo scrolling message right/left.
lcd.clear()
message = 'Scroll'
lcd.message(message)
for i in range(lcd_columns-len(message)):
    time.sleep(0.5)
    lcd.move_right()
for i in range(lcd_columns-len(message)):
    time.sleep(0.5)
    lcd.move_left()

# Demo turning backlight off and on.
lcd.clear()
lcd.message('Flash backlight\nin 5 seconds...')
time.sleep(5.0)
# Turn backlight off.
lcd.set_backlight(0)
time.sleep(2.0)
# Change message.
lcd.clear()
lcd.message('Goodbye!')
# Turn backlight on.
lcd.set_backlight(1)
