import numpy as np
import cv2 as cv
from operator import itemgetter
# from goboard import GoBoard
# import time

class GoImage:
    def __init__(self,img,detectboard=[]):

        self.img = img
        if len(detectboard) > 0:
            # self.img = img
            # self.gray = cv.cvtColor(self.img,cv.COLOR_BGR2GRAY)
            # self.edges = self.get_edges()
            # self.contours = self.get_contours()
            # self.lines = self.get_lines()
            # self.filter_contours = self.filter_contours()[0]
            # self.selectlines = self._selectlines()
            self.detectboard = detectboard
        else:
            self.gray = cv.cvtColor(self.img,cv.COLOR_BGR2GRAY)
            self.edges = self.get_edges()
            self.contours = self.get_contours()[0]
            self.lines = self.get_lines()
            # if len(self.filter_contours()) > 0:
            #     self.filter_contours = self.filter_contours()[-1]
            # else:
            #     self.contours = self.get_contours(200)[0]
            #     if len(self.filter_contours()) > 0:
            #         self.filter_contours = self.filter_contours()[-1]
            self.filter_contours = self._filter_contours()
            k = 150
            while not (len(self.filter_contours) > 0):
                k += 160
                self.contours = self.get_contours(k)[0]
                self.filter_contours = self._filter_contours()

            self.selectlines = self._selectlines()
            self.detectboard = self.detectboard()

        self.movelist,  self.lastmove = self.get_movelist()
    def get_edges(self):
        edges = cv.Canny(self.gray,50,150,apertureSize = 3)
        return edges
    # 检测直线
    def get_lines(self):
        newlines = []
        # 弈客检测表现好
        # lines = cv.HoughLinesP(self.edges,1,np.pi/180,100,minLineLength=50,maxLineGap=10)

        # 弈城表现调整
        lines = cv.HoughLinesP(self.edges,1,np.pi/180,100,minLineLength=50,maxLineGap=1)
        for line in lines:
            newlines.append(line[0])
        return newlines
    # 绘制检测到的直线
    def draw_lines(self):
        for line in self.lines:
            # print(line)
            a,b,c,d = line
            cv.line(self.img,(a,b),(c,d),(0,255,255),2)

    # 检测轮廓
    def get_contours(self,k=50):
        # ret, binary = cv.threshold(self.gray,200,255,cv.THRESH_BINARY)
        ret, binary = cv.threshold(self.gray,k,125,cv.THRESH_BINARY)
        # 轮廓检测
        _ ,contours, hierarchy = cv.findContours(binary, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
        return (contours,hierarchy)
    # 过滤轮廓，得到棋盘位置
    def _filter_contours(self):
        filter_contours_list = []
        n = 0
        max_area = 0
        #测试用
        arch = self.get_contours()[1]
        print(arch)
        for i in range(len(self.contours)):
            cnt = self.contours[i]
            M = cv.moments(cnt)
            if M['m00']:
                # cx = int(M['m10']/M['m00'])
                # cy = int(M['m01']/M['m00'])
                # centroids = (cx,cy)
                area = M['m00']
                # 轮廓面积限定
                if 500000 < area < 2880000 :
                    # 作轮廓的最小外接矩形
                    # x,y  矩形左上角坐标 w,h 矩形 宽，高
                    x,y,w,h = cv.boundingRect(self.contours[i])
                    print('size is ok')
                    # print(i,arch)
                    # 判断矩形是否为正方形
                    if abs(int(w)-int(h)) <= 10:
                        n += 1
                        print(area,w,h)
                        # 选择符合条件的最大正方形轮廓
                        if max_area < area:
                            max_area = area
                            filter_contours_list.append(self.contours[i])

        print('filter_contours nums : {} '.format(n))
        return filter_contours_list
    # 绘制轮廓 参数0,-1 选择绘制过滤 或者 全部轮廓
    def draw_contours(self,areas=-1):
        if areas == -1:
            cv.drawContours(self.img,self.contours,-1,(0,0,255),2)
        if areas == 0:
            cv.drawContours(self.img,self.filter_contours,-1,(0,0,255),1)
    # 选择棋盘最外测直线
    def _selectlines(self):

        a,b,c,d = cv.boundingRect(self.filter_contours[-1])
        print(a,b,c,d)

        # 弈客参数调整
        a += 20
        b += 20
        c -= 20
        d -= 20
        selectlines = []
        for line in self.lines:

            x1,y1,x2,y2 = line
            if  a < x1 < a+c-20 and a < x2 < a+c-20 and b < y1 <= b+d-20 and b < y2 < b+d-20 :
                selectlines.append(line)
        return selectlines
    # 绘制直线
    def draw_selectlines(self):
        for line in self.selectlines:
            # print(line)
            a,b,c,d = line
            cv.line(self.img,(a,b),(c,d),(0,255,255),2)


    def _four(self):
        if self.selectlines is not None:
            selectlines = sorted(self.selectlines,key=itemgetter(0))
            a1 = selectlines[0][0]
            a2 = selectlines[-1][0]
            selectlines = sorted(self.selectlines,key=itemgetter(1))
            b1 = selectlines[0][1]
            b2 = selectlines[-1][1]
            return (a1,b1,a2,b2)

    def four_spots(self):
        a1,b1,a2,b2 = self._four()
        tl = (a1,b1)
        tr = (a2,b1)
        bl = (a1,b2)
        br = (a2,b2)
        return tl,tr,bl,br
    # 通过最外测直线的参数计算出棋盘坐标点
    def detectboard(self):

        a1,b1,a2,b2 = self._four()
        print(a1,b1,a2,b2)
        dist =(a2-a1)/18
        detectboard =[]
        for i in range(19):
            detectboard.append([(b1 + dist*i,a1 + dist*j) for j in range(19)])
        return detectboard
    # 绘制棋盘坐标点
    def draw_board_spots(self):
        fb = self.detectboard
        for i in fb:
            for j in i:
                cv.circle(self.img,(int(j[0]),int(j[1])),3,(0,0,255),-1)

    # 棋子颜色信息检测，这个过程问题很多，效果不好，之前尝试过简化，但简化了应对不同的棋盘，会出错。
    def piece_color_val(self,coo):
        if coo:
            pcs1 = self.img[int(coo[0])-10:int(coo[0])-5,int(coo[1])+5:int(coo[1])+10]

            n = 0
            a,b,c = 0,0,0
            for i in pcs1:
                for j in i:
                    n += 1
                    a += int(j[0])
                    b += int(j[1])
                    c += int(j[2])
            pcs2 = self.img[int(coo[0])+5:int(coo[0])+10,int(coo[1])+5:int(coo[1])+10]

            d,e,f = 0,0,0
            for i in pcs2:
                for j in i:
                    d += int(j[0])
                    e += int(j[1])
                    f += int(j[2])
            print(a/n,b/n,c/n,d/n,e/n,f/n)
            return a/n,b/n,c/n,d/n,e/n,f/n
    # 之前用过的颜色分析方式之一，目前没有用到
    def piece_color_anal(self,coo):
        a ,b = int(coo[1]),int(coo[0])
        dist = 10
        cent = a, b
        top = a-dist, b
        left = a, b-dist
        right = a, b+dist
        botom = a+dist, b
        return cent,top,botom,left,right

    # 文字绘制
    def draw_text(self,string,addr):
        # font                   = cv.FONT_HERSHEY_SIMPLEX
        font                   = cv.FONT_HERSHEY_PLAIN
        fontScale              = 0.5
        fontColor              = (0,0,0)
        lineType               = 1
        cv.putText(self.img,string,addr,font,fontScale,fontColor,lineType)
    # 也是之前用过的颜色分析方式，目前无用
    def vag_color(self):

        a1,b1,a2,b2 = self._four()
        pcs = self.gray[b1:b2,a1:a2]
        # pcs = self.img[a1:a2,b1:b2]
        n = 0
        sum = 0
        for i in pcs:
            for j in i:
                n += 1
                sum += int(j)
        if n > 0:
            print('detectboard',sum/n)
            return sum/n
        else:
            print('no detectboard',a1,b1,a2,b2,pcs,self.img)
    # 分析棋盘每个坐标附近的颜色，得到棋盘信息。附加了棋子是否为最后一步的判断，这个过程用时太多，待简化
    def get_movelist(self):
        movelist = []
        lastmove = []
        def parse_coo(i,j):
            x = 19-int(i)
            def gocoo(a):
                lst = 'abcdefghijklmnopqrs'
                return lst[int(a)]
            y = gocoo(j)
            return str(x)+str(y)

        for i in range(19):
            for j in range(19):
                print(i,j)

                item = self.detectboard[i][j]

                a,b,c,d,e,f = self.piece_color_val(item)
                if e -d > 60 and f - d > 60:
                    print('pass',parse_coo(i,j))
                    pass
                else:

                    if d > 150:
                        movelist.append(('w',parse_coo(i,j)))
                        print('w',parse_coo(i,j))

                    if d < 70:
                        movelist.append(('b',parse_coo(i,j)))
                        print('b',parse_coo(i,j))

                    if (d - a > 80 or e - b > 80 or f -c > 80) and d > 150:
                        lastmove.append(('w',parse_coo(i,j)))
                        print('w',parse_coo(i,j))
                    if (a - d < 25 or b - e < 25 or c - f < 25) and d < 120:
                        lastmove.append(('b',parse_coo(i,j)))
                        print('b',parse_coo(i,j))

                        #需要再加黑棋最后的方法
        return movelist,lastmove

    def show(self):
        cv.imshow('goimage',self.img)
        cv.waitKey(0)
