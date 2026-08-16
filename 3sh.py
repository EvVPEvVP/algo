class IntervalTree:
    class Node:
        def __init__(self, center, intervals, left=None, right=None):
            self.center = center
            self.intervals = intervals          # пересекают center
            self.by_left = sorted(intervals)    # по левой границе
            self.by_right = sorted(intervals, key=lambda iv: iv[1])  # по правой
            self.left = left
            self.right = right

    def __init__(self, intervals):
        self.root = self._build(intervals)

    def _build(self, intervals):
        if not intervals:
            return None

        # точка разбиения — медиана всех концов
        points = sorted({x for iv in intervals for x in iv})
        center = points[len(points) // 2]

        mid, left, right = [], [], []
        for lo, hi in intervals:
            if hi < center:
                left.append((lo, hi))
            elif lo > center:
                right.append((lo, hi))
            else:
                mid.append((lo, hi))  # center ∈ [lo, hi]

        return self.Node(
            center,
            mid,
            self._build(left),
            self._build(right),
        )

    def query(self, x):
        # Все интервалы, содержащие точку x
        result = []
        self._query(self.root, x, result)
        return result

    def _query(self, node, x, result):
        if node is None:
            return

        # интервалы текущего узла, содержащие x
        if x < node.center:
            # идём слева направо, пока left <= x
            for lo, hi in node.by_left:
                if lo > x:
                    break
                if hi >= x:
                    result.append((lo, hi))
            self._query(node.left, x, result)
        else:
            # идём справа налево, пока right >= x
            for lo, hi in reversed(node.by_right):
                if hi < x:
                    break
                if lo <= x:
                    result.append((lo, hi))
            if x > node.center:
                self._query(node.right, x, result)
