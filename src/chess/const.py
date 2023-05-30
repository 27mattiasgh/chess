WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 750

#board
WIDTH = 700
HEIGHT = 700

#board 
ROWS = 8
COLS = 8

#squares
SQUARE_SIZE = (WIDTH // COLS) 


#engine settings
FIND_TIME = 850 #milliseconds
THREADS = 4 # < number of logical processors
HASH = 1024 #amount of allowed memory stockfish can use 

#more processing power for analysis
ANALISYS_THREADS = 16
ANALISYS_HASH = 16384

EVALUATION_SHALLOW_FIND_TIME = 15 #milliseconds
EVALUATION_DEEP_FIND_TIME = 35    #milliseconds