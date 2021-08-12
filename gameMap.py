class GameMap:
    def __init__(self, width=10, height=10):
        # self.map = [
        #     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        #     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        #     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        #     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        #     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        #     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        #     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        #     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        #     ['#', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
        #     ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
        # ]

        self.width = width
        self.height = height

        self.map = []
        self.create_empty_map_with_borders()

    def create_empty_map_with_borders(self):
        for y in range(self.height):
            self.map.append([])
            for x in range(self.width):
                self.map[y].append(Tile('#', True))

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                self.map[y][x] = Tile(' ', False)

    def print_map(self):
        for row in self.map:
            for tile in row:
                print(tile.sign, end='')
            print()

class Tile:
    def __init__(self, sign='?', blocks_movement=False):
        self.sign = sign
        self.blocks_movement = blocks_movement
