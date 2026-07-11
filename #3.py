class EulerTree:
    def __init__(self, path=None):
        self.path = path or []

    @staticmethod
    def from_tree(tree, root):
        path = []

        def dfs(v, parent):
            path.append(v)
            for u in tree[v]:
                if u != parent:
                    dfs(u, v)
                    path.append(v)

        dfs(root, None)
        return EulerTree(path)

    def reroot(self, v):
        i = self.path.index(v)

        A = self.path[:i]
        B = self.path[i:]

        if A:
            A = A[1:] + [v]

        self.path = B + A

    def contains(self, v):
        return v in self.path

    def __repr__(self):
        return str(self.path)


class EulerForest:
    def __init__(self):
        self.trees = []

    def add_tree(self, tree):
        self.trees.append(tree)

    def connected(self, v1, v2):
        return any(t.contains(v1) and t.contains(v2)
                   for t in self.trees)

    def link(self, v1, v2):
        t1 = t2 = None

        for t in self.trees:
            if t.contains(v1):
                t1 = t
            if t.contains(v2):
                t2 = t

        if t1 is None or t2 is None:
            raise ValueError("Вершина не найдена")

        if t1 is t2:
            raise ValueError("Вершины уже в одном дереве")

        t1.reroot(v1)
        t2.reroot(v2)

        new_tree = EulerTree(t1.path + t2.path + [v1])

        self.trees.remove(t1)
        self.trees.remove(t2)
        self.trees.append(new_tree)
