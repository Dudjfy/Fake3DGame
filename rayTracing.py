import math


class RayTracing:
    def __init__(self, rays, steps, radius=10):
        self.rays = rays
        self.steps = steps
        self.radius = radius
        self.step_size = radius / steps

        self.distances = []
        for item in range(rays):
            self.distances.append(self.radius + 1)

    def calc_distances(self, player, game_map):
        for ray in range(self.rays):
            ray_angle = math.radians((player.angle - player.fov / 2) + (ray / self.rays) * player.fov)
            x = math.cos(ray_angle)
            y = math.sin(ray_angle)
            for step in range(self.steps):
                coords = (int(player.x + x * self.step_size * step), int(player.y + y * self.step_size * step))
                tile = game_map.map.get(coords)
                if tile == None:
                    self.distances[ray] = self.radius + 1
                    break
                elif tile.blocks_movement:
                    self.distances[ray] = self.step_size * step
                    break
            else:
                self.distances[ray] = self.radius + 1
