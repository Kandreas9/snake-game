import pygame

class Trap:
    snake = None
    width = 20
    height = 20
    color = 'red'
    x = None
    y = None

    def __init__(self, x, y, snake):
        self.x = x
        self.y = y
        self.snake = snake
    #
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def removeTrapIfEaten(self):
        head = self.snake.parts[len(self.snake.parts) - 1]
        if head[0] == self.x and head[1] == self.y:
            self.snake.removeSnakePart()
            self.snake.points -= 1
            self.snake.speed -= .1

            return self
        return None
        
