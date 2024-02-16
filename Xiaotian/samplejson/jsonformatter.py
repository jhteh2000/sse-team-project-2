"""
    JSON File Formatter
"""
import json


with open("samplejson/recipe.json", "r") as read_file:
    data = json.load(read_file)


with open("samplejson/recipe.json", "w") as write_file:
    json.dump(data, write_file, indent=4)

print("done")
