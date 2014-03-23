from lynedisease.model import Edge, MultipassNode, ShapeNode

__author__ = 'ondra'


def copy_add_node_to_shape_path(shapes_to_paths, shape, node_id):
    ret = {}
    for (k, vs) in shapes_to_paths.items():
        ret[k] = vs.copy()
        if k == shape:
            ret[k].append(node_id)
    return ret


def remove_edge_and_conflicting_edges(puzzle, available_edges, new_edge):
    ret = set()
    for edge in available_edges:
        if edge == new_edge:
            continue
        conflict = False
        for pair in puzzle.conflict_edge_pairs:
            if new_edge in pair and edge in pair:
                conflict = True
                break
        if conflict:
            continue

        ret.add(edge)

    return ret


def remove_edges_containing_node(available_edges, node_id):
    ret = set()
    for edge in available_edges:
        if node_id in edge:
            continue
        ret.add(edge)
    return ret


def solve_step(
        puzzle, shapes_to_do, shapes_to_paths, shape_terminators, available_edges, multipass_counts
):
    """
    :type puzzle: lynedisease.model.Puzzle
    :type shapes_to_do: list[int]
    :type shapes_to_paths: dict[int, list[int]]
    :type shape_terminators: dict[int, set[int]]
    :type available_edges: set[Edge]
    :type multipass_counts: dict[int, int]
    return dict[int, list[int]]|None
    """

    #print(
    #    "solve_step",
    #    "  shapes_to_do={0}".format(shapes_to_do),
    #    "  shape_terminators={0}".format(shape_terminators),
    #    "  shapes_to_paths={0}".format(shapes_to_paths),
    #    "  available_edges={0}".format(available_edges),
    #    "  multipass_counts={0}".format(multipass_counts),
    #    sep="\n"
    #)

    if len(shapes_to_do) == 0:
        # check the multipass counts
        for (node_id, node) in puzzle.node_ids_to_nodes.items():
            if isinstance(node, MultipassNode):
                if multipass_counts[node_id] != node.count:
                    # humbug!
                    return None

        # well, we're done here
        return shapes_to_paths

    shape = shapes_to_do[0]

    if len(shapes_to_paths[shape]) == 0:
        # start at a terminator
        terminator = next(iter(shape_terminators[shape]))
        shapes_to_paths[shape] = [terminator]

    # go to the last node
    node_id = shapes_to_paths[shape][-1]
    node = puzzle.node_ids_to_nodes[node_id]

    # if it's a shape node, make sure it's never visited again
    if isinstance(node, ShapeNode):
        filtered_available_edges = remove_edges_containing_node(available_edges, node_id)
    else:
        filtered_available_edges = available_edges.copy()

    # let's see where we can go
    for edge in available_edges:
        sub_available_edges = filtered_available_edges

        if node_id not in edge:
            continue

        other_id = edge.other_node(node_id)
        other = puzzle.node_ids_to_nodes[other_id]

        if isinstance(other, ShapeNode):
            if other.shape == shape:
                # link potential!
                if other.terminates:
                    # this would terminate the path
                    # check if we thereby hit all nodes of this shape
                    all_hit = True
                    for (third_id, third) in puzzle.node_ids_to_nodes.items():
                        if isinstance(third, ShapeNode) \
                                and third.shape == shape \
                                and third_id != other_id \
                                and third_id not in shapes_to_paths[shape]:
                            all_hit = False
                            break

                    if all_hit:
                        # shape completed!
                        sub_shapes_to_do = shapes_to_do[1:]

                        # sub this
                        sub_shapes_to_paths = copy_add_node_to_shape_path(
                            shapes_to_paths, shape, other_id
                        )
                        sub_available_edges = remove_edge_and_conflicting_edges(
                            puzzle, sub_available_edges, edge
                        )
                        sub_ret = solve_step(
                            puzzle, sub_shapes_to_do, sub_shapes_to_paths, shape_terminators,
                            sub_available_edges, multipass_counts
                        )
                        if sub_ret is not None:
                            return sub_ret
                    # otherwise, do nothing -- premature termination leads us nowhere
                else:
                    # try this one
                    sub_shapes_to_paths = copy_add_node_to_shape_path(
                        shapes_to_paths, shape, other_id
                    )
                    sub_available_edges = remove_edge_and_conflicting_edges(
                        puzzle, sub_available_edges, edge
                    )
                    sub_ret = solve_step(
                        puzzle, shapes_to_do, sub_shapes_to_paths, shape_terminators,
                        sub_available_edges, multipass_counts
                    )
                    if sub_ret is not None:
                        return sub_ret

        elif isinstance(other, MultipassNode):
            # increase the counter
            sub_multipass_counts = multipass_counts.copy()
            sub_multipass_counts[other_id] += 1

            # go
            sub_shapes_to_paths = copy_add_node_to_shape_path(
                shapes_to_paths, shape, other_id
            )
            sub_available_edges = remove_edge_and_conflicting_edges(
                puzzle, sub_available_edges, edge
            )
            sub_ret = solve_step(
                puzzle, shapes_to_do, sub_shapes_to_paths, shape_terminators, sub_available_edges,
                sub_multipass_counts
            )
            if sub_ret is not None:
                return sub_ret


def solve(puzzle):
    """:type puzzle: lynedisease.model.Puzzle"""
    # calculate edge set
    available_edges = set()
    for (node_id, adjacent_ids) in puzzle.node_ids_to_adjacent_node_ids.items():
        for adjacent_id in adjacent_ids:
            available_edges.add(Edge(node_id, adjacent_id))

    # find terminators
    shapes = set()
    shape_terminators = {}
    multipass_counts = {}
    for (node_id, node) in puzzle.node_ids_to_nodes.items():
        if isinstance(node, ShapeNode):
            shapes.add(node.shape)
            if node.terminates:
                if node.shape not in shape_terminators:
                    shape_terminators[node.shape] = set()
                shape_terminators[node.shape].add(node_id)
        elif isinstance(node, MultipassNode):
            multipass_counts[node_id] = 0

    # validate that
    if len(shapes) != len(shape_terminators):
        raise ValueError(
            "some shapes are without terminators! (shapes: {0}, terminated shapes: {1})".format(
                sorted(shapes), sorted(shape_terminators.keys())
            )
        )

    # check for correct termination
    for (shape, terminators) in shape_terminators.items():
        if len(terminators) != 2:
            raise ValueError("shape {0} has {1} terminators".format(shape, len(terminators)))

    # empty paths
    shapes_to_paths = {}
    for shape in shapes:
        shapes_to_paths[shape] = []

    # go
    return solve_step(
        puzzle, sorted(shapes), shapes_to_paths, shape_terminators, available_edges,
        multipass_counts
    )
