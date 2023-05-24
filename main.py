import pygame
from sprites import Background, Vignette

pygame.init()
clock = pygame.time.Clock()

background_color = (0, 0, 0)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Lost')
screen.fill(background_color)

top_area_size = int(screen.get_height() * 0.6)
top_area = pygame.Surface((top_area_size, top_area_size))
top_area_offset = (screen.get_width() // 2 - top_area.get_width() // 2,
                   screen.get_height() / 20)
top_area.fill(background_color)

pygame.display.update()

game_exit = False

background = Background("images/background1.jpg", top_area)
vignette = Vignette(top_area)

while not game_exit:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            gameExit = True

    background.handle_events(events)
    background.update()
    background.draw()
    vignette.draw()
    screen.blit(top_area, top_area_offset)
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
quit()
