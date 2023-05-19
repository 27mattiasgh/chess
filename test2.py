import json

while True:
    # Load the JSON data
    with open('assets\data\games.json') as json_file:
        data = json.load(json_file)

    latest_opening = data[str(len(data))]['moves'][-1]['opening']


    print(latest_opening)
