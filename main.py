from goboard import GoBoard
import time
from goImage import GoImage
from screen_save import Screen
import cv2 as cv
import numpy as np


# 主进程，调用各个类，方便测试效果，最后的 go.show() 如果参数改为 go.show(1) 可循环运行。有时弹出的命令窗口会挡住棋盘，出现错误，需要调优，暂时双屏不影响。
scr = Screen()
scr.run(0.01)
detectboard = []
while True:
    while True:
        if len(scr.imglst) > 0 :
            img = scr.imglst.pop()
            break

    # gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    # iTmp = np.ones((img.shape),dtype=int)*255
    # a = iTmp - img
    # print(a)
    # cv.imshow('test',gray)
    # cv.waitKey(0)
    goImg = GoImage(img,detectboard)
    detectboard = goImg.detectboard
    # vag_color = goImg.v_col
    #
    # goImg.draw_contours()
    # # # goImg.draw_lines()
    # # # goImg.draw_selectlines()
    # # # goImg.draw_board_spots()
    # goImg.show()
    go = GoBoard()
    go.clear_board()
    print(goImg.lastmove)
    for a,b in goImg.movelist:
        go.draw_piece(a,b)
    # for a,b in goImg.lastmove:
    #     go.draw_last(a,b)
    # goImg.show()
    go.show(0)
