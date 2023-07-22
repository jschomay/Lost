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
blue = (153, 153, 255)


class GameMap:

    def __init__(self, screen, starting_index , ending_index):
        self.player_position = self.index_to_position(starting_index)
        self.ending_position = self.index_to_position(ending_index)
        self.screen = screen
        self.visited_coords = set()
        self.visited_coords.add(tuple(self.player_position))

    def draw(self, level = 0):

        if level < 1: return
            
        self.screen.fill((0, 0, 0))
        for x in range(grid_cols):
            for y in range(grid_rows):
                rect = pygame.Rect((cell_size + margin) * x + margin,
                                   (cell_size + margin) * y + margin,
                                   cell_size, cell_size)
                pygame.draw.rect(self.screen, yellow, rect, 1)

        
        player_center = [
            self.player_position[0] * (cell_size + margin) + margin +
            cell_size // 2, self.player_position[1] * (cell_size + margin) +
            margin + cell_size // 2
        ]
        pygame.draw.circle(self.screen, white, player_center, 4)

        if level < 2: return
            
        for coord in self.visited_coords:
            if coord[0] == self.player_position[0 ] and coord[1] == self.player_position[1]: continue
            center = (
                cell_size + margin) * coord[0] + margin + cell_size // 2, (
                    cell_size + margin) * coord[1] + margin + cell_size // 2
            pygame.draw.circle(self.screen, (255, 0, 0), center, 2, 0)

        if level < 3: return
            
        ending_center = [
            self.ending_position[0] * (cell_size + margin) + margin +
            cell_size // 2, self.ending_position[1] * (cell_size + margin) +
            margin + cell_size // 2
        ]
        pygame.draw.circle(self.screen, blue, ending_center, 4)


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

