import numpy as np
from math import cos, sin, pi, sqrt
from PIL import Image, ImageOps
from random import randint

img_mat = np.zeros((3000, 3000, 3), dtype=np.uint8)
z_buffer = np.full((3000, 3000), np.inf, dtype=np.float64)

def x_loop_line3(img, x0, y0, x1, y1, color):
    xchange = False
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        xchange = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    
    y = y0
    dy = 2 * abs(y1 - y0)
    derror = 0
    y_update = 1 if y1 > y0 else -1

    for x in range(int(x0), int(x1)):
        if xchange:
            
            if 0 <= y < img.shape[0] and 0 <= x < img.shape[1]:
                img[int(y), int(x)] = color
        else:
            
            if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
                img[int(y), int(x)] = color

        derror += dy
        if derror > (x1 - x0):
            derror -= 2 * (x1 - x0)
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

def bar_coord(x, y, x0, y0, x1, y1, x2, y2):
    
    denominator = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if abs(denominator) < 1e-10:
        return [0, 0, 0]
    
    lambda0 = ((y1 - y2) * (x - x2) + (x2 - x1) * (y - y2)) / denominator
    lambda1 = ((y2 - y0) * (x - x2) + (x0 - x2) * (y - y2)) / denominator
    lambda2 = 1 - lambda0 - lambda1
    return [lambda0, lambda1, lambda2]
def calculate_normal(v0, v1, v2):
    
    vector1 = np.array([v1[0] - v2[0], v1[1] - v2[1], v1[2] - v2[2]])
    vector2 = np.array([v1[0] - v0[0], v1[1] - v0[1], v1[2] - v0[2]])
    
    normal = np.cross(vector1, vector2)
    return normal
def calculate_light_intensity(normal, light_direction=np.array([0, 0, 1])):

    normal_norm = np.linalg.norm(normal)
    light_norm = np.linalg.norm(light_direction)
    
    if normal_norm == 0 or light_norm == 0:
        return 0
    
    cos_angle = np.dot(normal, light_direction) / (normal_norm * light_norm)
    
    return cos_angle
def draw_triangle(x0, y0, z0, x1, y1, z1, x2, y2, z2, img_mat, normal, cos_angle):
    if cos_angle >= 0:
        return
    
    
    intensity = -255 * cos_angle  # -255 * <n,l>/(||n||*||l||)
    intensity = max(0, min(255, int(intensity)))  # Ограничиваем диапазон
    
    color = [intensity*0.0005, intensity*0.6, intensity*0.07]



    xmin = min(x0, x1, x2)
    ymin = min(y0, y1, y2)
    xmax = max(x0, x1, x2)
    ymax = max(y0, y1, y2)
    
    
    xmin = max(0, int(xmin))
    ymin = max(0, int(ymin))
    xmax = min(img_mat.shape[1] - 1, int(xmax))
    ymax = min(img_mat.shape[0] - 1, int(ymax))
    
    
    for i in range(int(xmin), int(xmax + 1)):
        for j in range(int(ymin), int(ymax + 1)):
            bar = bar_coord(i, j, x0, y0, x1, y1, x2, y2)
            
            if bar[0] >= 0 and bar[1] >= 0 and bar[2] >= 0:
                # Вычисляем z-координату через барицентрические координаты
                z_current = bar[0] * z0 + bar[1] * z1 + bar[2] * z2
                
                
                if z_current < z_buffer[j, i]:
                    # Обновляем z-буфер и рисуем пиксель
                    z_buffer[j, i] = z_current
                    img_mat[j, i] = color




for k in range(len(f)):

    v0_orig = v[f[k][0]-1]
    v1_orig = v[f[k][1]-1]
    v2_orig = v[f[k][2]-1]
    
    normal = calculate_normal(v0_orig, v1_orig, v2_orig)
    
    cos_angle = calculate_light_intensity(normal)

    x0 = ((v[f[k][0]-1][0]*10000 +2000))
    y0 = ((v[f[k][0]-1][1]*10000 +2000))
    z0 = ((v[f[k][0]-1][2]))
    x1 = ((v[f[k][1]-1][0]*10000 +2000))
    y1 = ((v[f[k][1]-1][1]*10000 +2000))
    z1 = ((v[f[k][1]-1][2]))
    x2 = ((v[f[k][2]-1][0]*10000 +2000))
    y2 = ((v[f[k][2]-1][1]*10000 +2000))
    z2 = ((v[f[k][2]-1][2]))     
    draw_triangle(x0,y0,z0,x1,y1,z1,x2,y2,z2,img_mat,normal,cos_angle)


img = Image.fromarray(img_mat, mode ='RGB')
img=ImageOps.flip(img)
img.save('img.png')