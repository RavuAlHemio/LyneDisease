import lynedisease.link_shapes as ls
import lynedisease.model as m
import lynedisease.solver as s

from unittest import TestCase

__author__ = 'ondra'


def linear_pairs(max_value):
    for n in range(max_value):
        yield (n, n+1)


class SolverTests(TestCase):
    def test_single_edge(self):
        puzzle = m.Puzzle()

        n1 = m.ShapeNode(0, terminates=True)
        n2 = m.ShapeNode(0, terminates=True)

        ni1 = puzzle.add_node(n1)
        ni2 = puzzle.add_node(n2)

        puzzle.link_nodes(ni1, ni2)

        solution = s.solve(puzzle)

        self.assertIsNotNone(solution)
        self.assertEqual(1, len(solution))
        self.assertIn(0, solution.keys())
        self.assertEqual(
            {ni1, ni2},
            set(solution[0])
        )

    def test_connect_three(self):
        puzzle = m.Puzzle()

        n1 = m.ShapeNode(0, terminates=True)
        n2 = m.ShapeNode(0)
        n3 = m.ShapeNode(0, terminates=True)

        ni1 = puzzle.add_node(n1)
        ni2 = puzzle.add_node(n2)
        ni3 = puzzle.add_node(n3)

        puzzle.link_nodes(ni1, ni2)
        puzzle.link_nodes(ni2, ni3)

        solution = s.solve(puzzle)

        self.assertIsNotNone(solution)
        self.assertEqual(1, len(solution))
        self.assertIn(0, solution.keys())
        self.assertEqual(
            {ni1, ni2, ni3},
            set(solution[0])
        )

    def test_fork(self):
        puzzle = m.Puzzle()

        n1 = m.ShapeNode(0, terminates=True)
        n2 = m.ShapeNode(0)
        n3 = m.ShapeNode(0)
        n4 = m.ShapeNode(0, terminates=True)

        ni1 = puzzle.add_node(n1)
        ni2 = puzzle.add_node(n2)
        ni3 = puzzle.add_node(n3)
        ni4 = puzzle.add_node(n4)

        puzzle.link_nodes(ni1, ni2)
        puzzle.link_nodes(ni1, ni3)
        puzzle.link_nodes(ni2, ni3)
        puzzle.link_nodes(ni2, ni4)
        puzzle.link_nodes(ni3, ni4)

        solution = s.solve(puzzle)

        self.assertIsNotNone(solution)
        self.assertEqual(1, len(solution))
        self.assertIn(0, solution.keys())
        self.assertEqual(
            {ni1, ni2, ni3, ni4},
            set(solution[0])
        )

    def test_two_colors(self):
        puzzle = m.Puzzle()

        n1 = m.ShapeNode(0, terminates=True)
        n2 = m.ShapeNode(0, terminates=True)
        n3 = m.ShapeNode(1, terminates=True)
        n4 = m.ShapeNode(1, terminates=True)

        ni1 = puzzle.add_node(n1)
        ni2 = puzzle.add_node(n2)
        ni3 = puzzle.add_node(n3)
        ni4 = puzzle.add_node(n4)

        puzzle.link_nodes(ni1, ni2)
        puzzle.link_nodes(ni2, ni3)
        puzzle.link_nodes(ni3, ni4)

        solution = s.solve(puzzle)

        self.assertIsNotNone(solution)
        self.assertEqual(2, len(solution))
        self.assertEqual({0, 1}, set(solution.keys()))
        self.assertEqual(
            {ni1, ni2},
            set(solution[0])
        )
        self.assertEqual(
            {ni3, ni4},
            set(solution[1])
        )

    def test_not_enough_terminators(self):
        puzzle = m.Puzzle()

        n1 = m.ShapeNode(0, terminates=True)
        n2 = m.ShapeNode(0)

        ni1 = puzzle.add_node(n1)
        ni2 = puzzle.add_node(n2)

        puzzle.link_nodes(ni1, ni2)

        with self.assertRaises(ValueError):
            solution = s.solve(puzzle)

    def test_unconnected(self):
        puzzle = m.Puzzle()

        n1 = m.ShapeNode(0, terminates=True)
        n2 = m.ShapeNode(0, terminates=True)

        puzzle.add_node(n1)
        puzzle.add_node(n2)

        solution = s.solve(puzzle)

        self.assertIsNone(solution)

    def test_interrupted_line(self):
        puzzle = m.Puzzle()

        nodes = [
            m.ShapeNode(0, terminates=True),
            m.ShapeNode(1, terminates=True),
            m.ShapeNode(1, terminates=True),
            m.ShapeNode(0, terminates=True),
        ]

        node_ids = [puzzle.add_node(n) for n in nodes]

        for (a, b) in linear_pairs(3):
            puzzle.link_nodes(node_ids[a], node_ids[b])

        solution = s.solve(puzzle)

        self.assertIsNone(solution)

    def test_empty_puzzle(self):
        puzzle = m.Puzzle()
        solution = s.solve(puzzle)
        self.assertIsNotNone(solution)
        self.assertEqual(0, len(solution))

    def test_simple_multipass(self):
        puzzle = m.Puzzle()

        nodes = [
            m.ShapeNode(0, terminates=True),
            m.MultipassNode(1),
            m.ShapeNode(0, terminates=True),
        ]

        node_ids = [puzzle.add_node(n) for n in nodes]

        for (a, b) in linear_pairs(2):
            puzzle.link_nodes(node_ids[a], node_ids[b])

        solution = s.solve(puzzle)

        self.assertIsNotNone(solution)
        self.assertEqual(1, len(solution))
        self.assertEqual(
            set(node_ids),
            set(solution[0])
        )

    def test_simple_multipass_fail(self):
        puzzle = m.Puzzle()

        nodes = [
            m.ShapeNode(0, terminates=True),
            m.MultipassNode(2),
            m.ShapeNode(0, terminates=True),
        ]

        node_ids = [puzzle.add_node(n) for n in nodes]

        for (a, b) in linear_pairs(2):
            puzzle.link_nodes(node_ids[a], node_ids[b])

        solution = s.solve(puzzle)

        self.assertIsNone(solution)

    def test_multipass_two(self):
        puzzle = m.Puzzle()

        nodes = [
            m.ShapeNode(0, terminates=True),
            m.MultipassNode(2),
            m.ShapeNode(0),
            m.ShapeNode(0),
            m.ShapeNode(0, terminates=True),
        ]

        node_ids = [puzzle.add_node(n) for n in nodes]

        for (a, b) in ((0, 1), (1, 2), (2, 3), (3, 1), (1, 4)):
            puzzle.link_nodes(node_ids[a], node_ids[b])

        solution = s.solve(puzzle)

        self.assertIsNotNone(solution)
        self.assertEqual(1, len(solution))
        self.assertIn(
            solution[0],
            ([0, 1, 2, 3, 1, 4], [4, 1, 3, 2, 1, 0])
        )

    def test_c16(self):
        puzzle = m.Puzzle()

        # 0 = triangle, 1 = square-on-tip
        nodes = [
            m.ShapeNode(0),
            # nothing
            m.ShapeNode(1, terminates=True),
            m.MultipassNode(2),
            m.MultipassNode(2),
            m.ShapeNode(0, terminates=True),
            m.ShapeNode(0, terminates=True),
            m.MultipassNode(3),
            m.ShapeNode(0),
            m.ShapeNode(1),
            m.MultipassNode(2),
            m.ShapeNode(1, terminates=True),
        ]

        node_ids = [puzzle.add_node(n) for n in nodes]

        for triangle in ((0, 2, 3), (1, 3, 4)):
            triangle_ids = [node_ids[i] for i in triangle]
            ls.triangle_link(puzzle, *triangle_ids)

        for square in ((2, 3, 5, 6), (3, 4, 6, 7), (5, 6, 8, 9), (6, 7, 9, 10)):
            square_ids = [node_ids[i] for i in square]
            ls.square_link(puzzle, *square_ids)

        solution = s.solve(puzzle)

        self.assertIsNotNone(solution)

    def test_c17(self):
        puzzle = m.Puzzle()

        # 0 = square-on-tip, 1 = square
        nodes = [
            m.ShapeNode(0),
            m.ShapeNode(1),
            m.ShapeNode(1, terminates=True),
            m.ShapeNode(0, terminates=True),
            m.MultipassNode(3),
            m.ShapeNode(0, terminates=True),
            m.ShapeNode(0),
            m.MultipassNode(2),
            m.MultipassNode(2),
            m.ShapeNode(1, terminates=True),
            m.MultipassNode(2),
            m.ShapeNode(0),
        ]

        node_ids = [puzzle.add_node(n) for n in nodes]

        ls.square_lattice(puzzle, node_ids, 3, 4)

        solution = s.solve(puzzle)

        self.assertIsNotNone(solution)

    def test_c18(self):
        puzzle = m.Puzzle()

        # 0 = square-on-tip, 1 = triangle
        nodes = [
            m.ShapeNode(0),
            m.MultipassNode(2),
            m.ShapeNode(1, terminates=True),
            m.MultipassNode(2),
            m.MultipassNode(2),
            m.ShapeNode(0, terminates=True),
            m.ShapeNode(1, terminates=True),
            m.MultipassNode(3),
            m.ShapeNode(0),
            m.ShapeNode(1),
            m.ShapeNode(1),
            m.ShapeNode(0, terminates=True),
        ]

        node_ids = [puzzle.add_node(n) for n in nodes]

        ls.square_lattice(puzzle, node_ids, 3, 4)

        solution = s.solve(puzzle)

        self.assertIsNotNone(solution)

    def test_d13(self):
        puzzle = m.Puzzle()

        nodes = [
            # nothing
            m.ShapeNode(0, terminates=True),
            m.ShapeNode(1, terminates=True),
            m.ShapeNode(2),
            m.ShapeNode(2, terminates=True),
            m.MultipassNode(2),
            m.ShapeNode(2, terminates=True),
            m.MultipassNode(3),
            m.MultipassNode(2),
            m.ShapeNode(1, terminates=True),
            m.ShapeNode(2),
            m.ShapeNode(0, terminates=True),
        ]

        node_ids = [puzzle.add_node(n) for n in nodes]

        ls.triangle_link(puzzle, node_ids[0], node_ids[2], node_ids[3])
        for square in (
                (0, 1, 3, 4),
                (2, 3, 5, 6),
                (3, 4, 6, 7),
                (5, 6, 8, 9),
                (6, 7, 9, 10),
        ):
            square_ids = [node_ids[i] for i in square]
            ls.square_link(puzzle, *square_ids)

        solution = s.solve(puzzle)

        self.assertIsNotNone(solution)
        print(solution)

    def test_d18(self):
        puzzle = m.Puzzle()

        # 0 = square, 1 = square-on-tip, 2 = triangle
        nodes = [
            m.ShapeNode(0, terminates=True),
            m.ShapeNode(1, terminates=True),
            m.ShapeNode(1, terminates=True),
            m.MultipassNode(2),
            m.MultipassNode(2),
            m.MultipassNode(2),
            m.ShapeNode(2, terminates=True),
            m.MultipassNode(3),
            m.ShapeNode(0),
            # nothing
            m.ShapeNode(0, terminates=True),
            m.ShapeNode(2, terminates=True),
        ]

        node_ids = [puzzle.add_node(n) for n in nodes]

        ls.triangle_link(puzzle, node_ids[6], node_ids[7], node_ids[9])
        for square in (
                (0, 1, 3, 4),
                (1, 2, 4, 5),
                (3, 4, 6, 7),
                (4, 5, 7, 8),
                (7, 8, 9, 10),
        ):
            square_ids = [node_ids[i] for i in square]
            ls.square_link(puzzle, *square_ids)

        solution = s.solve(puzzle)

        self.assertIsNotNone(solution)
        print(solution)
