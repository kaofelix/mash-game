#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyglet

class Player(object):
    def __init__(self, name, position):
        image = pyglet.image.load("../data/blueplayer.png")
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

        self.sprite = pyglet.sprite.Sprite(image)
        self.label = pyglet.text.Label(name,
                                       font_name='Helvetica',
                                       font_size=10,
                                       anchor_x='center')
        self.position = position

    def draw(self):
        self.sprite.draw()
        self.label.draw()

    @property
    def position(self):
        return self.sprite.position

    @position.setter
    def position(self, value):
        x, y = value
        self.sprite.set_position(x, y)
        self.label.x = x
        self.label.y = y + self.sprite.height//2

window = pyglet.window.Window(800, 600)
player = Player("Name", (100, 100))

@window.event
def on_draw():
    window.clear()
    player.draw()

def main():
    pyglet.app.run()

if __name__ == '__main__':
    main()
