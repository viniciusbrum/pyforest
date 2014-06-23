from __builtin__ import isinstance
from types import NoneType
from exceptions.pfexceptions import PFTypeError


class NodeBSTree(object):
    _key = None
    _left = None
    _right = None
    _parent = None

    def __init__(self, key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None

    def __str__(self):
        return '{0:s}'.format(str(self.key))

    def __repr__(self):
        str_repr = "'<{0:s}.".format(self.__module__)
        str_repr += "{0:s} object at ".format(self.__class__.__name__)
        str_repr += "{0:#x} with key: {1:s}>'".format(id(self), str(self.key))
        return str_repr

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, node):
        if isinstance(node, self.__class__) or isinstance(node, NoneType):
            self._left = node
        else:
            raise PFTypeError('left',
                              '%s or NoneType' % (self.__class__.__name__))

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, node):
        if isinstance(node, self.__class__) or isinstance(node, NoneType):
            self._right = node
        else:
            raise PFTypeError('right',
                              '%s or NoneType' % (self.__class__.__name__))

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, node):
        if isinstance(node, self.__class__) or isinstance(node, NoneType):
            self._parent = node
        else:
            raise PFTypeError('parent',
                              '%s or NoneType' % (self.__class__.__name__))


class BinarySearchTree(object):
    _root = None
    _num_nodes = None

    def __init__(self, key=None):
        if key is not None:
            self._root = NodeBSTree(key)
            self._num_nodes = 1
        else:
            self._root = None
            self._num_nodes = 0

    def __repr__(self):
        str_repr = "'<{0:s}.".format(self.__module__)
        str_repr += "{0:s} object at ".format(self.__class__.__name__)
        str_repr += "{0:#x} with {1:d} nodes".format(id(self), self.num_nodes)
        str_repr += " and root: {0:s}>'".format(eval(repr(self.root)))
        return str_repr

    @property
    def root(self):
        return self._root

    @property
    def num_nodes(self):
        return self._num_nodes

    def in_order_walk(self):
        walk_result = list()
        self._in_order_walk(self.root, walk_result)
        return walk_result

    def search(self, key):
        return self._search(self.root, key)

    def min(self):
        return self._minimum(self.root)

    def max(self):
        return self._maximum(self.root)

    def sucessor(self, root=None):
        root = self.root if root is None else root
        return self._sucessor(root)

    def predecessor(self, root=None):
        root = self.root if root is None else root
        return self._predecessor(root)

    def insert(self, key):
        if self.root is None:
            self._root = NodeBSTree(key)
            self._num_nodes = 1
        else:
            new_node = NodeBSTree(key)
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

    def print_tree(self, root=None, space=' |    ', level=0, root_prefix='[*]',
                   debug=False):
        root = self.root if root is None else root
        print '*' * 10
        self._print(root, space, level, root_prefix, debug)
        print '*' * 10

    def get_height(self):
        return self._get_height(self.root)

    def _in_order_walk(self, root, walk_result):
        if root is not None:
            self._in_order_walk(root.left, walk_result)
            walk_result.append(root.key)
            self._in_order_walk(root.right, walk_result)

    def _search(self, root, key):
        if root is None or key == root.key:
            return root
        if key < root.key:
            return self._search(root.left, key)
        else:
            return self._search(root.right, key)

    def _minimum(self, root):
        if root.left is None:
            return root
        return self._minimum(root.left)

    def _maximum(self, root):
        if root.right is None:
            return root
        return self._maximum(root.right)

    def _sucessor(self, root):
        if root.right is not None:
            return self._minimum(root.right)
        parent = root.parent
        node = root
        while parent is not None and node is parent.right:
            node = parent
            parent = parent.parent
        return parent

    def _predecessor(self, root):
        if root.left is not None:
            return self._maximum(root.left)
        parent = root.parent
        node = root
        while parent is not None and node is parent.left:
            node = parent
            parent = parent.parent
        return parent

    def _insert(self, new_node):
        parent = None
        node = self._root
        while node is not None:
            parent = node
            node = node.left if new_node.key < node.key else node.right
        new_node.parent = parent
        if new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

    def _transplant(self, old_node, new_node):
        if old_node.parent is None:
            self._root = new_node
        elif old_node is old_node.parent.left:
            old_node.parent.left = new_node
        else:
            old_node.parent.right = new_node
        if new_node is not None:
            new_node.parent = old_node.parent

    def _delete(self, node_key):
        if node_key.left is None:
            self._transplant(node_key, node_key.right)
        elif node_key.right is None:
            self._transplant(node_key, node_key.left)
        else:
            suce_node_key = self._minimum(node_key.right)
            if suce_node_key.parent != node_key:
                self._transplant(suce_node_key, suce_node_key.right)
                suce_node_key.right = node_key.right
                suce_node_key.right.parent = suce_node_key
            self._transplant(node_key, suce_node_key)
            suce_node_key.left = node_key.left
            suce_node_key.left.parent = suce_node_key

    def _print(self, root, space, level, root_prefix, debug):
        if root is not None:
            print space * level, root_prefix, '{', root, '}',
            print (eval(repr(root)) if debug else '')
            self._print(root.left, space, level + 1, '[l]', debug)
            self._print(root.right, space, level + 1, '[r]', debug)

    def _get_height(self, root):
        if root is None:
            return -1
        left_height = self._get_height(root.left)
        right_height = self._get_height(root.right)
        return max(left_height, right_height) + 1
