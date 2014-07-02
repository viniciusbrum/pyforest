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
        return 'black' if self._color is _BLACK else 'red'

    def is_red(self):
        return self._color is _RED

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

    def _insert_fixup(self, node):
        while node.parent.is_red():
            if node.parent is node.parent.parent.left:
                y = node.parent.parent.right
                if y.is_red():
                    node.parent._set_black()
                    y._set_black()
                    node.parent.parent._set_red()
                    node = node.parent.parent
                else:
                    if node is node.parent.right:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent._set_black()
                    node.parent.parent._set_red()
                    self._right_rotate(node.parent.parent)
            else:
                y = node.parent.parent.left
                if y.is_red():
                    node.parent._set_black()
                    y._set_black()
                    node.parent.parent._set_red()
                    node = node.parent.parent
                else:
                    if node is node.parent.left:
                        node = node.parent
                        self._left_rotate(node)
                    node.parent._set_black()
                    node.parent.parent._set_red()
                    self._right_rotate(node.parent.parent)
        self._root._set_black()

    def _insert(self, new_node):
        BinarySearchTree._insert(self, new_node)
        self.print_tree()
        self._insert_fixup(new_node)

    def _transplant(self, old_node, new_node):
        if old_node.parent is None:
            self._root = new_node
        elif old_node is old_node.parent.left:
            old_node.parent.left = new_node
        else:
            old_node.parent.right = new_node
        new_node.parent = old_node.parent

    def _delete_fixup(self, node):
        while node is not self.root and node.is_black():
            if node is node.parent.left:
                w = node.parent.right
                if w.is_red():
                    w._set_black()
                    node.parent._set_red()
                    self._left_rotate(node.parent)
                    w = node.parent.right
                if not w.left.is_red() and not w.right.is_red():
                    w._set_red()
                    node = node.parent
                else:
                    if not w.right.is_red():
                        w.left._set_black()
                        w._set_red()
                        self._right_rotate(w)
                        w = node.parent.right
                    if node.parent.is_red():
                        w._set_red()
                    else:
                        w._set_black()
                    node.parent._set_black()
                    w.right._set_black()
                    self._left_rotate(node.parent)
                    node = self.root
            else:
                w = node.parent.left
                if w.is_red():
                    w._set_black()
                    node.parent._set_red()
                    self._left_rotate(node.parent)
                    w = node.parent.left
                if not w.right.is_red() and not w.left.is_red():
                    w._set_red()
                    node = node.parent
                else:
                    if not w.left.is_red():
                        w.right._set_black()
                        w._set_red()
                        self._right_rotate(w)
                        w = node.parent.left
                    if node.parent.is_red():
                        w._set_red()
                    else:
                        w._set_black()
                    node.parent._set_black()
                    w.left._set_black()
                    self._left_rotate(node.parent)
                    node = self.root
        node._set_black()

    def _delete(self, node_key):
        suce_node_key = node_key
        suce_orig_color = suce_node_key.color
        if node_key.left is None:
            node = node_key.right
            self._transplant(node_key, node_key.right)
        elif node_key.right is None:
            node = node_key.left
            self._transplant(node_key, node_key.left)
        else:
            suce_node_key = self._minimum(node_key.right)
            suce_orig_color = suce_node_key.color
            node = suce_node_key.right
            if suce_node_key.parent is None:
                node.parent = suce_node_key
            else:
                self._transplant(suce_node_key, suce_node_key.right)
                suce_node_key.right = node_key.right
                suce_node_key.right.parent = suce_node_key
            self._transplant(node_key, suce_node_key)
            suce_node_key.left = node_key.left
            suce_node_key.left.parent = suce_node_key
            if node_key.is_red():
                suce_node_key._set_red()
            else:
                suce_node_key._set_black()
        if suce_orig_color == 'black':
            self._delete_fixup(node)

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
