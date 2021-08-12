import math

import pygame


class Player:
    def __init__(self, x, y, vel=1, fov=(math.pi / 2), angle=0, angle_change=1):
        self.x = x
        self.y = y
        self.fov = fov
        self.angle = angle
        self.angle_change = angle_change

        self.new_x = 0
        self.new_y = 0
        self.new_angle = 0

        self.move_distance = vel
        self.tick = 0

        self.moves = {
            pygame.K_w: (0, -self.move_distance),
            pygame.K_UP: (0, -self.move_distance),
            pygame.K_s: (0, self.move_distance),
            pygame.K_DOWN: (0, self.move_distance),
            pygame.K_a: (-self.move_distance, 0),
            pygame.K_LEFT: (-self.move_distance, 0),
            pygame.K_d: (self.move_distance, 0),
            pygame.K_RIGHT: (self.move_distance, 0)
        }

    def move(self, dt, game_map):
        if not game_map.map.get((int(self.x + self.new_x), int(self.y))).blocks_movement:
            self.x += self.new_x
        if not game_map.map.get((int(self.x), int(self.y + self.new_y))).blocks_movement:
            self.y += self.new_y

    def change_angle(self, dt):
        # print(self.angle, self.new_angle)
        self.angle += self.new_angle
