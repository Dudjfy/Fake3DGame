import math
import time

import pygame as pygame

from gameMap import GameMap, Tile
from player import Player
from pygameWin import PygameWin
from rayTracing import RayTracing
from line_profiler_pycharm import profile

# @profile
def main():
    game_map = GameMap(20, 20)
    # game_map.create_map_from_file('map.txt')
    game_map.create_map_from_file('map_SA.txt')
    # game_map.create_empty_map_with_borders()
    # game_map.map[(5, 5)] = Tile('#', True)

    # p_x = (game_map.height + 1) / 2
    # p_y = (game_map.height + 1) / 2

    p_x = 78
    p_y = 19

    # p_x, p_y = game_map.return_random_empty_spot()

    game_width_factor = 1
    game_height_factor = 2

    player = Player(x=p_x, y=p_y, vel=10, fov=math.pi / 2, angle=math.pi, angle_change=(math.pi / 2))

    """         Window presets          """

    # Classic
    w, h, i_w = 1000, 600, 200

    # Info bar and mini map
    # w, h, i_w = 1000, 300, 200

    # Only mini map
    # w, h, i_w = 1000, 200, 200

    # Full screen large info
    # w, h, i_w = 1920, 1080, 400

    # Full screen smaller info
    # w, h, i_w = 1920, 1080, 200

    # Full screen no info
    # w, h, i_w = 1920, 1080, 0

    # Performance 1
    # w, h, i_w = 500, 300, 100

    # Performance 2
    # w, h, i_w = 300, 200, 100

    # Performance 3
    # w, h, i_w = 200, 100, 0

    py_win = PygameWin(win_width=w, win_height=h, fps=400, win_name='Ray Tracing Test',
                       mouse_sensitivity=0.1, arrows_sensitivity=2, info_width=i_w)

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
    rt = RayTracing(int(py_win.game_surface.get_width() / game_width_factor), steps=100, radius=10, player=player)

    game_on = True
    while game_on:
        py_win.clock.tick(py_win.fps)

        dt.new_dt()

        py_win.mouse_movement(player, dt)
        game_on = py_win.event_handler(player, dt)

        player.move(dt, game_map)
        player.change_angle(dt)

        rt.calc_distances_dda(player, game_map)
        # rt.calc_distances_old(player, game_map)

        py_win.draw_on_update(player, game_map, rt, game_height_factor, game_width_factor)


if __name__ == '__main__':
    main()
