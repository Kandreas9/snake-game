import pygame
import random

from snake import Snake
from items.apple import Apple
from items.trap import Trap

#===Pygame Setup===
pygame.init()
screen_width = 300
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0
frame_count = 0
frame_rate = 60
font = pygame.font.SysFont('arial', 20)

#===Initialise Classes===
snake = Snake(screen)
apples = []
traps = []

BLACK = (0, 0, 0)

#===Helper Functions===

#===Draws the grid in the background===
def drawGrid():
    GRAY = (105, 105, 105)
    
    blockSize = 20 #Set the size of the grid block
    for x in range(0, screen_width, blockSize):
        for y in range(0, screen_height, blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(screen, GRAY, rect, 1)

#===Generate apple only if the spot is empty===
def generateApple():
    xTiles = int(screen_width / 20)
    yTiles = int(screen_height / 20)
    xCoord = random.randrange(xTiles) * 20
    yCoord = random.randrange(yTiles) * 20
    
    for part in snake.parts:
        if part[0] == xCoord and part[1] == yCoord:
            return generateApple()

    return Apple(xCoord, yCoord, snake)

#===Generate trap only if the spot is empty===
def generateTrap():
    xTiles = int(screen_width / 20)
    yTiles = int(screen_height / 20)
    xCoord = random.randrange(xTiles) * 20
    yCoord = random.randrange(yTiles) * 20
    
    for part in snake.parts:
        if part[0] == xCoord and part[1] == yCoord:
            return generateTrap()

    return Trap(xCoord, yCoord, snake)

#===Draw text on screen for menu===
def draw_start_menu():
    title = font.render('Snake Game', True, (255, 255, 255), BLACK)
    start_button = font.render('Enter - Start', True, (255, 255, 255), BLACK)
    screen.blit(title, ((screen_width/4) * 3 - title.get_width()/2, screen_height/2 - title.get_height()/2))
    screen.blit(start_button, ((screen_width/4) * 3 - start_button.get_width()/2, screen_height/2 + start_button.get_height()/2))

#===Draw text on screen for game over screen===
def draw_game_over_screen():
    title = font.render('Game Over', True, (255, 255, 255), BLACK)
    restart_button = font.render('R - Restart', True, (255, 255, 255), BLACK)
    quit_button = font.render('Q - Quit', True, (255, 255, 255), BLACK)
    screen.blit(title, ((screen_width/4) * 3 - title.get_width()/2, screen_height/2 - title.get_height()/3))
    screen.blit(restart_button, ((screen_width/4) * 3 - restart_button.get_width()/2, screen_height/1.9 + restart_button.get_height()))
    screen.blit(quit_button, ((screen_width/4) * 3 - quit_button.get_width()/2, screen_height/2 + quit_button.get_height()/2))

#===Draw Timer===
def draw_timer():
    global frame_count
    global frame_rate
    
    # Calculate total seconds
    total_seconds = frame_count // frame_rate

    # Divide by 60 to get total minutes
    minutes = total_seconds // 60
 
    # Use modulus (remainder) to get seconds
    seconds = total_seconds % 60

    # Use python string formatting to format in leading zeros
    output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)

    # Blit to the screen
    text = font.render(output_string, True, (255, 255, 255))
    screen.blit(text, [20, 20])

    frame_count += 1

#===Draw number of points===
def draw_points():
    text = font.render(str(snake.points), True, (255, 255, 255))
    screen.blit(text, [screen_width - 20,  20])

#===Game Loop===
game_state = 'start_menu'
game_over = False
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if game_state == "start_menu":
        screen.fill("black")
        snake.draw(screen, False)
        draw_start_menu()
        if keys[pygame.K_RETURN]:
            game_state = "game"
            game_over = False
    elif game_state == "game_over":
        screen.fill("black")
        draw_points()
        snake.draw(screen, False)
        draw_game_over_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_state = "start_menu"
            snake.reset(screen)
            frame_count = 0
            apples = []
            traps = []
        if keys[pygame.K_q]:
            pygame.quit()
            quit()

    if game_state == "game":
        screen.fill("black")
        drawGrid()
        snake.draw(screen, True)
        coliding = snake.isSnakeColidingItself()
        screenColiding = snake.isSnakeColidingScreen(screen_width, screen_height)

        #===If hit wall or self DIE===
        if screenColiding or coliding:
            game_state = 'game_over'
            game_over = True
            continue

        #===If no apples, generate and if score more than 5 generate 2
        if len(apples) == 0 and snake.points < 5:
            apples.append(generateApple())
        elif snake.points >= 5 and len(apples) == 0:
            apples.append(generateApple())
            apples.append(generateApple())
            traps = [generateTrap()]
        else:
            for trap in traps:
                trap.item.draw(screen)
                if trap.removeTrapIfEaten() is not None:
                    traps.remove(trap)
            for apple in apples:
                apple.item.draw(screen)
                if apple.removeAppleIfEaten() is not None:
                    apples.remove(apple)


        #===Snake controls===
        if keys[pygame.K_UP]:
            snake.changeDirection('up')
        if keys[pygame.K_DOWN]:
            snake.changeDirection('down')
        if keys[pygame.K_RIGHT]:
            snake.changeDirection('right')
        if keys[pygame.K_LEFT]:
            snake.changeDirection('left')
    
        draw_timer()
        draw_points()

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(frame_rate) / 1000

#===When alls done quit===
pygame.quit()
