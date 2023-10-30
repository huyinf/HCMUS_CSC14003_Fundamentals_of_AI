import pygame
import math

pygame.init()
PI = math.pi

# Funtionc to read map 
def read_map(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()

    rows, cols = map(int, lines[0].split())
    grid = [[int(cell) for cell in line.strip()] for line in lines[1:rows + 1]]

    pacman_pos = tuple(map(int, lines[rows + 1].split()))

    return rows, cols, grid, pacman_pos

# Load Map
WIDTH, HEIGHT, level, pacman_pos = read_map(r'level_1/map_1.txt')

# Load wall
wall = pygame.transform.scale(pygame.image.load(f'assets/wall9.png'), (20, 20))
space = pygame.transform.scale(pygame.image.load(f'assets/space.jpg'), (20, 20))
# Create the Pygame window with the specified width and height
screen = pygame.display.set_mode((600, 450))
pygame.display.set_caption("Pac-Man")

timer = pygame.time.Clock()
font = pygame.font.SysFont('sans', 20)

color = 'blue'

player_images = []
for i in range(1, 5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (20, 20)))

# Initialize player position and direction
player_x = pacman_pos[0]
player_y = pacman_pos[1]

# Start with the right direction
direction = 0

counter = 0
flicker = False

# R, L, U, D
turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2

# Draw board (surface map)
def draw_board():
    num1 = HEIGHT
    num2 = WIDTH

    for i in range(len(level)):
        for j in range(len(level[i])):

            ''' Draw full food in map'''
            # if level[i][j] == 0:
            #     pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2) * 3, i * num1 + (0.5 * num1) * 2.5), 4)
            
            # Draw food 2
            if level[i][j] == 2 and not flicker: 
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2) * 3.1, i * num1 + (0.5 * num1) * 3.1), 8 )
            
            # Draw wall
            if level[i][j] == 1:
                screen.blit(wall, (j * num2 + (0.5 * num2) * 2, i * num1 + (0.5 * num1) * 2))
                

# Draw player - Pacman
def draw_player():
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
    if direction == 0:
        screen.blit(player_images[counter // 5], (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 5], True, False), (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 90), (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 5], 270), (player_x, player_y))


'''
    Bug check position
'''
# Check position
# def check_position(center_x, center_y):
#     # Calculate the grid position of the player
#     grid_x = int((center_x - (0.5 * WIDTH)) / WIDTH)
#     grid_y = int((center_y - (0.5 * HEIGHT)) / HEIGHT)

#     # Get the current cell value in the grid
#     current_cell = level[grid_y][grid_x]

#     # Initialize the allowed turns list
#     turns_allowed = [False, False, False, False]

#     # Check if the player can turn right
#     if direction != 1 and current_cell != 1 and level[grid_y][grid_x + 1] != 1:
#         turns_allowed[0] = True

#     # Check if the player can turn left
#     if direction != 0 and current_cell != 1 and level[grid_y][grid_x - 1] != 1:
#         turns_allowed[1] = True

#     # Check if the player can turn up
#     if direction != 3 and current_cell != 1 and level[grid_y - 1][grid_x] != 1:
#         turns_allowed[2] = True

#     # Check if the player can turn down
#     if direction != 2 and current_cell != 1 and level[grid_y + 1][grid_x] != 1:
#         turns_allowed[3] = True

#     return turns_allowed

'''
    Bug Move PLayer
'''
# Move Player
# def move_player(play_x, play_y):
#     # Calculate the new player position based on the current direction
#     if direction == 0:
#         new_x = play_x + player_speed
#         new_y = play_y
#     elif direction == 1:
#         new_x = play_x - player_speed
#         new_y = play_y
#     elif direction == 2:
#         new_x = play_x
#         new_y = play_y - player_speed
#     elif direction == 3:
#         new_x = play_x
#         new_y = play_y + player_speed

#     # Calculate the grid position of the new player position
#     grid_x = int((new_x - (0.5 * WIDTH)) / WIDTH)
#     grid_y = int((new_y - (0.5 * HEIGHT)) / HEIGHT)

#     # Check if the new position is valid (not a wall)
#     if direction == 0 and level[grid_y][grid_x + 1] != 1:
#         return new_x, new_y
#     elif direction == 1 and level[grid_y][grid_x - 1] != 1:
#         return new_x, new_y
#     elif direction == 2 and level[grid_y - 1][grid_x] != 1:
#         return new_x, new_y
#     elif direction == 3 and level[grid_y + 1][grid_x] != 1:
#         return new_x, new_y

#     # If the new position is a wall, return the current position
#     return play_x, play_y

fps = 60
run = True

while run:
    timer.tick(fps)
    screen.fill('black')

    if counter < 19:
        counter += 1
        if counter > 3:
            flicker = False
    else:
        counter = 0
        flicker = True

    draw_board()
    draw_player()
    center_x = player_x + 23
    center_y = player_y + 24
    # turns_allowed = check_position(center_x, center_y)

    # player_x, player_y = move_player(player_x, player_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    '''
        Bug phần bên dưới
    '''
    #     if event.type == pygame.KEYDOWN:
    #         if event.key == pygame.K_RIGHT:
    #             direction_command = 0
    #         if event.key == pygame.K_LEFT:
    #             direction_command = 1
    #         if event.key == pygame.K_UP:
    #             direction_command = 2
    #         if event.key == pygame.K_DOWN:
    #             direction_command = 3
        
    #     if event.type == pygame.KEYUP:
    #         if event.key == pygame.K_RIGHT and direction_command == 0:
    #             direction_command = direction
    #         if event.key == pygame.K_LEFT and direction_command == 1:
    #             direction_command = direction
    #         if event.key == pygame.K_UP and direction_command == 2:
    #             direction_command = direction
    #         if event.key == pygame.K_DOWN and direction_command == 3:
    #             direction_command = direction
    
    # for i in range(4):
    #     if direction_command == i and turns_allowed[i]:
    #         direction = i

    # if direction_command == 0 and turns_allowed[0]:
    #     direction = 0
    # if direction_command == 1 and turns_allowed[1]:
    #     direction = 1
    # if direction_command == 2 and turns_allowed[2]:
    #     direction = 2
    # if direction_command == 3 and turns_allowed[3]:
    #     direction = 3

    # if player_x > 650:
    #     player_x = -47
    # elif player_x < -50:
    #     player_x = 600

    pygame.display.flip()

pygame.quit()