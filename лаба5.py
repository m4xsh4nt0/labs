import numpy as np
from math import cos, sin, pi
from PIL import Image, ImageOps
from My_quat import quaternion

SCREEN_SIZE = [3000, 3000]
BACKGROUND_COLOR = [0, 0, 100] 
LIGHT_DIRECTION = np.array([1, 0, 0])
CAMERA_SCALE = 10000
Z_BUFFER_INIT = np.inf 

MODELS = [
    {
        'obj': 'Borderlands cosplay-obj.obj',
        'texture': 'Borderlands cosplay-obj_0.jpg',
        'scale': 1.5,  # Масштаб модели
        'rotation': {'type': 'euler', 'angles': (-pi/2, pi, 0)},  # Поворот Эйлера
        'shift': (1, 0, 30),  # Смещение
        'render_scale': CAMERA_SCALE  # Масштаб проекции для этой модели
    },
    {
        'obj': 'model_1.obj',
        'texture': 'bunny-atlas.jpg',
        'scale': 1,
        'rotation': {'type': 'quaternion', 'w': -0.5, 'x': 0, 'y': -1, 'z': 0},
        'shift': (-1, 0, 30),
        'render_scale': CAMERA_SCALE
    }
]

ENABLE_TEXTURING = True
ENABLE_LIGHTING = True
OUTPUT_FILENAME = 'rendered_scene.png'

def normalize_coordinates(V):
    """
    Нормализует координаты вершин так, чтобы модель помещалась в куб [-1, 1]³.
    Это нужно для удобного масштабирования и позиционирования моделей.
    """
    V_arr = np.array(V)
    
    min_vals = V_arr.min(axis=0)
    max_vals = V_arr.max(axis=0)
    
    center = (min_vals + max_vals) / 2
    size = max_vals - min_vals
    
    max_size = max(size)
    
    normalized_v = (V_arr - center) / (max_size / 2)
    
    return normalized_v.tolist()

def bari_coord(x, y, x0, y0, x1, y1, x2, y2):
    """
    Вычисляет барицентрические координаты для точки (x, y)
    относительно треугольника с вершинами (x0,y0), (x1,y1), (x2,y2).
    
    Барицентрические координаты используются для интерполяции
    цветов, текстурных координат и нормалей по треугольнику.
    """
    denominator = (x0 - x2) * (y1 - y2) - (x1 - x2) * (y0 - y2)
    
    # Избегаем деления на ноль
    if abs(denominator) < 1e-10:
        return [0, 0, 0]
    
    lambda0 = ((x - x2) * (y1 - y2) - (x1 - x2) * (y - y2)) / denominator
    lambda1 = ((x0 - x2) * (y - y2) - (x - x2) * (y0 - y2)) / denominator
    lambda2 = 1.0 - lambda0 - lambda1
    
    return [lambda0, lambda1, lambda2]

def get_texture_color(u, v, texture, texture_width, texture_height):
    """
    Получает цвет из текстуры по координатам (u, v).
    u, v: текстурные координаты в диапазоне [0, 1]
    """
    # Преобразуем нормализованные координаты в пиксельные
    x = int(u * (texture_width - 1))
    y = int((1 - v) * (texture_height - 1))  # Инвертируем v для систем с началом вверху
    
    # Ограничиваем координаты размерами текстуры
    x = max(0, min(x, texture_width - 1))
    y = max(0, min(y, texture_height - 1))
    
    return texture[y, x]

def parse_obj_file(filepath):
    """
    Парсит OBJ файл, извлекает вершины, текстурные координаты, нормали и полигоны.
    Автоматически разбивает полигоны с более чем 3 вершинами на треугольники.
    
    Возвращает: (vertices, faces, texture_coords, vertex_normals)
    """
    v = []
    tex_c = []
    v_n = []
    f = []  # Каждый элемент: [(v_idx, vt_idx, vn_idx), ...] для треугольника
    
    print(f"Загрузка модели: {filepath}")
    
    with open(filepath, 'r') as file:
        for line_num, line in enumerate(file):
            line = line.strip()
            
            parts = line.split()
            if not parts:
                continue
            
            try:
                if parts[0] == 'v':
                    # Вершина: v x y z
                    v.append([float(x) for x in parts[1:4]])
                
                elif parts[0] == 'vt':
                    # Текстурная координата: vt u v
                    tex_c.append([float(x) for x in parts[1:3]])
                
                elif parts[0] == 'vn':
                    # Нормаль вершины: vn x y z
                    v_n.append([float(x) for x in parts[1:4]])
                
                elif parts[0] == 'f':
                    # Полигон: f v1/vt1/vn1 v2/vt2/vn2 ...
                    face_vertices = []
                    
                    for vertex_data in parts[1:]:
                        # Разбираем данные вершины (может быть v, v/vt, v/vt/vn, v//vn)
                        subparts = vertex_data.split('/')
                        
                        v_idx = int(subparts[0]) if subparts[0] else 0
                        
                        # Обрабатываем текстурные координаты
                        if len(subparts) > 1 and subparts[1]:
                            vt_idx = int(subparts[1])
                        else:
                            vt_idx = 0
                        
                        # # Обрабатываем нормали
                        # if len(subparts) > 2 and subparts[2]:
                        #     vn_idx = int(subparts[2])
                        # else:
                        #     vn_idx = 0
                        
                        # face_vertices.append((v_idx, vt_idx, vn_idx))
                    
                    # Разбиваем полигон на треугольники (триангуляция веером)
                    if len(face_vertices) >= 3:
                        first_vertex = face_vertices[0]
                        for i in range(1, len(face_vertices) - 1):
                            triangle = [first_vertex, face_vertices[i], face_vertices[i + 1]]
                            f.append(triangle)
            
            except (ValueError, IndexError) as e:
                print(f"Предупреждение: ошибка в строке {line_num}: {line}")
                print(f"Ошибка: {e}")
                continue
    
    return v, f, tex_c, v_n

