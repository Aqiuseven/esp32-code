from machine import Pin
import time


LEDS = {
    'LED1' : 19,
    'LED2' : 18,
    'LED3' : 5,
    'LED4' : 17,
    'LED5' : 16
}

LED_List = [Pin(item,Pin.OUT) for item in LEDS.values()]


if __name__ == '__main__':
    while 1:
        for item in  LED_List:
            item.on()
            time.sleep(0.2)
            item.off()