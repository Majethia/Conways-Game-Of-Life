import pygame
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (96, 96, 96)


WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600

BOARD = 20

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()
SCREEN.fill(WHITE)


class Node():
    def __init__(self, x, y, dead=True):
        self.x = x
        self.y = y
        self.dead = dead

    def draw(self, SCREEN):
        x = self.x * WINDOW_HEIGHT / BOARD
        y = self.y * WINDOW_HEIGHT / BOARD
        rectangle = pygame.Rect(x, y, WINDOW_HEIGHT / BOARD, WINDOW_HEIGHT / BOARD)
        rectangle1 = pygame.Rect(x+2, y+2, WINDOW_HEIGHT / BOARD - 4, WINDOW_HEIGHT / BOARD - 4)

        pygame.draw.rect(SCREEN, BLACK, rectangle)
        if self.dead == True:
            pygame.draw.rect(SCREEN, WHITE, rectangle1)
        else:
            pygame.draw.rect(SCREEN, GREY, rectangle1)


class Grid():
    def __init__(self, size):
        self.alive = []
        self.size = size
        self.grid = [[[] for _ in range(size)] for _ in range(size)]
        for i in range(size):
            for j in range(size):
                self.grid[i][j] = Node(i, j)

    def find_all_surroundings(self, current: Node):
        sr = []
        if (current.x + 1) < self.size and (current.y + 1) < self.size:
            sr.append(self.grid[current.x + 1][current.y + 1])
        if (current.x + 1) < self.size:
            sr.append(self.grid[current.x + 1][current.y])
        if (current.y + 1) < self.size:
            sr.append(self.grid[current.x][current.y + 1])
        if (current.x - 1) >= 0 and (current.y - 1) >= 0:
            sr.append(self.grid[current.x - 1][current.y - 1])
        if (current.x - 1) >= 0:
            sr.append(self.grid[current.x - 1][current.y])
        if (current.y - 1) >= 0:
            sr.append(self.grid[current.x][current.y - 1])
        if (current.x - 1) >= 0 and (current.y + 1) < self.size:
            sr.append(self.grid[current.x - 1][current.y + 1])
        if (current.y - 1) >= 0 and (current.x + 1) < self.size:
            sr.append(self.grid[current.x + 1][current.y - 1]) 
        return sr
    
    def find_alive_surr(self, current: Node):
        sr = self.find_all_surroundings(current)
        res_sr = []
        for i in sr:
            if i.dead == True:
                pass
            else:
                res_sr.append(i)
        return len(res_sr)
    
    def __str__(self) -> str:
        res = ''
        for i in range(self.size):
            for j in range(self.size):
                res += f"{self.grid[i][j].x}, {self.grid[i][j].y}, {self.grid[i][j].dead} |"
        return res

def main():
    grid = Grid(BOARD)
    run = True
    select_mode = False
    erase_mode = False
    while run:
        for i in range(BOARD):
            for j in range(BOARD):
                grid.grid[i][j].draw(SCREEN)
        pygame.display.update()      

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    run = False

            if select_mode:
                pos = pygame.mouse.get_pos()
                x, y = pos[0]// (WINDOW_HEIGHT/BOARD), pos[1]// (WINDOW_HEIGHT/BOARD)
                x = int(x)
                y = int(y)
                grid.grid[x][y].dead = False
                grid.alive.append(grid.grid[x][y])
            
            if erase_mode:
                pos = pygame.mouse.get_pos()
                x, y = pos[0]// (WINDOW_HEIGHT/BOARD), pos[1]// (WINDOW_HEIGHT/BOARD)
                x = int(x)
                y = int(y)
                grid.grid[x][y].dead = True
                grid.alive.remove(grid.grid[x][y])

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    select_mode = True
                if event.button == 3:
                    erase_mode = True
                
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    select_mode = False
                if event.button == 3:
                    erase_mode = False
        
    sim = True
    pause = False
    while sim:
        CLOCK.tick(5)
        
        for i in range(BOARD):
            for j in range(BOARD):
                grid.grid[i][j].draw(SCREEN)
        pygame.display.update() 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.quit()
                    sys.exit()
                
                elif event.key == pygame.K_p:
                    pause = not pause

                elif event.key == pygame.K_r:
                    main()
                    pygame.quit()
                    sys.exit()
        
        if pause:
            continue
                
        active_nodes = set()
        kills = set()
        births = set()
        
        for i in grid.alive:
            active_nodes = active_nodes|set(grid.find_all_surroundings(i))
            
        for i in active_nodes:
            n = grid.find_alive_surr(i)
            if not i.dead and n not in [2, 3]:
                kills.add(i)
            if n == 3:
                births.add(i)

        for i in kills:
            i.dead = True
            grid.alive.remove(i)
        
        for i in births:
            i.dead = False
            grid.alive.append(i)

main()

