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

def set_window_position(screen_number):
    info = pygame.display.get_desktop_sizes()
    if screen_number < len(info):
        x_offset = info[screen_number][0] * screen_number
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x_offset},0"

pygame.init()
display = (700, 700)
fullscreen = True
target_screen = 0 

set_window_position(target_screen)

info = pygame.display.get_desktop_sizes()
if fullscreen and target_screen < len(info):
    display = info[target_screen]
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL | FULLSCREEN)
else:
    display = (700, 700)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

gluOrtho2D(0, display[0], 0, display[1])



square_size = display[1] * 0.3  # 20% of screen height
x_center = (display[0] - square_size) / 2

squares = [
    Square(x_center, display[1] * 0.2 - square_size / 2, square_size, 'images/image1.png'), 
    Square(x_center, display[1] * 0.5 - square_size / 2, square_size, 'images/image2.png'),  
    Square(x_center, display[1] * 0.8 - square_size / 2, square_size, 'images/image3.png')   
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
            elif event.key == K_ESCAPE:
                running = False

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    for square in squares:
        square.draw()

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()