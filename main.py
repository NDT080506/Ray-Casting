import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *

class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()
        pg.display.set_caption(f"I dont what i am doing")
    
    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = Raycasting(self)
        self.static_sprite = SpriteObject(self)
        self.animation_sprite = AnimatedSprite(self)

    def update(self):
        self.raycasting.update()
        self.player.update()
        self.static_sprite.update()
        self.animation_sprite.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        
    def draw(self):
        #self.screen.fill("black")
        self.object_renderer.draw()
        #self.map.draw()
        #self.player.draw()
    
    def check_event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
    
    def run(self):
        while True:
            self.check_event()
            self.update()
            self.draw()
    

if __name__ == "__main__":
    game = Game()
    game.run()
