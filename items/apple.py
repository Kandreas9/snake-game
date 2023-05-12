from items.item import Item
import pygame

class Apple:
    def __init__(self, x, y, snake):
        self.item = Item(x, y, snake, 'green')
    
    def handleRemoval(self):
        self.item.snake.addSnakePart()
        self.item.snake.points += 1
        self.item.snake.speed += .1

    def removeAppleIfEaten(self):
        return self.item.removeIfEaten(self.handleRemoval) 
        
