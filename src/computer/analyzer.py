import ujson as json
import multiprocessing
import chess
from pathlib import Path
from stockfish import Stockfish

class Analyzer:
    def __init__(self, stockfish_path, data_file):
        self.stockfish_path = Path(stockfish_path)
        self.data_file = Path(data_file)
        self.data = None
        self.fen_list = []
        self.move_list = []

    def load_data(self):
        with open(self.data_file, 'r') as file:
            self.data = json.load(file)
        self.fen_list = [move['old_fen'] for move in self.data['1']['moves']]
        self.move_list = [move['move'] for move in self.data['1']['moves']]

    @staticmethod
    def categorize_move(position, total_moves):
        if position == 0:
            return "Best Move"
        elif position <= total_moves * 0.1:
            return "Great"
        elif position <= total_moves * 0.25:
            return "Good"
        elif position <= total_moves * 0.75:
            return "Inaccuracy"
        elif position <= total_moves * 0.9:
            return "Mistake"
        else:
            return "Blunder"

    def process_fen(self, fen):
        stockfish = Stockfish(path=self.stockfish_path)
        stockfish.set_fen_position(fen)
        moves = stockfish.get_top_moves(10)
        
        total_moves = len(moves)
        result = []
        played_move = self.move_list[self.fen_list.index(fen)]
        found_move = False

        for position, move in enumerate(moves):
            if move['Move'] == played_move:
                accuracy = round((1 - position / total_moves) * 100, 2)



                result.append({"Move": move['Move'], "Best Move": moves[0]['Move'], "Type": self.categorize_move(position, total_moves), "Accuracy": accuracy, "FEN": fen})


                found_move = True

        if not found_move:
            result.append({"Move": move['Move'], "Type": "Blunder", "Accuracy": 0, "FEN": fen})

        if chess.Board(fen).legal_moves.count() == 1:
            result.append({"Move": move['Move'], "Type": "Forced", "Accuracy": 100, "FEN": fen})


        return result

    def analyze(self):
        with multiprocessing.Pool() as pool: 
            results = pool.map(self.process_fen, self.fen_list)

        print(results)

        with open('assets/data/analyzer.json', 'w') as f:
            json.dump(results, f)

        