def calculate_light_intensity(normal, light_direction):
    normal_norm = np.linalg.norm(normal)
    light_norm = np.linalg.norm(light_direction)
    
    if normal_norm == 0 or light_norm == 0:
        return 0
    
    cos_angle = np.dot(normal, light_direction) / (normal_norm * light_norm)
    return cos_angle

def compute_normals(vertices, faces, existing_normals):
    """
    Вычисляет нормали вершин, если они не были загружены из файла.
    Использует усреднение нормалей соседних полигонов.
    """
    if len(existing_normals) == len(vertices):
        # Нормали уже есть в файле
        return existing_normals
    
    print("  Вычисление нормалей вершин...")
    
    # Инициализируем массив нормалей нулями
    vertex_normals = [np.zeros(3, dtype=np.float32) for _ in range(len(vertices))]
    
    # Для каждого треугольника вычисляем его нормаль и добавляем к вершинам
    for face in faces:
        # Получаем индексы вершин треугольника
        v0_idx, v1_idx, v2_idx = face[0][0] - 1, face[1][0] - 1, face[2][0] - 1
        
        # Получаем координаты вершин
        v0 = np.array(vertices[v0_idx])
        v1 = np.array(vertices[v1_idx])
        v2 = np.array(vertices[v2_idx])
        
        # Вычисляем нормаль треугольника
        edge1 = v1 - v0
        edge2 = v2 - v0
        face_normal = np.cross(edge1, edge2)
        
        # Нормализуем нормаль
        norm = np.linalg.norm(face_normal)
        if norm > 0:
            face_normal = face_normal / norm
        
        # Добавляем нормаль ко всем вершинам треугольника
        vertex_normals[v0_idx] += face_normal
        vertex_normals[v1_idx] += face_normal
        vertex_normals[v2_idx] += face_normal
    
    # Нормализуем все нормали вершин
    for i in range(len(vertex_normals)):
        norm = np.linalg.norm(vertex_normals[i])
        if norm > 0:
            vertex_normals[i] = vertex_normals[i] / norm
    
    return vertex_normals

# ============================================================
# ФУНКЦИИ ТРАНСФОРМАЦИИ И РЕНДЕРИНГА
# ============================================================
def rotate_and_shift(vertex, angles):
    a, b, c = angles
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
    rotated_v = rotation_matrix @ np.array(vertex)
    
    return rotated_v

def transform_vertices(vertices, rotation_info, shift, scale_factor=1.0):
    """
    Применяет трансформации к вершинам: поворот, смещение, масштабирование.
    
    rotation_info: dict с информацией о повороте
      - 'type': 'euler' или 'quaternion'
      - 'angles': (x, y, z) для эйлеровых углов
      - или 'w', 'x', 'y', 'z' для кватерниона
    """
    transformed_vertices = []
    
    for vertex in vertices:
        # Масштабирование
        scaled_vertex = np.array(vertex) * scale_factor
        
        # Поворот
        if rotation_info['type'] == 'euler':
            rotated_vertex = rotate_and_shift(scaled_vertex, rotation_info['angles'])
        elif rotation_info['type'] == 'quaternion':
            rotation_quat = quaternion(
                rotation_info.get('w', 1),
                rotation_info.get('x', 0),
                rotation_info.get('y', 0),
                rotation_info.get('z', 0)
            ).normalize()
            rotated_vertex = rotation_quat.rotate_vector(scaled_vertex)
        else:
            rotated_vertex = scaled_vertex  # Без поворота
        
        # Смещение
        transformed_vertex = rotated_vertex + np.array(shift)
        
        transformed_vertices.append(transformed_vertex)
    
    return transformed_vertices

