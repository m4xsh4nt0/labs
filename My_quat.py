from math import *
import os
import numpy as np 

class quaternion:
    
    def __init__(self,a,b,c,d):
        self.a=a
        self.b=b
        self.c=c
        self.d=d

    def __add__(self,other):
        a1,a2=self.a , other.a
        b1,b2=self.b , other.b
        c1,c2=self.c , other.c
        d1,d2=self.d , other.d
        return quaternion(a1+a2, b1+b2 , c1+c2 , d1+d2)
    
    def __sub__(self,other):
        a1,a2=self.a , other.a
        b1,b2=self.b , other.b
        c1,c2=self.c , other.c
        d1,d2=self.d , other.d
        return quaternion(a1-a2, b1-b2 , c1-c2 , d1-d2)
    

    def __mul__(self,other):
        a1,a2=self.a , other.a
        b1,b2=self.b , other.b
        c1,c2=self.c , other.c
        d1,d2=self.d , other.d
        return quaternion(a1*a2 - b1*b2 - c1*c2 - d1*d2 , 
           a1*b2 + b1*a2 + c1*d2 - d1*c2 , 
           a1*c2 - b1*d2 + c1*a2 + d1*b2 , 
           a1*d2 + b1*c2 - c1*b2 + d1*a2)
    
    
    
    def conjugate(self):
        return quaternion(self.a, -self.b , -self.c, -self.d)

    def norm(self):
        return (self.a**2+ self.b**2 +self.c**2+self.d**2)**0.5
    

    def inverse(self):
        norm_sq = self.norm()**2
        if norm_sq == 0:
            raise ValueError("!!!!!")
        inv_norm_sq = 1 / norm_sq
        return quaternion(
            self.a * inv_norm_sq,
            -self.b * inv_norm_sq,
            -self.c * inv_norm_sq,
            -self.d * inv_norm_sq
        )
    
    def rotate_vector(self, vector):
        """
        Поворачивает вектор с помощью этого кватерниона.
        vector: список или массив numpy с 3 элементами [x, y, z]
        Возвращает: повернутый вектор в виде numpy array
        """
        # Нормализуем кватернион для чистого поворота
        q_normalized = self.normalize()
        
        # Создаем чисто мнимый кватернион из вектора
        v_quat = quaternion(0, vector[0], vector[1], vector[2])
        
        # Формула поворота: v' = q * v * q⁻¹
        # Где q - единичный кватернион, q⁻¹ - его сопряженный (для единичного кватерниона)
        q_conjugate = q_normalized.conjugate()
        
        # Выполняем поворот: v_rotated = q * v * q⁻¹
        v_rotated_quat = q_normalized * v_quat * q_conjugate
        
        # Извлекаем векторную часть
        rotated_vector = np.array([v_rotated_quat.b, v_rotated_quat.c, v_rotated_quat.d])
        
        return rotated_vector
    

    def normalize(self):
        n=self.norm()
        if n == 0:
            raise ValueError("!!!")
        return quaternion(self.a/n, self.b/n , self.c/n, self.d/n)
    def print(self):
        print(f"{self.a} +{self.b}i +{self.c}j +{self.d}k" )
    