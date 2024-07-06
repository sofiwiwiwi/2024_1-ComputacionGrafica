import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image

def load_texture(image_path):
    image = Image.open(image_path)
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    width, height = image.size
    
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    return texture_id

class Square:
    def __init__(self, x, y, size, texture_path):
        self.vertices = [
            [x, y],
            [x + size, y],
            [x + size, y + size],
            [x, y + size]
        ]
        self.texture_id = load_texture(texture_path)
        self.selected_corner = None
        self.tex_coords = [(0, 0), (1, 0), (1, 1), (0, 1)]  # Correct texture coordinates

    def draw(self):
        glBindTexture(GL_TEXTURE_2D, self.texture_id)
        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        for i, vertex in enumerate(self.vertices):
            glTexCoord2f(*self.tex_coords[i])
            glVertex2f(vertex[0], vertex[1])
        glEnd()
        glDisable(GL_TEXTURE_2D)

    def check_corners(self, mx, my):
        for i, (vx, vy) in enumerate(self.vertices):
            if np.hypot(vx - mx, vy - my) < 10:
                return i
        return None

    def update_corner(self, corner_index, mx, my):
        self.vertices[corner_index] = [mx, my]
        self.update_texture_coords()

    def update_texture_coords(self):
        min_x = min(v[0] for v in self.vertices)
        max_x = max(v[0] for v in self.vertices)
        min_y = min(v[1] for v in self.vertices)
        max_y = max(v[1] for v in self.vertices)
        
        self.tex_coords = [
            [(v[0] - min_x) / (max_x - min_x), (v[1] - min_y) / (max_y - min_y)]
            for v in self.vertices
        ]