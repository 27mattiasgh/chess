import json
import random
import sys
import threading
import getpass
import time

import pygame


import chess

from src.chess.home import Home

from src.chess.const import *
from src.chess.game import Game
from src.chess.move import Move
from src.chess.sound import Sound
from src.chess.square import Square
from src.computer.analysis import Analysis
from src.computer.computer import Computer
from src.multiplayer.multiplayer import Multiplayer


class Main:
    def __init__(self):
        self.home = Home()
        self.game = Game()
        self.sound = Sound()
        self.analysis = Analysis()
        self.computer = Computer()
        self.multiplayer = Multiplayer()

        with open(r'assets\data\puzzles.json', 'r') as json_file: self.puzzle_data = json.load(json_file)
        
        

        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()


        self.background = pygame.transform.scale(pygame.image.load(r'assets\images\background.png'), (1000, 750))
        pygame.display.set_caption('Chess')


    def mode_computer(self):
        self.analysis.new()
        self.py_chess = chess.Board()  

        self.game.mode = 'computer'
        self.game.own_color = 'white'
        self.game.current_color = 'white'
        self.game.setup()

    def mode_multiplayer(self):
        self.analysis.new()
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
        self.game.puzzle_correct = None

        self.game.setup(self.random_puzzle["FEN"])





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
        self.game.board.move(piece, move)

        uci_format = chess.Move.from_uci(best_move)
        is_capture = self.py_chess.is_capture(uci_format)

        self.py_chess.push(uci_format)
        self.analysis.add(old_fen, self.py_chess.fen(), best_move)
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
        self.game.board.move(piece, move)    
        self.py_chess.push(uci_format)
        self.sound.play(check=self.py_chess.is_check(), capture=is_capture, mate=None)
        self.game.highlighted_squares.clear()

        self.game.puzzle_correct = None  

    def incorrect_puzzle(self, piece, initial_row, initial_col, released_row, released_col):
        initial = Square(initial_row, initial_col)
        final = Square(released_row, released_col)

        move = Move(initial, final)
        self.game.board.puzzle_move(piece, move)
        self.game.add_highlight(initial_row, initial_col, 'puzzle_incorrect')
        self.game.add_highlight(released_row, released_col, 'puzzle_incorrect')

    
    def multiplayer_host(self):
        self.analysis.new()
        self.py_chess = chess.Board() 

        self.game.mode = 'multiplayer' 
        self.game.own_color = 'white' 
        self.game.current_color = 'white'
        self.multiplayer.setup = True

        self.game.setup()
        self.multiplayer.host_setup()


    def multiplayer_user(self):
        self.analysis.new()
        self.py_chess = chess.Board() 

        self.game.mode = 'multiplayer' 
        self.game.own_color = 'black' 
        self.game.current_color = 'white'
        self.multiplayer.setup = True

        self.game.setup()
        self.multiplayer.user_setup(getpass.getuser().split()[0])



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

    def mainloop(self):
        while True:

            while self.game.mode is None:
                self.home.home(self.screen)
                self.clock.tick(60)

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:


                        if pygame.Rect(25, 230, 512, 300).collidepoint(event.pos):
                            self.multiplayer_user()






                pygame.display.flip()
                

            





            screen = self.screen
            game = self.game
            board = self.game.board
            dragger = self.game.dragger
            computer = self.computer
            analysis = self.analysis
            py_chess = self.py_chess
            multiplayer = self.multiplayer
            self.showing()

            if(game.mode == 'multiplayer' and game.current_color == game.own_color and multiplayer.new_move):
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

                self.game.board.move(piece, move)

                uci_format = chess.Move.from_uci(multiplayer.move)
                is_capture = self.py_chess.is_capture(uci_format)

                self.py_chess.push(uci_format)
                self.analysis.add(old_fen, self.py_chess.fen(), multiplayer.move)
                self.sound.play(check=self.py_chess.is_check(), capture=is_capture, mate='lost' if self.py_chess.is_checkmate() else None)

                multiplayer.new_move = False
                




            if (game.mode == 'puzzles' and game.current_color == game.own_color) or (game.mode == 'computer' and game.current_color == game.own_color) or (game.mode == 'multiplayer' and game.current_color == game.own_color):


                if len(game.premoves) > 0 and threading.active_count() == 1:
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
                    board.move(piece, rowcol_move)
                    py_chess.push(chess.Move.from_uci(uci_move))
                    self.sound.play(check=self.py_chess.is_check(), capture=is_capture, mate='won' if self.py_chess.is_checkmate() else None)

                    game.highlighted_squares.remove((initial_row, initial_col, 'premove'))
                    game.highlighted_squares.remove((final_row, final_col, 'premove'))

                    self.showing()
                    game.next_turn()
                    continue
                     
                if dragger.dragging:
                    dragger.update_blit(screen)

                for event in pygame.event.get():
                    #click
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

                    #mouse motion
                    elif event.type == pygame.MOUSEMOTION and event.pos[1] > (WINDOW_HEIGHT-HEIGHT)//2 and event.pos[1] < WINDOW_HEIGHT - (WINDOW_HEIGHT-HEIGHT)//2:
                        motion_row = (event.pos[1] - (WINDOW_HEIGHT-HEIGHT)//2) // SQUARE_SIZE
                        motion_col = event.pos[0] // SQUARE_SIZE

                        game.set_hover(motion_row, motion_col)
                        if dragger.dragging:
                            dragger.update_mouse((event.pos[0], event.pos[1] - (WINDOW_HEIGHT-HEIGHT)//2))
                            self.showing()

                            dragger.update_blit(screen)
                            
                    #click release
                    elif event.type == pygame.MOUSEBUTTONUP:

                        if dragger.dragging:
                            dragger.update_mouse((event.pos[0], event.pos[1] - (WINDOW_HEIGHT-HEIGHT)//2))

                            released_row = dragger.mouseY // SQUARE_SIZE
                            released_col = dragger.mouseX // SQUARE_SIZE


                            initial = Square(dragger.initial_row, dragger.initial_col) #change?
                            final = Square(released_row, released_col)


                            
                            move = Move(initial, final)
                            #premove


                            if threading.active_count() > 1: #adding premoves while computer is thinking

                                if not(dragger.initial_row == released_row and dragger.initial_col == released_col):
                                    game.add_highlight(dragger.initial_row, dragger.initial_col, 'premove')
                                    game.add_highlight(released_row, released_col, 'premove')
                                    game.premoves.append(game.rowcol_to_uci(dragger.initial_row, dragger.initial_col, released_row, released_col))
                                    dragger.undrag_piece()
                                    self.showing()
                                    continue
                            

                            elif (board.valid_move(dragger.piece, move) and game.mode == 'computer'): 
                                board.move(dragger.piece, move)

                                if game.own_color == 'black':
                                    move = game.rowcol_to_uci(7 - dragger.initial_row, dragger.initial_col, 7 - released_row, released_col) 
                                else:
                                    move = game.rowcol_to_uci(dragger.initial_row, dragger.initial_col, released_row, released_col) 



                                uci_format = chess.Move.from_uci(move)
                                old_fen = py_chess.fen()
                                is_capture = self.py_chess.is_capture(uci_format)



                                py_chess.push(uci_format)
                                threading.Thread(name='analysis Add Thread', target=analysis.add, args=(old_fen, py_chess.fen(), move)).start()
                                self.sound.play(check=self.py_chess.is_check(), capture=is_capture, mate='won' if self.py_chess.is_checkmate() else None)
                                self.showing()
                                game.next_turn() 

                            elif(board.valid_move(dragger.piece, move) and game.mode == 'multiplayer'): 
                                board.move(dragger.piece, move)

                                if game.own_color == 'black':
                                    move = game.rowcol_to_uci(7 - dragger.initial_row, dragger.initial_col, 7 - released_row, released_col) 
                                else:
                                    move = game.rowcol_to_uci(dragger.initial_row, dragger.initial_col, released_row, released_col) 


                                uci_format = chess.Move.from_uci(move)
                                old_fen = py_chess.fen()
                                is_capture = self.py_chess.is_capture(uci_format)


                                py_chess.push(uci_format)
                                
                                multiplayer.send(move)

                                threading.Thread(name='analysis Add Thread', target=analysis.add, args=(old_fen, py_chess.fen(), move)).start()
                                self.sound.play(check=self.py_chess.is_check(), capture=is_capture, mate='won' if self.py_chess.is_checkmate() else None)
                                self.showing()
                                game.next_turn() 


                            elif (board.valid_move(dragger.piece, move) and game.mode == 'puzzles'):

                                if game.rowcol_to_uci(dragger.initial_row, dragger.initial_col, released_row, released_col) == self.moves[0] and game.own_color == 'white' or game.rowcol_to_uci(7 - dragger.initial_row, dragger.initial_col, 7 - released_row, released_col) == self.moves[0] and game.own_color == 'black':
                                    uci_format = chess.Move.from_uci(self.moves[0])
                                    self.moves.pop(0)

                                    is_capture = self.py_chess.is_capture(uci_format)
                                    py_chess.push(uci_format)

                                    board.move(dragger.piece, move)
                                    move = game.rowcol_to_uci(dragger.initial_row, dragger.initial_col, released_row, released_col)

                                    
                                    game.add_highlight(dragger.initial_row, dragger.initial_col, 'puzzle_correct')
                                    game.add_highlight(released_row, released_col, 'puzzle_correct')


                                    self.sound.play(check=py_chess.is_check(), capture=is_capture, mate=None)

                                    self.showing()
                                    game.next_turn()

                                else:
                                    t = threading.Thread(name='Puzzle Incorrect Thread', target=self.incorrect_puzzle, args=(dragger.piece, dragger.initial_row, dragger.initial_col, released_row, released_col))
                                    t.start()
                                    game.puzzle_correct = False           
                            dragger.undrag_piece()


                        if pygame.Rect(WIDTH + 30, HEIGHT - 35, (WINDOW_WIDTH-WIDTH) - 60, 50).collidepoint(event.pos) and game.mode == 'puzzles':
                            self.mode_puzzles(self.random_puzzle)

                        elif pygame.Rect(WIDTH + 30, HEIGHT - 95, (WINDOW_WIDTH-WIDTH) - 60, 50).collidepoint(event.pos) and game.puzzle_correct:
                            self.mode_puzzles()

                        elif pygame.Rect(WIDTH + 30, HEIGHT - 35, (WINDOW_WIDTH-WIDTH) - 60, 50).collidepoint(event.pos) and game.mode == 'computer':
                            print('resign triggered')

                        elif pygame.Rect(WIDTH + 30, HEIGHT - 95, (WINDOW_WIDTH-WIDTH) - 60, 50).collidepoint(event.pos) and game.mode == 'puzzles':
                            threading.Thread(name='Puzzle Computer Process Thread', target=self.computer_puzzle_process).start()  
                            time.sleep(0.85)
                            game.next_turn() 

                        


                    #quit
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            elif(game.mode == 'computer' and game.current_color != game.own_color):

                    self.showing()
                    while threading.active_count() > 2: 
                        time.sleep(0.05)
                        self.showing()

                    threading.Thread(name='Computer Process', target=self.computer_process).start()
                    game.next_turn() 

            elif(game.mode == 'multiplayer' and game.current_color != game.own_color):
                threading.Thread(name='Multiplayer Host Actual', target=self.multiplayer.recv).start()
                game.next_turn()

            elif (game.mode == 'puzzles' and game.current_color != game.own_color):
                if len(self.moves) == 0:
                    game.puzzle_correct = True
                else:
                    threading.Thread(name='Puzzle Computer Process Thread', target=self.computer_puzzle_process).start()  
                game.next_turn()

            pygame.display.update()

main = Main()
main.mainloop()