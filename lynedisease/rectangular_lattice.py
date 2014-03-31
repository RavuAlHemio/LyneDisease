import lynedisease.link_shapes as ls
import lynedisease.model as m
import lynedisease.solver as s

__author__ = 'ondra'


def format_solution_table_calc(solution, node_ids_to_nodes):
    """
    :type solution: dict[int, list[int]]
    :type node_ids_to_nodes: dict[int, int]
    :rtype: dict[int, str]
    """
    new_solution = {}
    for (color, path) in solution.items():
        new_path = []
        for p in path:
            back_p = node_ids_to_nodes[p]
            new_p = "{0}{1}".format(
                chr(back_p % width + ord("A")),
                chr(back_p // width + ord("0")),
            )
            new_path.append(new_p)
        new_solution[color] = " ".join(new_path)

    return new_solution


def format_solution_relative_movement(solution, node_ids_to_nodes):
    """
    :type solution: dict[int, list[int]]
    :type node_ids_to_nodes: dict[int, int]
    :rtype: dict[int, str]
    """
    new_solution = {}
    for (color, path) in solution.items():
        new_path = []
        last_c, last_r = None, None
        for p in path:
            back_p = node_ids_to_nodes[p]
            c = back_p % width
            r = back_p // width

            if last_c is None or last_r is None:
                new_p = "{0}{1}".format(
                    chr(c + ord("A")),
                    chr(r + ord("0")),
                )
            else:
                delta_c = last_c - c
                delta_r = last_r - r
                if delta_c == -1:
                    # right
                    if delta_r == -1:
                        # down
                        new_p = "\u2198"
                    elif delta_r == 0:
                        # vertical stay
                        new_p = "\u2192"
                    elif delta_r == 1:
                        # up
                        new_p = "\u2197"
                elif delta_c == 0:
                    # horizontal stay
                    if delta_r == -1:
                        # down
                        new_p = "\u2193"
                    elif delta_r == 1:
                        # up
                        new_p = "\u2191"
                elif delta_c == 1:
                    # left
                    if delta_r == -1:
                        # down
                        new_p = "\u2199"
                    elif delta_r == 0:
                        # vertical stay
                        new_p = "\u2190"
                    elif delta_r == 1:
                        # up
                        new_p = "\u2196"
            new_path.append(new_p)
            last_c = c
            last_r = r

        new_solution[color] = new_path

    return new_solution

if __name__ == '__main__':
    while True:
        line = input("w:h:line (a-z colors, A-Z terminators, 1-9 multipasses, _ none): ")
        split_line = line.split(":")
        if len(split_line) != 3 or not split_line[0].isnumeric() or not split_line[1].isnumeric():
            print("format: width:height:spec")
            continue

        width = int(split_line[0])
        height = int(split_line[1])

        if len(split_line[2]) != (width*height):
            print("need {0} characters".format(width*height))
            continue

        nodes = []

        for c in split_line[2]:
            if "a" <= c <= "z":
                color = ord(c) - ord("a")
                nodes.append(m.ShapeNode(color, terminates=False))
            elif "A" <= c <= "Z":
                color = ord(c) - ord("A")
                nodes.append(m.ShapeNode(color, terminates=True))
            elif "1" <= c <= "9":
                count = ord(c) - ord("0")
                nodes.append(m.MultipassNode(count))
            elif c == "_":
                nodes.append(None)

        puzzle = m.Puzzle()

        node_ids = [(puzzle.add_node(n) if n is not None else None) for n in nodes]
        ls.square_lattice(puzzle, node_ids, width, height)

        node_ids_to_nodes = {}
        for (k, v) in enumerate(node_ids):
            if v is not None:
                node_ids_to_nodes[v] = k

        solution = s.solve(puzzle)
        #print(format_solution_table_calc(solution, node_ids_to_nodes))
        print(format_solution_relative_movement(solution, node_ids_to_nodes))
