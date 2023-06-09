import pygame

grid_cols = 4
grid_rows = 4
cell_size = 15
margin = 0
grid_width = (cell_size + margin) * grid_cols + margin
grid_height = (cell_size + margin) * grid_rows + margin

red = (255, 0, 0)
yellow = (245, 245, 153)

class Map:
    def __init__(self, screen):
        self.screen = screen

    def draw(self):
        for x in range(grid_cols):
            for y in range(grid_rows):
                rect = ((cell_size + margin) * x + margin, (cell_size + margin) * y + margin, cell_size, cell_size)
                pygame.draw.rect(self.screen, yellow, rect, 1)
