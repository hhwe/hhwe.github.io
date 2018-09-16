# bianary tree
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

    def add(self, val):
        """ 添加节点 """
        if self.root is None:
            self.root = Node(val)
        else:
            self._add(self.root, val)

    def _add(self, node, val):
        if val < node.v:
            if node.l is None:
                node.l = Node(val)
            else:
                self._add(node.l, val)
        else:
            if node.r is None:
                node.r = Node(val)
            else:
                self._add(node.r, val)

    def find(self, val):
        """ 查找元素 """
        if self.root is None:
            return None
        else:
            return self._find(self.root, val)

    def _find(self, node, val):
        if val == node.v:
            return val
        elif val < node.v and node.l is None:
            return self._find(node.l, val)
        elif val > node.v and node.r is None:
            return self._find(node.r, val)

    def pre_order_traversal(self, node):
        """ 深度先序遍历,根->左->右 """
        if node is None:
            return
        print(node.v)
        self.pre_order_traversal(node.l)
        self.pre_order_traversal(node.r)

    def mid_order_traversal(self, node):
        """ 深度中序遍历,左->根->右 """
        if node is None:
            return
        self.mid_order_traversal(node.l)
        print(node.v)
        self.mid_order_traversal(node.r)

    def post_order_traversal(self, node):
        """ 深度后序遍历,左->右->根 """
        if node is None:
            return
        self.post_order_traversal(node.l)
        self.post_order_traversal(node.r)
        print(node.v)

    def layer_traversal(self, node):
        """ 广度优先遍历,层级 """
        if node is None:
            return
        q = []
        q.append(node)
        while q:
            n = q.pop(0)
            print(n.v)
            if n.l is not None:
                q.append(n.l)
            if n.r is not None:
                q.append(n.r)

    def max_depth(self, node):
        """ 最大深度 """
        if node is None:
            return
        lp, rp = 0, 0
        if node.l is not None:
            lp = self.max_depth(node.l)
        if node.r is not None:
            rp = self.max_depth(node.r)
        return max(lp, rp) + 1


tree = Tree()
tree.add(5)
tree.add(2)
tree.add(8)
tree.add(4)
tree.add(9)
tree.add(7)
tree.add(1)
tree.add(6)
tree.add(3)
print(tree.find(15))
print(tree.find(6))
print('====== 先序遍历 ========')
tree.pre_order_traversal(tree.root)
print('====== 中序遍历 ========')
tree.mid_order_traversal(tree.root)
print('====== 后序遍历 ========')
tree.post_order_traversal(tree.root)
print('====== 广度遍历 ========')
tree.layer_traversal(tree.root)
print('deep: ', tree.max_depth(tree.root))
