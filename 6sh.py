class Node:
    def __init__(self, key, priority, left=None, right=None):
        self.key = key
        self.priority = priority
        self.left = left
        self.right = right

    def __repr__(self):
        return f"({self.key},{self.priority})"


def build_treap(pairs):
    if not pairs:
        return None

    # корень — пара с максимальным приоритетом
    i = max(range(len(pairs)), key=lambda j: pairs[j][1])
    key, priority = pairs[i]

    left_pairs = pairs[:i]
    right_pairs = pairs[i + 1:]

    left_pairs = [p for p in left_pairs if p[0] < key] + \
                 [p for p in left_pairs if p[0] > key]

    return Node(
        key,
        priority,
        build_treap([p for p in pairs[:i]]),
        build_treap([p for p in pairs[i + 1:]]),
    )


def build_treap_sorted(pairs):
    if not pairs:
        return None

    i = max(range(len(pairs)), key=lambda j: pairs[j][1])
    key, priority = pairs[i]

    return Node(
        key,
        priority,
        build_treap_sorted(pairs[:i]),
        build_treap_sorted(pairs[i + 1:]),
    )


def build(pairs):
    return build_treap_sorted(sorted(pairs, key=lambda p: p[0]))
