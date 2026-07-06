#1.

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

#2.

class ImmutableStack:
    def __init__(self, head=None, tail=None):
        self._head = head
        self._tail = tail  # Ссылка на предыдущий ImmutableStack

    def is_empty(self):
        return self._tail is None

    def push(self, val):
        return ImmutableStack(val, self)

    def pop(self):
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self._head, self._tail

    def peek(self):
        if self.is_empty():
            raise IndexError("Стек пуст")
        return self._head

    def __iter__(self):
        curr = self
        while not curr.is_empty():
            yield curr._head
            curr = curr._tail

# Инициализация пустого стека
EMPTY_STACK = ImmutableStack()

#3.

class ImmutableQueue:
    def __init__(self, forward=EMPTY_STACK, back=EMPTY_STACK):
        self._forward = forward
        self._back = back

    def is_empty(self):
        return self._forward.is_empty() and self._back.is_empty()

    def enqueue(self, val):
        if self.is_empty():
            return ImmutableQueue(self._forward.push(val), self._back)
        return ImmutableQueue(self._forward, self._back.push(val))

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Очередь пуста")
        
        val, new_forward = self._forward.pop()
        if not new_forward.is_empty():
            return val, ImmutableQueue(new_forward, self._back)
        
        if self._back.is_empty():
            return val, EMPTY_QUEUE
        
        # Переворачиваем
        temp, inv_forward = self._back, EMPTY_STACK
        while not temp.is_empty():
            v, temp = temp.pop()
            inv_forward = inv_forward.push(v)
            
        return val, ImmutableQueue(inv_forward, EMPTY_STACK)

    def peek(self):
        if self.is_empty():
            raise IndexError("Очередь пуста")
        return self._forward.peek()

    def __iter__(self):
        yield from self._forward
        yield from reversed(list(self._back))

EMPTY_QUEUE = ImmutableQueue()



