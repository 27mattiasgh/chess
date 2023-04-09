from src.computer.computer import Computer

class Formatter:

    def __init__(self):
        pass

    def rowcol_to_uci(self, initial_row, initial_col, final_row, final_col):
        """
        Formats pygame coordinates into acceptable stockfish move values (uci) 
        """
        key = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

        initial_row = 7 - initial_row
        final_row = 7 - final_row

        initial_col = key[initial_col]
        final_col = key[final_col]

        initial = initial_col + str(initial_row + 1)
        final = final_col + str(final_row + 1)
            
        return initial + final
    
    def uci_to_rowcol(self, move):
        """
        Formats stockfish move values (uci) into pygame coordinates  
        """        


        key = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

        initial_col = key[move[0]]
        initial_row = int(move[1]) - 1

        final_col = key[move[2]]
        final_row = int(move[3]) - 1

        initial_row = 7 - initial_row
        final_row = 7 - final_row

        return initial_row, initial_col, final_row, final_col



