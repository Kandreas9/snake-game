from items.item import Item
import pygame

class Trap:
    def __init__(self, x, y, snake):
        self.item = Item(x, y, snake, 'red')
    
    def handleRemoval(self):
        self.item.snake.removeSnakePart()
        self.item.snake.points -= 1
        self.item.snake.speed -= .1


    def removeTrapIfEaten(self):
        return self.item.removeIfEaten(self.handleRemoval) 
        
