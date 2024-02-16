"""
240216 main of T-pico_C3 (LilyGo T-PicoC3)
used to summary all the available tool and object file in the folder
for future used

"""

# fmt: off
import machine
from machine import Pin
# the micropython time module
import utime
import rp2
import uos

# default frequency 150MHz
f_now = machine.freq()
machine.freq(250000000)

# this is for the AT command sender interface to ESP32C3
import esp_at_port as esp_c
# the LCD on T-PicoC3
import st7789_tft_obj as tft_c
# the two button on T-PicoC3
import tft_buttons as button_c

# special operation for tft XD
import feather_ex
import scroll_ex
import pinball_ex
import hello_ex
