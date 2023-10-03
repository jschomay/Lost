import pygame
import utils

EXIT_EVENT = pygame.USEREVENT + 1


class Background(pygame.sprite.Sprite):
    INITIAL_SCALE_FACTOR = 2
    FULL_SCALE_FACTOR = 1.5
    ASPECT_RATIO = 1
    BASE_SPEED = 0.9
    MAX_SPEED_INC = 0.2

    FEATHER_SIZE = 8

    def __init__(self, image, screen):
        pygame.sprite.Sprite.__init__(self)

        self.original_image = image
        self.image = None
        self.screen = screen
        self.position = [0, 0]
        self.speed_x = 0
        self.speed_y = 0
        self.key_downs = set()

        Vignette.feather(self.original_image,
                         self.original_image.get_width() // self.FEATHER_SIZE)

        self.scale_image()

    def scale_image(self):
        factor = self.INITIAL_SCALE_FACTOR + self.FULL_SCALE_FACTOR * self.position[
            1] / self.screen.get_height()
        new_size = (int(self.screen.get_width() * factor),
                    int(self.screen.get_height() * factor))

        self.image = pygame.transform.scale(self.original_image, new_size)

    def update(self, speed_percent):
        self.move(speed_percent)

        self.speed_x *= speed_percent
        self.speed_y *= speed_percent

        self.position[0] += self.speed_x
        self.position[1] += self.speed_y

        self.scale_image()

        # check for exit
        if self.position[0] > self.screen.get_width() * 0.4:
            exit_event = {"direction": "left"}
            pygame.event.post(pygame.event.Event(EXIT_EVENT, exit_event))
        elif self.position[0] < -self.screen.get_width() * 0.4:
            exit_event = {"direction": "right"}
            pygame.event.post(pygame.event.Event(EXIT_EVENT, exit_event))
        elif self.position[1] > self.screen.get_height() * 0.5:
            exit_event = {"direction": "up"}
            pygame.event.post(pygame.event.Event(EXIT_EVENT, exit_event))
        elif self.position[1] < -self.screen.get_height() * 0.4:
            exit_event = {"direction": "down"}
            pygame.event.post(pygame.event.Event(EXIT_EVENT, exit_event))

    def move(self, speed_percent):
        speed = self.BASE_SPEED + self.MAX_SPEED_INC * speed_percent
        self.speed_x = 0
        self.speed_y = 0
        if pygame.K_UP in self.key_downs:
            self.speed_y += speed
        if pygame.K_DOWN in self.key_downs:
            self.speed_y += -speed
        if pygame.K_LEFT in self.key_downs:
            self.speed_x += speed
        if pygame.K_RIGHT in self.key_downs:
            self.speed_x += -speed

        # Normalize speed vector
        speed_magnitude = (self.speed_x**2 + self.speed_y**2)**0.5
        if speed_magnitude != 0:
            self.speed_x /= speed_magnitude
            self.speed_y /= speed_magnitude

        # Multiply speed vector by constant value
        self.speed_x *= speed
        self.speed_y *= speed

        self.position[0] += self.speed_x
        self.position[1] += self.speed_y

    def draw(self):
        offset_x = (self.screen.get_width() - self.image.get_width()) // 2
        offset_y = (self.screen.get_height() - self.image.get_height()) // 2
        pos = [
            int(self.position[0] + offset_x),
            int(self.position[1] + offset_y)
        ]
        self.screen.blit(self.image, pos)

    def handle_events(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN and event.key in [
                    pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT
            ]:
                self.key_downs.add(event.key)

            elif event.type == pygame.KEYUP and event.key in self.key_downs:
                self.key_downs.remove(event.key)


class Vignette():

    def __init__(self, screen):
        self.screen = screen
        self.vignette_layer = pygame.Surface(screen.get_size(),
                                             pygame.SRCALPHA)

    def linear_gradient_left(surface, size):
        alpha_gradient = pygame.Surface((size, surface.get_height()),
                                        pygame.SRCALPHA)
        for x in range(0, size):
            alpha = 255 - int(255 * x / size)
            pygame.draw.line(alpha_gradient, (0, 0, 0, alpha), (x, 0),
                             (x, alpha_gradient.get_height()))
        surface.blit(alpha_gradient, (0, 0))

    def linear_gradient_right(surface, size):
        alpha_gradient = pygame.Surface((size, surface.get_height()),
                                        pygame.SRCALPHA)
        for x in range(0, size):
            alpha = int(255 * x / size)
            pygame.draw.line(alpha_gradient, (0, 0, 0, alpha), (x, 0),
                             (x, alpha_gradient.get_height()))
        surface.blit(alpha_gradient, (surface.get_width() - size, 0))

    def linear_gradient_top(surface, size):
        alpha_gradient = pygame.Surface((surface.get_width(), size),
                                        pygame.SRCALPHA)
        for y in range(0, size):
            alpha = 255 - int(255 * y / size)
            pygame.draw.line(alpha_gradient, (0, 0, 0, alpha), (0, y),
                             (alpha_gradient.get_width(), y))
        surface.blit(alpha_gradient, (0, 0))

    def linear_gradient_bottom(surface, size):
        alpha_gradient = pygame.Surface((surface.get_width(), size),
                                        pygame.SRCALPHA)
        for y in range(0, size):
            alpha = int(255 * y / size)
            pygame.draw.line(alpha_gradient, (0, 0, 0, alpha), (0, y),
                             (alpha_gradient.get_width(), y))
        surface.blit(alpha_gradient, (0, surface.get_height() - size))

    def feather(surface, size):
        Vignette.linear_gradient_top(surface, size)
        Vignette.linear_gradient_bottom(surface, size)
        Vignette.linear_gradient_left(surface, size)
        Vignette.linear_gradient_right(surface, size)

    def circle_gradient(self, size, smoothness=0.8):
        alpha_gradient = pygame.Surface(size, pygame.SRCALPHA)
        alpha_gradient.fill((0, 0, 0))
        radius = int(min(size) / 2)
        for y in range(radius):
            alpha = int(255 * (1 - y / radius))
            # pygame.draw.circle(alpha_gradient, (0, 0, 0, alpha), center, 1.0 * radius - y)
            y = y * smoothness
            rect = pygame.Rect(y, y, size[0] - y * 2, size[1] - y * 2)
            pygame.draw.ellipse(alpha_gradient, (0, 0, 0, alpha), rect)
        return alpha_gradient

    def draw(self, amount):
        black = (0, 0, 0)
        self.vignette_layer.fill(black)
        circle_gradient = self.circle_gradient(self.screen.get_size())
        circle_center = (int(self.screen.get_width() / 2),
                         int(self.screen.get_height() / 2))
        scale_factor = 0.5 + 0.5 * amount
        circle_gradient = pygame.transform.rotozoom(circle_gradient, 0,
                                                    scale_factor)
        blit_pos = (int(circle_center[0] - circle_gradient.get_width() / 2),
                    int(circle_center[1] - circle_gradient.get_height() / 2))
        self.vignette_layer.blit(circle_gradient,
                                 blit_pos,
                                 special_flags=pygame.BLEND_RGBA_MULT)
        self.screen.blit(self.vignette_layer, (0, 0))
