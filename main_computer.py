import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import sys
import pygame
import threading
from colorama import Fore

from src.game.const import *
from src.game.game import Game
from src.game.square import Square
from src.game.move import Move
from src.game.pgn import Pgn

from src.computer.computer import Computer

import chess
from stockfish import Stockfish

stockfish = Stockfish(path=r"src\computer\engine.exe", parameters={"Threads": THREADS, "Hash": HASH})


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('MatiChess')

        self.game = Game()
        self.Pgn = Pgn()
        self.computer = Computer()

        self.py_chess = chess.Board()
  
    def computer_process(self):
        #finds the best move in chess standard notation (e.g. a1-a8)
        best_move = self.computer.best_move(self.py_chess.fen())

        self.py_chess.push(chess.Move.from_uci(best_move))

        print(Fore.YELLOW + best_move, Fore.WHITE + self.py_chess.fen(), Fore.RED + 'COMPUTER')

        #translate the stockfish notation to the pychess notation (returns inital square and final square)
        initial_row, initial_col, final_row, final_col = self.Pgn.computer_to_rowcol(best_move)

        #edits Square values
        initial = Square(initial_row, initial_col)
        final = Square(final_row, final_col)

        #edits Move values
        move = Move(initial, final)


        #updates the values required to update the board
        initial_square = self.game.board.squares[move.initial.row][move.initial.col]
        piece = initial_square.piece
        self.game.board.move(piece, move)

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger
        pgn = self.Pgn

        while True:
            #showing
            game.show_background(screen)
            game.show_last_move(screen)
            game.show_highlight(screen)
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if game.next_player == 'white': #player move


                if dragger.dragging:
                    dragger.update_blit(screen)

                for event in pygame.event.get():
                    #click
                    if event.type == pygame.MOUSEBUTTONDOWN:


                        dragger.update_mouse(event.pos)
                        clicked_row = dragger.mouseY // SQU_SIZE
                        clicked_col = dragger.mouseX // SQU_SIZE

                        #LEFT CLICK
                        if event.button == 1:

                            #clear highlights
                            game.highlighted_squares.clear()

                            #if the clicked square contains a piece
                            if board.squares[clicked_row][clicked_col].has_piece():
                                piece = board.squares[clicked_row][clicked_col].piece
                                #check if valid piece(color)?
                                if piece.color == game.next_player:

                                    board.calculate_moves(piece, clicked_row, clicked_col)
                                    dragger.save_initial(event.pos)
                                    dragger.drag_piece(piece)

                                    game.show_background(screen)
                                    game.show_last_move(screen)
                                    game.show_moves(screen)
                                    game.show_pieces(screen)


                        #RIGHT CLICK
                        elif event.button == 3:

                            if (clicked_row, clicked_col) not in game.highlighted_squares:
                                game.add_highlight(clicked_row, clicked_col)
                            else:
                                game.remove_highlight(clicked_row, clicked_col)

                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_highlight(screen)
                            game.show_pieces(screen)

                    #mouse motion
                    elif event.type == pygame.MOUSEMOTION:
                        motion_row = event.pos[1] // SQU_SIZE
                        motion_col = event.pos[0] // SQU_SIZE
                        game.set_hover(motion_row, motion_col)

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)
                            #showing

                            game.show_background(screen)

                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)
                            game.show_hover(screen)

                            dragger.update_blit(screen)
                            
                    #click release
                    elif event.type == pygame.MOUSEBUTTONUP:

                        if dragger.dragging:
                            dragger.update_mouse(event.pos)


                            released_row = dragger.mouseY // SQU_SIZE
                            released_col = dragger.mouseX // SQU_SIZE


                            # create possible move
                            initial = Square(dragger.initial_row, dragger.initial_col)
                            final = Square(released_row, released_col)


                            move = Move(initial, final)

                            #if is valid move
                            if board.valid_move(dragger.piece, move):
                                board.move(dragger.piece, move)


                                move = pgn.rowcol_to_computer(dragger.initial_row, dragger.initial_col, released_row, released_col)
                                self.py_chess.push(chess.Move.from_uci(move))

                                print(Fore.YELLOW + move, Fore.WHITE + self.py_chess.fen(), Fore.GREEN + 'HUMAN')



                                #showing
                                game.show_background(screen)
                                game.show_last_move(screen)
                                game.show_pieces(screen)

                                #next turn
                                game.next_turn()


                        dragger.undrag_piece()

                    #quit
                    elif event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()


            elif game.next_player == 'black': #computer move
                t = threading.Thread(target=self.computer_process)
                t.start()



                game.next_turn()

            pygame.display.update()

main = Main()
main.mainloop()