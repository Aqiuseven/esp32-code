import os
import time

from sprite import BinloaderFile


def get_file_list(file_path):
    """
获取文件夹下所有文件的路径
    :param file_path: 文件夹路径
    :return: 文件夹下所有文件路径
    """
    try:
        file_list = [f'{file_path}/{file_name}' for file_name in os.listdir(file_path)]
        return file_list
    except OSError as e:
        print(e)
        return -1


def gif(display, file_list, delay):
    """
GIF逐帧显示
    :param display: oled 显示设备
    :param file_list: 帧路径
    :param delay: 帧延迟
    """
    for frame in file_list:
        p = BinloaderFile(frame)
        p.draw(display)
        display.show()
        time.sleep(delay)  # 帧延迟
