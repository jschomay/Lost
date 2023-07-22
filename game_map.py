import pygame

grid_cols = 4
grid_rows = 4
cell_size = 15
margin = 0
grid_width = (cell_size + margin) * grid_cols + margin
grid_height = (cell_size + margin) * grid_rows + margin

red = (255, 0, 0)
yellow = (245, 245, 153)
white = (255, 255, 255)


class GameMap:

    def __init__(self, screen, starting_index = 0):
        starting_cell = self.index_to_position(starting_index)
        self.screen = screen
        self.player_position = starting_cell
        self.visited_coords = set()
        self.visited_coords.add(tuple(self.player_position))

    def draw(self):
        self.screen.fill((0, 0, 0))
        for x in range(grid_cols):
            for y in range(grid_rows):
                rect = pygame.Rect((cell_size + margin) * x + margin,
                                   (cell_size + margin) * y + margin,
                                   cell_size, cell_size)
                pygame.draw.rect(self.screen, yellow, rect, 1)

        for coord in self.visited_coords:
            center = (
                cell_size + margin) * coord[0] + margin + cell_size // 2, (
                    cell_size + margin) * coord[1] + margin + cell_size // 2
            pygame.draw.circle(self.screen, (255, 0, 0), center, 2, 0)

        player_center = [
            self.player_position[0] * (cell_size + margin) + margin +
            cell_size // 2, self.player_position[1] * (cell_size + margin) +
            margin + cell_size // 2
        ]

        pygame.draw.circle(self.screen, white, player_center, 4)

    def update(self, direction):
        if direction == 'up':
            self.player_position[1] -= 1
        elif direction == 'down':
            self.player_position[1] += 1
        elif direction == 'left':
            self.player_position[0] -= 1
        elif direction == 'right':
            self.player_position[0] += 1

        self.player_position[0] = self.player_position[0] % grid_cols
        self.player_position[1] = self.player_position[1] % grid_rows
        self.visited_coords.add(tuple(self.player_position))

    def positon_to_index(self):
        return self.player_position[0] + self.player_position[1] * grid_cols
    
    def index_to_position(self, index):
        return [index % grid_cols, index // grid_cols]

