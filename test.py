import chess

# Create a chess board
board = chess.Board(fen='rnbqkbnr/ppp1p1pp/8/3pPp2/8/8/PPPP1PPP/RNBQKBNR w KQkq f6 0 3')

# Make a move (en passant capture)


move = chess.Move.from_uci("e5f6")


# Check if the move is an en passant capture
if board.is_en_passant(move):
    print("The move is an en passant capture!")
else:
    print("The move is not an en passant capture.")
