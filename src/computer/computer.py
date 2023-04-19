import random
import time

from colorama import Fore
from stockfish import Stockfish

import chess
from src.chess.const import *

stockfish = Stockfish(path=r"src\computer\engine.exe")

class Computer:
    def __init__(self):
        pass

    def best_move(self, fen):
        '''
        Returns a uci-style move using stockfish 15.1.3 (ex. 'e2e4')
        '''

        stockfish.set_fen_position(fen)
        try:
            return stockfish.get_best_move_time(FIND_TIME) 
        except:
            print(Fore.BLUE + "CALCULATIONERROR", Fore.WHITE + "MOVE INVALID")

    def is_valid_move(self, fen, move):
        '''
        Checks if the uci-style move is valid (in list of valid moves)
        '''
        board = chess.Board(fen)
        legal_moves = [move.uci() for move in board.legal_moves]

        return True if move in legal_moves else False
    
    


