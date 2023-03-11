from const import *
from piece import *
from square import Square
from move import Move




class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]


        self.create()
        self.add_pieces('white')
        self.add_pieces('black')

    def calculate_moves(self, piece, row ,col):
        '''
        Calculates all possible/valid moves for a specific piece on a specific square
        '''

        def pawn_moves():
            steps = 1 if piece.moved else 2
            #vertical moves
            #it appears that the square is too far, but is 0 inclusive
            start = row + piece.direction
            end = row + (piece.direction * (1 + steps))
            for possible_move_row in range(start, end, piece.direction):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        #create inital/final move squares

                        initial = Square(row, col)
                        final = Square(possible_move_row, col)

                        move = Move(initial, final)
                        piece.add_move(move)
                    #blocked from moving to either squ
                    else:break
                #not in range
                else:break

            #diagonal moves
            possible_move_row = row + piece.direction
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        #create inital/final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)

                        move = Move(initial, final)
                        piece.add_move(move)

        def knight_moves():
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),]
 
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_col, possible_move_row):
    
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def straghtline_moves(increments):
            for increment in increments:
                row_increment, col_increment = increment
                possible_move_row = row + row_increment
                possible_move_col = col + col_increment

                while True:
                    if Square.in_range(possible_move_col, possible_move_row):
                        #create squares of the possible moves
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create a possible new move
                        move = Move(initial, final)


                        # empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                            #append new move
                            piece.add_move(move)
                            

                        # has enemy piece - break loop
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            #append new move
                            piece.add_move(move)
                            break

                        #has team piece - break loop
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                        #incrementing increments 
                        possible_move_row = possible_move_row + row_increment
                        possible_move_col = possible_move_col + col_increment

                    #break
                    else:break

        def king_moves():
            adj = [
                (row-1, col+0), # up
                (row-1, col+1), # up-right
                (row+0, col+1), # right
                (row+1, col+1), # down-right
                (row+1, col+0), # down
                (row+1, col-1), # down-left
                (row+0, col-1), # left
                (row-1, col-1), # up-left
            ]

            for possible_moves in adj:
                possible_move_row, possible_move_col = possible_moves

                if Square.in_range(possible_move_col, possible_move_row):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

            # castling moves

            #queen castling

            #king castling


        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straghtline_moves([
                (-1, +1), #upright
                (-1, -1), #upleft
                (1, 1), #downright
                (1, -1), #downleft
            ])

        elif isinstance(piece, Rook):
            straghtline_moves([
                (-1, 0), #up
                (0, 1), #right
                (1, 0), #down
                (0, -1), #left
            ])

        elif isinstance(piece, Queen): 
            straghtline_moves([
                (-1, +1), #upright
                (-1, -1), #upleft
                (1, 1), #downright
                (1, -1), #downleft
                (-1, 0), #up
                (0, 1), #right
                (1, 0), #down
                (0, -1) #left
            ])

        elif isinstance(piece, King): 
            king_moves()
        
    def create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)


    def add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

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




        






    