from spotify_web_api import (
    spotify_client,
    SpotifyWebApiError,
)

import time
import machine
##import st7789
from presto import Presto
from touch import Button

#Connect to Spotify using the library
presto = Presto(ambient_light=True)
display = presto.display
touch = presto.touch

WIDTH, HEIGHT = display.get_bounds()

#connect to WIFI using secrets.py
connection_successful = presto.connect()
print(connection_successful)
spotify = spotify_client()

WIDTH, HEIGHT = display.get_bounds()
BLUE = display.create_pen(28, 181, 202)
WHITE = display.create_pen(255, 255, 255)

RED = display.create_pen(230, 60, 45)
ORANGE = display.create_pen(245, 165, 4)
GREEN = display.create_pen(9, 185, 120)
PINK = display.create_pen(250, 125, 180)
PURPLE = display.create_pen(118, 95, 210)
BLACK = display.create_pen(0, 0, 0)

button_1 = Button(0, HEIGHT-50, 100, 50)

pen = display.create_pen_hsv(1.0, 1.0, 1.0)

display.set_pen(BLACK)
display.clear()
presto.update()

while True:
    touch.poll()
    now_playing = spotify.get_currently_playing
    current_track = now_playing()
    is_playing = current_track['is_playing']
    if is_playing is True:
        display.set_pen(BLUE)
        display.clear()
        display.set_pen(WHITE)
        display.text(current_track['item']['artists'][0]['name'], 8, 10, WIDTH, 4)
        display.text(current_track['item']['name'], 10, 85, WIDTH, 4)
        if button_1.is_pressed():
            display.set_pen(RED)
            print("pausing")
            #display.text("Pressed", 10, HEIGHT-20, 100, 2)
            spotify.pause()
            #time.sleep(0.05)
            #while button_1.is_pressed():
            #    touch.poll()
        else:
            display.set_pen(GREEN)
        display.rectangle(*button_1.bounds)
    else:
        #display.set_pen(BLACK)
        if button_1.is_pressed():
            print("playing")
            spotify.play()
    presto.update()
    time.sleep(0.05)
