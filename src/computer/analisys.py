import json
import chess
from src.chess.const import *
from stockfish import Stockfish
stockfish = Stockfish(path=r"src\computer\engine.exe", parameters={"Threads": ANALISYS_THREADS, "Hash": ANALISYS_HASH})

class Analisys:
    def __init__(self):
        self.id = None

        self.config_path = r'assets\data\config.json'
        self.game_path = r'assets\data\games.json'
        self.openings_path = r'assets\data\openings.json'
        self.puzzles_path = r'assets\data\puzzles.json'


    def accuracy(self, fen, move_played):
        '''
        Calculate the accuracy of the move. NEEDS TO BE ADJUSTED
        '''

        board = chess.Board(fen=fen)
        stockfish.set_fen_position(fen)


        number_legal_moves = len(list(board.legal_moves))
        top_moves = stockfish.get_top_moves(number_legal_moves)

        for i, move in enumerate(top_moves, 1):
            if move['Move'] == move_played:
                return round((number_legal_moves - i + 1) / number_legal_moves * 100, 1)

    def opening(self, move_number):
        with open(self.game_path, 'r') as f:
            data = json.load(f)

        opening_name = None

        for game_id, game_data in data.items():
            if game_id == str(self.id):
                moves = [move['move'] for move in game_data['moves']]

                with open(self.openings_path, 'r') as json_file:
                    openings_data = json.load(json_file)

                    for opening in openings_data:
                        if opening['uci'] == moves:
                            opening_name = opening['name']
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
                    break

            f.seek(0)
            f.truncate()
            json.dump(data, f, indent=4)

    def new_game(self):
        '''
        Starts a new game in the games.json file.
        '''
        with open(self.game_path, 'r') as file:
            data = json.load(file)
        max_id = max(map(int, data.keys()))
        self.id = max_id
        data[str(max_id + 1)] = {"moves": []}
        with open(self.game_path, 'w') as file:
            json.dump(data, file)

    def add(self, fen, move):
        '''
        Adds the move, current fen, and move accuracy to the game json file.
        '''

        print('adding to file...')

        with open(self.game_path, 'r') as f:
            data = json.load(f)

        for game_id, game_data in data.items():
            if game_id == str(self.id):

                new_move = {
                    "move_number": len(game_data['moves']) + 1,
                    "move": move,
                    "fen": fen,
                    "accuracy": 0,
                    "opening": None
                }

                game_data['moves'].append(new_move)
                break


        with open(self.game_path, 'w') as f:
            json.dump(data, f, indent=2)
        self.opening(len(game_data['moves']))
        print('adding complete!')