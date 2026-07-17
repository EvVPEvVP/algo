from collections import defaultdict

class Graph:
    def __init__(self):
        self.g = defaultdict(set)

    def add_edge(self, u, v):
        self.g[u].add(v)
        self.g[v].add(u)

    def remove_edge(self, u, v):
        self.g[u].discard(v)
        self.g[v].discard(u)

    def connected(self, u, v):
        if u not in self.g or v not in self.g:
            return False

        seen = set()

        def dfs(x):
            seen.add(x)
            for y in self.g[x]:
                if y not in seen:
                    dfs(y)

        dfs(u)
        return v in seen

    def components(self):
        seen = set()
        comp = []

        for v in self.g:
            if v in seen:
                continue

            cur = []
            stack = [v]
            seen.add(v)

            while stack:
                x = stack.pop()
                cur.append(x)

                for y in self.g[x]:
                    if y not in seen:
                        seen.add(y)
                        stack.append(y)

            comp.append(cur)

        return comp

    def bridges(self):
        tin = {}
        low = {}
        timer = 0
        ans = []

        def dfs(v, p):
            nonlocal timer

            tin[v] = low[v] = timer
            timer += 1

            for to in self.g[v]:
                if to == p:
                    continue

                if to in tin:
                    low[v] = min(low[v], tin[to])
                else:
                    dfs(to, v)
                    low[v] = min(low[v], low[to])

                    if low[to] > tin[v]:
                        ans.append((v, to))

        for v in self.g:
            if v not in tin:
                dfs(v, -1)

        return ans

    def biconnected_components(self):
        bridges = {frozenset(e) for e in self.bridges()}

        seen = set()
        result = []

        for start in self.g:
            if start in seen:
                continue

            comp = []
            stack = [start]
            seen.add(start)

            while stack:
                v = stack.pop()
                comp.append(v)

                for u in self.g[v]:
                    if frozenset((v, u)) in bridges:
                        continue

                    if u not in seen:
                        seen.add(u)
                        stack.append(u)

            result.append(comp)

        return result
    
    def bridge_forest(self):
        comps = self.biconnected_components()

        index = {}
        for i, comp in enumerate(comps):
            for v in comp:
                index[v] = i

        forest = defaultdict(set)

        for u, v in self.bridges():
            a = index[u]
            b = index[v]

            forest[a].add(b)
            forest[b].add(a)

        return forest










