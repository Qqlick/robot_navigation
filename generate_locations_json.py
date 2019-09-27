import json
from random import randint

with open('list_of_streets', 'r') as f:
    locations = list()
    line = "test"
    while line:
        line = f.readline()
        if line:
            locations.append({"name": line.strip(),
                              "x": randint(1, 100),
                              "y": randint(1, 100)})
    with open("list_of_locs.json", "w") as locs:
        json.dump(locations, locs, indent=4)
