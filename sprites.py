import pygame
import utils

EXIT_EVENT = pygame.USEREVENT + 1


class Background(pygame.sprite.Sprite):
    INITIAL_SCALE_FACTOR = 2
    SPEED = 3
    ZOOM_SPEED = 0.002
    ASPECT_RATIO = 1

    def __init__(self, background, screen):
        pygame.sprite.Sprite.__init__(self)

        self.screen = screen
        self.original_image = background

        (screen_width, screen_height) = screen.get_size()
        screen_aspect_ratio = screen_width / screen_height
        if screen_aspect_ratio < self.ASPECT_RATIO:
            new_size = (int(screen_height * self.ASPECT_RATIO), screen_height)
        else:
            new_size = (screen_width, int(screen_width / self.ASPECT_RATIO))
        self.image = pygame.Surface(new_size)

        cropped_offset = (
            (self.original_image.get_width() - self.image.get_width()) / 2,
            (self.original_image.get_height() - self.image.get_height()) / 2)
        cropped_rect = pygame.Rect(cropped_offset[0], cropped_offset[1],
                                   self.image.get_width(),
                                   self.image.get_height())
        self.image.blit(self.original_image.subsurface(cropped_rect), (0, 0))

        new_size = (screen.get_width() * self.INITIAL_SCALE_FACTOR,
                    screen.get_height() * self.INITIAL_SCALE_FACTOR)
        self.image = pygame.transform.scale(self.original_image, new_size)

        self.position = [(screen.get_width() - self.image.get_width()) / 2,
                         (screen.get_height() - self.image.get_height()) / 2]
        self.speed_x = 0
        self.speed_y = 0
        self.y = 0
        self.key_downs = set()

        self.exits = {}

    def update(self):
        self.move()

        self.y += self.speed_y
        zoom_factor = 1 + self.y * self.ZOOM_SPEED

        old_size = self.image.get_size()
        new_size = (int(self.screen.get_width() * self.INITIAL_SCALE_FACTOR *
                        zoom_factor),
                    int(self.screen.get_height() * self.INITIAL_SCALE_FACTOR *
                        zoom_factor))

        self.position[0] -= (new_size[0] - old_size[0]) / 2
        self.position[1] -= (new_size[1] - old_size[1]) / 2

        self.image = pygame.transform.scale(self.original_image, new_size)

        # check if exiting
        exit_event = None
        image_center = [
            self.position[0] + self.image.get_width() / 2,
            self.position[1] + self.image.get_height() / 2
        ]

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        if image_center[0] < screen_width * -0.5:
            exit_event = {"direction": "right"}
        elif image_center[0] > screen_width * 1.5:
            exit_event = {"direction": "left"}
        elif image_center[1] < screen_height * -0.1:
            exit_event = {"direction": "down"}
        elif image_center[1] > screen_height * 1.4:
            exit_event = {"direction": "up"}

        if exit_event:
            pygame.event.post(pygame.event.Event(EXIT_EVENT, exit_event))

    def move(self):
        self.speed_x = 0
        self.speed_y = 0
        if pygame.K_UP in self.key_downs:
            self.speed_y += self.SPEED
        if pygame.K_DOWN in self.key_downs:
            self.speed_y += -self.SPEED
        if pygame.K_LEFT in self.key_downs:
            self.speed_x += self.SPEED
        if pygame.K_RIGHT in self.key_downs:
            self.speed_x += -self.SPEED

        self.position[0] += self.speed_x
        self.position[1] += self.speed_y

    def draw(self):
        Vignette.feather(self.image, self.image.get_width() // 3)
        self.screen.blit(self.image, self.position)

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
        black = (0, 0, 0)
        self.vignette_layer = pygame.Surface(screen.get_size(),
                                             pygame.SRCALPHA)
        self.vignette_layer.fill(black)
        circle_gradient = self.circle_gradient(screen.get_size())
        circle_center = (int(screen.get_width() / 2),
                         int(screen.get_height() / 2))
        scale_factor = 1.0
        circle_gradient = pygame.transform.rotozoom(circle_gradient, 0,
                                                    scale_factor)
        blit_pos = (int(circle_center[0] - circle_gradient.get_width() / 2),
                    int(circle_center[1] - circle_gradient.get_height() / 2))
        self.vignette_layer.blit(circle_gradient,
                                 blit_pos,
                                 special_flags=pygame.BLEND_RGBA_MULT)


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

    def draw(self):
        self.screen.blit(self.vignette_layer, (0, 0))