def transform_normals(normals, rotation_info):
    """
    Поворачивает нормали с использованием того же поворота, что и вершины.
    Нормали должны быть повернуты, но не смещены.
    """
    transformed_normals = []
    for normal in normals:
        # Масштабирование
        # Поворот
        if rotation_info['type'] == 'euler':
            rotated_normal = rotate_and_shift(normal, rotation_info['angles'])
        elif rotation_info['type'] == 'quaternion':
            rotation_quat = quaternion(
                rotation_info.get('w', 1),
                rotation_info.get('x', 0),
                rotation_info.get('y', 0),
                rotation_info.get('z', 0)
            ).normalize()
            rotated_normal = rotation_quat.rotate_vector(normal)
        else:
            rotated_normal = normal  # Без поворота
        
        # Нормализуем результат
        norm = np.linalg.norm(rotated_normal)
        if norm > 0:
            rotated_normal = rotated_normal / norm
        
        transformed_normals.append(rotated_normal)
    
    return transformed_normals

def render_triangle(x0, y0, z0, x1, y1, z1, x2, y2, z2, I0,I1,I2, texture_coords, texture, img_mat, z_buffer, model_scale):
    """
    Отрисовывает один треугольник с использованием:
    - Z-буфера для корректного порядка отрисовки
    - Интерполяции Гуро для плавного освещения
    - Текстурных координат для наложения текстуры
    """
    # Пропускаем треугольники за камерой
    if z0 <= 0 or z1 <= 0 or z2 <= 0:
        return
    
    # 1. Проецируем вершины на экран
    x0_s = x0 * model_scale / z0 + SCREEN_SIZE[0] / 2
    y0_s = y0 * model_scale / z0 + SCREEN_SIZE[1] / 2
    x1_s = x1 * model_scale / z1 + SCREEN_SIZE[0] / 2
    y1_s = y1 * model_scale / z1 + SCREEN_SIZE[1] / 2
    x2_s = x2 * model_scale / z2 + SCREEN_SIZE[0] / 2
    y2_s = y2 * model_scale / z2 + SCREEN_SIZE[1] / 2
    
    # 2. Определяем ограничивающий прямоугольник
    xmin = max(0, int(min(x0_s, x1_s, x2_s)))
    ymin = max(0, int(min(y0_s, y1_s, y2_s)))
    xmax = min(SCREEN_SIZE[0], int(max(x0_s, x1_s, x2_s)) + 1)
    ymax = min(SCREEN_SIZE[1], int(max(y0_s, y1_s, y2_s)) + 1)
    
    if xmin >= xmax or ymin >= ymax:
        return
    
    # 4. Получаем текстурные координаты
    if ENABLE_TEXTURING and texture is not None and texture_coords:
        vt0, vt1, vt2 = texture_coords
        texture_width, texture_height = texture.shape[1], texture.shape[0]
    else:
        vt0 = vt1 = vt2 = [0, 0]
        texture_width = texture_height = 1
    
    # 5. Растеризация треугольника
    for y in range(ymin, ymax):
        for x in range(xmin, xmax):
            # Вычисляем барицентрические координаты
            bary = bari_coord(x, y, x0_s, y0_s, x1_s, y1_s, x2_s, y2_s)
            lambda0, lambda1, lambda2 = bary
            
            # Проверяем, находится ли точка внутри треугольника
            if lambda0 >= 0 and lambda1 >= 0 and lambda2 >= 0:
                # Интерполируем глубину (z-координату)
                z = 1.0 / (lambda0/z0 + lambda1/z1 + lambda2/z2)
                
                # Проверяем z-буфер
                if z < z_buffer[y, x]:
                    # Вычисляем интенсивность освещения в точке
                    if ENABLE_LIGHTING:
                        intensity = lambda0 * I0 + lambda1 * I1 + lambda2 * I2
                        intensity = max(0.1, min(1.0, intensity))  # Ограничиваем диапазон
                    else:
                        intensity = 1.0
                    
                    # Получаем цвет текстуры
                    if ENABLE_TEXTURING and texture is not None:
                        # Интерполируем текстурные координаты
                        u = lambda0 * vt0[0] + lambda1 * vt1[0] + lambda2 * vt2[0]
                        v_coord = lambda0 * vt0[1] + lambda1 * vt1[1] + lambda2 * vt2[1]
                        
                        # Получаем цвет из текстуры
                        tex_color = get_texture_color(u, v_coord, texture, texture_width, texture_height)
                        
                        # Применяем освещение к цвету текстуры
                        color = [
                            int(tex_color[0] * intensity),
                            int(tex_color[1] * intensity),
                            int(tex_color[2] * intensity)
                        ]
                    else:
                        # Используем серый цвет без текстуры
                        gray_value = int(200 * intensity)
                        color = [gray_value, gray_value, gray_value]
                    
                    # Записываем пиксель
                    img_mat[y, x] = color
                    z_buffer[y, x] = z

