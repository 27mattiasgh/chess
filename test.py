import json

# Load the JSON data
with open('assets/data/analyzer.json', 'r') as f:
    data = json.load(f)


white_move_types = {}
black_move_types = {}

for index, move in enumerate(data[1:], start=1):
    move_data = move[0]
    move_type = move_data.get('Type')
    if move_type:
        if index % 2 == 1:
            if move_type in black_move_types:
                black_move_types[move_type] += 1
            else:
                black_move_types[move_type] = 1
        else:
            if move_type in white_move_types:
                white_move_types[move_type] += 1
            else:
                white_move_types[move_type] = 1



# Print black move types and their counts
print("Black Move Classifications:")
for move_type, count in black_move_types.items():
    print(f"{count} {move_type}(s)")

# Print a separator
print("\n---\n")

# Print white move types and their counts
print("White Move Classifications:")
for move_type, count in white_move_types.items():
    print(f"{count} {move_type}(s)")
