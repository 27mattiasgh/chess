import ujson as json
import multiprocessing
import chess
from pathlib import Path
from stockfish import Stockfish
import random
class Analyzer:
    def __init__(self, stockfish_path, data_file):
        self.stockfish_path = Path(stockfish_path)
        self.data_file = Path(data_file)
        self.data = None
        self.old_fen_list = []
        self.move_list = []

        self.best_move_descriptions = [
            "Incredible move! You've demonstrated exceptional tactical awareness.",
            "A masterstroke! Your move showcases deep understanding of the position.",
            "Genius move! You've outplayed your opponent with this brilliant choice.",
            "Flawless move! You're dominating the game with your exceptional play.",
            "Remarkable move! Your strategic insight is truly impressive.",
            "A superb move! You've seized a significant advantage in the position.",
            "Outstanding play! Your move sets up a powerful attack.",
            "Excellent decision! You've found the most promising continuation.",
            "A stunning move! You're showing great precision in your play.",
            "An amazing move! Your calculation skills are paying off handsomely."
        ]

        self.great_descriptions = [
            "Terrific move! Your positional understanding is top-notch.",
            "Impressive play! Your moves consistently show deep understanding.",
            "Excellent maneuver! Your grasp of strategy is highly commendable.",
            "Superb choice! Your positional play is a joy to behold.",
            "Splendid move! Your intuition in this game is truly remarkable.",
            "Great decision! Your moves consistently put pressure on your opponent.",
            "Well executed! Your play demonstrates a high level of competence.",
            "A commendable move! You're consistently making strong decisions.",
            "You're playing brilliantly! Your moves are filled with creativity.",
            "Masterful move! Your play exhibits a profound understanding of chess."
        ]

        self.good_descriptions = [
            "Solid move! You're steadily improving your position.",
            "Decisive play! Your moves are efficient and effective.",
            "Nice maneuver! Your strategic choices are paying off.",
            "Well done! Your consistent play is keeping the game balanced.",
            "Good decision! You're making smart moves to maintain control.",
            "Resolute move! Your play displays determination and focus.",
            "Capable choice! Your moves are proving to be well thought out.",
            "You're on the right track! Your play is solid and reliable.",
            "Impressive performance! Your moves reflect good judgment.",
            "Your play is commendable! You're making sensible decisions."
        ]

        self.inaccuracy_descriptions = [
            "A minor slip. You overlooked a slightly stronger move.",
            "A slight misstep. There was a more accurate option available.",
            "Not the most precise move. You missed a subtler possibility.",
            "A small deviation. Your move slightly weakens your position.",
            "A slight miscalculation. You could have gained a bit more.",
            "An imprecise move. Your decision could have been sharper.",
            "A minor error. Your move could have been a touch more optimal.",
            "You missed a small opportunity. Your move could have been stronger.",
            "A slight oversight. There was a more precise move to consider.",
            "A tiny inaccuracy. Your move doesn't fully exploit the position."
        ]

        self.mistake_descriptions = [
            "A regrettable mistake. You missed a significant chance.",
            "An unfortunate blunder. Your move hands the advantage to your opponent.",
            "A costly error. Your decision puts you on the back foot.",
            "A major oversight. Your move allows your opponent a strong counterplay.",
            "A critical mistake. Your position has been seriously compromised.",
            "A significant misjudgment. Your move leads to unfavorable consequences.",
            "A grave blunder. Your opponent now has a decisive advantage.",
            "A substantial mistake. Your move undermines your own position.",
            "A serious lapse. Your decision allows your opponent to seize control.",
            "A major misstep. Your move jeopardizes your chances of success."
        ]

        self.blunder_descriptions = [
            "A disastrous blunder! Your move is a catastrophic mistake.",
            "A fatal error. Your decision leads to an irreparable loss of material.",
            "A crushing blunder. Your position now teeters on the brink of collapse.",
            "A game-changing mistake. Your move completely turns the tables.",
            "An epic blunder. Your opponent must be ecstatic with this gift.",
            "A monumental error. Your move virtually hands the victory to your opponent.",
            "A colossal blunder. Your position now looks nearly hopeless.",
            "A catastrophic oversight. Your move leads to a quick and decisive defeat.",
            "A devastating blunder. Your chances of recovery are extremely slim.",
            "A horrendous mistake. Your move leaves you in an almost impossible situation."
        ]

        self.forced_descriptions = [
            "No other choice. You played the only move available.",
            "A forced decision. All other options were unfavorable.",
            "Your move was inevitable. There were no better alternatives.",
            "A constrained move. The position allowed no other possibilities.",
            "You had to play that move. No other option would suffice.",
            "The only reasonable move. Other choices were unsound.",
            "A necessary decision. All other moves would lead to disaster.",
            "Your move was dictated by the position. No other moves made sense.",
            "You were compelled to make that move. There were no better options.",
            "A mandatory move. You had no other viable alternatives."
        ]

        self.book_move_descriptions = [
            "A solid opening move! You're following a well-known book line.",
            "A classic opening move! You're playing a common and respected variation.",
            "A strong opening move! You're establishing a solid foundation for your position.",
            "A well-chosen opening move! You're entering a familiar territory.",
            "A traditional opening move! You're adhering to established principles.",
            "A popular opening move! You're playing a move frequently seen in high-level games.",
            "A strategic opening move! You're positioning your pieces optimally.",
            "A recommended opening move! You're following the footsteps of grandmasters.",
            "A common opening move! You're playing a move often seen in this opening.",
            "A book move! You're making a well-known and respected choice in this position.",
            "A great opening move! You're setting yourself up for success right from the start.",
            "A strong choice! You're starting the game with a well-regarded move.",
            "A wise opening move! You're displaying good opening preparation.",
            "A respected opening move! You're playing a move favored by experts.",
            "A reliable opening move! You're entering a line known for its solid play.",
            "A recommended choice! You're making a move that leads to promising positions.",
            "An excellent opening move! You're demonstrating sound opening principles.",
            "A strategic choice! You're aiming for a favorable middlegame with this move.",
            "A popular move! You're selecting a line that has been extensively studied.",
            "A well-established opening move! You're in familiar territory with this choice."
        ]







    def load_data(self):
        with open(self.data_file, 'r') as file:
            self.data = json.load(file)

        number = str(max(map(int, self.data.keys())))

        self.old_fen_list = [move['old_fen'] for move in self.data[number]['moves']]
        self.new_fen_list = [move['new_fen'] for move in self.data[number]['moves']]

        print(len(self.old_fen_list), len(self.new_fen_list))


        self.classification_list = [move['classification'] for move in self.data[number]['moves']]
        self.move_list = [move['move'] for move in self.data[number]['moves']]




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
        



    def generate_description(self, categorization):
        if categorization == "Best Move": return random.choice(self.best_move_descriptions)
        if categorization == "Great": return random.choice(self.great_descriptions)
        if categorization == "Good": return random.choice(self.good_descriptions)       
        if categorization == "Inaccuracy": return random.choice(self.inaccuracy_descriptions)
        if categorization == "Mistake": return random.choice(self.mistake_descriptions)
        if categorization == "Blunder": return random.choice(self.blunder_descriptions)
        if categorization == 'Book': return random.choice(self.book_move_descriptions)
        else: return random.choice(self.forced_descriptions)



    def process_fen(self, fen):
        stockfish = Stockfish(path=self.stockfish_path)
        stockfish.set_fen_position(fen)
        moves = stockfish.get_top_moves(10)


        
        total_moves = len(moves)
        result = []

        played_move = self.move_list[self.old_fen_list.index(fen)]
        is_book_move =  True if self.classification_list[self.old_fen_list.index(fen)] == 'book' else False



        new_fen = self.new_fen_list[self.old_fen_list.index(fen)]




        found_move = False

        for position, move in enumerate(moves):
            if move['Move'] == played_move:
                accuracy = round((1 - position / total_moves) * 100, 2)
                categorization = "Book" if is_book_move else self.categorize_move(position, total_moves)
                description = self.generate_description(categorization)

                result.append({"Move": move['Move'], "Best Move": moves[0]['Move'], "Type": categorization, "Description": description, "Accuracy": accuracy, "Old FEN": fen, "FEN": new_fen})
                found_move = True


        if not found_move:
            result.append({"Move": move['Move'], "Best Move": moves[0]['Move'], "Type": "Blunder", "Description":self.generate_description("Blunder"), "Accuracy": 0, "Old FEN": fen, "FEN": new_fen})

        if chess.Board(fen).legal_moves.count() == 1:
            result.append({"Move": move['Move'], "Best Move": moves[0]['Move'], "Type": "Forced", "Description":self.generate_description("Forced"), "Accuracy": 100, "Old FEN": fen,  "FEN": new_fen})


        return result

    def analyze(self):

        results = [[{"Move": None, "Best Move": None, "Type": None, "Description": None, "Accuracy": None, "Old FEN": 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',  "FEN": 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'}]]



        with multiprocessing.Pool() as pool: 
            results += pool.map(self.process_fen, self.old_fen_list)



        with open('assets/data/analyzer.json', 'w') as f:
            json.dump(results, f)

        





