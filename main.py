import pygame
from sprites import Background, Vignette, EXIT_EVENT
import glob
import random
from map import Map

pygame.init()
clock = pygame.time.Clock()

background_color = (0, 0, 0)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill(background_color)
pygame.display.set_caption('Lost')

# loading backgrounds
background_files = glob.glob("images/backgrounds/*")
background_images = []
for file in background_files:
    img = pygame.image.load(file).convert()
    background_images.append(img)
scenes = random.sample(background_images, len(background_files))

# top area
top_area_size = int(screen.get_height() * 0.6)
top_area = pygame.Surface((top_area_size, top_area_size))
top_area_offset = (screen.get_width() // 2 - top_area.get_width() // 2,
                   screen.get_height() / 20)
top_area.fill(background_color)

# map area (bottom left)
map_area_size = 100
map_area = pygame.Surface((map_area_size, map_area_size))
map_area_offset = (screen.get_width() - map_area.get_width(), 40)

# story area
story_texts = [
    "... the air is thick with fog...", "... the sky is dark....",
    "... I hear noises in the bushes around me...",
    "... the trees quake overhead...", "... the ground is damp ...",
    "... am I lost?...", "... this path is going in circles...",
    "... there are trees in every direction...",
    "... have I been here before?..."
]
story_text = random.choice(story_texts)
story_area_size = (screen.get_width() - top_area_size, \
                   screen.get_height() // 4)
story_area = pygame.Surface(story_area_size)
story_area_offset = (screen.get_width() // 2 - story_area.get_width() // 2,
                     top_area_offset[1] + 20 + top_area_size)

story_font = pygame.font.SysFont('Calibri', 16)
story_font.set_italic(True)


def draw_story(text):
    text_surface = story_font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.center = (story_area.get_width() // 2, text_rect.height)
    story_area.fill(background_color)
    story_area.blit(text_surface, text_rect)


# fade transition
fade_alpha = 255
fade_speed = 2
fade_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

# game elements
background = Background(scenes.pop(), top_area)
vignette = Vignette(top_area)
map = Map(map_area)

player_x, player_y = 0, 0

game_exit = False
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
            story_text = random.choice(story_texts)
            map.update(event.direction)

    background.handle_events(events)
    background.update()
    background.draw()
    vignette.draw()
    background.draw_exits()
    map.draw()
    screen.blit(top_area, top_area_offset)
    screen.blit(story_area, story_area_offset)
    screen.blit(map_area, map_area_offset)
    draw_story(story_text)

    fade_surface.fill((0, 0, 0, fade_alpha))
    screen.blit(fade_surface, (0, 0))

    pygame.display.flip()

    if fade_alpha > 0:
        fade_alpha = max(0, fade_alpha - fade_speed)

    clock.tick(60)

pygame.quit()
quit()
