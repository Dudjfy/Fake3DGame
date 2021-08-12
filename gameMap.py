import random


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

        self.map = {}
        # self.create_empty_map_with_borders()

    def create_map_from_file(self, file_name):
        file = open(file_name, 'r')

        for y, row in enumerate(file):
            for x, tile in enumerate(row):
                if tile == '#':
                    self.map[(x, y)] = Tile('#', True)
                elif tile == ' ':
                    self.map[(x, y)] = Tile(' ', False)
                self.width = x + 1
            self.height = y + 1

        file.close()

    def create_empty_map_with_borders(self):
        for y in range(self.height):
            for x in range(self.width):
                self.map[(x, y)] = Tile('#', True)

        for y in range(1, self.height - 1):
            for x in range(1, self.width - 1):
                self.map[(x, y)] = Tile(' ', False)

    def return_random_empty_spot(self):
        while True:
            rand_x = random.randint(0, self.width - 1)
            rand_y = random.randint(0, self.height - 1)
            coords = (rand_x, rand_y)
            print(coords, self.map.get(coords))
            if not (self.map.get(coords)).blocks_movement:
                return coords

class Tile:
    def __init__(self, sign='?', blocks_movement=False):
        self.sign = sign
        self.blocks_movement = blocks_movement
