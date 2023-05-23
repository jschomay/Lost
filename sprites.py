import pygame


class Background(pygame.sprite.Sprite):
    INITIAL_SCALE_FACTOR = 2
    SPEED = 1
    ZOOM_SPEED = 0.002

    def __init__(self, background, screen):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.image.load(background).convert()
        new_size = (screen.get_width() * self.INITIAL_SCALE_FACTOR,
                    screen.get_height() * self.INITIAL_SCALE_FACTOR)
        self.image = pygame.transform.scale(self.original_image, new_size)

        self.position = [(screen.get_width() - self.image.get_width()) / 2,
                         (screen.get_height() - self.image.get_height())]
        self.speed_x = 0
        self.speed_y = 0
        self.y = 0

    def update(self, screen):
        self.position[0] += self.speed_x
        self.position[1] += self.speed_y

        if self.position[0] > 0: self.position[0] = 0
        if self.position[0] < screen.get_width() - self.image.get_width():
            self.position[0] = screen.get_width() - self.image.get_width()

        if self.position[1] > 0:
            self.position[1] = 0
        elif self.position[1] < screen.get_height() - self.image.get_height():
            self.position[1] = screen.get_height() - self.image.get_height()
        else:
            self.y += self.speed_y

        zoom_factor = 1 + self.y * self.ZOOM_SPEED

        old_size = self.image.get_size()
        new_size = (int(screen.get_width() * self.INITIAL_SCALE_FACTOR *
                        zoom_factor),
                    int(screen.get_height() * self.INITIAL_SCALE_FACTOR *
                        zoom_factor))

        self.position[0] -= (new_size[0] - old_size[0]) / 2
        self.position[1] -= (new_size[1] - old_size[1]) / 2

        self.image = pygame.transform.scale(self.original_image, new_size)

    def draw(self, surface):
        surface.blit(self.image, self.position)

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.speed_y = self.SPEED
                elif event.key == pygame.K_DOWN:
                    self.speed_y = -self.SPEED
                elif event.key == pygame.K_LEFT:
                    self.speed_x = self.SPEED
                elif event.key == pygame.K_RIGHT:
                    self.speed_x = -self.SPEED

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    self.speed_y = 0
                elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.speed_x = 0


class Vignette():

    def __init__(self, screen):
        black = (0, 0, 0)
        self.vignette_layer = pygame.Surface(screen.get_size(),
                                             pygame.SRCALPHA)
        self.vignette_layer.fill(black)
        circle_gradient = self.circle_gradient(screen.get_size())
        circle_center = (int(screen.get_width() / 2), int(screen.get_height() / 2))
        scale_factor = 1.0
        circle_gradient = pygame.transform.rotozoom(circle_gradient, 0, scale_factor)
        blit_pos = (int(circle_center[0] - circle_gradient.get_width() / 2),
                    int(circle_center[1] - circle_gradient.get_height() / 2))
        self.vignette_layer.blit(circle_gradient, blit_pos,
                                 special_flags=pygame.BLEND_RGBA_MULT)

    def linear_gradient(self, size):
        alpha_gradient = pygame.Surface(size, pygame.SRCALPHA)
        for y in range(alpha_gradient.get_height()):
            alpha = int(255 * y / alpha_gradient.get_height())
            pygame.draw.line(alpha_gradient, (255, 255, 255, alpha), (0, y),
                             (alpha_gradient.get_width(), y))
        return alpha_gradient

    def circle_gradient(self, size):
        alpha_gradient = pygame.Surface(size, pygame.SRCALPHA)
        alpha_gradient.fill((0, 0, 0))
        radius = int(min(size) / 2)
        for y in range(radius):
            alpha = int(255 * (1 - y / radius))
            # pygame.draw.circle(alpha_gradient, (0, 0, 0, alpha), center, 1.0 * radius - y)
            y = y * 0.8
            rect = pygame.Rect(y, y, size[0] - y * 2, size[1] - y * 2)
            pygame.draw.ellipse(alpha_gradient, (0, 0, 0, alpha), rect)
        return alpha_gradient

    def draw(self, screen):
        screen.blit(self.vignette_layer, (0, 0))
