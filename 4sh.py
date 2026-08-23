from bisect import bisect_left, bisect_right


class RangeTree2D:
    class Node:
        def __init__(self, point, left=None, right=None):
            self.point = point          # (x, y) — разделитель
            self.left = left
            self.right = right
            # все точки поддерева отсортированные по y
            pts = []
            if left:
                pts.extend(left.points)
            pts.append(point)
            if right:
                pts.extend(right.points)
            pts.sort(key=lambda p: p[1])
            self.points = pts
            self.ys = [p[1] for p in pts]

    def __init__(self, points):
        pts = sorted(set(points))  # по x, затем y; уникальные
        self.root = self._build(pts)

    def _build(self, pts):
        if not pts:
            return None
        mid = len(pts) // 2
        return self.Node(
            pts[mid],
            self._build(pts[:mid]),
            self._build(pts[mid + 1:]),
        )

    def query(self, x1, x2, y1, y2):
        result = []
        self._query(self.root, x1, x2, y1, y2, result)
        return result

    def _in_y(self, node, y1, y2, result):
        lo = bisect_left(node.ys, y1)
        hi = bisect_right(node.ys, y2)
        result.extend(node.points[lo:hi])

    def _query(self, node, x1, x2, y1, y2, result):
        if node is None:
            return

        x, y = node.point

        if x < x1:
            self._query(node.right, x1, x2, y1, y2, result)
        elif x > x2:
            self._query(node.left, x1, x2, y1, y2, result)
        else:
            # x внутри [x1, x2]
            if y1 <= y <= y2:
                result.append(node.point)
            self._from_left(node.left, x1, y1, y2, result)
            self._from_right(node.right, x2, y1, y2, result)

    def _from_left(self, node, x1, y1, y2, result):
        if node is None:
            return
        x, y = node.point
        if x < x1:
            self._from_left(node.right, x1, y1, y2, result)
        else:
            if y1 <= y <= y2:
                result.append(node.point)
            if node.right:
                self._in_y(node.right, y1, y2, result)
            self._from_left(node.left, x1, y1, y2, result)

    def _from_right(self, node, x2, y1, y2, result):
        if node is None:
            return
        x, y = node.point
        if x > x2:
            self._from_right(node.left, x2, y1, y2, result)
        else:
            if y1 <= y <= y2:
                result.append(node.point)
            if node.left:
                self._in_y(node.left, y1, y2, result)
            self._from_right(node.right, x2, y1, y2, result)
