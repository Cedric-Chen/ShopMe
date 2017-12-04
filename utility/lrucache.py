#!/usr/bin/python
# -*- coding: utf-8 -*-


# Class for the node objects.
class _dlnode(object):
    def __init__(self):
        self.empty = True


class LRUCache(object):

    def __init__(self, size, callback=None):

        self.callback = callback

        # Create an empty hash table.
        self.table = {}

        self.head = _dlnode()
        self.head.next = self.head
        self.head.prev = self.head

        self.tail = self.head

        self.listSize = 1

        # Adjust the size
        self.size(size)


    def __len__(self):
        return len(self.table)

    def clear(self):
        for node in self.dli():
            node.empty = True
            node.key = None
            node.value = None

        self.table.clear()

        self.tail = self.head


    def __contains__(self, key):
        return key in self.table

    # Looks up a value in the cache without affecting cache order.
    def peek(self, key):
        # Look up the node
        node = self.table[key]
        return node.value


    def __getitem__(self, key):
        # Look up the node
        node = self.table[key]

        self.mtf(node)
        self.head = node

        # Return the value.
        return node.value

    def get(self, key, default=None):
        """Get an item - return default (None) if not present"""
        if key not in self.table:
            return default

        return self[key]

    def __setitem__(self, key, value):
        # First, see if any value is stored under 'key' in the cache already.
        # If so we are going to replace that value with the new one.
        if key in self.table:

            # Lookup the node
            node = self.table[key]

            # Replace the value.
            node.value = value

            # Update the list ordering.
            self.mtf(node)
            self.head = node

            return

        node = self.head.prev

        if not node.empty:
            if self.callback is not None:
                self.callback(node.key, node.value)
            del self.table[node.key]

        # Place the new key and value in the node
        node.empty = False
        node.key = key
        node.value = value

        # Add the node to the dictionary under the new key.
        self.table[key] = node

        self.head = node

        self.movetail(node)

    def update(self, items):

        # Add multiple items to the cache.
        for n, v in items.items():
            self[n] = v

    def __delitem__(self, key):

        # Lookup the node, then remove it from the hash table.
        node = self.table[key]
        del self.table[key]

        node.empty = True

        # Not strictly necessary.
        node.key = None
        node.value = None

        self.mtf(node)
        self.head = node.next

    def __iter__(self):
        for node in self.dli():
            yield node.key

    def items(self):
        for node in self.dli():
            yield (node.key, node.value)

    def keys(self):
        for node in self.dli():
            yield node.key

    def values(self):
        for node in self.dli():
            yield node.value


    def size(self, size=None):

        if size is not None:
            assert size > 0
            if size > self.listSize:
                self.addTailNode(size - self.listSize)
            elif size < self.listSize:
                self.removeTailNode(self.listSize - size)

        return self.listSize


    def addTailNode(self, n):
        for i in range(n):
            node = _dlnode()
            node.next = self.head
            node.prev = self.head.prev

            self.head.prev.next = node
            self.head.prev = node

        self.listSize += n


    def removeTailNode(self, n):
        assert self.listSize > n
        for i in range(n):
            node = self.head.prev
            if not node.empty:
                if self.callback is not None:
                    self.callback(node.key, node.value)
                del self.table[node.key]

            # Splice the tail node out of the list
            self.head.prev = node.prev
            node.prev.next = self.head

            self.movetail(node)

            # The next four lines are not strictly necessary.
            node.prev = None
            node.next = None

            node.key = None
            node.value = None

        self.listSize -= n


    def mtf(self, node):
        self.movetail(node)

        node.prev.next = node.next
        node.next.prev = node.prev

        node.prev = self.head.prev
        node.next = self.head.prev.next

        node.next.prev = node
        node.prev.next = node

    # This method returns an iterator that iterates over the non-empty nodes
    # in the doubly linked list in order from the most recently to the least
    # recently used.
    def dli(self):
        node = self.head
        for i in range(len(self.table)):
            yield node
            node = node.next

    def movetail(self, node):
        if self.tail == node:
            self.tail = self.tail.prev

    def least(self):
        # peek item from the least used
        node = self.tail
        if self.tail == self.head:
            return node.value
        self.tail = self.tail.prev
        while node.empty:
            node = self.tail
            self.tail = self.tail.prev
        return node.value
