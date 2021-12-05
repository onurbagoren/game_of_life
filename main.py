import numpy as np
import pygame

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 900
SCREEN = pygame.display.set_mode((900, 900))
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

NUM_COLS = int(WINDOW_WIDTH / 10)
NUM_ROWS = int(WINDOW_HEIGHT / 10)


class Grid:
    """
    Grid class
    """

    def __init__(self, num_rows, num_cols, screen, game_of_life):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.game_of_life = game_of_life
        self.grid = np.zeros((num_rows, num_cols))
        self.tmp_grid = self.grid.copy()
        self.screen = screen
        self.create_grid()
        self.drawGrid()

    def getCell(self, x, y):
        """
        Get the value of a cell
        """
        return self.grid[x][y]

    def setCell(self, x, y, value):
        """
        Set the value of a cell
        """
        self.grid[x][y] = value

    def create_grid(self):
        """
        Create a grid with random values
        """
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if i <= 1:
                    if j > 2 * self.num_cols / 3:
                        self.grid[i][j] = 4
                    elif j > self.num_cols / 3:
                        self.grid[i][j] = 3
                    elif j >= 0:
                        self.grid[i][j] = 2
                else:
                    self.grid[i][j] = 0

    def drawGrid(self):
        """
        Draw a grid on pygame screen
        """
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.grid[i][j] == 0:
                    pygame.draw.rect(SCREEN, WHITE, (j * 10, i * 10, 10, 10))
                elif self.grid[i][j] == 1:
                    pygame.draw.rect(SCREEN, BLACK, (j * 10, i * 10, 10, 10))
                elif self.grid[i][j] == 2:
                    pygame.draw.rect(SCREEN, GREEN, (j * 10, i * 10, 10, 10))
                elif self.grid[i][j] == 3:
                    pygame.draw.rect(SCREEN, YELLOW, (j * 10, i * 10, 10, 10))
                elif self.grid[i][j] == 4:
                    pygame.draw.rect(SCREEN, RED, (j * 10, i * 10, 10, 10))
        self.tmp_grid = self.grid.copy()

    def get_closest_cell(self, x, y):
        """
        Get the closest grid cell to the x y point
        """
        return x // 10, y // 10

    def get_neighbours(self, x, y):
        """
        Get the neighbours of a cell

        Returns:
            neighbours: list of neighbours
            [top_left, top, top_right, left, right, bottom_left, bottom, bottom_right]
        """
        neighbours = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i >= 0 and i < self.num_rows and j >= 0 and j < self.num_cols:
                    if i != x or j != y:
                        if self.grid[i][j] not in [2, 3, 4]:
                            neighbours.append(self.grid[i][j])
        return neighbours

    def draw_cell(self, x, y):
        """
        Draw a cell on pygame screen
        """
        if x > 1:
            if self.grid[x][y] == 0:
                pygame.draw.rect(SCREEN, BLACK, (y * 10, x * 10, 10, 10))
                self.grid[x][y] = 1

    def get_color(self, neighbours):
        """
        Get the color of a cell based on its neighbours
        """
        if neighbours == 3:
            return GREEN
        elif neighbours == 2:
            return YELLOW
        else:
            return RED

    def reset_grid(self):
        """
        Reset the grid to the initial state
        """
        self.create_grid()
        self.drawGrid()

    def start_game_of_life(self):
        """
        Game of life function
        """
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if i > 1:
                    neighbours = self.get_neighbours(i, j)
                    num_occupied = sum(neighbours)
                    if self.grid[i][j] == 1:
                        if num_occupied < 2 or num_occupied > 3:
                            self.tmp_grid[i][j] = 0
                        elif num_occupied >= 2 and num_occupied <= 3:
                            self.tmp_grid[i][j] = 1
                    else:
                        if num_occupied == 3:
                            self.tmp_grid[i][j] = 1
        self.grid = self.tmp_grid.copy()
        self.drawGrid()


if __name__ == "__main__":
    pygame.init()
    grid = Grid(NUM_ROWS, NUM_COLS, SCREEN, False)
    draw = True
    while True:
        # Flip the display
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

        if grid.game_of_life:
            grid.start_game_of_life()
        else:
            pass

        # get mouse click
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            x, y = grid.get_closest_cell(mouse_pos[1], mouse_pos[0])
            if x > 1:
                if draw:
                    grid.draw_cell(x, y)
                else:
                    print(x, y)
            else:
                if y > 2 * grid.num_cols / 3:
                    grid.game_of_life = False
                elif y > grid.num_cols / 3:
                    grid.reset_grid()
                elif y >= 0:
                    grid.game_of_life = True

