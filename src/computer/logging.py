import time
import json
import chess
from src.chess.const import *
from stockfish import Stockfish

board = chess.Board()
try: stockfish = Stockfish(path=r"src\computer\stockfish executables\stockfish_15.1_avx2\stockfish-windows-2022-x86-64-avx2.exe")
except: stockfish = Stockfish(path=r"src\computer\stockfish executables\stockfish_15.1_popcnt\stockfish-windows-2022-x86-64-modern.exe")
    


#CLASSIFY MOVES:

#Brilliant - Shallow find doesn't it to be best move, but deep find does
#Great - Both deep and shallow find it to be best move
#Best - Shallow find it to be best move









class Logging:
    def __init__(self):
        self.id = 1

        self.config_path = r'assets\data\config.json'
        self.game_path = r'assets\data\games.json'
        self.openings_path = r'assets\data\openings.json'
        self.puzzles_path = r'assets\data\puzzles.json'



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

    def new(self, mode, own_color):
        '''
        Starts a new game in the games.json file.
        '''
        with open(self.game_path, 'r') as file:
            data = json.load(file)

        try: new_id = max(map(int, data.keys())) + 1
        except: new_id = 1
        self.id = new_id

        data[str(new_id)] = {"data":{'mode': mode, 'own_color': own_color}, "moves": []}
        with open(self.game_path, 'w') as file:
            json.dump(data, file)


    def log(self, mode, update_type):
        with open(self.config_path, 'r') as file: data = json.load(file)
        data[mode][update_type] += 1
        with open(self.config_path, 'w') as file: json.dump(data, file)










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
                    "accuracy": None,
                    "classification": None,

                    }
                
                game_data['moves'].append(new_move)
                break


        with open(self.game_path, 'w') as f:
            json.dump(data, f, indent=2)
        self.opening(len(game_data['moves']))