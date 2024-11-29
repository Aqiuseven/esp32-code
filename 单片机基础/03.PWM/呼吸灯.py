from machine import Pin,PWM
import time

led = PWM(Pin(19,Pin.OUT))
led.freq(1000)

while True:
    for u in range(0,1024) :
        led.duty(u)
        time.sleep_ms(10)
    for d in range(1023,0,-1) :
        led.duty(d)
        time.sleep_ms(10)