class BNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.child = None
        self.sibling = None


class BinomialHeap:
    def __init__(self):
        self.head = None

    # слияние двух деревьев одного rank
    @staticmethod
    def _link(t1, t2):
        if t1.key < t2.key:
            t1, t2 = t2, t1
        t2.sibling = t1.child
        t1.child = t2
        t1.degree += 1
        return t1

    # слияние двух куч (как сложение двоичных чисел)
    def merge(self, other):
        self.head = self._merge_roots(self.head, other.head)
        other.head = None
        if not self.head:
            return self

        prev, x, nxt = None, self.head, self.head.sibling
        while nxt:
            if (x.degree != nxt.degree or
                (nxt.sibling and nxt.sibling.degree == x.degree)):
                prev, x = x, nxt
            else:
                if x.key >= nxt.key:
                    x.sibling = nxt.sibling
                    x = self._link(x, nxt)
                    if prev:
                        prev.sibling = x
                    else:
                        self.head = x
                else:
                    if prev:
                        prev.sibling = nxt
                    else:
                        self.head = nxt
                    x = self._link(nxt, x)
            nxt = x.sibling
        return self

    @staticmethod
    def _merge_roots(h1, h2):
        dummy = BNode(None)
        tail = dummy
        while h1 and h2:
            if h1.degree <= h2.degree:
                tail.sibling, h1 = h1, h1.sibling
            else:
                tail.sibling, h2 = h2, h2.sibling
            tail = tail.sibling
        tail.sibling = h1 or h2
        return dummy.sibling

    # вставка
    def insert(self, key):
        h = BinomialHeap()
        h.head = BNode(key)
        return self.merge(h)

    # максимум
    def find_max(self):
        if not self.head:
            return None
        m = self.head
        cur = self.head.sibling
        while cur:
            if cur.key > m.key:
                m = cur
            cur = cur.sibling
        return m.key

    # отладочный вид
    def trees(self):
        res, cur = [], self.head
        while cur:
            res.append((cur.degree, cur.key))
            cur = cur.sibling
        return res

    def __repr__(self):
        return f"BinomialHeap{self.trees()}"
