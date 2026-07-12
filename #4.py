from collections import Counter
from math import log2

# Тестовый набор
data = [
    {"Outlook":"Sunny","Temperature":"Hot","Humidity":"High","Wind":"Weak","Play":"No"},
    {"Outlook":"Sunny","Temperature":"Hot","Humidity":"High","Wind":"Strong","Play":"No"},
    {"Outlook":"Overcast","Temperature":"Hot","Humidity":"High","Wind":"Weak","Play":"Yes"},
    {"Outlook":"Rain","Temperature":"Mild","Humidity":"High","Wind":"Weak","Play":"Yes"},
    {"Outlook":"Rain","Temperature":"Cool","Humidity":"Normal","Wind":"Weak","Play":"Yes"},
    {"Outlook":"Rain","Temperature":"Cool","Humidity":"Normal","Wind":"Strong","Play":"No"},
    {"Outlook":"Overcast","Temperature":"Cool","Humidity":"Normal","Wind":"Strong","Play":"Yes"},
    {"Outlook":"Sunny","Temperature":"Mild","Humidity":"High","Wind":"Weak","Play":"No"},
    {"Outlook":"Sunny","Temperature":"Cool","Humidity":"Normal","Wind":"Weak","Play":"Yes"},
    {"Outlook":"Rain","Temperature":"Mild","Humidity":"Normal","Wind":"Weak","Play":"Yes"},
    {"Outlook":"Sunny","Temperature":"Mild","Humidity":"Normal","Wind":"Strong","Play":"Yes"},
    {"Outlook":"Overcast","Temperature":"Mild","Humidity":"High","Wind":"Strong","Play":"Yes"},
    {"Outlook":"Overcast","Temperature":"Hot","Humidity":"Normal","Wind":"Weak","Play":"Yes"},
    {"Outlook":"Rain","Temperature":"Mild","Humidity":"High","Wind":"Strong","Play":"No"},
]

def entropy(values):
    n = len(values)
    counts = Counter(values)
    return -sum((c / n) * log2(c / n) for c in counts.values())

def split_entropy(data, attr, target):
    result = {}

    for value in {row[attr] for row in data}:
        subset = [row[target] for row in data if row[attr] == value]
        result[value] = entropy(subset)

    return result

def information_gain(data, attr, target):
    total = entropy([row[target] for row in data])

    weighted = 0
    n = len(data)

    for value in {row[attr] for row in data}:
        subset = [row[target] for row in data if row[attr] == value]
        weighted += len(subset) / n * entropy(subset)

    return total - weighted

for attr in ["Outlook", "Humidity", "Wind", "Temperature"]:
    print(attr, round(information_gain(data, attr, "Play"), 3))
