import pygame


class Background():
    SCALE_FACTOR = 3
    SPEED = 5

    def __init__(self, background, screen):
        self.image = pygame.image.load(background).convert()
        new_size = (screen.get_width() * self.SCALE_FACTOR,
                    screen.get_height() * self.SCALE_FACTOR)
        self.image = pygame.transform.scale(self.image, new_size)
        self.position = [0, 0]
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.position[0] += self.speed_x
        self.position[1] += self.speed_y

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
