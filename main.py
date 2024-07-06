import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
from PIL import Image
from cube import Square

def swap_textures(squares):
    textures = [square.texture_id for square in squares]
    textures = textures[-1:] + textures[:-1]
    for square, texture in zip(squares, textures):
        square.texture_id = texture

pygame.init()
display = (700, 700)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluOrtho2D(0, display[0], 0, display[1])

squares = [
    Square(250, 50, 150,'images/image1.png'),
    Square(250, 250, 150,'images/image2.png'),
    Square(250, 450, 150,'images/image3.png')
]

running = True
selected_square = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            mx, my = event.pos
            for square in squares:
                corner_index = square.check_corners(mx, display[1] - my)
                if corner_index is not None:
                    selected_square = square
                    square.selected_corner = corner_index
                    break
        elif event.type == MOUSEBUTTONUP:
            selected_square = None
        elif event.type == MOUSEMOTION:
            if selected_square:
                mx, my = event.pos
                selected_square.update_corner(selected_square.selected_corner, mx, display[1] - my)
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                swap_textures(squares)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for square in squares:
        square.draw()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()