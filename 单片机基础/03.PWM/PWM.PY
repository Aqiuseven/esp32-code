from machine import Pin,PWM

led = PWM(Pin(16,Pin.OUT))
led.freq(1000)
led.duty(512)

led2 = Pin(17,Pin.OUT)
led2.value(1)

while True:
    pass