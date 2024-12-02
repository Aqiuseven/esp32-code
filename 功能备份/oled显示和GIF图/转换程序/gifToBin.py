import os
from PIL import Image


def getPageLen(num: int) -> int:
    temp = num >> 3
    if num & 7:
        return temp + 1
    else:
        return temp


def bmpdecode(filename, file_dir, newname=None, biasY=0, limit=128, log=False, InvertColor=False, delAfterDecode=False):
    f = open(filename, 'rb')
    if f.read(2) == b'BM':
        dummy = f.read(8)
        offset = int.from_bytes(f.read(4), 'little')
        hdrsize = int.from_bytes(f.read(4), 'little')
        width = int.from_bytes(f.read(4), 'little')
        height = int.from_bytes(f.read(4), 'little')
        if int.from_bytes(f.read(2), 'little') == 1:
            depth = int.from_bytes(f.read(2), 'little')
            if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:
                # print("Image size:", width, "x", height)  #  检查生成的图片是否比例正确
                rowsize = (width * 3 + 3) & ~3
                if height < 0:
                    height = -height
                    flip = False
                else:
                    flip = True
                row = 0
                if newname is None:
                    newname = filename[:-4]
                    # 假设 gif_name 是全局变量或已作为参数传递到此函数
                output_dir = f"{file_dir}/"
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                bin_filename = os.path.join(output_dir, os.path.basename(newname) + '.bin')
                buff = open(bin_filename, 'wb+')
                buff.write(b'\x22\x01')
                buff.write(width.to_bytes(2, 'little'))
                buff.write((getPageLen(height) * 8).to_bytes(2, 'little'))
                temp = [0] * width
                temp2 = height - 1 + biasY
                if InvertColor:
                    while row < height:
                        if row != 0 and row % 8 == 0:
                            buff.write(bytearray(temp))
                            temp = [0] * width
                        if flip:
                            pos = offset + (temp2 - row) * rowsize
                        else:
                            pos = offset + (row + biasY) * rowsize
                        if f.tell() != pos:
                            f.seek(pos)
                        col = 0
                        while col < width:
                            bgr = f.read(3)
                            gray = (bgr[2] * 77 + bgr[1] * 151 + bgr[0] * 28) >> 8
                            if gray <= limit:
                                data = 128  # 1<<7
                            else:
                                data = 0
                            temp[col] = (temp[col] >> 1) + data
                            col += 1
                        row += 1
                        if log:
                            print("decoding :%d%%" % (row * 100 // height))
                else:  # 空间换时间 本质一个if
                    while row < height:
                        if row != 0 and row % 8 == 0:
                            buff.write(bytearray(temp))
                            temp = [0] * width
                        if flip:
                            pos = offset + (temp2 - row) * rowsize
                        else:
                            pos = offset + (row + biasY) * rowsize
                        if f.tell() != pos:
                            f.seek(pos)
                        col = 0
                        while col < width:
                            bgr = f.read(3)
                            gray = (bgr[2] * 77 + bgr[1] * 151 + bgr[0] * 28) >> 8
                            if gray > limit:
                                data = 128  # 1<<7
                            else:
                                data = 0
                            temp[col] = (temp[col] >> 1) + data
                            col += 1
                        row += 1
                        if log:
                            print("decoding :%d%%" % (row * 100 // height))
    else:
        raise TypeError("Type not support")
    shift = height % 8
    if shift != 0:
        shift = (8 - shift)
        i = 0
        while i < len(temp):
            temp[i] >>= shift
            i += 1
    buff.write(bytearray(temp))
    f.close()
    buff.close()
    if delAfterDecode:
        os.remove(filename)
    return 0


def process_frame(frame, target_size=(128, 64)):
    if frame.mode == 'RGBA':  # 如果帧是RGBA模式（即包含alpha通道），则需要处理透明度
        background = Image.new('RGB', frame.size, (255, 255, 255))  # 将透明背景设置为白色
        background.paste(frame, mask=frame.split()[3])  # 使用alpha通道作为掩码，将frame粘贴到background上
        frame = background
    elif frame.mode == 'P':  # 处理调色板模式
        frame = frame.convert('RGBA')  # 将调色板模式转换为RGBA模式，以便处理透明度
        background = Image.new('RGB', frame.size, (255, 255, 255))   # 如果是透明gif需要预处理
        background.paste(frame, mask=frame.split()[3])
        frame = background
    frame = frame.convert('L')  # 转换为灰度模式
    original_width, original_height = frame.size  # 获取原始图片大小
    new_frame = Image.new('RGB', target_size, color=(255, 255, 255))  # 创建新的空白图片，背景色设为白色
    x_offset = (target_size[0] - original_width) // 2  # 保证图像居中
    y_offset = (target_size[1] - original_height) // 2
    new_frame.paste(frame, (x_offset, y_offset))  # 将原图粘贴到新图片上
    new_frame = new_frame.convert('1').convert('RGB')  # 先转成1位黑白，再转回24位RGB以保持颜色信息
    return new_frame


def extract_and_convert_gif_frames(gif_path, output_prefix):
    with Image.open(gif_path) as im:
        for i in range(im.n_frames):
            im.seek(i)
            frame = im.copy()
            frame_with_white_bg = process_frame(frame)  # 处理当前帧，设置白色背景
            output_filename = f"{output_prefix}_{i:03d}.bmp"  # 保存当前帧为BMP格式
            frame_with_white_bg.save(output_filename, 'BMP')
            bmpdecode(output_filename, output_prefix, limit=180)  # 生成bin文件
            os.remove(output_filename)  # 删除bmp


if __name__ == '__main__':
    gif_name = input("键入gif名称（只需要名字不需要后缀）：")
    if not os.path.exists(gif_name):
        os.makedirs(gif_name) # 如果目录不存在，则创建
    extract_and_convert_gif_frames(f'{gif_name}.gif', gif_name)
    print(f"文件已生成在{gif_name}文件夹下！")
