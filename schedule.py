from PIL import Image, ImageFilter
import numpy as np
from operator import itemgetter 
import os

class ValidTokenException(Exception):
    def __init__(self):
        super(ValidTokenException, self).__init__("ValidTokenException")


class Schedule:
    def __init__(self, filePath):
        try:
            self.filePath = filePath
            self.img = Image.open(filePath) 
            self.pix = np.array(self.img)
            

            self.json = {'월':[],'화':[],'수':[],'목':[],'금':[]}
            self.w, self.h = self.img.size

            self.line_rgb = (0,0,0)
            self.bg_rgb = (0,0,0)
            self.getToImg()
        except:
            raise ValidTokenException
        

    def getToImg(self):

        w, h = self.w, self.h
        
        

        self.bg_rgb, self.line_rgb = self.getRgb()

        x_s, y_s = self.getXYStart()

        
        a, b = self.getPointLine(x_s, y_s)

        self.findBlank(a,b)



        
    def getRgb(self):
        pix = self.pix
        line_rgb_h = 1#int(h/150)
        line_rgb_w = 1#int(w/50)
        
        horizontal = pix[:line_rgb_h]
        hor_unique = np.unique(horizontal.reshape((-1,3)), axis=0, return_counts=True)

        sort_hor_count = np.unique(horizontal.reshape((-1,3)), axis=0, return_counts=True)[1]
        sort_hor_count.sort()

        bg_rgb_idx = np.where(hor_unique[1] == sort_hor_count[-1])[0][0]
        line_rgb_idx = np.where(hor_unique[1] == sort_hor_count[-2])[0][0]

        bg_rgb = hor_unique[0][bg_rgb_idx]
        line_rgb = hor_unique[0][line_rgb_idx] 

        return bg_rgb, line_rgb
    
    def getXYStart(self):
        pix = self.pix
        w, h = self.w, self.h
        line_rgb = self.line_rgb

        x_start = 0
        y_start = 0
            
        for i in range(0,w):
            if (pix[0][i] == line_rgb).all():
                x_start = i
                break;

        for i in range(0,h):
            if(pix[i][0]==line_rgb).all():
                y_start = i
                break;

        return x_start, y_start
    
    def getPointLine(self, x_start, y_start):

        w, h = self.w, self.h
        line_rgb = self.line_rgb
        pix = self.pix

        _cor = 5 # 찾는 보정값

        ew = w - x_start
        eh = h - y_start

        lw = int(ew/10)
        lh = 0
        
        for i in range(y_start+20, h):
            if (pix[i][0] == line_rgb).all() :
                lh = int((i-y_start)/2)+2
                break;
        
        lw_list = [ x_start+ lw*i for i in range(1, int(ew/lw),2)]

        lh_list = [lh]


        
        while(lh_list[-1]+lh+_cor + 30 + y_start < h ):
            tmp_lh = lh
            if len(lh_list) > 1:
                tmp_lh = lh_list[-1]-lh_list[-2]
            
            check_range = [i for i in range(tmp_lh + lh_list[-1] - _cor,tmp_lh + lh_list[-1] + _cor )]

            for i in check_range:
                if (pix[y_start+i][0] == line_rgb).all() :
                    lh_list.append(i)
                    break;
                if (i == check_range[-1]):
                    lh_list.append(lh_list[-1]+tmp_lh)
            
        lh_list = [i + y_start for i in lh_list]

        return lw_list, lh_list

    def findBlank(self,lw_list, lh_list, start_time=9):
        pix = self.pix
        bg_rgb, line_rgb = self.bg_rgb, self.line_rgb
        
        days = ['월','화','수','목','금']
        times = [i for i in np.arange(start_time,24.0,0.5)]

        tests = {'월':[],'화':[],'수':[],'목':[],'금':[]}
        for day,x in enumerate(lw_list):
            for time,y in enumerate(lh_list):
                if (pix[y][x]==bg_rgb).all() or (pix[y][x] == line_rgb).all():
                    tests[days[day]].append(times[time])

        self.json = tests
        
                


    def openImg(self):
        img = Image.fromarray(self.pix)
        img.show()




