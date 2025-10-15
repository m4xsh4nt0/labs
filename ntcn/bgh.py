import numpy as np
from math import cos,sin,pi,sqrt
from PIL import Image ,ImageOps
img_mat = np.zeros((4000,4000,3),dtype=np.uint8)
# for i in range(1120):
#     for j in range(1080):
#         img_mat[i,j] = [(i+j)%256,0,0]
def dotted_line(self, image, x0, y0, x1, y1, count, color):
    step = 1.0/count
    for t in np.arange(0, 1, step):
        x = round ((1.0-t)*x0 + t*x1)
        y = round ((1.0-t)*y0 + t*y1)
    image[y, x] = color

def drawline(self, x0, y0, x1, y1, color):

    count = sqrt((x0 -x1)**2 + (y0 -y1)**2)
    step = 1.0/count
    for t in np.arange(0, 1, step):
        x = round ((1.0-t)*x0 + t*x1)
        y = round ((1.0-t)*y0 + t*y1)
        self[y, x] = color

def x_loop_line1(self, x0, y0, x1, y1, color):
    if (x0 > x1):#без этой штуки будет только правая часть звезды
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    for x in range (x0, x1):
        t = (x-x0)/(x1 -x0)
        y = round ((1.0-t)*y0 + t*y1)
        self[y, x] = color

def x_loop_line2(self, x0, y0, x1, y1, color):
    xchange = False
    if (abs(x0-x1) < abs(y0 -y1)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if (x0 > x1):#без этой штуки будет только правая часть звезды
        x0, x1 = x1, x0
        y0, y1 = y1, y0    
    for x in range (x0, x1):
        t = (x-x0)/(x1 -x0)
        y = round ((1.0-t)*y0 + t*y1)
        if (xchange):
            self[x, y] = color
        else:
            self[y, x] = color

def x_loop_line3(self, x0, y0, x1, y1, color):
    xchange = False
    if (abs(x0-x1) < abs(y0 -y1)):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if (x0 > x1):#без этой штуки будет только правая часть звезды
        x0, x1 = x1, x0
        y0, y1 = y1, y0    
        
    y = y0
    dy = 2*abs(y1-y0)
    derror = 0
    y_update = 1 if y1 > y0 else-1

    for x in range (x0,x1):
       
        if (xchange):
            self[x, y] = color
        else:
            self[y, x] = color

        derror+= dy
        if (derror >(x1-x0)):
            derror-= 2*(x1-x0)
            y += y_update

v =[]
f =[]
file = open ('model_1.obj')
for s in file:
    sp = s.split()
    if(sp[0]=='v'):
        
        v.append([float(x) for x in sp[1:4]])
    elif(sp[0]=='f'):
       
        f.append([int(sp[1].split('/')[0]),int(sp[2].split('/')[0]),int(sp[3].split('/')[0])])


for i in range(len(v)):
    x = int(20000*v[i][0]) + 2000
    y = int(20000*v[i][1]) + 2000
    img_mat[y,x] = [0,20,20]

for k in range(len(f)):
    x0 = int((v[f[k][0]-1][0]*20000 +2000))
    y0 = int((v[f[k][0]-1][1]*20000 +2000))
    x1 = int((v[f[k][1]-1][0]*20000 +2000))
    y1 = int((v[f[k][1]-1][1]*20000 +2000))
    x2 = int((v[f[k][2]-1][0]*20000 +2000))
    y2 = int((v[f[k][2]-1][1]*20000 +2000))     
    x_loop_line3(img_mat, x0, y0, x1, y1, [2,200,20])
    x_loop_line3(img_mat, x0, y0, x2, y2, [2,10,200])
    x_loop_line3(img_mat, x1, y1, x2, y2, [200,15,20])




img = Image.fromarray(img_mat, mode ='RGB')
img=ImageOps.flip(img)
img.save('img.png')