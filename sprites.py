import pygame


class Background():
    INITIAL_SCALE_FACTOR = 3
    SPEED = 3
    ZOOM_EFFECT = 1

    def __init__(self, background, screen):
        self.original_image = pygame.image.load(background).convert()
        new_size = (screen.get_width() * self.INITIAL_SCALE_FACTOR,
                    screen.get_height() * self.INITIAL_SCALE_FACTOR)
        self.image = pygame.transform.scale(self.original_image, new_size)

        self.position = [(screen.get_width() - self.image.get_width()) / 2,
                         (screen.get_height() - self.image.get_height())]
        self.speed_x = 0
        self.speed_y = 0

    def update(self, screen):
        self.position[0] += self.speed_x
        self.position[1] += self.speed_y

        if self.position[1] > 0: self.position[1] = 0
        if self.position[0] > 0: self.position[0] = 0
        if self.position[1] < screen.get_height() - self.image.get_height():
            self.position[1] = screen.get_height() - self.image.get_height()
        if self.position[0] < screen.get_width() - self.image.get_width():
            self.position[0] = screen.get_width() - self.image.get_width()

        old_size = self.image.get_size()
        center = self.position[1] + self.image.get_height() / 2
        zoom_factor = (1 + (center - screen.get_height() / 2) /
                       screen.get_height()) * self.ZOOM_EFFECT
        new_size = (int(self.original_image.get_width() * zoom_factor),
                    int(self.original_image.get_height() * zoom_factor))

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
