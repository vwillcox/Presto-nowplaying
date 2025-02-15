from spotify_web_api import (
    spotify_client,
    SpotifyWebApiError,
)

import datetime
import time
import machine
import urequests

from picovector import ANTIALIAS_BEST, PicoVector, Polygon, Transform
from presto import Presto
from touch import Button
import jpegdec

presto = Presto(ambient_light=True, full_res=True)
display = presto.display
connection_successful = presto.connect()
spotify = spotify_client()

WIDTH, HEIGHT = display.get_bounds()
CX, CY = WIDTH // 2, HEIGHT // 2

# Colors
WHITE, RED, GREEN, BLACK = (display.create_pen(r, g, b) for r, g, b in [(255, 255, 255), (230, 60, 45), (9, 185, 120), (0, 0, 0)])

# Touch elements
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
skip_button = Button(WIDTH - CX, HEIGHT - 50, CX -2, 49)

# Button Polygons
def create_button_polygon(bounds, radius):
    polygon = Polygon()
    polygon.rectangle(*bounds, (radius, radius, radius, radius))
    return polygon

start = create_button_polygon(start_button.bounds, 5)
skip = create_button_polygon(skip_button.bounds, 5)
outline = Polygon()
outline.rectangle(5, 20, WIDTH - 10, HEIGHT - 100, (5, 5, 5, 5),2) # Updated to specify outline parameter


j = jpegdec.JPEG(display)

def truncate_string(input_string, max_length=36):
    return input_string[:max_length] if len(input_string) > max_length else input_string

while True:
    try:
        touch.poll()
        current_track = spotify.get_currently_playing()
        is_playing = current_track['is_playing']
        
        display.set_pen(BLACK)
        display.clear()
        display.set_pen(GREEN)
        vector.draw(start)
        display.set_pen(RED)
        vector.draw(skip)
        display.set_pen(WHITE)
        vector.draw(outline)
        vector.set_font_size(32)
        
        if is_playing:
            artist_name = current_track['item']['artists'][0]['name']
            x, y, w, h = vector.measure_text(artist_name, x=0, y=0, angle=None)
            text_x = int(CX - (w // 2))
            text_y = int(CY + (h // 2))
            text_x_offset = text_x + 2
            text_y_offset = text_y + 2
            vector.text(artist_name, text_x, 50)
            display_track = truncate_string(current_track['item']['name'])
            x, y, w, h = vector.measure_text(display_track, x=0, y=0, angle=None)
            text_x = int(CX - (w // 2))
            text_y = int(CY + (h // 2))
            text_x_offset = text_x + 2
            text_y_offset = text_y + 2
            artworks = [image['url'] for image in current_track['item']['album']['images']]
            response2 = urequests.get(artworks[1])
            image_data = response2.content
            j.open_file(image_data)
            x_center = (480 - 300) // 2
            y_center = (480 - 300) // 2
            vector.text(display_track, text_x, 80)
            vector.text("Pause", start_button.bounds[0] + 83, start_button.bounds[1] + 33)
            vector.text("Skip", skip_button.bounds[0] + 83, skip_button.bounds[1] + 33)
            j.decode(x_center, y_center, jpegdec.JPEG_SCALE_FULL, dither=True)

            if skip_button.is_pressed():
                spotify.skip()

            if start_button.is_pressed():
                spotify.pause()
        else:
            vector.text("Play", start_button.bounds[0] + 83, start_button.bounds[1] + 33)
            if start_button.is_pressed():
                spotify.play()

        presto.update()
    except Exception as e:
        print(e)


