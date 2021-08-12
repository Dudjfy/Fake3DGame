import math
import time

import pygame as pygame

from gameMap import GameMap, Tile
from player import Player
from pygameWin import PygameWin
from rayTracing import RayTracing

game_map = GameMap(17, 17)
# game_map.create_map_from_file()
game_map.create_empty_map_with_borders()
game_map.map[(5, 5)] = Tile('#', True)
# game_map.print_map()

player = Player(game_map.width / 2, game_map.height / 2, vel=10, fov=math.pi / 2, angle_change=(math.pi))

py_win = PygameWin(win_width=1000, win_height=600, fps=60, win_name='Ray Tracing Test')

# print(win.get_width(), win.get_height(), game_surface.get_width(), game_surface.get_height(),
#       info_surface.get_width(), info_surface.get_height())


class DeltaTime:
    def __init__(self):
        self.dt = 0
        self.prev_time = time.time()
        self.now = 0

    def new_dt(self):
        self.now = time.time()
        self.dt = self.now - self.prev_time
        self.prev_time = self.now


dt = DeltaTime()
rt = RayTracing(py_win.game_surface.get_width(), 100, 10)


game_on = True
while game_on:
    py_win.clock.tick(py_win.fps)

    dt.new_dt()

    game_on = py_win.event_handler(player, dt)

    player.move(dt, game_map)
    player.change_angle(dt)

    rt.calc_distances(player, game_map)

    py_win.draw_on_update(player, game_map, rt)

