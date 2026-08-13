class SegmentTree:
    def __init__(self, arr, f, neutral):
        self.n = len(arr)
        self.f = f
        self.neutral = neutral
        self.arr = arr

    def build_top_down(self):
        self.tree = [self.neutral] * (4 * self.n)
        self._build(1, 0, self.n - 1)
        return self

    def _build(self, v, tl, tr):
        if tl == tr:
            self.tree[v] = self.arr[tl]
            return

        tm = (tl + tr) // 2
        self._build(2 * v, tl, tm)
        self._build(2 * v + 1, tm + 1, tr)
        self.tree[v] = self.f(self.tree[2 * v], self.tree[2 * v + 1])

    def build_bottom_up(self):
        size = 1
        while size < self.n:
            size *= 2

        self.size = size
        self.tree = [self.neutral] * (2 * size)

        # листья
        for i in range(self.n):
            self.tree[size + i] = self.arr[i]

        # родители
        for i in range(size - 1, 0, -1):
            self.tree[i] = self.f(self.tree[2 * i], self.tree[2 * i + 1])

        return self

    def query(self, l, r):
        # если дерево построено сверху вниз
        if not hasattr(self, "size"):
            return self._query_td(1, 0, self.n - 1, l, r)
        # если снизу вверх
        return self._query_bu(l, r)

    def _query_td(self, v, tl, tr, l, r):
        if l > r:
            return self.neutral
        if l == tl and r == tr:
            return self.tree[v]

        tm = (tl + tr) // 2
        left = self._query_td(2 * v, tl, tm, l, min(r, tm))
        right = self._query_td(2 * v + 1, tm + 1, tr, max(l, tm + 1), r)
        return self.f(left, right)

    def _query_bu(self, l, r):
        l += self.size
        r += self.size
        res = self.neutral

        while l <= r:
            if l % 2 == 1:
                res = self.f(res, self.tree[l])
                l += 1
            if r % 2 == 0:
                res = self.f(res, self.tree[r])
                r -= 1
            l //= 2
            r //= 2

        return res
