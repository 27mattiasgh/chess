from src.chess.const import *
from src.chess.piece import *
from src.chess.square import Square
from src.chess.move import Move
import time

import chess

class Board:
    def __init__(self, fen=None, own_color=None):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for row in range(ROWS)]
        
        self.last_move = None
        self.create()
        self.add_pieces(fen=fen, own_color=own_color)

        


    def move(self, piece, move):
        """
        Updates the internal board state (used to display board)
        """
        
        initial = move.initial
        final = move.final



        #console board move update
        self.squares[initial.row][initial.col].piece = None #changed
        self.squares[final.row][final.col].piece = piece #changed

    

        if isinstance(piece, Pawn):
            self.check_promote(piece, final)

        #for pawns
        piece.moved = True

        #clear valid moves
        piece.clear_moves()

        #set last move
        self.last_move = move

    def puzzle_move(self, piece, move):
        """
        Updates the internal board state (used to display board)
        """
        
        initial = move.initial
        final = move.final


        final_piece = self.squares[final.row][final.col].piece
        
        #console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        time.sleep(0.2)
        self.squares[initial.row][initial.col].piece = piece
        self.squares[final.row][final.col].piece = final_piece


        piece.moved = True
        piece.clear_moves()
        self.last_move = move



    def valid_move(self, piece, move):
        return move in piece.moves
    
    def check_promote(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)


    def calculate_moves(self, fen, initial_row, initial_col, piece):
        board = chess.Board(fen)

        for move in board.legal_moves:
            row_col = self.uci_to_rowcol(board.uci(move), piece.color)
            if row_col[0] == initial_row and row_col[1] == initial_col:
                initial = Square(initial_row, initial_col)
                final = Square(row_col[2], row_col[3])
                move = Move(initial, final)
                piece.add_move(move)



    def uci_to_rowcol(self, move, color):
        """Formats stockfish move values (uci) into pygame row col format """        

        key = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

        initial_col = key[move[0]]
        initial_row = int(move[1]) - 1

        final_col = key[move[2]]
        final_row = int(move[3]) - 1

        if color == 'white':
            initial_row = 7 - initial_row
            final_row = 7 - final_row

        return initial_row, initial_col, final_row, final_col


    def create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
    
    def add_pieces(self, fen=None, own_color=None):
        if fen:
            ranks, active_color, castling, en_passant, halfmove_clock, fullmove_number = fen.split()
            row = 7
            col = 0
            empty_squares = 0

            for rank_str in ranks.split('/'):
                for char in rank_str:
                    if char.isdigit():
                        num_empty_squares = int(char)
                        empty_squares += num_empty_squares
                        col += num_empty_squares
                    else:
                        if char == 'p':
                            piece = Pawn('black')
                        elif char == 'P':
                            piece = Pawn('white')
                        elif char == 'n':
                            piece = Knight('black')
                        elif char == 'N':
                            piece = Knight('white')
                        elif char == 'b':
                            piece = Bishop('black')
                        elif char == 'B':
                            piece = Bishop('white')
                        elif char == 'r':
                            piece = Rook('black')
                        elif char == 'R':
                            piece = Rook('white')
                        elif char == 'q':
                            piece = Queen('black')
                        elif char == 'Q':
                            piece = Queen('white')
                        elif char == 'k':
                            piece = King('black')
                        elif char == 'K':
                            piece = King('white')

                        if own_color == 'white':
                            self.squares[7 - row][col] = Square(row, col, piece)

                        if own_color == 'black':
                            self.squares[row][col] = Square(row, col, piece)
                        


                        col += 1
                row -= 1
                col = 0
                   
        else:
            for color in ('white', 'black'):

                if own_color == 'white': 
                    row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)
                else: 
                    row_pawn, row_other = (1, 0) if color == 'white' else (6, 7)

                #pawns 
                for col in range(COLS):
                    self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

                #knights
                self.squares[row_other][1] = Square(row_other, 1, Knight(color))
                self.squares[row_other][6] = Square(row_other, 6, Knight(color))

                #bishops
                self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
                self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

                #rooks
                self.squares[row_other][0] = Square(row_other, 0, Rook(color))
                self.squares[row_other][7] = Square(row_other, 7, Rook(color))

                #queen
                self.squares[row_other][3] = Square(row_other, 3, Queen(color))

                #king
                self.squares[row_other][4] = Square(row_other, 4, King(color))
                

