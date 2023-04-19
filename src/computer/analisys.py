import time
import json
import chess
import multiprocessing
from src.chess.const import *
from stockfish import Stockfish

board = chess.Board()
stockfish = Stockfish(path=r"src\computer\engine.exe")


#CLASSIFY MOVES:

#Brilliant - Shallow find doesn't it to be best move, but deep find does
#Great - Both deep and shallow find it to be best move
#Best - Shallow find it to be best move




class Analisys:
    def __init__(self):
        self.id = 1

        self.config_path = r'assets\data\config.json'
        self.game_path = r'assets\data\games.json'
        self.openings_path = r'assets\data\openings.json'
        self.puzzles_path = r'assets\data\puzzles.json'

        self.per_move_analisys = False


    def analyse(self):
        with open(self.game_path, 'r+') as f:
            data = json.load(f)

            # Create a process pool
            pool = multiprocessing.Pool()

            # Define the function to be mapped to each move in the pool
            func = self.accuracy

            # Use multiprocessing to parallelize the loop over moves
            results = pool.map(func, data[str(self.id)]['moves'])

            # Close the pool and wait for all processes to finish
            pool.close()
            pool.join()

            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

        print('Done!')



        #expands on the per-move analysis with longer think time 





    def accuracy(self, fen, move_played, bypass=False):
        '''
        Calculate the accuracy of the move. 
        '''
        if self.per_move_analisys or bypass:
            board = chess.Board(fen=fen)
            stockfish.set_fen_position(fen)

            legal_moves = board.legal_moves.count()
            top_moves = stockfish.get_top_moves(legal_moves)

            for i, move in enumerate(top_moves):
                if move_played == move['Move']:
                    return round(((legal_moves - i) / legal_moves) * 100, 1)
        return None

    def opening(self, move_number):
        with open(self.game_path, 'r') as f:
            data = json.load(f)

        book_move = False
        opening_name = None

        for game_id, game_data in data.items():
            if game_id == str(self.id):
                moves = [move['move'] for move in game_data['moves']]

                with open(self.openings_path, 'r') as json_file:
                    openings_data = json.load(json_file)

                    for opening in openings_data:
                        if opening['uci'] == moves:
                            opening_name = opening['name']
                            book_move = True
                            break


        if not opening_name:
            for move in reversed(data[str(self.id)]['moves']):
                    if move['opening'] is not None:
                        opening_name = move['opening'] 
                        break


        with open(self.game_path, 'r+') as f:
            data = json.load(f)

            for move in data[str(self.id)]['moves']: 
                if move['move_number'] == move_number:
                    move['opening'] = opening_name
                    if book_move: 
                        move['classification'] = 'book'
                    break

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)




    def new(self):
        '''
        Starts a new game in the games.json file.
        '''
        with open(self.game_path, 'r') as file:
            data = json.load(file)

        try: new_id = max(map(int, data.keys())) + 1
        except: new_id = 1
        self.id = new_id

        data[str(new_id)] = {"moves": []}
        with open(self.game_path, 'w') as file:
            json.dump(data, file)

    def add(self, old_fen, new_fen, move):
        '''
        Adds the move, current fen, and move accuracy (among others) to the game json file.
        '''
        stockfish.set_fen_position(old_fen)
        with open(self.game_path, 'r') as f:
            data = json.load(f)

        for game_id, game_data in data.items():
            if game_id == str(self.id):

                new_move = {
                    "move_number": len(game_data['moves']) + 1,
                    "move": move,
                    "old_fen": old_fen,
                    "new_fen": new_fen,

                    "opening": None,

                    "accuracy": self.accuracy(old_fen, move),
                    "classification": 'classification',

                    "shallow_evaluation": stockfish.get_best_move_time(EVALUATION_SHALLOW_FIND_TIME),
                    "deep_evaluation": stockfish.get_best_move_time(EVALUATION_DEEP_FIND_TIME),
                    }
                
                game_data['moves'].append(new_move)
                break


        with open(self.game_path, 'w') as f:
            json.dump(data, f, indent=2)
        self.opening(len(game_data['moves']))
    
        print('complete!')

