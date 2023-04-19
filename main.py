import json
import random
import sys
import threading
import time

import pygame
from colorama import Fore
from stockfish import Stockfish

import chess
from src.chess.clock import Clock
from src.chess.const import *
from src.chess.game import Game
from src.chess.move import Move
from src.chess.square import Square
from src.computer.analisys import Analisys
from src.computer.computer import Computer
from src.multiplayer.multiplayer import Multiplayer
stockfish = Stockfish(path=r"src\computer\engine.exe", parameters={"Threads": THREADS, "Hash": HASH})

class Main:
    def __init__(self):

        print("attempting to load classes...")

        self.game = Game()
        self.clock = Clock()
        self.analisys = Analisys()
        self.computer = Computer()


        print("Loading PyGame...")
        self.mode_computer()

        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('MatiChess')
   
    def mode_computer(self):
        self.game.setup()
        self.analisys.new()

        self.clock.reset(110)
        threading.Thread(name='Clock', target=self.clock.start, daemon=True).start()
        

        self.game.mode = 'computer'
        self.game.next_color = 'white'
        self.py_chess = chess.Board()  

    def mode_puzzles(self):
        with open(r'assets\data\puzzles.json', 'r') as json_file:
            data = json.load(json_file)

        random_puzzle = random.choice(data)
        self.moves = random_puzzle["Moves"]
        print(self.moves)
        
        fen = random_puzzle["FEN"]
        self.game.setup(fen)
        self.game.mode = 'puzzles'
        self.game.next_color = 'white'
        self.next_puzzle_player = 'computer'

        self.py_chess = chess.Board(fen=fen)  
        ranks, active_color, castling, en_passant, halfmove_clock, fullmove_number = random_puzzle["FEN"].split()
        self.game.next_color = 'white' if active_color == 'w' else 'black'


    def computer_process(self):
        """
        Calculates, updates and displays the computer's move.
        """
        best_move = self.computer.best_move(self.py_chess.fen())
        initial_row, initial_col, final_row, final_col = self.game.uci_to_rowcol(best_move)

        initial = Square(initial_row, initial_col)
        final = Square(final_row, final_col)
        move = Move(initial, final)

        initial_square = self.game.board.squares[move.initial.row][move.initial.col]
        piece = initial_square.piece

        old_fen = self.py_chess.fen()
        self.game.board.move(piece, move)
        self.py_chess.push(chess.Move.from_uci(best_move))

        self.analisys.add(old_fen, self.py_chess.fen(), best_move)

        print(self.clock.active)
        print(self.clock.black)

    def computer_puzzle_process(self): 

        if len(self.moves) == 0: 
            self.showing()
            self.mode_puzzles()
            self.game.highlighted_squares.clear()
            self.showing()
            self.game.next_puzzle_turn()
            self.game.next_color_turn()

        move = self.moves[0]
        self.moves.pop(0)
        
        
        print(Fore.YELLOW + move, Fore.WHITE + self.py_chess.fen(), Fore.RED + 'COMPUTER PUZZLE')
        initial_row, initial_col, final_row, final_col = self.game.uci_to_rowcol(move)

        time.sleep(0.85)
        initial = Square(initial_row, initial_col)
        final = Square(final_row, final_col)
        move = Move(initial, final)

        initial_square = self.game.board.squares[move.initial.row][move.initial.col]
        piece = initial_square.piece
        self.game.board.move(piece, move)        

    def incorrect_puzzle(self, piece, initial_row, initial_col, released_row, released_col):
        initial = Square(initial_row, initial_col)
        final = Square(released_row, released_col)
        move = Move(initial, final)
        self.game.board.move(piece, move)
        self.game.add_highlight(initial_row, initial_col, 'puzzle_incorrect')
        self.game.add_highlight(released_row, released_col, 'puzzle_incorrect')


        time.sleep(0.15)

        initial = Square(released_row, released_col)
        final = Square(initial_row, initial_col)
        move = Move(initial, final)
        self.game.board.move(piece, move)  

        self.game.remove_highlight(initial_row, initial_col, 'puzzle_incorrect')  
        self.game.remove_highlight(released_row, released_col, 'puzzle_incorrect') 


    def gamestate(self, fen):
        self.py_chess.set_fen(fen)
        if self.py_chess.is_stalemate() and self.game.mode == 'computer':
            print(Fore.MAGENTA + "GAMESTATE", Fore.WHITE + "STALEMATE")
            pygame.quit()
            sys.exit()

        if self.py_chess.is_insufficient_material() and self.game.mode == 'computer':
            print(Fore.MAGENTA + "GAMESTATE", Fore.WHITE + "INSUFFICIENT MATERIAL")
            pygame.quit()
            sys.exit()

        if self.py_chess.is_checkmate() and self.game.mode == 'computer':
            print(Fore.MAGENTA + "GAMESTATE", Fore.WHITE + " CHECKMATE")
            pygame.quit()
            sys.exit()


        #timeout
        if self.clock.white <= 0 and self.game.mode == 'computer':
            print(Fore.MAGENTA + "GAMESTATE", Fore.WHITE + " WHITE TIMEOUT")
            pygame.quit()
            sys.exit()

        if self.clock.black <= 0 and self.game.mode == 'computer':
            print(Fore.MAGENTA + "GAMESTATE", Fore.WHITE + " BLACK TIMEOUT")
            pygame.quit()
            sys.exit()     

    def showing(self):
        """
        Shows the game.
        """
        self.screen.fill((128, 128, 128))
        
        self.game.show_background(self.screen)
        self.game.show_last_move(self.screen)
        self.game.show_highlight(self.screen)
        self.game.show_moves(self.screen)
        self.game.show_pieces(self.screen)
        self.game.show_hover(self.screen)

    def mainloop(self):
        """
        Main loop of the game.
        """

        while True:
            #need to keep inside while loop for board restarts to work
            screen = self.screen
            game = self.game
            clock = self.clock
            board = self.game.board
            dragger = self.game.dragger
            computer = self.computer
            analisys = self.analisys

            py_chess = self.py_chess

            #showing
            self.showing()
            self.gamestate(py_chess.fen())

            if (game.mode == 'puzzles' and game.next_puzzle_player == 'human') or (game.mode == 'computer' and game.next_player == 'human'):
                if game.premoves and threading.active_count() == 2:
                    uci_move = game.premoves.pop(0) #remove from premove list

                    if not computer.is_valid_move(py_chess.fen(), uci_move):
                        game.premoves.clear()
                        game.highlighted_squares.clear()
                        continue



                    initial_row, initial_col, final_row, final_col = game.uci_to_rowcol(uci_move)
                    initial = Square(initial_row, initial_col)
                    final = Square(final_row, final_col)
                    rowcol_move = Move(initial, final)

                    
                    initial_square = game.board.squares[rowcol_move.initial.row][rowcol_move.initial.col]
                    piece = initial_square.piece
                    board.move(piece, rowcol_move)
                    

                    
                    py_chess.push(chess.Move.from_uci(uci_move))
                    
                    print(Fore.YELLOW + uci_move, Fore.WHITE + py_chess.fen(), Fore.GREEN + 'HUMAN | PREMOVEMENT')

                    game.highlighted_squares.remove((initial_row, initial_col, 'premove'))
                    game.highlighted_squares.remove((final_row, final_col, 'premove'))

                    self.showing()
                    game.next_computer_turn() 
                    game.next_puzzle_turn()
                    continue
                     
                if dragger.dragging:
                    dragger.update_blit(screen)

                for event in pygame.event.get():
                    #click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        dragger.update_mouse((event.pos[0], event.pos[1] - (WINDOW_HEIGHT-HEIGHT)//2))
                        clicked_row = dragger.mouseY // SQU_SIZE
                        clicked_col = dragger.mouseX // SQU_SIZE                     

                        #LEFT CLICK 
                        if event.button == 1 and clicked_row >= 0 and clicked_col < 8 and clicked_row < 8:

                            #clear highlights
                            game.premoves.clear()
                            game.highlighted_squares.clear()
                            
                            #if the clicked square contains a piece
                            if board.squares[clicked_row][clicked_col].has_piece():

                                piece = board.squares[clicked_row][clicked_col].piece
                                if piece.color == game.next_color:
                            
                                    board.calculate_moves(piece, clicked_row, clicked_col)            
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
                        motion_row = (event.pos[1] - (WINDOW_HEIGHT-HEIGHT)//2) // SQU_SIZE
                        motion_col = event.pos[0] // SQU_SIZE

                        game.set_hover(motion_row, motion_col)
                        if dragger.dragging:
                            dragger.update_mouse((event.pos[0], event.pos[1] - (WINDOW_HEIGHT-HEIGHT)//2))
                            self.showing()

                            dragger.update_blit(screen)
                            
                    #click release
                    elif event.type == pygame.MOUSEBUTTONUP:


                        if dragger.dragging:
                            dragger.update_mouse((event.pos[0], event.pos[1] - (WINDOW_HEIGHT-HEIGHT)//2))



                            released_row = dragger.mouseY // SQU_SIZE
                            released_col = dragger.mouseX // SQU_SIZE

                            # create possible move
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)
                            move = Move(initial, final)


                            #premove
                            if threading.active_count() > 2: #makes sure you can only add premove during computer thinking time
                                if not(dragger.initial_row == released_row and dragger.initial_col == released_col):
                                    game.add_highlight(dragger.initial_row, dragger.initial_col, 'premove')
                                    game.add_highlight(released_row, released_col, 'premove')

                                    game.premoves.append(game.rowcol_to_uci(dragger.initial_row, dragger.initial_col, released_row, released_col))
                                    print('PREMOVE ADDED', dragger.initial_row, dragger.initial_col, released_row, released_col)
                                    dragger.undrag_piece()
                                    self.showing()
                                    continue


                            #if is valid move
                            
                            
                            elif (board.valid_move(dragger.piece, move) and game.mode == 'computer'): 
                                print('valid move')
                                board.move(dragger.piece, move)
                                move = game.rowcol_to_uci(dragger.initial_row, dragger.initial_col, released_row, released_col)

                                old_fen = py_chess.fen()
                                py_chess.push(chess.Move.from_uci(move))
                                print(Fore.YELLOW + move, Fore.WHITE + py_chess.fen(), Fore.GREEN + 'HUMAN')
                                threading.Thread(name='Analisys Add Thread', target=analisys.add, args=(old_fen, py_chess.fen(), move)).start()
                                self.showing()

                                game.next_computer_turn() 
                                clock.swtich(game.next_player)

                            elif (board.valid_move(dragger.piece, move) and game.mode == 'puzzles'):
                                
                                if game.rowcol_to_uci(dragger.initial_row, dragger.initial_col, released_row, released_col) == self.moves[0]:
                                    self.moves.pop(0)

                                    board.move(dragger.piece, move)
                                    move = game.rowcol_to_uci(dragger.initial_row, dragger.initial_col, released_row, released_col)

                                    
                                    print(Fore.YELLOW + move, Fore.WHITE + py_chess.fen(), Fore.GREEN + 'HUMAN PUZZLE')
                                    
                                    game.add_highlight(dragger.initial_row, dragger.initial_col, 'puzzle_correct')
                                    game.add_highlight(released_row, released_col, 'puzzle_correct')


                                    self.showing()
                                    game.next_color_turn() 
                                    game.next_puzzle_turn()


                                else:
                                    t = threading.Thread(name='Puzzle Incorrect Thread', target=self.incorrect_puzzle, args=(dragger.piece, dragger.initial_row, dragger.initial_col, released_row, released_col))
                                    t.start()
                                    
                        dragger.undrag_piece()

                    #quit
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

            elif (game.mode == 'computer' and game.next_player == 'computer'):
                    self.showing()
                    while threading.active_count() > 2: 
                        time.sleep(0.05)
                        self.showing()

                    threading.Thread(name='Computer Process', target=self.computer_process).start()
                    game.next_computer_turn() 
                    clock.swtich(game.next_player)

            elif (game.mode == 'puzzles' and game.next_puzzle_player == 'computer'):
                if len(self.moves) == 0:
                    self.computer_puzzle_process()  
                else:
                    self.t = threading.Thread(name='Puzzle Computer Process Thread', target=self.computer_puzzle_process)
                    self.t.start()    
                    game.next_color_turn()
                    game.next_puzzle_turn()
                
            pygame.display.update()

main = Main()
main.mainloop()