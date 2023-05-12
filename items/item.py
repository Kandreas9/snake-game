import pygame

class Item:
    snake = None
    width = 20
    height = 20
    x = None
    y = None

    def __init__(self, x, y, snake, color):
        self.x = x
        self.y = y
        self.snake = snake
        self.color = color
    #
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def removeIfEaten(self, handleRemoval):
        head = self.snake.parts[len(self.snake.parts) - 1]
        if head[0] == self.x and head[1] == self.y:
            handleRemoval()
            return self
        return None
        
