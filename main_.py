# this is the main of T-pico_C3

import machine
import utime

# ===== the only LDE on PICO, reserve for LED
led = machine.Pin(25, machine.Pin.OUT)

state0 = 0
led.value(0)
while 1:
    led.value(state0)
    utime.sleep_ms(500)

    if state0 == 0:
        state0 = 1
    else:
        state0 = 0
