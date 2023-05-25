import json
import random
import sys
import threading
import getpass
import time
import socket
import netaddr
import pygame

import chess

from src.chess.home import Home

from src.chess.const import *
from src.chess.game import Game
from src.chess.move import Move
from src.chess.sound import Sound
from src.chess.square import Square

from src.computer.analyzer import Analyzer
from src.computer.logging import Logging
from src.computer.computer import Computer

from src.multiplayer.multiplayer import Multiplayer

large_font = pygame.font.Font(r"assets\fonts\HelveticaNeueBold.ttf", 70)
medium_font = pygame.font.Font(r"assets\fonts\HelveticaNeueBold.ttf", 30)

class Main:
    def __init__(self):
        self.home = Home()
        self.game = Game()
        self.sound = Sound()
        self.logging = Logging()
        self.computer = Computer()
        self.multiplayer = Multiplayer()

        
        with open(r'assets\data\puzzles.json', 'r') as f: self.puzzle_data = json.load(f)
        
        
        stockfish_path = "src\computer\stockfish executables\stockfish_15.1_popcnt\stockfish-windows-2022-x86-64-modern.exe"
        data_file = "assets/data/games.json"

        self.analyzer = Analyzer(stockfish_path, data_file)

        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()


        self.background = pygame.transform.scale(pygame.image.load(r'assets\images\background.png'), (1000, 750))
        pygame.display.set_caption('Chess')

    



    def mode_computer(self):
        self.logging.new()
        self.py_chess = chess.Board()  

        self.game.mode = 'computer'
        self.game.own_color = 'white'
        self.game.current_color = 'white'
        self.game.setup()

    def mode_multiplayer(self):
        self.logging.new()
        self.py_chess = chess.Board()  

        self.game.mode = 'multiplayer'
        self.game.own_color = 'white' 
        self.game.current_color = 'white'
        self.multiplayer.setup = True

        self.game.setup() #make sure its after so the game initialization values have been set #change

    def mode_puzzles(self, reset=False):
        
        self.random_puzzle = random.choice(self.puzzle_data) if not reset else reset.copy()

        while int(self.random_puzzle['Rating']) < 1000: 
            self.random_puzzle = random.choice(self.puzzle_data) if not reset else reset.copy()


        self.moves = list(self.random_puzzle["Moves"])
        print(self.moves, self.random_puzzle["Rating"])

        
        self.game.highlighted_squares.clear()
        self.py_chess = chess.Board(fen=self.random_puzzle["FEN"])  
        ranks, active_color, castling, en_passant, halfmove_clock, fullmove_number = self.random_puzzle["FEN"].split()

        self.game.mode = 'puzzles'
        self.game.current_color = 'white' if active_color == 'w' else 'black'
        self.game.own_color = 'white' if self.game.current_color == 'black' else 'black' #set to opposite of current color
        self.game.puzzle_user_correct = None

        self.game.setup(self.random_puzzle["FEN"])



    def mode_analyzer(self):
        self.analyzer.load_data()
        analysis_thread = threading.Thread(target=self.analyzer.analyze)

        analysis_thread.start()



        # Adjust Tic-Tac-Toe board size and position
        BOARD_SIZE = min(WINDOW_WIDTH, WINDOW_HEIGHT) * 0.8
        BOARD_X = (WINDOW_WIDTH - BOARD_SIZE) // 2
        BOARD_Y = (WINDOW_HEIGHT - BOARD_SIZE) // 2

        CELL_SIZE = BOARD_SIZE // 3
        LINE_COLOR = (255, 255, 255)
        LINE_WIDTH = 4

        x_image = pygame.image.load(r"assets\images\tictactoe\x.png")
        o_image = pygame.image.load(r"assets\images\tictactoe\o.png")
        x_image = pygame.transform.scale(x_image, (CELL_SIZE, CELL_SIZE))
        o_image = pygame.transform.scale(o_image, (CELL_SIZE, CELL_SIZE))

        grid = [['' for _ in range(3)] for _ in range(3)]

        def draw_grid():
            for i in range(1, 3):
                pygame.draw.line(self.screen, LINE_COLOR, (BOARD_X, BOARD_Y + i * CELL_SIZE), (BOARD_X + BOARD_SIZE, BOARD_Y + i * CELL_SIZE), LINE_WIDTH)
                pygame.draw.line(self.screen, LINE_COLOR, (BOARD_X + i * CELL_SIZE, BOARD_Y), (BOARD_X + i * CELL_SIZE, BOARD_Y + BOARD_SIZE), LINE_WIDTH)

        def draw_symbols():
            for row in range(3):
                for col in range(3):
                    if grid[row][col] == 'X':
                        self.screen.blit(x_image, (BOARD_X + col * CELL_SIZE, BOARD_Y + row * CELL_SIZE))
                    elif grid[row][col] == 'O':
                        self.screen.blit(o_image, (BOARD_X + col * CELL_SIZE, BOARD_Y + row * CELL_SIZE))

        def check_game_over():
            # Check for winning conditions
            for row in range(3):
                if grid[row][0] == grid[row][1] == grid[row][2] != '':
                    return True
            for col in range(3):
                if grid[0][col] == grid[1][col] == grid[2][col] != '':
                    return True
            if grid[0][0] == grid[1][1] == grid[2][2] != '':
                return True
            if grid[0][2] == grid[1][1] == grid[2][0] != '':
                return True

            # Check for a draw
            if all(grid[row][col] != '' for row in range(3) for col in range(3)):
                return True

            return False

        def clear_board():
            for row in range(3):
                for col in range(3):
                    grid[row][col] = ''

        def handle_events():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        if BOARD_X <= x <= BOARD_X + BOARD_SIZE and BOARD_Y <= y <= BOARD_Y + BOARD_SIZE:
                            row = int((y - BOARD_Y) // CELL_SIZE)
                            col = int((x - BOARD_X) // CELL_SIZE)
                            if grid[row][col] == '':
                                grid[row][col] = 'X'
                                if check_game_over():
                                    draw_grid()
                                    draw_symbols()
                                    pygame.display.update()
                                    time.sleep(1)
                                    clear_board()
                                else:
                                    draw_grid()
                                    draw_symbols()
                                    pygame.display.update()
                                    time.sleep(1)
                                    make_computer_move()

        def make_computer_move():
            # Find all available legal moves
            available_moves = []
            for row in range(3):
                for col in range(3):
                    if grid[row][col] == '':
                        available_moves.append((row, col))

            if available_moves:
                # Choose a random move from the available legal moves
                random_move = random.choice(available_moves)
                row, col = random_move
                grid[row][col] = 'O'

        while analysis_thread.is_alive():
            handle_events()
            self.screen.blit(self.background, (0, 0))
            draw_grid()
            draw_symbols()


            join_game_text = medium_font.render("Your Game Is Being Analyzed. Play Tic-Tac-Toe While You Wait!", True, (255, 255, 255))
            text_rect = join_game_text.get_rect()
            text_rect.centerx = self.screen.get_width() // 2
            text_rect.y = self.screen.get_rect().y
            self.screen.blit(join_game_text, text_rect)
            pygame.display.update()



        self.py_chess = chess.Board()  

        self.game.mode = 'analyzer'
        self.game.own_color = 'white'
        self.game.current_color = 'white'
        self.game.setup()




    def computer_process(self):
        best_move = self.computer.best_move(self.py_chess.fen())



        initial_row, initial_col, final_row, final_col = self.game.uci_to_rowcol(best_move)

        if self.game.own_color == 'black': #changed
            initial_row = 7 - initial_row
            final_row = 7 - final_row




        initial = Square(initial_row, initial_col)
        final = Square(final_row, final_col)
        move = Move(initial, final)

        initial_square = self.game.board.squares[move.initial.row][move.initial.col] #changed
        piece = initial_square.piece


        old_fen = self.py_chess.fen()
        self.game.board.move(piece, move, self.py_chess.fen())

        uci_format = chess.Move.from_uci(best_move)
        is_capture = self.py_chess.is_capture(uci_format)

        self.py_chess.push(uci_format)
        self.logging.add(old_fen, self.py_chess.fen(), best_move)
        self.sound.play(check=self.py_chess.is_check(), capture=is_capture, mate='lost' if self.py_chess.is_checkmate() else None)

    def computer_puzzle_process(self): 

        move = self.moves[0]
        uci_format = chess.Move.from_uci(move)



        

        self.moves.pop(0)
        initial_row, initial_col, final_row, final_col = self.game.uci_to_rowcol(move)

        if self.game.own_color == 'black': #changed
            initial_row = 7 - initial_row
            final_row = 7 - final_row


        time.sleep(0.85)
        initial = Square(initial_row, initial_col)
        final = Square(final_row, final_col)
        move = Move(initial, final)

        initial_square = self.game.board.squares[move.initial.row][move.initial.col]
        piece = initial_square.piece

        is_capture = self.py_chess.is_capture(uci_format)
        self.game.board.move(piece, move, self.py_chess.fen())    
        self.py_chess.push(uci_format)
        self.sound.play(check=self.py_chess.is_check(), capture=is_capture, mate=None)
        self.game.highlighted_squares.clear()

        self.game.puzzle_user_correct = None  

    def incorrect_puzzle(self, piece, initial_row, initial_col, released_row, released_col):
        initial = Square(initial_row, initial_col)
        final = Square(released_row, released_col)

        move = Move(initial, final)
        self.game.board.puzzle_move(piece, move)
        self.game.add_highlight(initial_row, initial_col, 'puzzle_incorrect')
        self.game.add_highlight(released_row, released_col, 'puzzle_incorrect')
   
    def multiplayer_host(self):
        self.logging.new()
        self.py_chess = chess.Board() 

        self.game.mode = 'multiplayer' 
        self.game.own_color = 'white' 
        self.game.current_color = 'white'
        self.multiplayer.setup = True


        #SHOW PASSWORD/CODE
        self.screen.blit(self.background, (0, 0))
        join_game_text = large_font.render(str(int(netaddr.IPAddress(str(socket.gethostbyname(socket.gethostname()))))), True, (255, 255, 255))
        text_rect = join_game_text.get_rect()
        text_rect.center = self.screen.get_rect().center
        self.screen.blit(join_game_text, text_rect)
        pygame.display.update()




        self.game.setup()
        self.multiplayer.host_setup()

    def multiplayer_user(self):
        self.logging.new()
        self.py_chess = chess.Board() 

        self.game.mode = 'multiplayer' 
        self.game.own_color = 'black' 
        self.game.current_color = 'white'
        self.multiplayer.setup = True


        password = "Type Code Given:"
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:

                    if password == "Type Code Given:":
                        password = ""

                    if event.key == pygame.K_RETURN:
                        if len(password) == 10:
                            running = False

                    elif event.key == pygame.K_BACKSPACE:
                        print(password)
                        password = password[:-1]

                    elif event.key in [pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                        if len(password) < 10:
                            password += str(event.key - pygame.K_0)


            self.screen.blit(self.background, (0, 0))
            password_text = password.replace("", " ")[1:-1] if password != 'Type Code Given:' else password
            password_rendered = large_font.render(password_text, True, (255, 255, 255))
            password_rect = password_rendered.get_rect()
            password_rect.center = self.screen.get_rect().center
            self.screen.blit(password_rendered, password_rect)
            pygame.display.update()

        time.sleep(0.3)

        self.screen.blit(self.background, (0, 0))
        password_rendered = large_font.render('Connecting To Host...', True, (255, 255, 255))
        password_rect = password_rendered.get_rect()
        password_rect.center = self.screen.get_rect().center
        self.screen.blit(password_rendered, password_rect)

        pygame.display.update()

        self.game.setup()
        self.multiplayer.user_setup(getpass.getuser().split()[0], password)

    def showing(self):
        """
        Shows the game.
        """
        self.screen.blit(self.background, (0, 0))
        
        self.game.show_background(self.screen)
        self.game.show_last_move(self.screen)
        self.game.show_highlight(self.screen)
        self.game.show_moves(self.screen)
        self.game.show_pieces(self.screen)
        self.game.show_hover(self.screen)

        self.game.game_ui(self.screen)
        self.game.puzzle_ui(self.screen)
        self.game.multiplayer_ui(self.screen)


    def mainloop(self):
        while True:

            while self.game.mode is None: #HOME SCREEN
                self.home.home(self.screen)
                self.clock.tick(60)

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:


                        #pygame.Rect(268, 260, 209, 85)
                        if pygame.Rect(268, 260, 209, 85).collidepoint(event.pos):
                            self.multiplayer_user()
                        if pygame.Rect(268, 365, 209, 85).collidepoint(event.pos):
                            self.multiplayer_host()


                        if pygame.Rect(760, 260, 209, 190).collidepoint(event.pos):
                            self.mode_computer()


                        if pygame.Rect(268, 505, 209, 190).collidepoint(event.pos):
                            self.mode_puzzles()


                        if pygame.Rect(760, 505, 209, 85).collidepoint(event.pos):
                            self.mode_analyzer()
                        if pygame.Rect(760, 610, 209, 85).collidepoint(event.pos):
                            self.mode_training()





                pygame.display.flip()
                

            screen = self.screen
            game = self.game
            board = self.game.board
            dragger = self.game.dragger
            computer = self.computer
            logging = self.logging
            py_chess = self.py_chess
            multiplayer = self.multiplayer


            if(game.mode == 'multiplayer' and game.current_color == game.own_color and multiplayer.new_move): #IF NEW MOVE INCOMING FROM OTHER PLAYER
                initial_row, initial_col, final_row, final_col = self.game.uci_to_rowcol(multiplayer.move)
                if self.game.own_color == 'black':
                    initial_row = 7 - initial_row
                    final_row = 7 - final_row


                initial = Square(initial_row, initial_col)
                final = Square(final_row, final_col)
                move = Move(initial, final)

                old_fen = self.py_chess.fen()
                
                initial_square = self.game.board.squares[move.initial.row][move.initial.col] #changed
                piece = initial_square.piece

                self.game.board.move(piece, move, self.py_chess.fen())

                uci_format = chess.Move.from_uci(multiplayer.move)
                is_capture = self.py_chess.is_capture(uci_format)

                self.py_chess.push(uci_format)
                self.logging.add(old_fen, self.py_chess.fen(), multiplayer.move)
                self.sound.play(check=self.py_chess.is_check(), capture=is_capture, mate='lost' if self.py_chess.is_checkmate() else None)

                multiplayer.new_move = False
                self.showing()
                
            if (game.mode == 'puzzles' and game.current_color == game.own_color) or (game.mode == 'computer' and game.current_color == game.own_color) or (game.mode == 'multiplayer' and game.current_color == game.own_color): #MAIN INTERACTION


                if len(game.premoves) > 0 and threading.active_count() == 2:
                    uci_move = game.premoves.pop(0)


                    if not computer.is_valid_move(py_chess.fen(), uci_move):
                        game.premoves.clear()
                        game.highlighted_squares.clear()
                        continue


                    initial_row, initial_col, final_row, final_col = game.uci_to_rowcol(uci_move)

                    if game.own_color == 'black':
                        initial_row = 7 - initial_row
                        final_row = 7 - final_row


                    initial = Square(initial_row, initial_col)
                    final = Square(final_row, final_col)
                    rowcol_move = Move(initial, final)
                    
                    initial_square = game.board.squares[rowcol_move.initial.row][rowcol_move.initial.col] 

                    piece = initial_square.piece


                    is_capture = self.py_chess.is_capture(uci_format)
                    board.move(piece, rowcol_move, py_chess.fen())
                    py_chess.push(chess.Move.from_uci(uci_move))

                    if self.py_chess.is_checkmate():
                        pass

                    self.sound.play(check=self.py_chess.is_check(), capture=is_capture, mate='won' if self.py_chess.is_checkmate() else None)

                    if game.mode == 'multiplayer':
                        multiplayer.send(uci_move)

                    game.highlighted_squares.remove((initial_row, initial_col, 'premove'))
                    game.highlighted_squares.remove((final_row, final_col, 'premove'))

                    self.showing()
                    game.next_turn()
                    continue
                     
                if dragger.dragging:
                    dragger.update_blit(screen)

                for event in pygame.event.get():

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse((event.pos[0], event.pos[1] - (WINDOW_HEIGHT-HEIGHT)//2))
                        clicked_row = dragger.mouseY // SQUARE_SIZE
                        clicked_col = dragger.mouseX // SQUARE_SIZE       

                        if game.own_color == 'black':
                            clicked_row = clicked_row     
       

                        #LEFT CLICK 
                        if event.button == 1 and clicked_row >= 0 and clicked_col < 8 and clicked_row < 8:



                            #clear highlights
                            game.premoves.clear()
                            game.highlighted_squares.clear()
                            
                            #if the clicked square contains a piece
                            if board.squares[clicked_row][clicked_col].has_piece():


                                piece = board.squares[clicked_row][clicked_col].piece
                                if piece.color == game.own_color:

                            
                                    board.calculate_moves(py_chess.fen(), clicked_row, clicked_col, piece)   


                                    dragger.save_initial((event.pos[0], event.pos[1] - (WINDOW_HEIGHT-HEIGHT)//2))
                                    dragger.drag_piece(piece)

                                    game.add_highlight(clicked_row, clicked_col, 'selection')

                                    self.showing()



                        #RIGHT CLICK 
                        elif event.button == 3 and clicked_row >= 0 and clicked_col < 8 and clicked_row < 8:        
                            if (clicked_row, clicked_col, 'highlight') not in game.highlighted_squares:
                                game.add_highlight(clicked_row, clicked_col, 'highlight')
                            else:
                                game.remove_highlight(clicked_row, clicked_col, 'highlight')


                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_highlight(screen)
                            game.show_pieces(screen)

                    elif event.type == pygame.MOUSEMOTION and event.pos[1] > (WINDOW_HEIGHT-HEIGHT)//2 and event.pos[1] < WINDOW_HEIGHT - (WINDOW_HEIGHT-HEIGHT)//2:
                        motion_row = (event.pos[1] - (WINDOW_HEIGHT-HEIGHT)//2) // SQUARE_SIZE
                        motion_col = event.pos[0] // SQUARE_SIZE
                        game.set_hover(motion_row, motion_col)

                        if dragger.dragging:
                            dragger.update_mouse((event.pos[0], event.pos[1] - (WINDOW_HEIGHT-HEIGHT)//2))
                            dragger.update_blit(screen)
                            


                    elif event.type == pygame.MOUSEBUTTONUP:

                        if dragger.dragging:
                            dragger.update_mouse((event.pos[0], event.pos[1] - (WINDOW_HEIGHT-HEIGHT)//2))

                            released_row = dragger.mouseY // SQUARE_SIZE
                            released_col = dragger.mouseX // SQUARE_SIZE


                            initial = Square(dragger.initial_row, dragger.initial_col) #change?
                            final = Square(released_row, released_col)


                            
                            move = Move(initial, final)
                            #premove


                            if threading.active_count() > 2: #adding premoves while computer is thinking

                                if not(dragger.initial_row == released_row and dragger.initial_col == released_col):
                                    game.add_highlight(dragger.initial_row, dragger.initial_col, 'premove')
                                    game.add_highlight(released_row, released_col, 'premove')
                                    game.premoves.append(game.rowcol_to_uci(dragger.initial_row, dragger.initial_col, released_row, released_col))
                                    dragger.undrag_piece()
                                    continue
                            
                            elif not (board.valid_move(dragger.piece, move)) and initial != final:
                                dragger.undrag_piece()

                            elif (board.valid_move(dragger.piece, move) and game.mode == 'computer'): 
                                board.move(dragger.piece, move, py_chess.fen())

                                if game.own_color == 'black':
                                    move = game.rowcol_to_uci(7 - dragger.initial_row, dragger.initial_col, 7 - released_row, released_col) 
                                else:
                                    move = game.rowcol_to_uci(dragger.initial_row, dragger.initial_col, released_row, released_col) 



                                uci_format = chess.Move.from_uci(move)
                                old_fen = py_chess.fen()
                                is_capture = self.py_chess.is_capture(uci_format)

                                dragger.undrag_piece()


                                py_chess.push(uci_format)
                                threading.Thread(name='logging Add Thread', target=logging.add, args=(old_fen, py_chess.fen(), move)).start()
                                self.sound.play(check=self.py_chess.is_check(), capture=is_capture, mate='won' if self.py_chess.is_checkmate() else None)
                                self.showing()
                                game.next_turn() 

                            elif(board.valid_move(dragger.piece, move) and game.mode == 'multiplayer'): 
                                board.move(dragger.piece, move, py_chess.fen())

                                if game.own_color == 'black':
                                    move = game.rowcol_to_uci(7 - dragger.initial_row, dragger.initial_col, 7 - released_row, released_col) 
                                else:
                                    move = game.rowcol_to_uci(dragger.initial_row, dragger.initial_col, released_row, released_col) 


                                uci_format = chess.Move.from_uci(move)
                                old_fen = py_chess.fen()
                                is_capture = self.py_chess.is_capture(uci_format)


                                py_chess.push(uci_format)
                                
                                multiplayer.send(move)
                                dragger.undrag_piece()
                                threading.Thread(name='logging Add Thread', target=logging.add, args=(old_fen, py_chess.fen(), move)).start()
                                self.sound.play(check=self.py_chess.is_check(), capture=is_capture, mate='won' if self.py_chess.is_checkmate() else None)
                                self.showing()
                                game.next_turn() 

                            elif (board.valid_move(dragger.piece, move) and game.mode == 'puzzles'):

                                if game.rowcol_to_uci(dragger.initial_row, dragger.initial_col, released_row, released_col) == self.moves[0] and game.own_color == 'white' or game.rowcol_to_uci(7 - dragger.initial_row, dragger.initial_col, 7 - released_row, released_col) == self.moves[0] and game.own_color == 'black':
                                    uci_format = chess.Move.from_uci(self.moves[0])
                                    self.moves.pop(0)

                                    is_capture = self.py_chess.is_capture(uci_format)
                                    py_chess.push(uci_format)

                                    board.move(dragger.piece, move, py_chess.fen())
                                    move = game.rowcol_to_uci(dragger.initial_row, dragger.initial_col, released_row, released_col)

                                    
                                    game.add_highlight(dragger.initial_row, dragger.initial_col, 'puzzle_user_correct')
                                    game.add_highlight(released_row, released_col, 'puzzle_user_correct')

                                    dragger.undrag_piece()

                                    self.sound.play(check=py_chess.is_check(), capture=is_capture, mate=None)

                                




                                    self.showing()
                                    game.next_turn()

                                else:
                                    t = threading.Thread(name='Puzzle Incorrect Thread', target=self.incorrect_puzzle, args=(dragger.piece, dragger.initial_row, dragger.initial_col, released_row, released_col))
                                    t.start()
                                    dragger.undrag_piece()
                                    game.puzzle_user_correct = False    

                            


                        if pygame.Rect(WIDTH + 30, HEIGHT - 35, (WINDOW_WIDTH-WIDTH) - 60, 50).collidepoint(event.pos) and game.mode == 'puzzles':
                            self.mode_puzzles(self.random_puzzle)

                        elif pygame.Rect(WIDTH + 30, HEIGHT - 95, (WINDOW_WIDTH-WIDTH) - 60, 50).collidepoint(event.pos) and game.puzzle_user_correct:


                            self.mode_puzzles()

                        elif pygame.Rect(WIDTH + 30, HEIGHT - 35, (WINDOW_WIDTH-WIDTH) - 60, 50).collidepoint(event.pos) and game.mode == 'computer':
                            print('resign triggered')

                        elif pygame.Rect(WIDTH + 30, HEIGHT - 95, (WINDOW_WIDTH-WIDTH) - 60, 50).collidepoint(event.pos) and game.mode == 'puzzles':
                            threading.Thread(name='Puzzle Computer Process Thread', target=self.computer_puzzle_process).start()  
                            game.puzzle_correct = False
                            time.sleep(0.85)
                            game.next_turn()


                    #quit
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    





            elif game.mode == 'analyzer':

                with open(r'assets\data\analyzer.json', 'r') as f: moves = json.load(f)

                self.screen.blit(self.background, (0, 0))
                
                self.game.show_background(self.screen)
                self.game.show_last_move(self.screen)
                self.game.show_highlight(self.screen)
                self.game.show_moves(self.screen)
                self.game.show_pieces(self.screen)
                self.game.show_hover(self.screen)


                game.setup(moves[game.analysis_current_move][0]['FEN']) 
                transparent_surface = pygame.Surface(((WINDOW_WIDTH-WIDTH) - 30, HEIGHT), pygame.SRCALPHA)
                pygame.draw.rect(transparent_surface, (255, 255, 255, 40), pygame.Rect(0, 0, (WINDOW_WIDTH-WIDTH) - 30, HEIGHT), border_radius=10)
                screen.blit(transparent_surface, (WIDTH + 15, (WINDOW_HEIGHT - HEIGHT)//2))

                margin = 10
                rectangle_width = 205
                rectangle_x = WIDTH + 30


                font_size = 24
                font_color = pygame.Color('white')
                font = pygame.font.Font(None, font_size)


                text = moves[game.analysis_current_move][0]['Description']

                if text is not None:
                    print(text)
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
                    rectangle_y = 200
                    rectangle = pygame.Rect(rectangle_x, rectangle_y, rectangle_width, rectangle_height)

                    text_x = rectangle.centerx - rectangle_width // 2 + margin
                    text_y = rectangle.centery - text_height // 2 + margin - 10

                    pygame.draw.rect(screen, pygame.Color('grey'), rectangle)



                    for line in lines:
                        rendered_text = font.render(line, True, font_color)
                        screen.blit(rendered_text, (text_x, text_y))
                        text_y += line_height



                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()


                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT and game.analysis_current_move > 0:
                            game.analysis_current_move -= 1
                            game.highlighted_squares.clear()
 
                            

                        elif event.key == pygame.K_RIGHT and game.analysis_current_move < len(moves) - 1:
                                game.analysis_current_move += 1
                                game.highlighted_squares.clear()




                        
                        # elif event.key == pygame.K_RIGHT and game.analysis_current_move == len(moves) - 1 and not game.analysis_last_move_found:

                        #     py_chess.set_fen(moves[-1][0]['FEN'])
                        #     py_chess.push_uci(moves[-1][0]['Move'])


                        #     moves.append([{"Move":moves[-1][0]['Move'], "Best Move": moves[-1][0]['Move'], "Type": "Best Move", "Description": "And thats checkmate. Great Game!", "Accuracy": "100%", "FEN": py_chess.fen()}])
                        #     with open('assets/data/analyzer.json', 'w') as f: json.dump(moves, f)

                        #     game.analysis_current_move += 1
                        #     game.analysis_last_move_found = True

                        #     if self.py_chess.is_checkmate():
                        #         row, col, finalrow, finalcol = game.uci_to_rowcol(moves[-1][0]['Move'])
                        #         game.add_highlight(finalrow, finalcol, 'checkmate')

                        #         checkmate_color = 'black' if py_chess.turn else 'white'

                        #         if checkmate_color == 'white':
                        #             initial_row, initial_col, final_row, final_col = game.uci_to_rowcol('a1' + chess.square_name(py_chess.king(chess.BLACK)))
                        #             game.add_highlight(final_row, final_col, 'highlight')

                        #         else:
                        #             initial_row, initial_col, final_row, final_col = game.uci_to_rowcol('a1' + chess.square_name(py_chess.king(chess.WHITE)))
                        #             game.add_highlight(finalrow, final_col, 'highlight')

            elif(game.mode == 'computer' and game.current_color != game.own_color):

                    self.showing()
                    while threading.active_count() > 2: 
                        time.sleep(0.05)

                    threading.Thread(name='Computer Process', target=self.computer_process).start()
                    game.next_turn() 
                    self.showing()

            elif(game.mode == 'multiplayer' and game.current_color != game.own_color): #MULTIPLAYER OPPONENT MOVING
                threading.Thread(name='Multiplayer Host Actual', target=self.multiplayer.recv).start()
                game.next_turn()
                self.showing()

            elif (game.mode == 'puzzles' and game.current_color != game.own_color): #PUZZLE COMPUTER MOVING
                if len(self.moves) == 0:
                    game.puzzle_user_correct = True
                else:
                    threading.Thread(name='Puzzle Computer Process Thread', target=self.computer_puzzle_process).start()  
                game.next_turn()
                self.showing()



            pygame.display.update()
            if game.mode != 'analyser': self.showing()






if __name__ == "__main__":
    main = Main()
    main.mainloop()
