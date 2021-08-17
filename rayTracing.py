import math

import pygame
from line_profiler_pycharm import profile


class RayTracing:
    def __init__(self, rays, steps, player, radius=10):
        self.rays = rays
        self.steps = steps
        self.radius = radius
        self.step_size = radius / steps

        self.distances = []
        # for item in range(rays):
        #     self.distances.append(Distance(player.pos + self.radius + 1, 0))
        for item in range(rays):
            self.distances.append(Distance(pygame.math.Vector2(player.pos.x + self.radius + 1,
                                                               player.pos.y + self.radius + 1),
                                           player.pos))

    # @profile
    def calc_distances_dda(self, player, game_map):
        start_pos = player.pos
        for ray in range(self.rays):
            ray_angle = (player.angle - player.fov / 2) + (ray / self.rays) * player.fov
            x_end = math.cos(ray_angle) * self.radius
            y_end = math.sin(ray_angle) * self.radius
            end_pos_norm = (pygame.math.Vector2(x_end, y_end)).normalize()

            if end_pos_norm.x == 0 or end_pos_norm.y == 0:
                self.distances[ray] = Distance(pygame.math.Vector2(start_pos.x + self.radius + 1,
                                                                   start_pos.y + self.radius + 1),
                                               start_pos)
                continue

            step_size = pygame.math.Vector2(math.sqrt(1 + (end_pos_norm.y / end_pos_norm.x) ** 2),
                                            math.sqrt(1 + (end_pos_norm.x / end_pos_norm.y) ** 2))

            map_coords = pygame.math.Vector2(int(start_pos.x), int(start_pos.y))
            ray_len = pygame.math.Vector2()
            step = pygame.math.Vector2()
            if end_pos_norm.x < 0:
                step.x = -1
                ray_len.x = (start_pos.x - map_coords.x) * step_size.x
            else:
                step.x = 1
                ray_len.x = ((map_coords.x + 1) - start_pos.x) * step_size.x

            if end_pos_norm.y < 0:
                step.y = -1
                ray_len.y = (start_pos.y - map_coords.y) * step_size.y
            else:
                step.y = 1
                ray_len.y = ((map_coords.y + 1) - start_pos.y) * step_size.y

            hit_tile = False
            distance = 0
            while (not hit_tile) and (distance < self.radius):
                if ray_len.x < ray_len.y:
                    map_coords.x += step.x
                    distance = ray_len.x
                    ray_len.x += step_size.x
                else:
                    map_coords.y += step.y
                    distance = ray_len.y
                    ray_len.y += step_size.y

                # if 0 <= map_coords.x < game_map.width and 0 <= map_coords.y < game_map.height:
                if game_map.map.get((map_coords.x, map_coords.y)).blocks_movement:
                    hit_tile = True

            if hit_tile:
                self.distances[ray] = Distance(start_pos + end_pos_norm * distance, start_pos)
            else:
                self.distances[ray] = Distance(pygame.math.Vector2(start_pos.x + self.radius + 1,
                                                                   start_pos.y + self.radius + 1),
                                               start_pos)

    @profile
    def calc_distances(self, player, game_map):
        for ray in range(self.rays):
            ray_angle = (player.angle - player.fov / 2) + (ray / self.rays) * player.fov
            x = math.cos(ray_angle)
            y = math.sin(ray_angle)
            for step in range(self.steps):
                float_x = player.pos.x + x * self.step_size * step
                float_y = player.pos.y + y * self.step_size * step
                coords = (int(float_x), int(float_y))
                tile = game_map.map.get(coords)
                if tile == None:
                    self.distances[ray] = Distance_old(self.radius + 1, 0)
                    break
                elif tile.blocks_movement:
                    tile_x, tile_y = coords
                    tile_mid_x = tile_x + 0.5
                    tile_mid_y = tile_y + 0.5

                    atan_angle = math.atan2(float_y - tile_mid_y, float_x - tile_mid_x)

                    sample_x = 0

                    if -math.pi * 0.25 <= atan_angle < math.pi * 0.25:
                        sample_x = float_y - tile_y
                    if math.pi * 0.25 <= atan_angle < math.pi * 0.75:
                        sample_x = float_x - tile_x
                    if -math.pi * 0.75 <= atan_angle < -math.pi * 0.25:
                        sample_x = float_x - tile_x
                    if math.pi * 0.75 <= atan_angle or atan_angle < -math.pi * 0.75:
                        sample_x = float_y - tile_y

                    # if -math.pi / 2 + math.pi / 4 <= atan_angle < math.pi / 4:
                    #     sample_x = float_x - tile_x
                    # if math.pi / 4 <= atan_angle < math.pi / 2 + math.pi / 4:
                    #     sample_x = float_y - tile_y
                    # if math.pi / 2 + math.pi / 4 <= atan_angle < math.pi + math.pi / 4:
                    #     sample_x = float_x - tile_x
                    # if math.pi + math.pi / 4 <= atan_angle < -math.pi / 2 + math.pi / 4:
                    #     sample_x = float_y - tile_y

                    self.distances[ray] = Distance_old(self.step_size * step, sample_x)
                    break
            else:
                self.distances[ray] = Distance_old(self.radius + 1, 0)


class Distance_old:
    def __init__(self, distance, sample_x_factor):
        self.distance = distance
        self.sample_x_factor = sample_x_factor

class Distance:
    def __init__(self, vector, start_pos):
        self.distance = (vector - start_pos).length()

        self.vector = vector

        # atan_angle = math.atan2(self.vector.x, self.vector.y)

        # self.sample_x = 0

        # if -math.pi * 0.25 <= atan_angle < math.pi * 0.25:
        #     self.sample_x = self.vector.y - int(self.vector.y)
        # elif math.pi * 0.25 <= atan_angle < math.pi * 0.75:
        #     self.sample_x = self.vector.x - int(self.vector.x)
        # elif -math.pi * 0.75 <= atan_angle < -math.pi * 0.25:
        #     self.sample_x = self.vector.x - int(self.vector.x)
        # elif math.pi * 0.75 <= atan_angle or atan_angle < -math.pi * 0.75:
        #     self.sample_x = self.vector.y - int(self.vector.y)

        # self.sample_x_factor = sample_x_factor