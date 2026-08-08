import random


class DSU:
    def __init__(self):
        self.parent = {}

    def make_set(self, x):
        self.parent[x] = x

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def unite(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return

        if random.random() < 0.5:
            self.parent[ry] = rx
        else:
            self.parent[rx] = ry

    def connected(self, x, y):
        return self.find(x) == self.find(y)
