import pygame

from const import *
from board import Board
from dragger import Dragger

class Game:

    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        


    #show the game
    def show_background(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0: 
                    color = (234, 235, 200) #light green
                else:
                    color = (119, 154, 88) #dark green

                rect = (col * SQU_SIZE, row * SQU_SIZE, SQU_SIZE, SQU_SIZE)

                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):

                #piece on specific square
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece

                    #should blit all pieces except for dragging ones 
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQU_SIZE + SQU_SIZE // 2, row * SQU_SIZE + SQU_SIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
