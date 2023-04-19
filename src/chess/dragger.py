import pygame
from src.chess.const import *

class Dragger:
 
    def __init__(self):
        self.piece = None
        self.mouseX = 0
        self.mouseY = 0
        self.initial_row = 0
        self.initial_col = 0
        self.dragging = False

    #blit
    def update_blit(self, surface):
        """
        Updates the piece to the 128-bit image.
        """

        #grabbing bigger image
        self.piece.set_texture(size=128)
        texture = self.piece.texture

        #loading image
        img = pygame.image.load(texture)
        img_center = (self.mouseX, self.mouseY + (WINDOW_HEIGHT-HEIGHT)//2)
        self.piece.texture_rect = img.get_rect(center = img_center)

        #blitting image
        surface.blit(img, self.piece.texture_rect)


    #other
    def update_mouse(self, pos):
        """
        Updates the mouse position.
        """
        #pos is tuple (x, y)
        self.mouseX, self.mouseY = pos

    def save_initial(self, pos):
        """
        Saves the initial mouse position.
        """
        self.initial_row = pos[1] // SQU_SIZE
        self.initial_col = pos[0] // SQU_SIZE

    def drag_piece(self, piece):
        """
        Enables dragging of the piece.
        """
        self.piece = piece
        self.dragging = True

    def undrag_piece(self):
        """
        Disables dragging of the piece.
        """
        self.piece = None
        self.dragging = False


