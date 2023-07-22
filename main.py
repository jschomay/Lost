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
    lines = []
    for line in text.split("\n"):
        words = line.split(" ")
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
    fps_text_rect.topleft = (screen.get_width() - 10 - fps_text_rect.w,
                             screen.get_height() - 50)
    screen.blit(fps_text_surface, fps_text_rect)


def get_story_text(scene, trigger="on_discover"):
    story_text = current_scene[trigger]["description"]
    return story_text


def draw_stats():
    fill_color = (245, 245, 153)
    empty_color = (100, 100, 100)
    width = 20
    height = 10
    margin = 4

    x = 10
    y = screen.get_height() - 30

    vigor_text = story_font.render("Vigor:", True, (255, 255, 255), (0, 0, 0))
    vigor_text_rect = vigor_text.get_rect()
    vigor_text_rect.topleft = (x, y - vigor_text.get_height())
    screen.blit(vigor_text, vigor_text_rect)

    courage_text = story_font.render("Courage:", True, (255, 255, 255),
                                     (0, 0, 0))
    courage_text_rect = courage_text.get_rect()
    courage_text_rect.topleft = (x, y + vigor_text_rect.height -
                                 courage_text.get_height())
    screen.blit(courage_text, courage_text_rect)

    for i in range(5):
        rect = pygame.Rect(
            courage_text_rect.width + margin * 3 + x + i * (width + margin),
            y - 15, width, height)
        if i < stats["vigor"]:
            pygame.draw.rect(screen, fill_color, rect)
        else:
            pygame.draw.rect(screen, empty_color, rect)

    for i in range(5):
        rect = pygame.Rect(
            courage_text_rect.width + margin * 3 + x + i * (width + margin),
            y - 15 + vigor_text_rect.height, width, height)
        if i < stats["courage"]:
            pygame.draw.rect(screen, fill_color, rect)
        else:
            pygame.draw.rect(screen, empty_color, rect)


# fade transition
fade_alpha = 255
fade_speed = 2
fade_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

# game elements and state
stats = {"vigor": 5, "courage": 5}
visited = set()

index = 0
for i, scene in enumerate(scenes):
    if scene['filename'] == 'lamp post.jpg':
        index = i
        break

vignette = Vignette(top_area)
game_map = GameMap(map_area, index)

current_scene_index = game_map.positon_to_index()
visited.add(current_scene_index)
current_scene = scenes[current_scene_index]
story_text = get_story_text(current_scene)
background = Background(background_images[current_scene_index], top_area)

game_exit = False
game_over = False
while not game_exit:
    if game_over:
        continue

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            game_exit = True
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
            trigger = "on_return" if current_scene_index in visited else "on_discover"
            visited.add(current_scene_index)
            current_scene = scenes[current_scene_index]

            for stat_def in current_scene[trigger]["stats"]:
                stat, diff = stat_def.values()
                if stat == "vigor" and diff < 0 \
                    and abs(diff) > stats["vigor"]:
                    stats["courage"] -= abs(diff) - stats["vigor"]
                stats[stat] = min(5, max(0, stats[stat] + diff))

            story_text = get_story_text(current_scene, trigger)

            if stats["courage"] == 0:
                game_over = True
                fade_alpha = 0
                story_text += "\nYou lost your courage.  Game Over."

            if current_scene["filename"] == "hut1.png":
                game_over = True
                fade_alpha = 0

            background = Background(background_images[current_scene_index],
                                    top_area)

    background.handle_events(events)
    background.update(stats["vigor"] / 5)
    background.draw()
    vignette.draw(stats["courage"] / 5)
    Vignette.feather(top_area, 40)
    game_map.draw()
    draw_story(story_text, story_area.get_width())
    screen.blit(top_area, top_area_offset)
    screen.blit(story_area, story_area_offset)
    screen.blit(map_area, map_area_offset)

    fade_surface.fill((0, 0, 0, fade_alpha))
    screen.blit(fade_surface, (0, 0))

    draw_stats()

    draw_fps()

    pygame.display.flip()

    if fade_alpha > 0:
        fade_alpha = max(0, fade_alpha - fade_speed)

    clock.tick(60)

pygame.quit()
quit()
