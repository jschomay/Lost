import pygame
from sprites import Background

pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((400,300))
pygame.display.set_caption('Lost')

pygame.display.update()

gameExit = False

background = Background("images/background1.jpg", screen)

while not gameExit:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            gameExit = True
    
    background.handle_events(events)
    background.update()
    background.draw(screen)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()