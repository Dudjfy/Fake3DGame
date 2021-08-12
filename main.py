import time

import pygame as pygame

from gameMap import GameMap
from player import Player
from pygameWin import PygameWin

game_map = GameMap(20, 20)
# game_map.print_map()

player = Player(game_map.width / 2, game_map.height / 2, 10)

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

game_on = True
while game_on:
    py_win.clock.tick(py_win.fps)

    dt.new_dt()

    game_on = py_win.event_handler(player)

    player.move(dt)

    py_win.draw_on_update(player, game_map)

