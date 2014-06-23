from bstree import BinarySearchTree
from bstree import NodeBSTree

_BLACK = True
_RED = False


class NodeRBTree(NodeBSTree):
    _color = None

    def __init__(self, key):
        NodeBSTree.__init__(self, key)
        self._set_red()

    def __str__(self):
        return '{0:s}, {1:s}'.format(str(self.key), self.color)

    def __repr__(self):
        str_repr = "'<{0:s}.".format(self.__module__)
        str_repr += "{0:s} object at ".format(self.__class__.__name__)
        str_repr += "{0:#x} with key: {1:s} ".format(id(self), str(self.key))
        str_repr += "in: {0:s}>'".format(self.color)
        return str_repr

    @property
    def color(self):
        return 'black' if self._color else 'red'

    def is_red(self):
        return self._color == _RED

    def _set_black(self):
        self._color = _BLACK

    def _set_red(self):
        self._color = _RED


class RedBlackTree(BinarySearchTree):

    def __init__(self, key=None):
        if key is not None:
            self._root = NodeRBTree(key)
            self._root._set_black()
            self._num_nodes = 1
        else:
            self._root = None
            self._num_nodes = 0

    def insert(self, key):
        if self.root is None:
            self._root = NodeRBTree(key)
            self._root._set_black()
            self._num_nodes = 1
        else:
            new_node = NodeRBTree(key)
            self._insert(new_node)
            self._num_nodes += 1

    def delete(self, key, debug=False):
        node_key = self.search(key)
        if node_key is not None:
            if debug:
                print 'before removing key', key, 'in', eval(repr(node_key))
                self.print_tree(debug=True)
            self._delete(node_key)
            if debug:
                print '... after removing', key, 'in', eval(repr(node_key))
                self.print_tree(debug=True)
            del(node_key)
            self._num_nodes -= 1
            return True
        elif debug:
            print 'key %s not found!' % key
        return False

    def get_height(self):
        return self._get_height(self.root)

    def get_black_height(self):
        return self._get_black_height(self.root)

    def _left_rotate(self, old_root):
        new_root = old_root.right
        old_root.right = new_root.left
        if new_root.left is not None:
            new_root.left.parent = old_root
        new_root.parent = old_root.parent
        if old_root.parent is None:
            self._root = new_root
        elif old_root is old_root.parent.left:
            old_root.parent.left = new_root
        else:
            old_root.parent.right = new_root
        new_root.left = old_root
        old_root.parent = new_root

    def _right_rotate(self, old_root):
        new_root = old_root.left
        old_root.left = new_root.right
        if new_root.right is not None:
            new_root.right.parent = old_root
        new_root.parent = old_root.parent
        if old_root.parent is None:
            self._root = new_root
        elif old_root is old_root.parent.left:
            old_root.parent.left = new_root
        else:
            old_root.parent.right = new_root
        new_root.right = old_root
        old_root.parent = new_root

    def _insert_fixup(self, z):
        while z.parent.is_red():
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y.is_red():
                    z.parent._set_black()
                    y._set_black()
                    z.parent.parent._set_red()
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent._set_black()
                    z.parent.parent._set_red()
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.is_red():
                    z.parent._set_black()
                    y._set_black()
                    z.parent.parent._set_red()
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent._set_black()
                    z.parent.parent._set_red()
                    self._right_rotate(z.parent.parent)
        self._root._set_black()

    def _insert(self, new_node):
        BinarySearchTree._insert(self, new_node)
        self.print_tree()
        self._insert_fixup(new_node)

    def _transplant(self, old_node, new_node):
        pass

    def _delete(self, node_key):
        pass

    def _get_height(self, root):
        if root is None:
            return -1
        if root.left is None:
            return self._get_height(root.right) + 1
        if root.right is None:
            return self._get_height(root.left) + 1
        if root.left.color == root.right.color:
            left_height = self._get_height(root.left)
            right_height = self._get_height(root.right)
            return max(left_height, right_height) + 1
        elif root.left.is_red():
            return self._get_height(root.left) + 1
        else:
            self._get_height(root.right) + 1

    def _get_black_height(self, root):
        black_height = 0
        node = root
        while node.left is not None:
            if not node.left.is_red():
                black_height += 1
            node = node.left
        return black_height
