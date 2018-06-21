import numpy as np
import cv2 as cv
import time

class GoBoard:
    img = np.ones((900,900,3),np.uint8)
    img *= 255
    def init(self):
        self.size = 19
        self.img = img

    # 棋盘绘制
    def drawboard(self):
        # img = np.ones((900,900,3),np.uint8)
        # img *= 255

        #draw line
        a = [45*i for i in range(1,20)]
        spots = [(x,y) for x in a for y in a]
        for x in a:
            cv.line(self.img,(x,45),(x,855),(0,0,0),1)
        for y in a:
            cv.line(self.img,(45,y),(855,y),(0,0,0),1)
        #draw star
        star = [(x,y) for x in [45*4,45*10,45*16] for y in [45*4,45*10,45*16]]
        for s in star:
            cv.circle(self.img,s,5,(0,0,0),-1)
        cv.rectangle(self.img,(35,35),(865,865),(100,100,100),4)
        # 坐标绘制
        def draw_coo(string,addr):
            # font                   = cv.FONT_HERSHEY_SIMPLEX
            font                   = cv.FONT_HERSHEY_PLAIN
            fontScale              = 1
            fontColor              = (0,0,0)
            lineType               = 1


            cv.putText(self.img,string,
                addr,
                font,
                fontScale,
                fontColor,
                lineType)
        string_left = [str(i) for i in range(19,0,-1)]
        string_botom = [j for j in 'ABCDEFGHIJKLMNOPQRS']
        addr_left = [(2,y+5) for y in a]
        addr_botom = [(x,898) for x in a]
        string = string_left + string_botom
        addr = addr_left + addr_botom
        for i in range(38):
            draw_coo(string[i],addr[i])

    # 棋子绘制
    def draw_piece(self,col,coo):
        if col == 'b':# black
            col = (0,0,0)
        elif col == 'w':
            col = (250,250,250)
        if len(coo) == 2:
            if coo[0] in '123456789':
                a,b = coo[0],coo[1]
            else:
                a,b = coo[1],coo[0]

        elif len(coo) == 3:
            if coo[0] in '123456789':
                a,b = coo[0:2],coo[2]
            else:
                a,b = coo[1:],coo[0]
        a = (20-int(a))*45
        def index(str):
            lst = [i for i in 'ABCDEFGHIJKLMNOPQRS']
            for i in range(len(lst)):
                if lst[i] == str.upper() or lst[i] == str.lower():
                    n = i+1
            return n
        b = int(index(b))*45


        cv.circle(self.img,(b,a),22,col,-1)
        cv.circle(self.img,(b,a),23,(0,0,0),1)

    # 最后一步棋子绘制
    def draw_last(self,col,coo):
        if col == 'b':# black
            col = (0,0,0)
        elif col == 'w':
            col = (250,250,250)
        if len(coo) == 2:
            if coo[0] in '123456789':
                a,b = coo[0],coo[1]
            else:
                a,b = coo[1],coo[0]

        elif len(coo) == 3:
            if coo[0] in '123456789':
                a,b = coo[0:2],coo[2]
            else:
                a,b = coo[1:],coo[0]
        a = (20-int(a))*45
        def index(str):
            lst = [i for i in 'ABCDEFGHIJKLMNOPQRS']
            for i in range(len(lst)):
                if lst[i] == str.upper() or lst[i] == str.lower():
                    n = i+1
            return n
        b = int(index(b))*45
        m,n = a,b
        dn = 15
        pts = np.array([[m,n+dn],[m-0.866*dn,n-dn/2],[m+0.866*dn,n-dn/2]], np.int32)
        pts = pts.reshape((-1,1,2))
        cv.circle(self.img,(a,b),22,col,-1)
        cv.circle(self.img,(a,b),23,(0,0,0),1)
        cv.fillPoly(self.img,[pts],(0,0,255))

    # 棋盘刷新
    def clear_board(self):
        img = np.ones((900,900,3),np.uint8)
        img *= 255
        self.img = img
        self.drawboard()
        return
    # 棋盘显示
    def show(self,key=1):

        cv.imshow('image',self.img)
        cv.waitKey(key)
