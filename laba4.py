import numpy as np
from math import cos, sin, pi, sqrt
from PIL import Image, ImageOps

scr_size = [3000, 3000]
sc = 15000

img_mat = np.zeros((scr_size[1], scr_size[0], 3), dtype=np.uint8)
z_buffer = np.full((scr_size[1], scr_size[0]), np.inf, dtype=np.float64)

texture_img = Image.open('12268_banjofrog_diffuse.jpg')
texture = np.array(texture_img)
texture_width, texture_height = texture_img.size

v = [] 
vt = []
f = [] 

with open('12268_banjofrog_v1_L3.obj') as file:
     for s in file:
        sp = s.split()
        if len(sp) == 0: continue
        if sp[0] == 'v':
            v.append([float(x) for x in sp[1:4]])
        elif sp[0] == 'vt':
            vt.append([float(x) for x in sp[1:3]])  # u, v координаты
        elif sp[0] == 'f':
            # Обрабатываем полигоны с любым количеством вершин
            face_vertices = []
            for vertex_data in sp[1:]:
                parts = vertex_data.split('/')
                v_index = int(parts[0])
                vt_index = int(parts[1]) if len(parts) > 1 and parts[1] else 0
                face_vertices.append((v_index, vt_index))
            
            if len(face_vertices) >= 3:
                first_vertex = face_vertices[0]
                for i in range(1, len(face_vertices) - 1):
                    triangle = [first_vertex, face_vertices[i], face_vertices[i + 1]]
                    f.append(triangle)

def bar_coord(x, y, x0, y0, x1, y1, x2, y2):
    denominator = (x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2)
    if abs(denominator) < 1e-10:
        return [0, 0, 0]
    
    lambda0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / denominator
    lambda1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / denominator
    lambda2 = 1.0 - lambda0 - lambda1
    return [lambda0, lambda1, lambda2]

def compute_vertex_normals(vertices, faces):
    v_normals = [np.zeros(3) for _ in range(len(vertices))]
    face_normals = []
    
    
    for fc in faces:
        v0 = np.array(vertices[fc[0][0]-1])
        v1 = np.array(vertices[fc[1][0]-1])
        v2 = np.array(vertices[fc[2][0]-1])
        
        # нормаль
        edge1 = v1 - v0
        edge2 = v2 - v0
        face_normal = np.cross(edge1, edge2)
        
        # нормализация
        norm = np.linalg.norm(face_normal)
        if norm > 0:
            face_normal = face_normal / norm
        
        face_normals.append(face_normal)
        # добавить нормали 
        for j in fc:
            v_index = j[0]
            v_normals[v_index-1] += face_normal
    
    for i in range(len(v_normals)): 
        norm = np.linalg.norm(v_normals[i])
        if norm > 0:
            v_normals[i] = v_normals[i] / norm
    
    return v_normals

v_normals = compute_vertex_normals(v, f)

def calculate_light_intensity(normal, light_direction):
    normal_norm = np.linalg.norm(normal)
    light_norm = np.linalg.norm(light_direction)
    
    if normal_norm == 0 or light_norm == 0:
        return 0
    
    cos_angle = np.dot(normal, light_direction) / (normal_norm * light_norm)
    return cos_angle

def scale(vertex, scale_x, scale_y, scale_z):
    return [vertex[0] * scale_x, vertex[1] * scale_y, vertex[2] * scale_z]


def rotate_and_shift(vertex, angles, shift, scaleX,scaleY,scaleZ):
    a, b, c = angles
    tx, ty, tz = shift
    
    # Масштабирование
    scaled_vertex = scale(vertex, scaleX,scaleY,scaleZ)
    
    # Поворот
    Rx = np.array([[1, 0, 0], 
                   [0, cos(a), sin(a)], 
                   [0, -sin(a), cos(a)]])
    Ry = np.array([[cos(b), 0, sin(b)], 
                   [0, 1, 0], 
                   [-sin(b), 0, cos(b)]])
    Rz = np.array([[cos(c), sin(c), 0], 
                   [-sin(c), cos(c), 0], 
                   [0, 0, 1]])
    
    rotation_matrix = Rx @ Ry @ Rz
    rotated = rotation_matrix @ np.array(scaled_vertex)
    
    # Смещение
    shifted = rotated + np.array([tx, ty, tz])
    return shifted

def get_texture_color(u, v, texture, texture_width, texture_height):
    # преобразовать по форумле u v
    x = int(u * (texture_width - 1))
    y = int((1 - v) * (texture_height - 1))  # важно!!!
    
    x = max(0, min(x, texture_width - 1))
    y = max(0, min(y, texture_height - 1))
    
    return texture[y, x]

