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

    def look_at(self, other_pos):
        v = (other_pos[0] - self.position[0], other_pos[1] - self.position[1])
        self.sprite.rotation = Vec2(*v).angle()

window = pyglet.window.Window(800, 600)
key_state = key.KeyStateHandler()
window.push_handlers(key_state)
player = Player("Name", (150, 150))
mouse_pos = (0,0)


@window.event
def on_draw():
    window.clear()
    player.draw()


@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_pos
    mouse_pos= (x, y)

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
    player.look_at(mouse_pos)

def main():
    pyglet.clock.schedule_interval(update, 1.0/60.0)
    pyglet.app.run()

if __name__ == '__main__':
    main()
