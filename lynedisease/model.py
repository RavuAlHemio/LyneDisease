from functools import total_ordering

__author__ = 'ondra'


class Node:
    def __init__(self):
        pass

    @property
    def terminates(self):
        return False


class ShapeNode(Node):
    def __init__(self, shape, terminates=False):
        Node.__init__(self)

        self.shape = shape
        self._terminates = terminates

    @property
    def terminates(self):
        return self._terminates

    @terminates.setter
    def terminates(self, value):
        self._terminates = value


class MultipassNode(Node):
    def __init__(self, count):
        Node.__init__(self)

        self.count = count


@total_ordering
class Edge:
    def __init__(self, one, two):
        """
        :type one: int
        :type two: int
        """
        if one > two:
            self.one = two
            self.two = one
        else:
            self.one = one
            self.two = two

    def __eq__(self, you):
        return (self.one, self.two) == (you.one, you.two)

    def __lt__(self, you):
        return (self.one, self.two) < (you.one, you.two)

    def __repr__(self):
        return "Edge({0}, {1})".format(self.one, self.two)

    def __hash__(self):
        return 3 * (self.one, self.two).__hash__()

    def __contains__(self, what):
        return what in (self.one, self.two)

    def other_node(self, one_node):
        if self.one == one_node:
            return self.two
        elif self.two == one_node:
            return self.one
        return None


class Puzzle:
    def __init__(self):
        self.node_ids_to_nodes = {}
        """:type: dict[int, Node]"""
        self.node_ids_to_adjacent_node_ids = {}
        """:type: dict[int, set[int]]"""
        self.conflict_edge_pairs = set()
        """:type: set[(Edge, Edge)]"""

        self.next_node_id = 0

    def copy(self):
        p = Puzzle()
        p.node_ids_to_nodes = self.node_ids_to_nodes.copy()
        for (k, v) in self.node_ids_to_adjacent_node_ids:
            p.node_ids_to_adjacent_node_ids[k] = v.copy()
        p.conflict_edge_pairs = self.conflict_edge_pairs.copy()

        return p

    def add_node(self, node):
        """
        :type node: Node
        """
        node_id = self.next_node_id
        self.next_node_id += 1

        self.node_ids_to_nodes[node_id] = node
        self.node_ids_to_adjacent_node_ids[node_id] = set()

        return node_id

    def link_nodes(self, one_id, two_id):
        """
        :type one_id: int
        :type two_id: int
        """
        if one_id > two_id:
            one_id, two_id = two_id, one_id

        self.node_ids_to_adjacent_node_ids[one_id].add(two_id)

    def unlink_nodes(self, one_id, two_id):
        """
        :type one_id: int
        :type two_id: int
        """
        if one_id > two_id:
            one_id, two_id = two_id, one_id

        self.node_ids_to_adjacent_node_ids[one_id].remove(two_id)

    def are_nodes_linked(self, one_id, two_id):
        """
        :type one_id: int
        :type two_id: int
        :rtype: bool
        """
        if one_id > two_id:
            one_id, two_id = two_id, one_id

        return two_id in self.node_ids_to_adjacent_node_ids[one_id]

    @staticmethod
    def normalize_edge_couple(first, second):
        """
        :type first: Edge
        :type second: Edge
        :rtype: (Edge, Edge)
        """
        if first > second:
            first, second = second, first

        return first, second

    def add_edge_conflict(self, first, second):
        """
        :type first: Edge
        :type second: Edge
        """
        first, second = self.normalize_edge_couple(first, second)
        self.conflict_edge_pairs.add((first, second))

    def is_edge_conflict(self, first, second):
        """
        :type first: Edge
        :type second: Edge
        :rtype: bool
        """
        first, second = self.normalize_edge_couple(first, second)

        return (first, second) in self.conflict_edge_pairs
