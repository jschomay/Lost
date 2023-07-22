import pygame
from sprites import Background, Vignette, EXIT_EVENT
import random
from game_map import GameMap
from manifest import manifest


class Game():

    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()

        self.background_color = (0, 0, 0)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screen.fill(self.background_color)
        pygame.display.set_caption('Lost')

        self.background_images = {}
        for scene in manifest:
            img = pygame.image.load("images/backgrounds/" +
                                    scene["filename"]).convert()
            self.background_images[scene["filename"]] = img

        # top area
        top_area_size = int(self.screen.get_height() * 0.6)
        self.top_area = pygame.Surface((top_area_size, top_area_size))
        self.top_area_offset = (self.screen.get_width() // 2 -
                                self.top_area.get_width() // 2,
                                self.screen.get_height() / 20)
        self.top_area.fill(self.background_color)

        # game_map area (bottom left)
        map_area_size = 100
        self.map_area = pygame.Surface((map_area_size, map_area_size))
        self.map_area_offset = (self.screen.get_width() -
                                self.map_area.get_width(), 40)

        # story area
        story_area_size = (self.screen.get_width() * 0.9, \
                           self.screen.get_height() - top_area_size)
        self.story_area = pygame.Surface(story_area_size)
        self.story_area_offset = (self.screen.get_width() // 2 -
                                  self.story_area.get_width() // 2,
                                  self.top_area_offset[1] + 20 + top_area_size)

        self.story_font = pygame.font.SysFont('Calibri', 16)
        self.story_font.set_italic(True)

        # fade transition
        self.fade_speed = 2
        self.fade_surface = pygame.Surface(self.screen.get_size(),
                                           pygame.SRCALPHA)

        self.vignette = Vignette(self.top_area)

    def init(self):
        self.stats = {"vigor": 5, "courage": 5}
        self.visited = set()
        self.fade_alpha = 255

        self.scenes = random.sample(manifest, len(manifest))

        starting_index = 0
        for i, scene in enumerate(self.scenes):
            if scene['filename'] == 'lamp post.jpg':
                starting_index = i
                break

        ending_index = 0
        for i, scene in enumerate(self.scenes):
            if scene['filename'] == 'hut1.png':
                ending_index = i
                break

        self.map_level = 0
        self.map_item_locations = set(random.sample(range(0, 15), 3))

        self.game_map = GameMap(self.map_area, starting_index, ending_index)

        self.current_scene_index = self.game_map.positon_to_index()
        self.visited.add(self.current_scene_index)
        self.current_scene = self.scenes[self.current_scene_index]

        self.set_story_text()
        self.background = Background(
            self.background_images[self.current_scene["filename"]],
            self.top_area)

        self.game_exit = False
        self.game_over = False

    def run(self):
        while not self.game_exit:
            events = pygame.event.get()
            if self.game_over:
                keys_pressed = pygame.key.get_pressed()
                if keys_pressed[pygame.K_RETURN]:
                    self.game_exit = True
                continue

            for event in events:
                if event.type == pygame.QUIT:
                    self.game_exit = True
                if event.type == EXIT_EVENT:
                    while self.fade_alpha < 255:
                        self.fade_surface.fill((0, 0, 0, self.fade_alpha))
                        self.screen.blit(self.fade_surface, (0, 0))
                        pygame.display.flip()
                        self.fade_alpha += self.fade_speed

                    self.fade_alpha = 255
                    self.background.kill()
                    self.game_map.update(event.direction)

                    self.current_scene_index = self.game_map.positon_to_index()
                    trigger = "on_return" if self.current_scene_index in self.visited else "on_discover"
                    self.visited.add(self.current_scene_index)
                    self.current_scene = self.scenes[self.current_scene_index]

                    self.set_story_text(trigger)

                    if self.map_level == 0 and self.current_scene_index in self.map_item_locations:
                        self.map_level = 1
                        self.map_item_locations.remove(
                            self.current_scene_index)
                        self.story_text += "\nYou found a map!"
                    elif self.map_level == 1 and self.current_scene_index in self.map_item_locations:
                        self.map_level = 2
                        self.map_item_locations.remove(
                            self.current_scene_index)
                        self.story_text += "\nYou found a compass!"
                    elif self.map_level == 2 and self.current_scene_index in self.map_item_locations:
                        self.map_level = 3
                        self.map_item_locations.remove(
                            self.current_scene_index)
                        self.story_text += "\nYou found some binoculars!"

                    for stat_def in self.current_scene[trigger]["stats"]:
                        stat, diff = stat_def.values()
                        if stat == "vigor" and diff < 0 \
                            and abs(diff) > self.stats["vigor"]:
                            self.stats["courage"] -= abs(diff) - stats["vigor"]
                        self.stats[stat] = min(5,
                                               max(0, self.stats[stat] + diff))

                    if self.stats["courage"] == 0:
                        self.game_over = True
                        self.fade_alpha = 0
                        self.story_text += "\nYou lost your courage.  Game over.\nPress 'Enter' to try again."

                    if self.current_scene["filename"] == "hut1.png":
                        self.game_over = True
                        self.fade_alpha = 0

                    self.background = Background(
                        self.background_images[self.current_scene["filename"]],
                        self.top_area)

            self.background.handle_events(events)
            self.background.update(self.stats["vigor"] / 5)
            self.background.draw()
            self.vignette.draw(self.stats["courage"] / 5)
            Vignette.feather(self.top_area, 40)
            self.game_map.draw(self.map_level)
            self.draw_story()
            self.screen.blit(self.top_area, self.top_area_offset)
            self.screen.blit(self.story_area, self.story_area_offset)
            self.screen.blit(self.map_area, self.map_area_offset)

            self.fade_surface.fill((0, 0, 0, self.fade_alpha))
            self.screen.blit(self.fade_surface, (0, 0))

            self.draw_stats()

            self.draw_fps()

            pygame.display.flip()

            if self.fade_alpha > 0:
                self.fade_alpha = max(0, self.fade_alpha - self.fade_speed)

            self.clock.tick(60)

    def clean_up(self):
        self.background.kill()
        self.game_map = None

    def quit(self):
        pygame.quit()

    def draw_story(self):
        lines = []
        for line in self.story_text.split("\n"):
            words = line.split(" ")
            current_line = ""
            for word in words:
                test_line = current_line + " " + word if current_line else word
                if self.story_font.size(
                        test_line)[0] > self.story_area.get_width():
                    lines.append(current_line)
                    current_line = word
                else:
                    current_line = test_line
            lines.append(current_line)

        self.story_area.fill(self.background_color)
        line_height = self.story_font.get_linesize()
        y = line_height
        for line in lines:
            text_surface = self.story_font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.center = (self.story_area.get_width() // 2, y)
            self.story_area.blit(text_surface, text_rect)
            y += line_height

    def draw_fps(self):
        fps_text = "FPS: " + str(self.clock.get_fps() * 100 // 100)
        fps_text_surface = self.story_font.render(fps_text, True,
                                                  (255, 255, 255), (0, 0, 0))
        fps_text_rect = fps_text_surface.get_rect()
        fps_text_rect.topleft = (self.screen.get_width() - 10 -
                                 fps_text_rect.w,
                                 self.screen.get_height() - 50)
        self.screen.blit(fps_text_surface, fps_text_rect)

    def set_story_text(self, trigger="on_discover"):
        self.story_text = self.current_scene[trigger]["description"]

    def draw_stats(self):
        fill_color = (245, 245, 153)
        empty_color = (100, 100, 100)
        width = 20
        height = 10
        margin = 4

        x = 10
        y = self.screen.get_height() - 30

        vigor_text = self.story_font.render("Vigor:", True, (255, 255, 255),
                                            (0, 0, 0))
        vigor_text_rect = vigor_text.get_rect()
        vigor_text_rect.topleft = (x, y - vigor_text.get_height())
        self.screen.blit(vigor_text, vigor_text_rect)

        courage_text = self.story_font.render("Courage:", True,
                                              (255, 255, 255), (0, 0, 0))
        courage_text_rect = courage_text.get_rect()
        courage_text_rect.topleft = (x, y + vigor_text_rect.height -
                                     courage_text.get_height())
        self.screen.blit(courage_text, courage_text_rect)

        for i in range(5):
            rect = pygame.Rect(
                courage_text_rect.width + margin + x + i * (width + margin),
                y - 15, width, height)
            if i < self.stats["vigor"]:
                pygame.draw.rect(self.screen, fill_color, rect)
            else:
                pygame.draw.rect(self.screen, empty_color, rect)

        for i in range(5):
            rect = pygame.Rect(
                courage_text_rect.width + margin + x + i * (width + margin),
                y - 15 + vigor_text_rect.height, width, height)
            if i < self.stats["courage"]:
                pygame.draw.rect(self.screen, fill_color, rect)
            else:
                pygame.draw.rect(self.screen, empty_color, rect)
