from machine import Pin
import time

button = Pin(18,Pin.IN,Pin.PULL_UP)
led = Pin(17,Pin.OUT)

def callback_led(pin): # 注意需要接收一个回调参数 // [!code highlight]
    time.sleep_ms(200) # 消抖
    led.value(not led.value())

button.irq(callback_led,Pin.IRQ_FALLING)

if __name__ == '__main__':
    while True:
        pass # 这个死循环是保证单片机持续运行
