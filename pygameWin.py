import math

import pygame


class PygameWin:
    colors = {
        'white': (255, 255, 255),
        'green': (0, 255, 0),
        'red': (255, 0, 0),
        'black': (0, 0, 0),
        'gray': (100, 100, 100),
    }

    def __init__(self, win_width=1000, win_height=600, fps=60, win_name='Ray Tracing Test',
                 mouse_sensitivity=0.1, arrows_sensitivity=2, info_width=200):
        self.win_name = win_name
        self.fps = fps
        self.tick = 0

        self.info_width = info_width

        self.win = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption(self.win_name)
        pygame.font.init()
        self.big_font = pygame.font.SysFont('Roboto Mono', 40)
        self.small_font = pygame.font.SysFont('Roboto Mono', 20)
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        self.mouse_sensitivity = mouse_sensitivity
        self.arrows_sensitivity = arrows_sensitivity

        self.game_surface = pygame.Surface((self.win.get_width() - self.info_width, self.win.get_height()))
        self.info_surface = pygame.Surface((self.win.get_width() - self.game_surface.get_width(),
                                            self.win.get_height()))
        self.mini_map_surface = pygame.Surface((self.info_surface.get_width(), self.info_surface.get_width()))

    def event_handler(self, player, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

            keys = pygame.key.get_pressed()

            player.new_x = 0
            player.new_y = 0

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.new_x = math.cos(player.angle) * player.move_distance * dt.dt
                player.new_y = math.sin(player.angle) * player.move_distance * dt.dt
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.new_x = -math.cos(player.angle) * player.move_distance * dt.dt
                player.new_y = -math.sin(player.angle) * player.move_distance * dt.dt
            if keys[pygame.K_a]:
                player.new_x = math.cos(player.angle - math.pi / 2) * player.move_distance * dt.dt
                player.new_y = math.sin(player.angle - math.pi / 2) * player.move_distance * dt.dt
            if keys[pygame.K_d]:
                player.new_x = math.cos(player.angle + math.pi / 2) * player.move_distance * dt.dt
                player.new_y = math.sin(player.angle + math.pi / 2) * player.move_distance * dt.dt

        return True

    def mouse_movement(self, player, dt):
        player.new_angle = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            if keys[pygame.K_LEFT]:
                player.new_angle -= player.angle_change * dt.dt * self.arrows_sensitivity
            if keys[pygame.K_RIGHT]:
                player.new_angle += player.angle_change * dt.dt * self.arrows_sensitivity
        else:
            player.new_angle = pygame.mouse.get_rel()[0] * dt.dt * self.mouse_sensitivity

    def draw_on_update(self, player, game_map, rt):
        self.win.fill(self.colors.get('green'))
        self.game_surface.fill(self.colors.get('black'))
        self.info_surface.fill(self.colors.get('gray'))

        self.draw_ray_traced_lines(rt)
        self.draw_info(player)
        self.draw_mini_map(player, game_map)

        self.win.blit(self.game_surface, (0, 0))
        self.info_surface.blit(self.mini_map_surface,
                               (0, self.info_surface.get_height() - self.mini_map_surface.get_height()))
        self.win.blit(self.info_surface, (self.game_surface.get_width(), 0))

        pygame.display.update()

    def draw_info(self, player):
        x_text = self.small_font.render('X: {:.2f}'.format(player.x), True, self.colors.get('white'))
        y_text = self.small_font.render('Y: {:.2f}'.format(player.y), True, self.colors.get('white'))
        angle_text = self.small_font.render('Angle: {:.0f}'
                                            .format(abs(math.degrees(player.angle) % 360), player.angle),
                                            True, self.colors.get('white'))
        fps_text = self.small_font.render('FPS: {:.2f}'.format(self.clock.get_fps()), True, self.colors.get('white'))

        self.info_surface.blit(fps_text, (20, 20))
        self.info_surface.blit(x_text, (20, 40))
        self.info_surface.blit(y_text, (20, 60))
        self.info_surface.blit(angle_text, (20, 80))

    def draw_mini_map(self, player, game_map):
        self.mini_map_surface.fill(self.colors.get('green'))

        tile_size_x = self.mini_map_surface.get_width() / game_map.width
        tile_size_y = self.mini_map_surface.get_height() / game_map.height

        for coords, tile in game_map.map.items():
            x, y = coords
            if tile.blocks_movement:
                pygame.draw.rect(self.mini_map_surface, self.colors.get('white'),
                                 pygame.Rect(math.ceil(x * tile_size_x), math.ceil(y * tile_size_y), math.ceil(tile_size_x), math.ceil(tile_size_y)))
            else:
                pygame.draw.rect(self.mini_map_surface, self.colors.get('black'),
                                 pygame.Rect(math.ceil(x * tile_size_x), math.ceil(y * tile_size_y), math.ceil(tile_size_x), math.ceil(tile_size_y)))

        pygame.draw.rect(self.mini_map_surface, self.colors.get('red'),
                         pygame.Rect(player.x * tile_size_x - tile_size_x / 2,
                                     player.y * tile_size_y - tile_size_x / 2,
                                     tile_size_x,
                                     tile_size_y))
        pygame.draw.line(self.mini_map_surface,
                         self.colors.get('green'),
                         (player.x * tile_size_x, player.y * tile_size_y),
                         (int((player.x * tile_size_x + 10 * math.cos(player.angle))),
                          int((player.y * tile_size_y + 10 * math.sin(player.angle)))))

    def draw_ray_traced_lines(self, rt):
        for i, distance in enumerate(rt.distances):
            if distance <= rt.radius:
                line_start_y = (self.game_surface.get_height() / 2) - (self.game_surface.get_height() / distance)
                line_end_y = self.game_surface.get_height() - line_start_y
                shading = 255 - int((distance / rt.radius) * 255)
                pygame.draw.line(self.game_surface,
                                 (shading, shading, shading),
                                 (i, line_start_y),
                                 (i, line_end_y))
