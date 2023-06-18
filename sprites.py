import pygame
import utils

EXIT_EVENT = pygame.USEREVENT + 1


class Background(pygame.sprite.Sprite):
    INITIAL_SCALE_FACTOR = 2
    SPEED = 3
    ZOOM_SPEED = 0.002
    # TODO base this off of image size
    EXIT_PROXIMITY = 100
    EXIT_TRIGGER_PROXIMITY = EXIT_PROXIMITY / 3
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
        self.update_exit_positions()

    def update(self):
        self.move()
        x_edge = self.screen.get_width() * 0.2

        if self.position[0] > x_edge:
            self.position[0] = x_edge
        elif self.position[0] + x_edge < \
            self.screen.get_width() - self.image.get_width():
            self.position[0] = self.screen.get_width() - \
                self.image.get_width() - x_edge

        y_edge = self.screen.get_height() * 0.2
        if self.position[1] > -0.2 * self.screen.get_height() + y_edge:
            self.position[1] = -0.2 * self.screen.get_height() + y_edge
        elif self.position[1] + y_edge < \
            self.screen.get_height() - self.image.get_height():
            self.position[1] = self.screen.get_height() - \
                self.image.get_height() - y_edge
        else:
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
        self.update_exit_positions()
        exit_event = None
        screen_center = self.screen.get_rect().center
        for exit_name, exit_pos in self.exits.items():
            if exit_pos.distance_to(
                    screen_center) < self.EXIT_TRIGGER_PROXIMITY:
                exit_event = {"direction": exit_name}
                break

        if exit_event:
            pygame.event.post(pygame.event.Event(EXIT_EVENT, exit_event))

    def update_exit_positions(self):
        bg_rect = self.image.get_rect()
        pos_vec = pygame.math.Vector2(self.position)

        top = (bg_rect.width // 2, bg_rect.height * 0.1)
        top_vec = pos_vec + pygame.math.Vector2(top)
        self.exits["up"] = top_vec

        bottom = (bg_rect.width // 2, bg_rect.height)
        bottom_vec = pos_vec + pygame.math.Vector2(bottom)
        self.exits["down"] = bottom_vec

        left = (0, bg_rect.height // 2)
        left_vec = pos_vec + pygame.math.Vector2(left)
        self.exits["left"] = left_vec

        right = (bg_rect.width, bg_rect.height // 2)
        right_vec = pos_vec + pygame.math.Vector2(right)
        self.exits["right"] = right_vec

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
        # s = Vignette.circle_gradient(self, size)
        # self.image.blit(s, (0,0))
        self.screen.blit(self.image, self.position)

    def draw_exits(self):
        for name, exit_pos in self.exits.items():
            self.draw_exit(name, exit_pos)

    def draw_exit(self, text, center):


        yellow = (255, 255, 153)
        black = (0, 0, 0)
        white = (255, 255, 255)
        radius_full = self.original_image.get_width() // 10
        radius_full = 50
        proximity = radius_full * 2
        
        screen_center = pygame.math.Vector2(self.screen.get_rect().center)
        
        distance = screen_center.distance_to(center)
        p = utils.progress(proximity * 1, proximity * 1.5, distance)
        
        s = pygame.Surface((radius_full * 2, radius_full * 2), pygame.SRCALPHA)
        draw_radius = radius_full - radius_full * p
        pygame.draw.circle(s, black, (radius_full, radius_full), draw_radius)
        # v = Vignette.circle_gradient(self, s.get_size())
        # self.image.blit(v, (0,0), special_flags=pygame.BLEND_RGBA_MULT)

        self.screen.blit(s, (center[0] - radius_full, center[1] - radius_full))


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

    def linear_gradient(self, size):
        alpha_gradient = pygame.Surface(size, pygame.SRCALPHA)
        for y in range(alpha_gradient.get_height()):
            alpha = int(255 * y / alpha_gradient.get_height())
            pygame.draw.line(alpha_gradient, (255, 255, 255, alpha), (0, y),
                             (alpha_gradient.get_width(), y))
        return alpha_gradient

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
