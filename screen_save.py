import pyautogui
import time
import threading
import cv2 as cv


class Screen:
    def __init__(self):
        self.addr = '/home/lotus/Documents/execise/opencv/go_detect/last.png'
        self.imglst = []



    def _catch(self,t):
        while True:
            pyautogui.screenshot(self.addr)
            img = cv.imread(self.addr)

            if len(self.imglst) == 0:
                self.imglst.append(img)
            else:
                pass
            time.sleep(t)
    def run(self,t):
        p = threading.Thread(target=self._catch,args=(t,))
        p.start()

if __name__ == '__main__':
    scr = Screen()
    scr.run(3)
