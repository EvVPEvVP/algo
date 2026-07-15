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


def information_gain(data, attr, target):
    total = entropy([row[target] for row in data])

    weighted = 0
    for value in {row[attr] for row in data}:
        subset = [row[target] for row in data if row[attr] == value]
        weighted += len(subset) / len(data) * entropy(subset)

    return total - weighted

def id3(data, attrs, target):
    results = [row[target] for row in data]
    if len(set(results)) == 1:
        return results[0]

    if not attrs:
        return Counter(results).most_common(1)[0][0]

    best = max(attrs, key=lambda a: information_gain(data, a, target))

    tree = {best: {}}

    for value in {row[best] for row in data}:
        subset = [row for row in data if row[best] == value]

        if subset:
            rest = [a for a in attrs if a != best]
            tree[best][value] = id3(subset, rest, target)
        else:
            tree[best][value] = Counter(results).most_common(1)[0][0]

    return tree

def print_tree(tree, indent=""):
    if isinstance(tree, str):
        print(indent + tree)
        return

    attr = next(iter(tree))

    print(indent + attr)

    for value, branch in tree[attr].items():
        print(indent + f"├─ {value}")
        print_tree(branch, indent + "│  ")

attrs = ["Outlook", "Temperature", "Humidity", "Wind"]

tree = id3(data, attrs, "Play")

print_tree(tree)