def render_model(model_info, img_mat, z_buffer):
    """
    Рендерит одну модель на сцену.
    model_info: словарь с параметрами модели из списка MODELS
    """
    print(f"\nРендеринг модели: {model_info['obj']}")
    
    # 1. Загружаем модель
    v, f, tex_c, v_n = parse_obj_file(model_info['obj'])
    
    # 2. Нормализуем координаты вершин
    v = normalize_coordinates(v)
    
    # 3. Вычисляем или используем нормали из файла
    if len(v_n) !=0 :
        print("  Используем нормали из файла")
    else:
        print("  Вычисляем нормали")
        v_n = compute_normals(v, f, v_n)
    
    # 4. Загружаем текстуру
    if ENABLE_TEXTURING and 'texture' in model_info:
        try:
            texture_img = Image.open(model_info['texture'])
            texture = np.array(texture_img)
            print(f"  Текстура загружена: {model_info['texture']}")
        except Exception as e:
            print(f"  Ошибка загрузки текстуры: {e}")
            texture = None 
    else:
        texture = None
    
    # 5. Применяем трансформации к вершинам и нормалям
    print("  Применяем трансформации...")
    transformed_vertices = transform_vertices(
        v, 
        model_info['rotation'], 
        model_info['shift'],
        model_info.get('scale', 1.0)
    )
    
    transformed_normals = transform_normals(
        v_n,
        model_info['rotation']
    )
    
    # 6. Рендерим все треугольники
    render_scale = model_info.get('render_scale', CAMERA_SCALE)
    triangles_count = len(f)
    
    print(f"  Рендеринг {triangles_count} треугольников...")
    for i, face in enumerate(f):
        # Получаем индексы вершин треугольника
        (v_idx0, vt_idx0, vn_idx0), (v_idx1, vt_idx1, vn_idx1), (v_idx2, vt_idx2, vn_idx2) = face
        
        # координаты вершин
        x0, y0, z0 = transformed_vertices[v_idx0 - 1]
        x1, y1, z1 = transformed_vertices[v_idx1 - 1]
        x2, y2, z2 = transformed_vertices[v_idx2 - 1]
        
        # нормали вершин
        n0 = transformed_normals[vn_idx0 - 1] if vn_idx0 > 0 else transformed_normals[v_idx0 - 1]
        n1 = transformed_normals[vn_idx1 - 1] if vn_idx1 > 0 else transformed_normals[v_idx1 - 1]
        n2 = transformed_normals[vn_idx2 - 1] if vn_idx2 > 0 else transformed_normals[v_idx2 - 1]
        
        # текстурные координаты
        if ENABLE_TEXTURING and tex_c and vt_idx0 > 0 and vt_idx1 > 0 and vt_idx2 > 0:
            vt0 = tex_c[vt_idx0 - 1]
            vt1 = tex_c[vt_idx1 - 1]
            vt2 = tex_c[vt_idx2 - 1]
        else:
            vt0 = vt1 = vt2 = [0, 0]
        
         # освещение
        I0 = calculate_light_intensity(n0, np.array(LIGHT_DIRECTION))
        I1 = calculate_light_intensity(n1, np.array(LIGHT_DIRECTION))
        I2 = calculate_light_intensity(n2, np.array(LIGHT_DIRECTION))
        # Рендерим треугольник
        render_triangle(
            x0, y0, z0, x1, y1, z1, x2, y2, z2,
            I0, I1, I2, [vt0, vt1, vt2],
            texture, img_mat, z_buffer, render_scale
        )
        
        # Показываем прогресс
        if i % 1000 == 0 and i > 0:
            print(f"    Отрисовано {i}/{triangles_count} треугольников")
    
    print(f"  Модель отрендерена")


def main():
    # 1. Инициализация буферов
    print(f"Инициализация буферов: {SCREEN_SIZE[0]}x{SCREEN_SIZE[1]}")
    img_mat = np.full((SCREEN_SIZE[1], SCREEN_SIZE[0], 3), BACKGROUND_COLOR, dtype=np.uint8)
    z_buffer = np.full((SCREEN_SIZE[1], SCREEN_SIZE[0]), Z_BUFFER_INIT, dtype=np.float64)
    
    # 2. Рендеринг всех моделей
    for i, model_info in enumerate(MODELS):
        print(f"\nМодель {i+1}/{len(MODELS)}")
        render_model(model_info, img_mat, z_buffer)
    
    # 3. Сохранение результата
    print(f"\nСохранение изображения: {OUTPUT_FILENAME}")
    img = Image.fromarray(img_mat, mode='RGB')
    img = ImageOps.flip(img) 
    img.save(OUTPUT_FILENAME)
    
main()