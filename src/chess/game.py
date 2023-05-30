import re
import random
import pygame
import pygame.freetype

from src.chess.const import *
from src.chess.prompts import *

from src.chess.dragger import Dragger
import sys

font = pygame.font.Font(r"assets\fonts\HelveticaNeueBold.ttf", 18)
small_font = pygame.font.Font(r"assets\fonts\HelveticaNeueBold.ttf", 9)

beginner_fish = pygame.transform.scale(pygame.image.load(r'assets\images\beginner_blobfish.jpg'), (100, 100))
intermediate_fish = pygame.transform.scale(pygame.image.load(r'assets\images\intermediate_icefish.jpg'), (100, 100))
advanced_fish = pygame.transform.scale(pygame.image.load(r'assets\images\advanced_arowana.png'), (100, 100))
grandmaster_fish = pygame.transform.scale(pygame.image.load(r'assets\images\grandmaster_grouper.png'), (100, 100))



beginner_fish_small = pygame.transform.scale(pygame.image.load(r'assets\images\beginner_blobfish.jpg'), (70, 70))
intermediate_fish_small = pygame.transform.scale(pygame.image.load(r'assets\images\intermediate_icefish.jpg'), (70, 70))
advanced_fish_small = pygame.transform.scale(pygame.image.load(r'assets\images\advanced_arowana.png'), (70, 70))
grandmaster_fish_small = pygame.transform.scale(pygame.image.load(r'assets\images\grandmaster_grouper.png'), (70, 70))