def triangle(x0, y0, z0, x1, y1, z1, x2, y2, z2, I0, I1, I2, vt0, vt1, vt2):
    # экранные координаты
    x0_s = x0 * sc / z0 + scr_size[0] / 2
    y0_s = y0 * sc / z0 + scr_size[1] / 2
    x1_s = x1 * sc / z1 + scr_size[0] / 2
    y1_s = y1 * sc / z1 + scr_size[1] / 2
    x2_s = x2 * sc / z2 + scr_size[0] / 2
    y2_s = y2 * sc / z2 + scr_size[1] / 2

    # границы
    xmin = max(0, int(min(x0_s, x1_s, x2_s)))
    ymin = max(0, int(min(y0_s, y1_s, y2_s)))
    xmax = min(scr_size[0], int(max(x0_s, x1_s, x2_s)) + 1)
    ymax = min(scr_size[1], int(max(y0_s, y1_s, y2_s)) + 1)

    if xmin >= xmax or ymin >= ymax:
        return

    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            bari = bar_coord(x, y, x0_s, y0_s, x1_s, y1_s, x2_s, y2_s)
            
            if bari[0] >= 0 and bari[1] >= 0 and bari[2] >= 0:
                # считать z
                z = z0 * bari[0] + z1 * bari[1] + z2 * bari[2]
                
                # z буфер
                if z < z_buffer[y, x]:
                    # считать u v
                    u = bari[0] * vt0[0] + bari[1] * vt1[0] + bari[2] * vt2[0]
                    v_coord = bari[0] * vt0[1] + bari[1] * vt1[1] + bari[2] * vt2[1]
                    
                    # цвет текстура
                    texture_color = get_texture_color(u, v_coord, texture, texture_width, texture_height)
                    
                    # гуро посичтать
                    I = bari[0] * I0 + bari[1] * I1 + bari[2] * I2
                    intensity = max(0, min(1, I))  # нормализуем интенсивность
                    
                    # гуро применить
                    color = [
                        int(texture_color[0] * intensity),
                        int(texture_color[1] * intensity),
                        int(texture_color[2] * intensity)
                    ]
                    
                    img_mat[y, x] = color
                    z_buffer[y, x] = z

ROTATION_ANGLES = (-1.57, 3.14, 0)
SHIFT = (0, 0, 70)  
SCALE_X = 1
SCALE_Y = 1
SCALE_Z = 1

# рендеринг
for i in range(len(f)):
    (t1, vt1_idx), (t2, vt2_idx), (t3, vt3_idx) = f[i]
    
    # поворот смещение и масштаб
    v0_transformed = rotate_and_shift(v[t1-1], ROTATION_ANGLES, SHIFT, SCALE_X, SCALE_Y, SCALE_Z)
    v1_transformed = rotate_and_shift(v[t2-1], ROTATION_ANGLES, SHIFT, SCALE_X, SCALE_Y, SCALE_Z)
    v2_transformed = rotate_and_shift(v[t3-1], ROTATION_ANGLES, SHIFT, SCALE_X, SCALE_Y, SCALE_Z)
    
    x0, y0, z0 = v0_transformed
    x1, y1, z1 = v1_transformed
    x2, y2, z2 = v2_transformed

    vt0 = vt[vt1_idx-1] if vt1_idx > 0 else [0, 0]
    vt1 = vt[vt2_idx-1] if vt2_idx > 0 else [0, 0]
    vt2 = vt[vt3_idx-1] if vt3_idx > 0 else [0, 0]
    
    # повернуть и сдвинуть нормали
    n0_transformed = rotate_and_shift(v_normals[t1-1], ROTATION_ANGLES, SHIFT, SCALE_X, SCALE_Y, SCALE_Z)
    n1_transformed = rotate_and_shift(v_normals[t2-1], ROTATION_ANGLES, SHIFT, SCALE_X, SCALE_Y, SCALE_Z)
    n2_transformed = rotate_and_shift(v_normals[t3-1], ROTATION_ANGLES, SHIFT, SCALE_X, SCALE_Y, SCALE_Z)
    
    # Нормализовать нормали
    for normal in [n0_transformed, n1_transformed, n2_transformed]:
        norm = np.linalg.norm(normal)
        if norm > 0:
            normal /= norm
    
    # освещение
    I0 = calculate_light_intensity(n0_transformed, np.array([1, 0, 1]))
    I1 = calculate_light_intensity(n1_transformed, np.array([1, 0, 1]))
    I2 = calculate_light_intensity(n2_transformed, np.array([1, 0, 1]))

    triangle(x0, y0, z0, x1, y1, z1, x2, y2, z2, I0, I1, I2, vt0, vt1, vt2)

img = Image.fromarray(img_mat, mode='RGB')
img = ImageOps.flip(img)
img.save('img.png')