import machine

# 创建定时器
timer = machine.Timer(0)

# 创建输出引脚
pin = machine.Pin(18, machine.Pin.OUT)

# 创建 Signal 对象，绑定引脚并设置反转逻辑
signal = machine.Signal(pin, invert=True)

# 定义定时器回调函数
def leds(timer):
    signal.value(not signal.value())  # 反转信号状态

# 启动定时器，周期为 1000 毫秒（1 秒），并设置为周期性触发
timer.init(period=1000, mode=machine.Timer.PERIODIC, callback=leds)

# 保持主程序运行
while True:
    pass