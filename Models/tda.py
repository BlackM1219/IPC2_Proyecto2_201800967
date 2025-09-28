# Implementación de TDAs propios: ListaSimple, Cola, Pila (opcional)

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None

class ListaSimple:
    """Lista simple enlazada sin uso de list/dict/tuple."""
    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def append(self, data):
        node = Node(data)
        if not self.head:
            self.head = node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = node
        self.size += 1

    def iter(self):
        cur = self.head
        while cur:
            yield cur.data
            cur = cur.next

    def find(self, predicate):
        cur = self.head
        while cur:
            if predicate(cur.data):
                return cur.data
            cur = cur.next
        return None

class Cola:
    def __init__(self):
        self.front = None
        self.rear = None
        self._size = 0

    def enqueue(self, data):
        node = Node(data)
        if not self.rear:
            self.front = node
            self.rear = node
        else:
            self.rear.next = node
            self.rear = node
        self._size += 1

    def dequeue(self):
        if not self.front:
            return None
        node = self.front
        self.front = node.next
        if not self.front:
            self.rear = None
        node.next = None
        self._size -= 1
        return node.data

    def is_empty(self):
        return self.front is None

    def size(self):
        return self._size