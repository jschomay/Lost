import pygame
from sprites import Background

pygame.init()
clock = pygame.time.Clock()

background_color = (40, 40, 40)
screen = pygame.display.set_mode((400,300))
pygame.display.set_caption('Lost')
screen.fill(background_color)

pygame.display.update()

game_exit = False

background = Background("images/background1.jpg", screen)

while not game_exit:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            gameExit = True
    
    background.handle_events(events)
    background.update(screen)
    background.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
quit()