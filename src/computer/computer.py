from src.game.const import *
import random
from stockfish import Stockfish
from colorama import Fore
import chess
import time
stockfish = Stockfish(path=r"src\computer\engine.exe")

class Computer:
    def __init__(self):
        pass

    def best_move(self, fen):
        '''
        Returns a uci-style move using stockfish 15.1.3 (ex. 'e2e4')
        '''

        if fen == 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1': #'e2e4
            return self.book_move(fen)

        stockfish.set_fen_position(fen)
        try:
            return stockfish.get_best_move_time(FIND_TIME) 
        except:
            print(Fore.BLUE + "CALCULATIONERROR", Fore.WHITE + "MOVE INVALID")


    def book_move(self, fen):
        '''
        Returns a completely random uci-style legal move. Should only be used for the opening.
        '''

        board = chess.Board(fen)
        legal_moves = [move.uci() for move in board.legal_moves]
        time.sleep(2) #seem like the computer "thought" of the move
        return random.choice(legal_moves)
    
    


