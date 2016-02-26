# coding=utf-8
# 获得每个色块中心处的像素颜色 (r, g, b)
# 获得每个色块中心块的坐标 (x, y)
# 获得每个色块的边长 l 以及间隔处的宽度 d
# 获得一条边上色块的个数 m
# 总色块数: n= m * m
# 图片宽度 wid = m * l + (m - 1) * d
# 图片高度 hei = wid
# wid 已知, m 可以求, l 可以求, d 可以求
import win32api
import win32gui
import win32con
import ctypes
from ImageGrab import grab
from time import sleep

# import win32clipboard as clip

# im = Image.open('test.png')
im = None


def set_window_top():
    hwnd = win32gui.GetForegroundWindow()
    (left, top, right, bottom) = win32gui.GetWindowRect(hwnd)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, left, top, right - left, bottom - top, 0)


def mouse_move((x, y)):
    ctypes.windll.user32.SetCursorPos(x, y)


def mouse_click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def get_position():
    in_status = 1
    out_status = 0
    cur_status = out_status
    pix = im.load()
    width, height = im.size
    sep_count = 0
    sep_all_width = 0
    block_all_width = 0
    for x in range(width):
        if pix[x, 0] == (33, 33, 33):
            sep_all_width += 1
            if cur_status == out_status:
                sep_count += 1
                cur_status = in_status
        elif cur_status == in_status:
            cur_status = out_status
            block_all_width += 1
        else:
            block_all_width += 1
    block_count = sep_count + 1
    sep_width = sep_all_width / sep_count
    block_width = block_all_width / block_count
    std_start_x = std_start_y = block_width / 2
    data_list = []
    for std_x in range(std_start_x, width, block_width + sep_width):
        for std_y in range(std_start_y, width, block_width + sep_width):
            d = Dot((std_x, std_y), im.getpixel((std_x, std_y)))
            data_list.append(d)
    for d in range(-2, len(data_list) - 1):
        if data_list[d].get_rgb() != data_list[d + 1].get_rgb() != \
                data_list[d + 2].get_rgb():
            return data_list[d + 1].get_xy()


class Dot:
    def __init__(self, (x, y), (r, g, b)):
        self.x, self.y = x, y
        self.r, self.g, self.b = r, g, b

    def get_xy(self):
        return self.x, self.y

    def get_rgb(self):
        return self.r, self.g, self.b


def count_down(n):
    for i in range(int(n), 0, -1):
        print u'稍等 %d 秒...' % i
        sleep(1)


def main():
    set_window_top()
    print u'本软件针对 http://cn.vonvon.net/quiz/743 颜色自动找色'
    print u'使用默认偏移量还是手动设置偏移量? y/n\n> ',
    choice = raw_input()
    offset_x, offset_x_r, offset_y, offset_y_r = 0, 0, 0, 0
    if choice == 'y':
        offset_x = 770
        offset_y = 265
        offset_x_r = 1145
        offset_y_r = 640
    elif choice == 'n':
        print u'稍后设置偏移量, 提前将鼠标放置在方块最左上角'
        count_down(3)
        offset_x, offset_y = win32api.GetCursorPos()
        print u'设置偏移量, 将鼠标放在右下角'
        count_down(3)
        offset_x_r, offset_y_r = win32api.GetCursorPos()
        print u'自动寻找色块开始...'
    global im
    count = 50
    while count:
        count -= 1
        im = grab((offset_x, offset_y, offset_x_r, offset_y_r))
        mouse_move([sum(i) for i in zip((offset_x, offset_y), get_position())])
        sleep(0.1)
        mouse_click()
        sleep(0.2)


if __name__ == '__main__':
    main()
