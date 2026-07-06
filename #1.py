class MaxStack:
    def __init__(self):
        self.stack = []  # Хранит кортеж (значение, текущий_максимум)

    def push(self, val):
        cur_max = val if not self.stack else max(val, self.stack[-1][1])
        self.stack.append((val, cur_max))

    def pop(self):
        return self.stack.pop()[0]

    def get_max(self):
        return self.stack[-1][1]


class MaxQueue:
    def __init__(self):
        # Очередь на двух стеках
        self.instack = MaxStack()
        self.outstack = MaxStack()

    def enqueue(self, val):
        self.instack.push(val)

    def dequeue(self):
        if not self.outstack.stack:
            while self.instack.stack:
                self.outstack.push(self.instack.pop())
        return self.outstack.pop()

    def get_max(self):
        if not self.instack.stack:
            return self.outstack.get_max()
        if not self.outstack.stack:
            return self.instack.get_max()
        return max(self.instack.get_max(), self.outstack.get_max())
