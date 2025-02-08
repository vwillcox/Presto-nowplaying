from spotify_web_api import (
    spotify_client,
    SpotifyWebApiError,
)

import datetime
import time

from picovector import ANTIALIAS_BEST, PicoVector, Polygon, Transform
from presto import Presto
from touch import Button

presto = Presto(ambient_light=True, full_res=True)
display = presto.display
connection_successful = presto.connect()
spotify = spotify_client()

WIDTH, HEIGHT = display.get_bounds()

CX = WIDTH // 2
CY = HEIGHT // 2

# Couple of colours for use later
WHITE = display.create_pen(255, 255, 255)
RED = display.create_pen(230, 60, 45)
GREEN = display.create_pen(9, 185, 120)
BLACK = display.create_pen(0, 0, 0)

# We'll need this for the touch element of the screen
touch = presto.touch

# Pico Vector
vector = PicoVector(display)
vector.set_antialiasing(ANTIALIAS_BEST)
t = Transform()

vector.set_font("Roboto-Medium.af", 54)
vector.set_font_letter_spacing(100)
vector.set_font_word_spacing(100)
vector.set_transform(t)

# Touch buttons
start_button = Button(1, HEIGHT - 50, CX - 2, 49)

start = Polygon()
start.rectangle(*start_button.bounds, (5, 5, 5, 5))

outline = Polygon()
outline.rectangle(5, 20, WIDTH - 10, HEIGHT - 100, (5, 5, 5, 5), 2)

def truncate_string(input_string):
    if len(input_string) > 38:
        return input_string[:38]
    else:
        return(input_string)
    return 

while True:
    try:
        now_playing = spotify.get_currently_playing
        current_track = now_playing()
        is_playing = current_track['is_playing']
        display.set_pen(BLACK)
        display.clear()    
        display.set_pen(GREEN)
        vector.draw(start)
        display.set_pen(WHITE)
        vector.draw(outline)
        vector.set_font_size(32)
    #vector.text("Pause", start_button.bounds[0] +83, start_button.bounds[1] + 33)
        if is_playing is True:
            vector.text(current_track['item']['artists'][0]['name'], 10, 50)
            cur_track = (current_track['item']['name'])
            display_track = truncate_string(str(cur_track))
            vector.text(str(display_track), 10, 80)
            vector.text("Pause", start_button.bounds[0] +83, start_button.bounds[1] + 33)
            if start_button.is_pressed():
                spotify.pause()
        else:
            vector.text("Play", start_button.bounds[0] +83, start_button.bounds[1] + 33)
            if start_button.is_pressed():
                spotify.play()
        presto.update()
    except Exception as e:
        print(e)
    


