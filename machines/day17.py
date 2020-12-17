from itertools import product
from collections import defaultdict
from utilities.operator import Base


# this code was written in rush, super ugly, and will be refactor later
class Operator(Base):
    def exec(self, part: int = 1):
        return (parts := {1: self.__part1, 2: self.__part2}).get(part if part in parts else 1)()

    def __part1(self) -> int:
        cycles = 6
        size_ranges = [0, len(self.data) + 2 * cycles]

        self.__parse_raw_data(cycles, size_ranges)
        new_state = self.__copy_state(self.__state)

        for _ in range(cycles):
            for cube in self.__cubes:
                neighbors = self.__get_neighbors(cube)
                neighbors_active_count = self.__get_neighbors_active_count(neighbors)
                x, y, z = cube
                if self.__state[x][y][z] == "#" and neighbors_active_count not in [2, 3]:
                    new_state[x][y][z] = "."
                elif self.__state[x][y][z] == "." and neighbors_active_count == 3:
                    new_state[x][y][z] = "#"
            self.__state = self.__copy_state(new_state)
        return self.__get_all_active_count()

    def __part2(self) -> int:
        cycles = 6
        size_ranges = [0, len(self.data) + 2 * cycles]

        self.__parse_raw_data_4d(cycles, size_ranges)
        new_state = self.__copy_state_4d(self.__state)

        for _ in range(cycles):
            for cube in self.__cubes:
                neighbors = self.__get_neighbors_4d(cube)
                neighbors_active_count = self.__get_neighbors_active_count_4d(neighbors)
                x, y, z, w = cube
                if self.__state[x][y][z][w] == "#" and neighbors_active_count not in [2, 3]:
                    new_state[x][y][z][w] = "."
                elif self.__state[x][y][z][w] == "." and neighbors_active_count == 3:
                    new_state[x][y][z][w] = "#"
            self.__state = self.__copy_state_4d(new_state)
        return self.__get_all_active_count_4d()

    def __parse_raw_data(self, cycles, pos_range):
        self.__cubes = list(product(list(range(pos_range[0], pos_range[1])), list(range(pos_range[0], pos_range[1])), list(range(-cycles, 1 + cycles))))
        self.__state = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: ".")))
        for y, line in enumerate(self.data):
            s = list(line)
            for x, v in enumerate(s):
                self.__state[cycles + x][cycles + y][0] = v

    def __get_neighbors(self, pos: tuple):
        x, y, z = pos
        neighbors = []
        for a in range(-1, 2):
            for b in range(-1, 2):
                for c in range(-1, 2):
                    neighbors += [(x + a, y + b, z + c)]
        neighbors.remove(pos)
        return neighbors

    def __get_neighbors_active_count(self, cubes):
        count = 0
        for cube in cubes:
            x, y, z = cube
            count += 1 if self.__state[x][y][z] == "#" else 0
        return count

    def __get_all_active_count(self):
        count = 0
        for x in self.__state:
            for y in self.__state[x]:
                for z in self.__state[x][y]:
                    count += 1 if self.__state[x][y][z] == "#" else 0
        return count

    def __copy_state(self, from_state):
        new_state = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: ".")))
        for x in from_state:
            for y in from_state[x]:
                for z in from_state[x][y]:
                    new_state[x][y][z] = from_state[x][y][z]
        return new_state

    def __parse_raw_data_4d(self, cycles, pos_range):
        self.__cubes = list(product(list(range(pos_range[0], pos_range[1])), list(range(pos_range[0], pos_range[1])), list(range(-cycles, 1 + cycles)), list(range(-cycles, 1 + cycles))))
        self.__state = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: "."))))
        for y, line in enumerate(self.data):
            s = list(line)
            for x, v in enumerate(s):
                self.__state[cycles + x][cycles + y][0][0] = v

    def __get_neighbors_4d(self, pos: tuple):
        x, y, z, w = pos
        neighbors = []
        for a in range(-1, 2):
            for b in range(-1, 2):
                for c in range(-1, 2):
                    for d in range(-1, 2):
                        neighbors += [(x + a, y + b, z + c, w + d)]
        neighbors.remove(pos)
        return neighbors

    def __get_neighbors_active_count_4d(self, cubes):
        count = 0
        for cube in cubes:
            x, y, z, w = cube
            count += 1 if self.__state[x][y][z][w] == "#" else 0
        return count

    def __get_all_active_count_4d(self):
        count = 0
        for x in self.__state:
            for y in self.__state[x]:
                for z in self.__state[x][y]:
                    for w in self.__state[x][y][z]:
                        count += 1 if self.__state[x][y][z][w] == "#" else 0
        return count

    def __copy_state_4d(self, from_state):
        new_state = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: "."))))
        for x in from_state:
            for y in from_state[x]:
                for z in from_state[x][y]:
                    for w in from_state[x][y][z]:
                        new_state[x][y][z][w] = from_state[x][y][z][w]
        return new_state

    def __print(self, c, d):
        for w in range(-c, 1 + c):
            for z in range(-c, 1 + c):
                print(f"z={z}, w={w}")
                for y in range(d[0], d[1]):
                    for x in range(d[0], d[1]):
                        print(self.__state[x][y][z][w], end="")
                    print()
                print()
            print()
