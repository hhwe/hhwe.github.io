# /usr/bin/env python
# -*- coding:utf-8 -*-


def bubble_sort(arr):
    """
    time complexity: O(n^2)
    space complexity: O(1)
    :prarm arr: list
    :return: list
    """
    if not isinstance(arr, list):
        raise TypeError
    for i in range(len(arr)):
        for j in range(len(arr)-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def insettion_sort(arr):
    """
    time complexity: O(n^2)
    space complexity: O(1)
    :prarm arr: list
    :return: list
    """
    if not isinstance(arr, list):
        raise TypeError
    for i in range(1, len(arr)):
        for j in range(i):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr


def selection_sort(arr):
    """
    time complexity: O(n^2)
    space complexity: O(1)
    :prarm arr: list
    :return: list
    """
    if not isinstance(arr, list):
        raise TypeError
    for i in range(len(arr)):
        min = i
        for j in range(i+1, len(arr)):
            if arr[j] < arr[min]:
                min = j
        if min != i:
            arr[i], arr[min] = arr[min], arr[i]
    return arr


def merge_sort(arr):
    """
    time complexity: O(n*logn)
    space complexity: O(n)
    :prarm arr: list
    :return: list
    """
    if not isinstance(arr, list):
        raise TypeError
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    k, i, j = 0, 0, 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        k += 1
    if i < len(left):
        arr[k:] = left[i:]
    if j < len(right):
        arr[k:] = right[j:]
    return arr


def quick_sort(arr):
    """
    time complexity: O(n*logn)
    space complexity: O(1)
    :prarm arr: list
    :return: list
    """
    if not isinstance(arr, list):
        raise TypeError
    if len(arr) <= 1:
        return arr
    else:
        left = quick_sort([x for x in arr[1:] if x < arr[0]])
        mid = [arr[0]]
        right = quick_sort([x for x in arr[1:] if x >= arr[0]])
        return left + mid + right


class Node:
    """ binary tree node """
    def __init__(self, val):
        self.l = None
        self.r = None
        self.v = val


class Tree:
    """ binary tree """
    def __init__(self):
        self.root = None

    def get_root(self):
        return self.root

    def add(self, val):
        if self.root is None:
            self.root = Node(val)
        else:
            self._add(val, self.root)

    def _add(self, val, node):
        if val < node.v:
            if node.l is not None:
                self._add(val, node.l)
            else:
                node.l = Node(val)
        else:
            if node.r is not None:
                self._add(val, node.r)
            else:
                node.r = Node(val)

    def find(self, val):
        if self.root is not None:
            return self._find(val, self.root)
        else:
            return None

    def _find(self, val, node):
        if val == node.v:
            return node
        elif val < node.v and node.l is not None:
            self._find(val, node.l)
        elif val > node.v and node.r is not None:
            self._find(val, node.r)

    def delete_tree(self):
        self.root = None

    def print_tree(self):
        if self.root is not None:
            self._print_tree(self.root)

    def _print_tree(self, node):
        if node is not None:
            self._print_tree(node.l)
            print(str(node.v) + ' ')
            self._print_tree(node.r)


if __name__ == "__main__":
    arr = [4, 5, 6, 2, 4, 8, 9, 3, 5, 4, 7, 6, 2, 1, 5]
    print(arr)
    b_arr = bubble_sort(arr.copy())
    print(b_arr)
    i_arr = insettion_sort(arr.copy())
    print(i_arr)
    s_arr = selection_sort(arr.copy())
    print(s_arr)
    m_arr = merge_sort(arr.copy())
    print(m_arr)
    q_arr = quick_sort(arr.copy())
    print(q_arr)

    tree = Tree()
    tree.add(3)
    tree.add(4)
    tree.add(0)
    tree.add(8)
    tree.add(2)
    tree.print_tree()
    print((tree.find(3)).v)
    print(tree.find(10))
    tree.delete_tree()
    tree.print_tree()
