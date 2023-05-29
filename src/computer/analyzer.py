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




        self.opponent_best_move_descriptions = [
    "That was a strong move by your opponent. They've demonstrated exceptional tactical awareness.",
    "The opponent's play is impressive! Their move showcases deep understanding of the position.",
    "Your opponent made a genius move! They've outplayed you with this brilliant choice.",
    "The opponent's move is flawless! They're dominating the game with exceptional play.",
    "Your opponent's strategic insight is truly impressive. They made a remarkable move!",
    "The opponent's move is superb! They've seized a significant advantage in the position.",
    "Your opponent's play is outstanding! Their move sets up a powerful attack.",
    "The opponent's decision is excellent! They found the most promising continuation.",
    "That was a stunning move by your opponent! They're showing great precision in their play.",
    "The opponent made an amazing move! Their calculation skills are paying off handsomely."
]

        self.opponent_great_descriptions = [
            "That was a terrific move by your opponent! Their positional understanding is top-notch.",
            "The opponent's play is impressive! Their moves consistently show deep understanding.",
            "Your opponent made an excellent maneuver! Their grasp of strategy is highly commendable.",
            "The opponent's choice is superb! Their positional play is a joy to behold.",
            "That was a splendid move by your opponent! Their intuition in this game is truly remarkable.",
            "The opponent made a great decision! Their moves consistently put pressure on you.",
            "Well executed by your opponent! Their play demonstrates a high level of competence.",
            "That was a commendable move by your opponent! They're consistently making strong decisions.",
            "Your opponent is playing brilliantly! Their moves are filled with creativity.",
            "The opponent made a masterful move! Their play exhibits a profound understanding of chess."
        ]

        self.opponent_good_descriptions = [
            "That was a solid move by your opponent! They're steadily improving their position.",
            "The opponent's play is decisive! Their moves are efficient and effective.",
            "Nice maneuver by your opponent! Their strategic choices are paying off.",
            "Well done by your opponent! Their consistent play is keeping the game balanced.",
            "Good decision by your opponent! They're making smart moves to maintain control.",
            "Resolute move by your opponent! Their play displays determination and focus.",
            "Capable choice by your opponent! Their moves are proving to be well thought out.",
            "Your opponent is on the right track! Their play is solid and reliable.",
            "Impressive performance by your opponent! Their moves reflect good judgment.",
            "Your opponent's play is commendable! They're making sensible decisions."
        ]

        self.opponent_inaccuracy_descriptions = [
            "The opponent made a minor slip. They overlooked a slightly stronger move.",
            "That was a slight misstep by your opponent. There was a more accurate option available.",
            "Not the most precise move by your opponent. They missed a subtler possibility.",
            "The opponent made a small deviation. Their move slightly weakens their position.",
            "A slight miscalculation by your opponent. They could have gained a bit more.",
            "An imprecise move by your opponent. Their decision could have been sharper.",
            "A minor error by your opponent. Their move could have been a touch more optimal.",
            "The opponent missed a small opportunity. Their move could have been stronger.",
            "A slight oversight by your opponent. There was a more precise move to consider.",
            "A tiny inaccuracy by your opponent. Their move doesn't fully exploit the position."
        ]

        self.opponent_mistake_descriptions = [
            "That was a regrettable mistake by your opponent. They missed a significant chance.",
            "An unfortunate blunder by your opponent. Their move hands the advantage to you.",
            "A costly error by your opponent. Their decision puts them on the back foot.",
            "A major oversight by your opponent. Their move allows you a strong counterplay.",
            "A critical mistake by your opponent. Their position has been seriously compromised.",
            "A significant misjudgment by your opponent. Their move leads to unfavorable consequences.",
            "A grave blunder by your opponent. You now have a decisive advantage.",
            "A substantial mistake by your opponent. Their move undermines their own position.",
            "A serious lapse by your opponent. Their decision allows you to seize control.",
            "A major misstep by your opponent. Their move jeopardizes their chances of success."
        ]

        self.opponent_blunder_descriptions = [
            "That was a disastrous blunder by your opponent! Their move is a catastrophic mistake.",
            "A fatal error by your opponent. Their decision leads to an irreparable loss of material.",
            "A crushing blunder by your opponent. Their position now teeters on the brink of collapse.",
            "A game-changing mistake by your opponent. Their move completely turns the tables.",
            "An epic blunder by your opponent. You must be ecstatic with this gift.",
            "A monumental error by your opponent. Their move virtually hands the victory to you.",
            "A colossal blunder by your opponent. Their position now looks nearly hopeless.",
            "A catastrophic oversight by your opponent. Their move leads to a quick and decisive defeat.",
            "A devastating blunder by your opponent. Their chances of recovery are extremely slim.",
            "A horrendous mistake by your opponent. Their move leaves them in an almost impossible situation."
        ]

        self.opponent_forced_descriptions = [
            "No other choice for your opponent. They played the only move available.",
            "A forced decision by your opponent. All other options were unfavorable.",
            "Their move was inevitable. Your opponent had no better alternatives.",
            "A constrained move by your opponent. The position allowed no other possibilities.",
            "They had to play that move. Your opponent had no other option that would suffice.",
            "The only reasonable move by your opponent. Other choices were unsound.",
            "A necessary decision by your opponent. All other moves would lead to disaster.",
            "Their move was dictated by the position. No other moves made sense for your opponent.",
            "Your opponent was compelled to make that move. They had no better options.",
            "A mandatory move by your opponent. They had no other viable alternatives."
        ]

        self.opponent_book_move_descriptions = [
            "That was a strong opening move by your opponent! They're following a well-known book line.",
            "A classic opening move by your opponent! They're playing a common and respected variation.",
            "A strong opening move by your opponent! They're establishing a solid foundation for their position.",
            "A well-chosen opening move by your opponent! They're entering familiar territory.",
            "A traditional opening move by your opponent! They're adhering to established principles.",
            "A popular opening move by your opponent! They're playing a move frequently seen in high-level games.",
            "A strategic opening move by your opponent! They're positioning their pieces optimally.",
            "A recommended opening move by your opponent! They're following the footsteps of grandmasters.",
            "A common opening move by your opponent! They're playing a move often seen in this opening.",
            "A book move by your opponent! They're making a well-known and respected choice in this position.",
            "A great opening move by your opponent! They're setting themselves up for success right from the start.",
            "A strong choice by your opponent! They're starting the game with a well-regarded move.",
            "A wise opening move by your opponent! They're displaying good opening preparation.",
            "A respected opening move by your opponent! They're playing a move favored by experts.",
            "A reliable opening move by your opponent! They're entering a line known for its solid play.",
            "A recommended choice by your opponent! They're making a move that leads to promising positions.",
            "An excellent opening move by your opponent! They're demonstrating sound opening principles.",
            "A strategic choice by your opponent! They're aiming for a favorable middlegame with this move.",
            "A popular move by your opponent! They're selecting a line that has been extensively studied.",
            "A well-established opening move by your opponent! They're in familiar territory with this choice."
]



        self.missed_move = [
            " Unfortunately, you missed the opportunity to make the best move, {}. This move would have been a masterful decision, capitalizing on your opponent's oversight and paving the way for victory.",
            " It appears that you didn't recognize the best move, {}, which would have showcased your exceptional foresight and allowed you to anticipate future threats, securing a dominant position on the board.",
            " Regrettably, you didn't choose {} as the best move, missing out on an opportunity to demonstrate your impeccable calculation skills and exploit positional weaknesses, gaining a substantial advantage.",
            " According to optimal play, {} was the best move to make. Unfortunately, you didn't select it, which would have allowed you to leverage your superior strategic understanding and seize control of the game.",
            " It's unfortunate that you didn't make the best move, {}. This move would have demonstrated your profound knowledge of game principles and enabled you to maneuver towards a favorable outcome with precision and finesse.",
            " You missed the chance to choose {} as the best move, which would have showcased your deep positional understanding and strategically positioned your pieces for a decisive blow.",
            " It seems you overlooked the best move, {}, which would have been a testament to your sharp tactical vision. This move could have allowed you to exploit a tactical opportunity and achieve a decisive outcome.",
            " The best move, {}, eluded you this time. This move would have demonstrated your keen sense of strategy and positioned you for a favorable outcome, but unfortunately, you didn't play it.",
            " Unfortunately, you didn't recognize the optimal move, {}, missing an opportunity to showcase your tactical acumen. This move could have exploited a tactical weakness and led to a decisive advantage.",
            " You didn't choose {} as the best move, which is unfortunate. This move would have displayed your ability to capitalize on positional opportunities and gain a significant advantage over your opponent."
]


        self.opening_explanation = [
            "This opening is called {}.",
            "I recognize this opening! I believe it is called the {}.",
            "Ahh, the {}. This is one of my favorites!",
            "Ah, yes! The {}. A classic opening move.",
            "I'm familiar with this one. It's called the {}.",
            "The opening you've played is known as {}. It has been used by many chess players.",
            "I've seen this opening before. It's commonly referred to as {}.",
            "That's the {}. It's known for its strategic value.",
            "Interesting choice! You've played the {}. It has its own unique characteristics.",
            "Ah, the {}. It's known for its versatility in various chess positions.",
            "The opening move you made, {}. It's an exciting choice!",
            "Oh, the {}. It's a well-known opening among chess enthusiasts.",
            "The {}. A solid choice to start the game!",
            "Ah, the {}. It often leads to interesting middle game positions.",
            "That's the {}. It's known for its aggressive nature.",
            "You've played the {}. It's a popular choice in modern chess.",
            "Ah, the {}. It's a strategic opening with multiple variations.",
            "That's the {}. It's a tactical opening that can catch opponents off guard.",
            "You've chosen the {}. It's a flexible opening with many possible outcomes.",
            "The opening move you made, {}. It's known for its solid positional play.",
            "Oh, the {}. It's a dynamic opening that can lead to sharp and complex positions."
        ]


    def load_data(self):
        with open(self.data_file, 'r') as file:
            self.data = json.load(file)

        number = str(max(map(int, self.data.keys())))

        self.old_fen_list = [move['old_fen'] for move in self.data[number]['moves']]
        self.new_fen_list = [move['new_fen'] for move in self.data[number]['moves']]
        self.opening_list = [move['opening'] for move in self.data[number]['moves']]


        self.classification_list = [move['classification'] for move in self.data[number]['moves']]
        self.move_list = [move['move'] for move in self.data[number]['moves']]

        self.own_color = self.data[number]['data']['own_color']




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
        



    def generate_description(self, categorization, is_own, best_move, opening):
        prompt = None

        if categorization == "Best Move": prompt = random.choice(self.best_move_descriptions if is_own else self.opponent_best_move_descriptions)
        elif categorization == "Great": prompt = random.choice(self.great_descriptions if is_own else self.opponent_great_descriptions)
        elif categorization == "Good": prompt = random.choice(self.good_descriptions if is_own else self.opponent_good_descriptions)       
        elif categorization == "Inaccuracy": prompt = random.choice(self.inaccuracy_descriptions if is_own else self.opponent_inaccuracy_descriptions)
        elif categorization == "Mistake": prompt = random.choice(self.mistake_descriptions if is_own else self.opponent_mistake_descriptions)
        elif categorization == "Blunder": prompt = random.choice(self.blunder_descriptions if is_own else self.opponent_blunder_descriptions)
        elif categorization == 'Book': prompt = None if is_own else random.choice(self.opponent_book_move_descriptions)
        elif categorization == 'Forced': prompt = random.choice(self.forced_descriptions if is_own else self.opponent_forced_descriptions)



        if categorization not in ["Best Move", "Forced", "Book"] and is_own:
            missed_prompt = random.choice(self.missed_move)
            prompt += missed_prompt.format(best_move)

        elif categorization == "Book" and is_own:
            book_prompt = random.choice(self.opening_explanation)
            prompt = book_prompt.format(opening)
        return prompt







    def process_fen(self, fen):
        stockfish = Stockfish(path=self.stockfish_path)
        stockfish.set_fen_position(fen)
        moves = stockfish.get_top_moves(10)

        ranks, active_color, castling, en_passant, halfmove_clock, fullmove_number = fen.split()
        active_color = 'white' if 'w' in active_color else 'black'
        is_own = True if active_color == self.own_color else False


        total_moves = len(moves)
        result = []

        played_move = self.move_list[self.old_fen_list.index(fen)]
        is_book_move =  True if self.classification_list[self.old_fen_list.index(fen)] == 'book' else False
        new_fen = self.new_fen_list[self.old_fen_list.index(fen)]
        found_move = False

        opening = self.opening_list[self.old_fen_list.index(fen)]
 
        for position, move in enumerate(moves):
            if move['Move'] == played_move:
                accuracy = round((1 - position / total_moves) * 100, 2)
                categorization = "Book" if is_book_move else self.categorize_move(position, total_moves)
                description = self.generate_description(categorization, is_own, moves[0]['Move'], opening)


                result.append({"Move": move['Move'], "Best Move": moves[0]['Move'], "Type": categorization, "Description": description, "Accuracy": accuracy, "Old FEN": fen, "FEN": new_fen, "Opening": opening})
                found_move = True


        if not found_move:
            result.append({"Move": move['Move'], "Best Move": moves[0]['Move'], "Type": "Blunder", "Description":self.generate_description("Blunder", is_own, moves[0]['Move'], opening), "Accuracy": 0, "Old FEN": fen, "FEN": new_fen, "Opening": opening})

        if chess.Board(fen).legal_moves.count() == 1:
            result.append({"Move": move['Move'], "Best Move": moves[0]['Move'], "Type": "Forced", "Description":self.generate_description("Forced", is_own, moves[0]['Move'], opening), "Accuracy": 100, "Old FEN": fen,  "FEN": new_fen, "Opening": opening})
        return result


    def analyze(self):
        results = [[{"own_color": self.own_color}], [{"Move": None, "Best Move": None, "Type": None, "Description": None, "Accuracy": None, "Old FEN": 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1',  "FEN": 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', "Opening": None}]]



        with multiprocessing.Pool() as pool: 
            results += pool.map(self.process_fen, self.old_fen_list)



        with open('assets/data/analyzer.json', 'w') as f:
            json.dump(results, f)

        


    def categorization_color(self, categorization):
        if categorization == "Best Move": return (80, 199, 80) 
        elif categorization == "Great": return (132, 209, 132) 
        elif categorization == "Good": return (158, 215, 158)
        elif categorization == "Inaccuracy": return (222, 222, 129)
        elif categorization == "Mistake": return (219, 152, 86)
        elif categorization == "Blunder": return (232, 112, 77)
        elif categorization == 'Book': return (166, 127, 89)
        elif categorization == 'Forced': return (131, 183, 235)





