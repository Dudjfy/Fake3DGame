import math

import pygame
# from line_profiler_pycharm import profile


class RayTracing:
    def __init__(self, rays, steps, radius=10):
        self.rays = rays
        self.steps = steps
        self.radius = radius
        self.step_size = radius / steps

        self.distances = []
        for item in range(rays):
            self.distances.append(Distance(self.radius + 1, 0))
        # for item in range(rays):
        #     self.distances.append(Distance(pygame.Vector2(100, 100)))

    # def calc_distances_dda(self, player, game_map):
    #     start_pos = player.pos
    #     for ray in range(self.rays):
    #         ray_angle = (player.angle - player.fov / 2) + (ray / self.rays) * player.fov
    #         x_end = math.cos(ray_angle) * self.radius
    #         y_end = math.sin(ray_angle) * self.radius
    #         end_pos = (pygame.math.Vector2(x_end, y_end) - start_pos).normalize()
    #
    #         step_size = pygame.math.Vector2(math.sqrt(1 + (end_pos.y / end_pos.x) * (end_pos.y / end_pos.x)),
    #                                         math.sqrt(1 + (end_pos.x / end_pos.y) * (end_pos.x / end_pos.y)))
    #         map_coords = pygame.math.Vector2(int(start_pos.x), int(start_pos.y))
    #
    #         ray_len = pygame.math.Vector2()
    #         step = pygame.math.Vector2()
    #
    #         if end_pos.x < 0:
    #             step.x = -1
    #             ray_len.x = (start_pos.x - map_coords.x) * step_size.x
    #         else:
    #             step.x = 1
    #             ray_len.x = ((map_coords.x + 1) - start_pos.x) * step_size.x
    #
    #         if end_pos.y < 0:
    #             step.y = -1
    #             ray_len.y = (start_pos.y - map_coords.y) * step_size.y
    #         else:
    #             step.y = 1
    #             ray_len.x = ((map_coords.y + 1) - start_pos.y) * step_size.y
    #
    #         hit_tile = False
    #         distance = 0
    #         while (not hit_tile) and (distance < self.radius):
    #             if ray_len.x < ray_len.y:
    #                 map_coords.x += step.x
    #                 distance = ray_len.x
    #                 ray_len.x += step_size.x
    #             else:
    #                 map_coords.y += step.y
    #                 distance = ray_len.y
    #                 ray_len.y += step_size.y
    #
    #             if 0 <= map_coords.x < game_map.width and 0 <= map_coords.y < game_map.height:
    #                 if game_map.map.get((map_coords.x, map_coords.y)).blocks_movement:
    #                     hit_tile = True
    #                     self.distances[ray] = Distance(start_pos + end_pos * distance)


    # @profile
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
                    self.distances[ray] = Distance(self.radius + 1, 0)
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

                    self.distances[ray] = Distance(self.step_size * step, sample_x)
                    break
            else:
                self.distances[ray] = Distance(self.radius + 1, 0)


class Distance:
    def __init__(self, distance, sample_x_factor):
        self.distance = distance
        self.sample_x_factor = sample_x_factor

# class Distance:
#     def __init__(self, vector):
#         self.vector = vector
#
#         self.distance = self.vector.length()
#         self.sample_x_factor = sample_x_factor