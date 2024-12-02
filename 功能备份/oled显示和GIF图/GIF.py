'''
* gif显示示例
'''
from machine import I2C, Pin
from sh1106 import SH1106_I2C
import tools

# 初始化I2C和显示器
i2c = I2C(scl=Pin(22), sda=Pin(21))
display = SH1106_I2C(128, 64, i2c, rotate=180)


if __name__ == '__main__':
    file_list = tools.get_file_list('ch4n')
    while True :
        tools.gif(display,file_list,0.1)

