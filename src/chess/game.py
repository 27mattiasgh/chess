import pygame
import pygame.freetype

from src.chess.const import *
from src.chess.dragger import Dragger
import sys

class Game:
    def __init__(self):
        self.mode = None



        self.own_color = None
        self.current_color = None
        self.puzzle_correct = None




        self.hovered_square = None

        self.highlighted_squares = []
        self.premoves = []



        


      
         
    def setup(self, fen=None):
        from src.chess.board import Board
        self.board = Board(fen, self.own_color)
        self.dragger = Dragger()


    #show 
    def show_background(self, surface):
        """
        Displays the background (squares) for the game.
        """
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0: 
                    color = (220, 220, 220) #light green
                else:
                    color = (171, 171, 171) #dark green

                #
                rect = (col * SQUARE_SIZE, row * SQUARE_SIZE+((WINDOW_HEIGHT-HEIGHT)//2), SQUARE_SIZE, SQUARE_SIZE)

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

                        #
                        img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, (row * SQUARE_SIZE + SQUARE_SIZE//2) + ((WINDOW_HEIGHT-HEIGHT)//2)
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        """
        Displays (not calculates) the possible moves for the game.
        """
        if self.dragger.dragging or self.dragger.clicking:
            piece = self.dragger.piece


            for move in piece.moves:
                color = '#c6c6c6' if (move.final.row + move.final.col) % 2 == 0 else '#9a9a9a' #light then dark

                circle_pos = (move.final.col * SQUARE_SIZE + SQUARE_SIZE//2, (move.final.row * SQUARE_SIZE + SQUARE_SIZE//2) + (WINDOW_HEIGHT-HEIGHT)//2)
                circle_radius = SQUARE_SIZE // 8
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
                rect = (pos.col * SQUARE_SIZE, pos.row * SQUARE_SIZE + (WINDOW_HEIGHT-HEIGHT)//2, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_hover(self, surface):
        """
        Displays a hover effect for the hovered square.
        """
        if self.hovered_square:
            color = (160, 160, 160)
            rect = (self.hovered_square.col * SQUARE_SIZE, self.hovered_square.row * SQUARE_SIZE + (WINDOW_HEIGHT-HEIGHT)//2, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(surface, color, rect, width=1)

    def show_highlight(self, surface):
        """
        Displays the highlighted squares for the game.
        """    
        for square in self.highlighted_squares:
            #darker goes first, then lighter
            if square[2] == 'highlight':
                color = '#C86464' if (square[0] + square[1]) % 2 == 0 else '#C15151'
            if square[2] == 'premove':
                color = '#72bdda' if (square[0] + square[1]) % 2 == 0 else '#5aabc1'
            if square[2] == 'puzzle_correct':
                color = '#92ae79' if (square[0] + square[1]) % 2 == 0 else '#a0b88a'
            if square[2] == 'puzzle_incorrect':
                color = '#ff8a80' if (square[0] + square[1]) % 2 == 0 else '#ff7f7f'

            if square[2] == 'selection':
                color = '#c0cad0' if (square[0] + square[1]) % 2 == 0 else '#a7b1b7' #light then dark
        
            rect = (square[1] * SQUARE_SIZE, square[0] * SQUARE_SIZE + (WINDOW_HEIGHT-HEIGHT)//2, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(surface, color, rect)



    #Showing UI elements
    def game_ui(self, surface):
        if self.mode != 'computer': return

        font = pygame.font.Font(r"assets\fonts\HelveticaNeueBold.ttf", 18)
        pygame.draw.rect(surface, (49, 47, 44), pygame.Rect(WIDTH + 15, (WINDOW_HEIGHT - HEIGHT)//2, (WINDOW_WIDTH-WIDTH) - 30, HEIGHT), border_radius=10) #Main

        resign_surface = font.render("Resign", True, (255, 255, 255))
        resign_rect = pygame.draw.rect(surface, (255, 84, 86), pygame.Rect(WIDTH + 30, HEIGHT - 35, (WINDOW_WIDTH-WIDTH) - 60, 50), border_radius=10)
        resign_surface_rect = resign_surface.get_rect(center=resign_rect.center)
        surface.blit(resign_surface, resign_surface_rect)



    def puzzle_ui(self, surface):
        if self.mode != 'puzzles': return

        font = pygame.font.Font(r"assets\fonts\HelveticaNeueBold.ttf", 18)
        pygame.draw.rect(surface, (49, 47, 44), pygame.Rect(WIDTH + 15, (WINDOW_HEIGHT - HEIGHT)//2, (WINDOW_WIDTH-WIDTH) - 30, HEIGHT), border_radius=10) #Main

        color_surface = pygame.font.Font(r"assets\fonts\HelveticaNeueBold.ttf", 24).render(f"{self.own_color.capitalize()} to Move", True, (255, 255, 255) if self.own_color == 'black' else (49, 46, 43))
        color_rect = pygame.draw.rect(surface, (241, 241, 241) if self.own_color == 'white' else (73, 72, 71), pygame.Rect(WIDTH + 15, (WINDOW_HEIGHT - HEIGHT)//2, (WINDOW_WIDTH-WIDTH) - 30, 80), border_top_left_radius=10, border_top_right_radius=10) #Color Turn
        color_surface_rect = color_surface.get_rect(center=color_rect.center)
        surface.blit(color_surface, color_surface_rect)
        
        reset_surface = font.render("Hint", True, (255, 255, 255))
        reset_rect = pygame.draw.rect(surface, (100, 100, 100), pygame.Rect(WIDTH + 30, HEIGHT - 95, (WINDOW_WIDTH-WIDTH) - 60, 50), border_radius=10)
        reset_surface_rect = reset_surface.get_rect(center=reset_rect.center)
        surface.blit(reset_surface, reset_surface_rect)

        reset_surface = font.render("Reset", True, (255, 255, 255))
        reset_rect = pygame.draw.rect(surface, (100, 100, 100), pygame.Rect(WIDTH + 30, HEIGHT - 35, (WINDOW_WIDTH-WIDTH) - 60, 50), border_radius=10)
        reset_surface_rect = reset_surface.get_rect(center=reset_rect.center)
        surface.blit(reset_surface, reset_surface_rect)

        if self.puzzle_correct:
            cont_surface = font.render("Next", True, (255, 255, 255))
            cont_rect = pygame.draw.rect(surface, (127, 166, 80), pygame.Rect(WIDTH + 30, HEIGHT - 95, (WINDOW_WIDTH-WIDTH) - 60, 50), border_radius=10)
            cont_surface_rect = cont_surface.get_rect(center=cont_rect.center)
            surface.blit(cont_surface, cont_surface_rect)

    






    # other 
    def next_turn(self):
        self.current_color = 'white' if self.current_color == 'black' else 'black'





    def set_hover(self, row, col):
        """
        Sets the hovered square to the given row and col.
        """
        try:
            self.hovered_square = self.board.squares[row][col]
        except:pass

    def add_highlight(self, row, col, style):
        """
        Adds a highlight to the given row and col.
        """
        self.highlighted_squares.append((row, col, style))

    def remove_highlight(self, row, col, style):
        """
        Removes a highlight to the given row and col.
        """
        self.highlighted_squares.remove((row, col, style))

    def rowcol_to_uci(self, initial_row, initial_col, final_row, final_col):
        """
        Formats pygame coordinates into acceptable stockfish move values (uci) 
        """
        key = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

        initial_row = 7 - initial_row
        final_row = 7 - final_row

        initial_col = key[initial_col]
        final_col = key[final_col]

        initial = initial_col + str(initial_row + 1)
        final = final_col + str(final_row + 1)
            
        return initial + final
    
    def uci_to_rowcol(self, move):
        """
        Formats stockfish move values (uci) into pygame coordinates  
        """        
        if not move: sys.exit(1)
        key = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

        initial_col = key[move[0]]
        initial_row = int(move[1]) - 1

        final_col = key[move[2]]
        final_row = int(move[3]) - 1

        initial_row = 7 - initial_row
        final_row = 7 - final_row

        return initial_row, initial_col, final_row, final_col