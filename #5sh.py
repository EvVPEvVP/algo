class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None


class SplayTree:
    def __init__(self, root=None):
        self.root = root
        if root:
            root.parent = None

    # вращения
    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x):
        y = x.left
        x.left = y.right
        if y.right:
            y.right.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # splay: поднять x в корень
    def splay(self, x):
        while x.parent:
            p = x.parent
            g = p.parent

            if not g:                          # zig
                if x is p.left:
                    self._rotate_right(p)
                else:
                    self._rotate_left(p)

            elif x is p.left and p is g.left:  # zig-zig
                self._rotate_right(g)
                self._rotate_right(p)

            elif x is p.right and p is g.right:
                self._rotate_left(g)
                self._rotate_left(p)

            elif x is p.right and p is g.left: # zig-zag
                self._rotate_left(p)
                self._rotate_right(g)

            else:
                self._rotate_right(p)
                self._rotate_left(g)

        self.root = x

    # поиск
    def find(self, key):
        x = self.root
        last = None
        while x:
            last = x
            if key < x.key:
                x = x.left
            elif key > x.key:
                x = x.right
            else:
                self.splay(x)
                return x
        if last:
            self.splay(last)
        return None

    # вставка
    def insert(self, key):
        if not self.root:
            self.root = Node(key)
            return

        x = self.root
        while True:
            if key < x.key:
                if x.left:
                    x = x.left
                else:
                    x.left = Node(key)
                    x.left.parent = x
                    self.splay(x.left)
                    return
            elif key > x.key:
                if x.right:
                    x = x.right
                else:
                    x.right = Node(key)
                    x.right.parent = x
                    self.splay(x.right)
                    return
            else:
                self.splay(x)  # уже есть
                return

    # слияние: все ключи t1 < всех ключей t2
    @staticmethod
    def merge(t1, t2):
        if not t1 or not t1.root:
            return t2
        if not t2 or not t2.root:
            return t1

        # splay максимума t1, у него не будет правого ребёнка
        x = t1.root
        while x.right:
            x = x.right
        t1.splay(x)

        x.right = t2.root
        t2.root.parent = x
        return t1

    # удаление
    def delete(self, key):
        node = self.find(key)
        if not node or node.key != key:
            return

        left = node.left
        right = node.right
        if left:
            left.parent = None
        if right:
            right.parent = None

        self.root = SplayTree.merge(
            SplayTree(left),
            SplayTree(right)
        ).root

    # обход
    def inorder(self):
        def dfs(x):
            if not x:
                return []
            return dfs(x.left) + [x.key] + dfs(x.right)
        return dfs(self.root)

    def __repr__(self):
        return str(self.inorder())
