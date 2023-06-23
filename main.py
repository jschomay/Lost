import pygame
from sprites import Background, Vignette, EXIT_EVENT
import random
from game_map import GameMap
from manifest import manifest

pygame.init()
clock = pygame.time.Clock()

background_color = (0, 0, 0)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen.fill(background_color)
pygame.display.set_caption('Lost')

# loading scenes
scenes = random.sample(manifest, len(manifest))
background_files = [scene["filename"] for scene in scenes]
background_images = []
for file in background_files:
    img = pygame.image.load("images/backgrounds/" + file).convert()
    background_images.append(img)

# top area
top_area_size = int(screen.get_height() * 0.6)
top_area = pygame.Surface((top_area_size, top_area_size))
top_area_offset = (screen.get_width() // 2 - top_area.get_width() // 2,
                   screen.get_height() / 20)
top_area.fill(background_color)

# game_map area (bottom left)
map_area_size = 100
map_area = pygame.Surface((map_area_size, map_area_size))
map_area_offset = (screen.get_width() - map_area.get_width(), 40)

# story area
story_area_size = (screen.get_width() * 0.9, \
                   screen.get_height() - top_area_size)
story_area = pygame.Surface(story_area_size)
story_area_offset = (screen.get_width() // 2 - story_area.get_width() // 2,
                     top_area_offset[1] + 20 + top_area_size)

story_font = pygame.font.SysFont('Calibri', 16)
story_font.set_italic(True)


def draw_story(text, width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if story_font.size(test_line)[0] > width:
            lines.append(current_line)
            current_line = word
        else:
            current_line = test_line
    lines.append(current_line)
    
    story_area.fill(background_color)
    line_height = story_font.get_linesize()
    y = line_height
    for line in lines:
        text_surface = story_font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.center = (story_area.get_width() // 2, y)
        story_area.blit(text_surface, text_rect)
        y += line_height


def draw_fps():
    fps_text = "FPS: " + str(clock.get_fps() * 100 // 100)
    fps_text_surface = story_font.render(fps_text, True, (255, 255, 255),
                                         (0, 0, 0))
    fps_text_rect = fps_text_surface.get_rect()
    fps_text_rect.topleft = (10, screen.get_height() - 30)
    screen.blit(fps_text_surface, fps_text_rect)

def get_story_text(scene):
    story_text = current_scene["description"]
    extra_text = current_scene["on_discover"]["description"]
    return story_text + "\n\n" + extra_text

# fade transition
fade_alpha = 255
fade_speed = 2
fade_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

# game elements
vignette = Vignette(top_area)
game_map = GameMap(map_area)

current_scene_index = game_map.positon_to_index()
current_scene = scenes[current_scene_index]
story_text = get_story_text(current_scene)
background = Background(background_images[current_scene_index], top_area)

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
            game_map.update(event.direction)
            current_scene_index = game_map.positon_to_index()
            current_scene = scenes[current_scene_index]
            story_text = get_story_text(current_scene)
            background = Background(background_images[current_scene_index],
                                    top_area)

    background.handle_events(events)
    background.update()
    background.draw()
    vignette.draw()
    game_map.draw()
    screen.blit(top_area, top_area_offset)
    screen.blit(story_area, story_area_offset)
    screen.blit(map_area, map_area_offset)
    draw_story(story_text, story_area.get_width())

    fade_surface.fill((0, 0, 0, fade_alpha))
    screen.blit(fade_surface, (0, 0))

    draw_fps()

    pygame.display.flip()

    if fade_alpha > 0:
        fade_alpha = max(0, fade_alpha - fade_speed)

    clock.tick(60)

pygame.quit()
quit()
