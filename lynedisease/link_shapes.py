import lynedisease.model as m

__author__ = 'ondra'


def triangle_link(puzzle, one, two, three):
    puzzle.link_nodes(one, two)
    puzzle.link_nodes(one, three)
    puzzle.link_nodes(two, three)


def square_link(puzzle, one, two, three, four):
    # 1 -- 2
    # | \/ |
    # | /\ |
    # 3 -- 4
    if one is not None:
        if two is not None:
            puzzle.link_nodes(one, two)
        if three is not None:
            puzzle.link_nodes(one, three)
        if four is not None:
            puzzle.link_nodes(one, four)
    if two is not None:
        if three is not None:
            puzzle.link_nodes(two, three)
        if four is not None:
            puzzle.link_nodes(two, four)
    if three is not None:
        if four is not None:
            puzzle.link_nodes(three, four)
    if one is not None and two is not None and three is not None and four is not None:
        puzzle.add_edge_conflict(m.Edge(one, four), m.Edge(two, three))


def square_lattice(puzzle, node_ids, columns, rows):
    for row in range(rows-1):
        for column in range(columns-1):
            top_left = node_ids[(row + 0) * columns + (column + 0)]
            top_right = node_ids[(row + 0) * columns + (column + 1)]
            bottom_left = node_ids[(row + 1) * columns + (column + 0)]
            bottom_right = node_ids[(row + 1) * columns + (column + 1)]

            square_link(puzzle, top_left, top_right, bottom_left, bottom_right)
