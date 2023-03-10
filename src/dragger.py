import pygame

from const import *

class Dragger:

    def __init__(self):
        self.piece = None
        self.mouseX = 0
        self.mouseY = 0
        self.inital_row = 0
        self.inital_col = 0
        self.dragging = False

    #blit

    def update_blit(self, surface):
        #grabbing bigger image
        self.piece.set_texture(size=128)
        texture = self.piece.texture

        #loading image
        img = pygame.image.load(texture)
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center = img_center)

        #blitting image
        surface.blit(img, self.piece.texture_rect)



    #other

    def update_mouse(self, pos):
        #pos is tuple (x, y)
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        self.inital_row = pos[1] // SQU_SIZE
        self.inital_col = pos[0] // SQU_SIZE

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        self.piece = None
        self.dragging = False







