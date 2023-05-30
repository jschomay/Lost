import pygame
from sprites import Background, Vignette, EXIT_EVENT
import glob
import random

pygame.init()
clock = pygame.time.Clock()

background_color = (0, 0, 0)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill(background_color)
pygame.display.set_caption('Lost')

background_files = glob.glob("images/background1*.jpg")
background_images = []
for file in background_files:
    img = pygame.image.load(file).convert()
    background_images.append(img)
scenes = random.sample(background_images, len(background_files))

top_area_size = int(screen.get_height() * 0.6)
top_area = pygame.Surface((top_area_size, top_area_size))
top_area_offset = (screen.get_width() // 2 - top_area.get_width() // 2,
                   screen.get_height() / 20)
top_area.fill(background_color)

fade_alpha = 255
fade_speed = 2
fade_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

pygame.display.update()

game_exit = False

background = Background(scenes.pop(), top_area)
vignette = Vignette(top_area)

while not game_exit:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == EXIT_EVENT:
            while fade_alpha < 255:
                fade_surface.fill((0, 0, 0, fade_alpha))
                screen.blit(fade_surface, (0, 0))
                pygame.display.flip()
                fade_alpha += fade_speed
                
            fade_alpha = 255
            background.kill()
            background = Background(scenes.pop(), top_area)

    background.handle_events(events)
    background.update()
    background.draw()
    vignette.draw()
    background.draw_exits()
    screen.blit(top_area, top_area_offset)
    
    fade_surface.fill((0, 0, 0, fade_alpha))
    screen.blit(fade_surface, (0, 0))
    pygame.display.flip()

    if fade_alpha > 0:
        fade_alpha = max(0, fade_alpha - fade_speed)

    clock.tick(60)

pygame.quit()
quit()
