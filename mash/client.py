#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import pyglet
from pyglet.window import key
from vec2 import Vec2

from twisted.internet.protocol import DatagramProtocol
import pygletreactor
pygletreactor.install()
from twisted.internet import reactor

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

player_map = {}

class MulticastServerUDP(DatagramProtocol):
    def startProtocol(self):
        print 'Started Listening'
        # Join a specific multicast group, which is the IP we will respond to
        self.transport.joinGroup('224.0.0.1')

    def send_pos(self, player):
        self.transport.write("XXX:%s:%s:%s:%s:%s"%(localname,'p',
                                               player.position[0], player.position[1],
                                               player.sprite.rotation), ('224.0.0.1',8005))

    def datagramReceived(self, datagram, address):
        global player_map
        if not datagram.startswith('XXX'):
            pass
        _, source, message, value1, value2, value3 = datagram.split(':')
        if source == localname:
            pass
        else:
            if not source in player_map:
                player_map[source] = Player(source, (float(value1), float(value2)))
            p = player_map[source]
            p.position = (float(value1), float(value2))
            p.sprite.rotation = float(value3)

server = MulticastServerUDP()
window = pyglet.window.Window(800, 600)
cursor = window.get_system_mouse_cursor(window.CURSOR_CROSSHAIR)
window.set_mouse_cursor(cursor)
key_state = key.KeyStateHandler()
window.push_handlers(key_state)

localname = sys.argv[1]
player = Player(localname, (150, 150))
mouse_pos = (0,0)


@window.event
def on_draw():
    window.clear()
    player.draw()
    for p in player_map.values():
        p.draw()


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
    server.send_pos(player)

def main():
    pyglet.clock.schedule_interval(update, 1.0/30.0)
    reactor.listenMulticast(8005, server, listenMultiple=True)
    reactor.run(call_interval=1/30.)

if __name__ == '__main__':
    main()
