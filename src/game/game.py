import pygame

from src.game.const import *
from src.game.board import Board
from src.game.dragger import Dragger


class Game:
    def __init__(self):
        self.next_player = 'white'
        self.hovered_square = None
        self.highlighted_squares = []
        self.board = Board()
        self.dragger = Dragger()
         

    #show 
    def show_background(self, surface):
        """
        Displays the background (squares) for the game.
        """
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0: 
                    color = (234, 235, 200) #light green
                else:
                    color = (119, 154, 88) #dark green

                rect = (col * SQU_SIZE, row * SQU_SIZE, SQU_SIZE, SQU_SIZE)

                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        """
        Displays the pieces for the game.
        """
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

    def show_moves(self, surface):
        """
        Displays (not calculates) the possible moves for the game.
        """
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.moves:

                color = '#C4BFAB' if (move.final.row + move.final.col) % 2 == 0 else '#6a874d'
                
                circle_pos = (move.final.col * SQU_SIZE + SQU_SIZE // 2, move.final.row * SQU_SIZE + SQU_SIZE // 2)
                circle_radius = SQU_SIZE // 8
                pygame.draw.circle(surface, color, circle_pos, circle_radius)
    
    def show_last_move(self, surface):
        """
        Highlights the last move for the game.
        """

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial, final]:
                # color
                color = (244, 247, 116) if (pos.row + pos.col) % 2 == 0 else (172, 195, 52)
                rect = (pos.col * SQU_SIZE, pos.row * SQU_SIZE, SQU_SIZE, SQU_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        """
        Displays a hover effect for the hovered square.
        """
        if self.hovered_square:
            color = (160, 160, 160)
            rect = (self.hovered_square.col * SQU_SIZE, self.hovered_square.row * SQU_SIZE, SQU_SIZE, SQU_SIZE)
            pygame.draw.rect(surface, color, rect, width=1)

    def show_highlight(self, surface):
        """
        Displays the highlighted squares for the game.
        """    
        for square in self.highlighted_squares:
            color = '#C86464' if (square[0] + square[1]) % 2 == 0 else '#C15151'
            rect = (square[1] * SQU_SIZE, square[0] * SQU_SIZE, SQU_SIZE, SQU_SIZE)
            pygame.draw.rect(surface, color, rect)
    

    # other 
    def next_turn(self):
        """
        Changes the next player.
        """
        self.next_player = 'white' if self.next_player == 'black' else 'black'
    
    def set_hover(self, row, col):
        """
        Sets the hovered square to the given row and col.
        """
        self.hovered_square = self.board.squares[row][col]

    def add_highlight(self, row, col):
        """
        Adds a highlight to the given row and col.
        """
        self.highlighted_squares.append((row, col))

    def remove_highlight(self, row, col):
        """
        Removes a highlight to the given row and col.
        """
        self.highlighted_squares.remove((row, col))

        







