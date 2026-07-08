from collections import Counter
import heapq


class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def huffman_codes(text):
    if not text:
        return {}

    heap = [Node(freq, char) for char, freq in Counter(text).items()]
    heapq.heapify(heap)

    if len(heap) == 1:
        return {heap[0].char: "0"}

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        heapq.heappush(heap, Node(left.freq + right.freq, left=left, right=right))

    root = heap[0]

    # Обход дерева
    codes = {}

    def dfs(node, code):
        if node.char is not None:
            codes[node.char] = code
            return
        dfs(node.left, code + "0")
        dfs(node.right, code + "1")

    dfs(root, "")

    return codes
