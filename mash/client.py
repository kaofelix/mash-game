#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pyglet
from pyglet.window import key
from vec2 import Vec2

class Player(object):
    speed = 75

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

    def move(self, direction, dt):
        self.position = Vec2(self.position) + direction * self.speed * dt

window = pyglet.window.Window(800, 600)
key_state = key.KeyStateHandler()
window.push_handlers(key_state)
player = Player("Name", (150, 150))

@window.event
def on_draw():
    window.clear()
    player.draw()

def update(dt):
    x, y = 0, 0
    if key_state[key.W]:
        y += 1
    if key_state[key.S]:
        y -=1
    if key_state[key.D]:
        x += 1
    if key_state[key.A]:
        x -= 1
    direction = Vec2(x,y).normalize()
    player.move(direction, dt)

def main():
    pyglet.clock.schedule_interval(update, 1.0/60.0)
    pyglet.app.run()

if __name__ == '__main__':
    main()
