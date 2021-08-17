import math


from line_profiler_pycharm import profile
import pygame


class PygameWin:
    colors = {
        'white': (255, 255, 255),
        'green': (0, 255, 0),
        'red': (255, 0, 0),
        'blue': (0, 0, 255),
        'black': (0, 0, 0),
        'yellow': (255,255,0),
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

        # self.wall_sprite = pygame.image.load('wall_16x16.png')
        self.wall_sprite = pygame.image.load('bricks_16x16.png')
        # self.wall_sprite = pygame.image.load('bricks_64x64.png')
        # self.wall_sprite = pygame.image.load('wall_256x265.png')
        # self.wall_sprite = pygame.image.load('gray_wall_256x256.png')
        # print(self.wall_sprite.get_at((0, 0)), self.wall_sprite.get_at((1, 0)))

        self.sprite_px_arr = pygame.PixelArray(self.wall_sprite.convert())

    def event_handler(self, player, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

            keys = pygame.key.get_pressed()

            player.new_x = 0
            player.new_y = 0
            player.move_distance = player.vel

            if keys[pygame.K_LSHIFT]:
                player.move_distance /= 10

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
            player.new_angle = player.angle_change * pygame.mouse.get_rel()[0] * dt.dt * self.mouse_sensitivity

    # @profile
    def draw_on_update(self, player, game_map, rt, game_height_factor, game_width_factor):
        self.win.fill(self.colors.get('green'))
        self.game_surface.fill(self.colors.get('black'))
        # self.game_surface.fill(self.colors.get('blue'), pygame.Rect(0,
        #                                                             0,
        #                                                             self.game_surface.get_width(),
        #                                                             (self.game_surface.get_height() / 2)))
        self.info_surface.fill(self.colors.get('gray'))

        self.draw_textures_with_px_arr(rt, game_height_factor, game_width_factor)

        # self.draw_ray_casted_lines(rt, game_height_factor, game_width_factor)
        # self.draw_lines_with_px_arr(rt, game_height_factor, game_width_factor)

        self.draw_info(player)
        # self.draw_mini_map(player, game_map, rt)

        self.win.blit(self.game_surface, (0, 0))
        self.info_surface.blit(self.mini_map_surface,
                               (0, self.info_surface.get_height() - self.mini_map_surface.get_height()))
        self.win.blit(self.info_surface, (self.game_surface.get_width(), 0))

        pygame.display.update()

    def draw_info(self, player):
        x_text = self.small_font.render('X: {:.2f}'.format(player.pos.x), True, self.colors.get('white'))
        y_text = self.small_font.render('Y: {:.2f}'.format(player.pos.y), True, self.colors.get('white'))
        angle_text = self.small_font.render('Angle: {:.0f}'
                                            .format(abs(math.degrees(player.angle) % 360), player.angle),
                                            True, self.colors.get('white'))
        fps_text = self.small_font.render('FPS: {:.2f}'.format(self.clock.get_fps()), True, self.colors.get('white'))

        self.info_surface.blit(fps_text, (20, 20))
        self.info_surface.blit(x_text, (20, 40))
        self.info_surface.blit(y_text, (20, 60))
        self.info_surface.blit(angle_text, (20, 80))

    # @profile
    def draw_mini_map(self, player, game_map, rt):
        self.mini_map_surface.fill(self.colors.get('green'))

        tile_size_x = self.mini_map_surface.get_width() / game_map.width
        tile_size_y = self.mini_map_surface.get_height() / game_map.height

        for coords, tile in game_map.map.items():
            x, y = coords
            if tile.blocks_movement:
                pygame.draw.rect(self.mini_map_surface, self.colors.get('white'),
                                 pygame.Rect(math.ceil(x * tile_size_x),
                                             math.ceil(y * tile_size_y),
                                             math.ceil(tile_size_x),
                                             math.ceil(tile_size_y)))
            else:
                pygame.draw.rect(self.mini_map_surface, self.colors.get('black'),
                                 pygame.Rect(math.ceil(x * tile_size_x),
                                             math.ceil(y * tile_size_y),
                                             math.ceil(tile_size_x),
                                             math.ceil(tile_size_y)))

        pygame.draw.rect(self.mini_map_surface, self.colors.get('red'),
                         pygame.Rect(player.pos.x * tile_size_x - tile_size_x / 2,
                                     player.pos.y * tile_size_y - tile_size_y / 2,
                                     tile_size_x,
                                     tile_size_y))
        pygame.draw.line(self.mini_map_surface,
                         self.colors.get('green'),
                         (player.pos.x * tile_size_x, player.pos.y * tile_size_y),
                         (int((player.pos.x * tile_size_x + 10 * math.cos(player.angle))),
                          int((player.pos.y * tile_size_y + 10 * math.sin(player.angle)))))

        # for distance in rt.distances:
        #     self.mini_map_surface.set_at((int(distance.vector.x * tile_size_x), int(distance.vector.y * tile_size_y)),
        #                                  self.colors.get('green'))

    # @profile
    def draw_ray_casted_lines(self, rt, game_height_factor, game_width_factor):
        for x, distance in enumerate(rt.distances):
            # i = i * game_px_width
            if distance.distance <= rt.radius:
                line_start_y = (self.game_surface.get_height() / 2) - \
                               (self.game_surface.get_height() / distance.distance) / game_height_factor
                line_end_y = self.game_surface.get_height() - line_start_y
                shading = 255 - int((distance.distance / rt.radius) * 255)

                # line_len = int(line_end_y - line_start_y)
                #
                # for y in range(line_len):
                #     sample_x = int(distance.sample_x * self.wall_sprite.get_width())
                #     sample_y = int((y / line_len) * self.wall_sprite.get_height())
                #     color = self.wall_sprite.get_at((sample_x, sample_y))
                #
                #     pygame.draw.line(self.game_surface, color,
                #                      (x, int(line_start_y + y)),
                #                      (int(x * game_width_factor), int(line_start_y + y)))

                pygame.draw.line(self.game_surface,
                                 (shading, shading, shading),
                                 (x * game_width_factor, line_start_y),
                                 (x * game_width_factor, line_end_y), game_width_factor)

    # @profile
    def draw_lines_with_px_arr(self, rt, game_height_factor, game_width_factor):
        px_arr = pygame.PixelArray(self.game_surface)
        for x, distance in enumerate(rt.distances):
            if distance.distance <= rt.radius:
                if distance.distance <= 1:
                    start_y = 0
                else:
                    start_y = (self.game_surface.get_height() / 2) - \
                               (self.game_surface.get_height() / distance.distance) / game_height_factor
                line_end_y = int(self.game_surface.get_height() - start_y)
                shading = 255 - int((distance.distance / rt.radius) * 255)
                start_x = int(x * game_width_factor)
                end_x = int(start_x + game_height_factor)

                px_arr[start_x:end_x, int(start_y):line_end_y] = (shading, shading, shading)

        px_arr.close()

    # @profile
    def draw_textures_with_px_arr(self, rt, game_height_factor, game_width_factor):
        px_arr = pygame.PixelArray(self.game_surface)
        for x, distance in enumerate(rt.distances):
            if distance.distance <= rt.radius:
                if distance.distance <= 1:
                    start_y = 0
                else:
                    start_y = (self.game_surface.get_height() / 2) - \
                                   (self.game_surface.get_height() / distance.distance) / game_height_factor
                end_y = int(self.game_surface.get_height() - start_y)
                start_x = int(x * game_width_factor)
                end_x = int(start_x + game_width_factor)

                line_len = int(end_y - start_y)
                sample_x = int(distance.sample_x * self.wall_sprite.get_width())

                if line_len <= self.wall_sprite.get_width():
                    for y in range(line_len):
                        sample_y = int((y / line_len) * self.wall_sprite.get_height())
                        # color = self.sprite_px_arr[sample_x, sample_y]
                        color = self.wall_sprite.get_at((sample_x, sample_y))

                        px_arr[start_x:end_x, int(start_y + y)] = color
                else:
                    y_step_len = line_len / self.wall_sprite.get_width()
                    for sample_y in range(self.wall_sprite.get_width()):
                        color = self.sprite_px_arr[sample_x, sample_y]
                        # color = self.wall_sprite.get_at((sample_x, sample_y))
                        y_step_start = int(start_y) + int(sample_y * y_step_len)
                        y_step_end = math.ceil(y_step_start + y_step_len)

                        px_arr[start_x:end_x, y_step_start:y_step_end] = color

        px_arr.close()
