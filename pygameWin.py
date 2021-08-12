import pygame


class PygameWin:
    colors = {
        'white': (255, 255, 255),
        'green': (0, 255, 0),
        'red': (255, 0, 0),
        'black': (0, 0, 0),
        'gray': (100, 100, 100),
    }

    def __init__(self, win_width=1000, win_height=600, fps=60, win_name='Ray Tracing Test'):
        self.win_name = win_name
        self.fps = fps
        self.tick = 0

        self.win = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption(self.win_name)
        pygame.font.init()
        self.big_font = pygame.font.SysFont('Roboto Mono', 40)
        self.small_font = pygame.font.SysFont('Roboto Mono', 30)
        self.clock = pygame.time.Clock()

        self.game_surface = pygame.Surface((self.win.get_width() - 200, self.win.get_height()))
        self.info_surface = pygame.Surface((self.win.get_width() - self.game_surface.get_width(),
                                            self.win.get_height()))
        self.mini_map_surface = pygame.Surface((self.info_surface.get_width(), self.info_surface.get_width()))

    def event_handler(self, player):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False

            keys = pygame.key.get_pressed()

            player.new_x = 0
            player.new_y = 0

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.new_y -= player.move_distance
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.new_y += player.move_distance
            if keys[pygame.K_a]:
                player.new_x -= player.move_distance
            if keys[pygame.K_d]:
                player.new_x += player.move_distance

        return True

    def draw_on_update(self, player, game_map):
        self.win.fill(self.colors.get('green'))
        self.game_surface.fill(self.colors.get('black'))
        self.info_surface.fill(self.colors.get('gray'))

        self.draw_info(player)
        self.draw_mini_map(player, game_map)

        self.win.blit(self.game_surface, (0, 0))
        self.info_surface.blit(self.mini_map_surface,
                               (0, self.info_surface.get_height() - self.mini_map_surface.get_height()))
        self.win.blit(self.info_surface, (self.game_surface.get_width(), 0))

        pygame.display.update()

    def draw_info(self, player):
        x_text = self.small_font.render('X: {:}'.format(player.x), True, self.colors.get('white'))
        y_text = self.small_font.render('Y: {:}'.format(player.y), True, self.colors.get('white'))
        fps_text = self.small_font.render('FPS: {:.2f}'.format(self.clock.get_fps()), True, self.colors.get('white'))

        self.info_surface.blit(fps_text, (20, 20))
        self.info_surface.blit(x_text, (20, 60))
        self.info_surface.blit(y_text, (20, 100))

    def draw_mini_map(self, player, game_map):
        self.mini_map_surface.fill(self.colors.get('red'))

        tile_size_x = self.mini_map_surface.get_width() / game_map.width
        tile_size_y = self.mini_map_surface.get_height() / game_map.height

        for coords, tile in game_map.map.items():
            x, y = coords
            if tile.blocks_movement:
                pygame.draw.rect(self.mini_map_surface, self.colors.get('white'),
                                 pygame.Rect(x * tile_size_x, y * tile_size_y, tile_size_x, tile_size_y))
            else:
                pygame.draw.rect(self.mini_map_surface, self.colors.get('black'),
                                 pygame.Rect(x * tile_size_x, y * tile_size_y, tile_size_x, tile_size_y))

        pygame.draw.rect(self.mini_map_surface, self.colors.get('red'),
                         pygame.Rect(player.x * tile_size_x - tile_size_x / 2,
                                     player.y * tile_size_y - tile_size_x / 2,
                                     tile_size_x,
                                     tile_size_y))
