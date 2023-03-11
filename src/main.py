import os
#hides the super annoying welcome message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import math
import sys

from const import *
from game import Game
from square import Square
from move import Move


class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')

        self.game = Game()
  

    def mainloop(self):
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        
        while True:
            #showing
            game.show_background(screen)
            game.show_last_move(screen)
            game.show_highlight(screen)
            game.show_moves(screen)
            game.show_pieces(screen)

            game.show_hover(screen)

            
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


                            #for later use
                            print(dragger.initial_row, dragger.initial_col)
                            print(released_row, released_col)

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


            pygame.display.update()


main = Main()
main.mainloop()