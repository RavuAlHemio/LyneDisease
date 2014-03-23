import lynedisease.link_shapes as ls
import lynedisease.model as m
import lynedisease.solver as s

__author__ = 'ondra'

if __name__ == '__main__':
    while True:
        line = input("line (a-z colors, A-Z terminators, 1-9 multipasses): ")
        if len(line) != 12:
            print("need 12 characters")
            continue

        nodes = []

        for c in line:
            if "a" <= c <= "z":
                color = ord(c) - ord("a")
                nodes.append(m.ShapeNode(color, terminates=False))
            elif "A" <= c <= "Z":
                color = ord(c) - ord("A")
                nodes.append(m.ShapeNode(color, terminates=True))
            elif "1" <= c <= "9":
                count = ord(c) - ord("0")
                nodes.append(m.MultipassNode(count))

        puzzle = m.Puzzle()

        node_ids = [puzzle.add_node(n) for n in nodes]
        ls.square_lattice(puzzle, node_ids, 3, 4)

        solution = s.solve(puzzle)

        print(solution)