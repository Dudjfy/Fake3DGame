import pygame


class Player:
    def __init__(self, x, y, vel=1):
        self.x = x
        self.y = y

        self.new_x = 0
        self.new_y = 0

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

    # def update_movement(self, key):
    #     self.new_x, self.new_y = self.moves.get(key, (0, 0))
    #
    def move(self, dt):
        self.x = round(self.x + self.new_x * dt.dt, 4)
        self.y = round(self.y + self.new_y * dt.dt, 4)

        # print(self.tick % (fps // self.speed))
        # self.tick += 1
        # if self.tick % (fps // self.speed) == 0:
        #     self.x = round(self.x + self.new_x, 2)
        #     self.y = round(self.y + self.new_y, 2)