class Game:
    def __init__(self):

        
        self.mode = None



        self.own_color = None
        self.current_color = None


        self.computer_character = None
        self.computer_prompt = None



        self.puzzle_correct = True
        self.puzzle_complete = None

        self.analysis_current_move = 0
        self.analysis_last_move_found = False


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

            if square[2] == 'checkmate':
                color = '#e0c141' if (square[0] + square[1]) % 2 == 0 else '#deba26' 
        

            rect = (square[1] * SQUARE_SIZE, square[0] * SQUARE_SIZE + (WINDOW_HEIGHT-HEIGHT)//2, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(surface, color, rect)



    #Showing UI elements
    def game_ui(self, surface):
        if self.mode != 'computer': return

        
        transparent_surface = pygame.Surface(((WINDOW_WIDTH-WIDTH) - 30, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (255, 255, 255, 40), pygame.Rect(0, 0, (WINDOW_WIDTH-WIDTH) - 30, HEIGHT), border_radius=10)
        surface.blit(transparent_surface, (WIDTH + 15, (WINDOW_HEIGHT - HEIGHT)//2))

        resign_surface = font.render("Resign", True, (255, 255, 255))
        resign_rect = pygame.draw.rect(surface, (255, 84, 86), pygame.Rect(WIDTH + 30, HEIGHT - 35, (WINDOW_WIDTH-WIDTH) - 60, 50), border_radius=10)
        resign_surface_rect = resign_surface.get_rect(center=resign_rect.center)
        surface.blit(resign_surface, resign_surface_rect)


        margin = 10
        rectangle_width = (WINDOW_WIDTH-WIDTH) - 60
        rectangle_x = WIDTH + 30

        font_color = (255, 255, 255)
        text = self.computer_prompt



        if text is not None:
            words = text.split()
            lines = []
            current_line = words[0]
            for word in words[1:]:
                if font.size(current_line + ' ' + word)[0] <= rectangle_width - 2 * margin: 
                    current_line += ' ' + word
                else:
                    lines.append(current_line)
                    current_line = word
            lines.append(current_line)
            line_height = font.size(lines[0])[1]
            text_height = len(lines) * line_height
            rectangle_height = text_height + 2 * margin + 5
            rectangle_y = 115
            rectangle = pygame.Rect(rectangle_x, rectangle_y, rectangle_width, rectangle_height)
            text_x = rectangle.centerx - rectangle_width // 2 + margin
            text_y = rectangle.centery - text_height // 2 + margin - 10

            
            transparent_surface = pygame.Surface((rectangle_width, rectangle_height), pygame.SRCALPHA)
            pygame.draw.rect(transparent_surface, (255, 255, 255, 25), pygame.Rect(0, 0, rectangle_width, rectangle_height), border_radius=10)
            surface.blit(transparent_surface, (rectangle_x, rectangle_y))


            for line in lines:
                rendered_text = font.render(line, True, font_color)
                surface.blit(rendered_text, (text_x, text_y))
                text_y += line_height



            triangle_points = [(rectangle_x + 200, rectangle_y + rectangle_height), (rectangle_x + 230, rectangle_y + rectangle_height), (rectangle_x + 215, rectangle_y + rectangle_height + 15)]
            transparent_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            pygame.draw.polygon(transparent_surface, (255, 255, 255, 25), triangle_points)
            surface.blit(transparent_surface, (0, 0))

            data = {'Beginner Blobfish': beginner_fish_small, 'Intermediate Icefish': intermediate_fish_small, 'Advanced Arowana': advanced_fish_small, 'Grandmaster Grouper': grandmaster_fish_small}

            surface.blit(data[self.computer_character], (rectangle_x, rectangle_y+rectangle_height+20))

            charater = self.computer_character.split()

            level = font.render(charater[0], True, font_color)
            fish = font.render(charater[1], True, font_color)
            surface.blit(level, (text_x + 73, rectangle_y+rectangle_height+30))
            surface.blit(fish, (text_x + 73, rectangle_y+rectangle_height+50))


        color_surface = font.render("Your Move" if self.own_color == self.current_color else "Computer Move", True, (73, 72, 71) if self.current_color == 'white' else (241, 241, 241))
        color_rect = pygame.draw.rect(surface, (241, 241, 241) if self.current_color == 'white' else (73, 72, 71), pygame.Rect(WIDTH + 15, (WINDOW_HEIGHT - HEIGHT)//2, (WINDOW_WIDTH-WIDTH) - 30, 80), border_top_left_radius=10, border_top_right_radius=10) #Color Turn
        color_surface_rect = color_surface.get_rect(center=color_rect.center)
        surface.blit(color_surface, color_surface_rect)

    def normal_ui(self, surface):
        resign_surface = small_font.render("Home", True, (255, 255, 255))
        resign_rect = pygame.draw.rect(surface, (100, 100, 100), pygame.Rect(5, 5, SQUARE_SIZE-5, 15), border_radius=5)
        resign_surface_rect = resign_surface.get_rect(center=resign_rect.center)
        surface.blit(resign_surface, resign_surface_rect)


        github = small_font.render(f"github.com/hyperrrrrrr/chess", True, (255, 255, 255))


        surface.blit(github, (WINDOW_WIDTH - github.get_width() - 3, WINDOW_HEIGHT- 10))

    def multiplayer_ui(self, surface):
        if self.mode != 'multiplayer': return


        transparent_surface = pygame.Surface(((WINDOW_WIDTH-WIDTH) - 30, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (255, 255, 255, 40), pygame.Rect(0, 0, (WINDOW_WIDTH-WIDTH) - 30, HEIGHT), border_radius=10)
        surface.blit(transparent_surface, (WIDTH + 15, (WINDOW_HEIGHT - HEIGHT)//2))




        resign_surface = font.render("Resign", True, (255, 255, 255))
        resign_rect = pygame.draw.rect(surface, (255, 84, 86), pygame.Rect(WIDTH + 30, HEIGHT - 35, (WINDOW_WIDTH-WIDTH) - 60, 50), border_radius=10)
        resign_surface_rect = resign_surface.get_rect(center=resign_rect.center)
        surface.blit(resign_surface, resign_surface_rect)


    def puzzle_ui(self, surface):
        if self.mode != 'puzzles': return

        font = pygame.font.Font(r"assets\fonts\HelveticaNeueBold.ttf", 18)
        transparent_surface = pygame.Surface(((WINDOW_WIDTH-WIDTH) - 30, HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(transparent_surface, (255, 255, 255, 40), pygame.Rect(0, 0, (WINDOW_WIDTH-WIDTH) - 30, HEIGHT), border_radius=10)
        surface.blit(transparent_surface, (WIDTH + 15, (WINDOW_HEIGHT - HEIGHT)//2))

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



        if self.puzzle_complete:
            cont_surface = font.render("Next", True, (255, 255, 255))
            cont_rect = pygame.draw.rect(surface, (127, 166, 80) if self.puzzle_correct else (255, 84, 86), pygame.Rect(WIDTH + 30, HEIGHT - 95, (WINDOW_WIDTH-WIDTH) - 60, 50), border_radius=10)
            cont_surface_rect = cont_surface.get_rect(center=cont_rect.center)
            surface.blit(cont_surface, cont_surface_rect)

            margin = 10
            rectangle_width = (WINDOW_WIDTH-WIDTH) - 60
            rectangle_x = WIDTH + 30

            font_color = (255, 255, 255)

            text = 'Nice Job!' if self.puzzle_correct else 'Nice try.'
            text += f" This puzzle has been played {self.computer_prompt['NbPlays']} times by various players with a ELO rating of {self.computer_prompt['Rating']}."

            if text is not None:
                words = text.split()
                lines = []
                current_line = words[0]
                for word in words[1:]:
                    if font.size(current_line + ' ' + word)[0] <= rectangle_width - 2 * margin: 
                        current_line += ' ' + word
                    else:
                        lines.append(current_line)
                        current_line = word
                lines.append(current_line)
                line_height = font.size(lines[0])[1]
                text_height = len(lines) * line_height
                rectangle_height = text_height + 2 * margin + 5
                rectangle_y = 115
                rectangle = pygame.Rect(rectangle_x, rectangle_y, rectangle_width, rectangle_height)
                text_x = rectangle.centerx - rectangle_width // 2 + margin
                text_y = rectangle.centery - text_height // 2 + margin - 10

                
                transparent_surface = pygame.Surface((rectangle_width, rectangle_height), pygame.SRCALPHA)
                pygame.draw.rect(transparent_surface, (255, 255, 255, 25), pygame.Rect(0, 0, rectangle_width, rectangle_height), border_radius=10)
                surface.blit(transparent_surface, (rectangle_x, rectangle_y))


                for line in lines:
                    rendered_text = font.render(line, True, font_color)
                    surface.blit(rendered_text, (text_x, text_y))
                    text_y += line_height



                triangle_points = [(rectangle_x + 200, rectangle_y + rectangle_height), (rectangle_x + 230, rectangle_y + rectangle_height), (rectangle_x + 215, rectangle_y + rectangle_height + 15)]
                transparent_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                pygame.draw.polygon(transparent_surface, (255, 255, 255, 25), triangle_points)
                surface.blit(transparent_surface, (0, 0))



                surface.blit(grandmaster_fish_small, (rectangle_x, rectangle_y+rectangle_height+20))


                level = font.render('Grandmaster', True, font_color)
                fish = font.render('Grouper', True, font_color)
                surface.blit(level, (text_x + 73, rectangle_y+rectangle_height+30))
                surface.blit(fish, (text_x + 73, rectangle_y+rectangle_height+50))


        else:
            margin = 10
            rectangle_width = (WINDOW_WIDTH-WIDTH) - 60
            rectangle_x = WIDTH + 30

            font_color = (255, 255, 255)

            text = f"You think you can solve this puzzle with a {self.computer_prompt['Rating']} rating?"

            if text is not None:
                words = text.split()
                lines = []
                current_line = words[0]
                for word in words[1:]:
                    if font.size(current_line + ' ' + word)[0] <= rectangle_width - 2 * margin: 
                        current_line += ' ' + word
                    else:
                        lines.append(current_line)
                        current_line = word
                lines.append(current_line)
                line_height = font.size(lines[0])[1]
                text_height = len(lines) * line_height
                rectangle_height = text_height + 2 * margin + 5
                rectangle_y = 115
                rectangle = pygame.Rect(rectangle_x, rectangle_y, rectangle_width, rectangle_height)
                text_x = rectangle.centerx - rectangle_width // 2 + margin
                text_y = rectangle.centery - text_height // 2 + margin - 10

                transparent_surface = pygame.Surface((rectangle_width, rectangle_height), pygame.SRCALPHA)
                pygame.draw.rect(transparent_surface, (255, 255, 255, 25), pygame.Rect(0, 0, rectangle_width, rectangle_height), border_radius=10)
                surface.blit(transparent_surface, (rectangle_x, rectangle_y))

                for line in lines:
                    rendered_text = font.render(line, True, font_color)
                    surface.blit(rendered_text, (text_x, text_y))
                    text_y += line_height


                triangle_points = [(rectangle_x + 200, rectangle_y + rectangle_height), (rectangle_x + 230, rectangle_y + rectangle_height), (rectangle_x + 215, rectangle_y + rectangle_height + 15)]
                transparent_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
                pygame.draw.polygon(transparent_surface, (255, 255, 255, 25), triangle_points)
                surface.blit(transparent_surface, (0, 0))

                surface.blit(grandmaster_fish_small, (rectangle_x, rectangle_y+rectangle_height+20))

                level = font.render('Grandmaster', True, font_color)
                fish = font.render('Grouper', True, font_color)
                surface.blit(level, (text_x + 73, rectangle_y+rectangle_height+30))
                surface.blit(fish, (text_x + 73, rectangle_y+rectangle_height+50))




    






    # other 
    def next_turn(self):
        self.current_color = 'white' if self.current_color == 'black' else 'black'

    def update_prompt(self, check, checkmate, player):
        if check:

            if player == 'human':
                if self.computer_character == 'Beginner Blobfish':
                    self.computer_prompt = random.choice(beginner_check_responses)
                elif self.computer_character == 'Intermediate Icefish':
                    self.computer_prompt = random.choice(intermediate_check_responses)
                elif self.computer_character == 'Advanced Arowana':
                    self.computer_prompt = random.choice(advanced_check_responses)
                elif self.computer_character == 'Grandmaster Grouper':
                    self.computer_prompt = random.choice(grandmaster_check_responses)

            else:
                if self.computer_character == 'Beginner Blobfish':
                    self.computer_prompt = random.choice(beginner_check_prompts)
                elif self.computer_character == 'Intermediate Icefish':
                    self.computer_prompt = random.choice(intermediate_check_prompts)
                elif self.computer_character == 'Advanced Arowana':
                    self.computer_prompt = random.choice(advanced_check_prompts)
                elif self.computer_character == 'Grandmaster Grouper':
                    self.computer_prompt = random.choice(grandmaster_check_prompts)


        if checkmate:

            if player == 'human':
                if self.computer_character == 'Beginner Blobfish':
                    self.computer_prompt = random.choice(beginner_checkmate_responses)
                elif self.computer_character == 'Intermediate Icefish':
                    self.computer_prompt = random.choice(intermediate_checkmate_responses)
                elif self.computer_character == 'Advanced Arowana':
                    self.computer_prompt = random.choice(advanced_checkmate_responses)
                elif self.computer_character == 'Grandmaster Grouper':
                    self.computer_prompt = random.choice(grandmaster_checkmate_responses)
            else:
                if self.computer_character == 'Beginner Blobfish':
                    self.computer_prompt = random.choice(beginner_checkmate_prompts)
                elif self.computer_character == 'Intermediate Icefish':
                    self.computer_prompt = random.choice(intermediate_checkmate_prompts)
                elif self.computer_character == 'Advanced Arowana':
                    self.computer_prompt = random.choice(advanced_checkmate_prompts)
                elif self.computer_character == 'Grandmaster Grouper':
                    self.computer_prompt = random.choice(grandmaster_checkmate_prompts)



        else:
            if player == 'human':
                if self.computer_character == 'Beginner Blobfish':
                    self.computer_prompt = random.choice(beginner_responses)
                elif self.computer_character == 'Intermediate Icefish':
                    self.computer_prompt = random.choice(intermediate_responses)
                elif self.computer_character == 'Advanced Arowana':
                    self.computer_prompt = random.choice(advanced_responses)
                elif self.computer_character == 'Grandmaster Grouper':
                    self.computer_prompt = random.choice(grandmaster_responses)

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