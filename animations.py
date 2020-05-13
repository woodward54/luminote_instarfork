# Functions for organization and animation of NeoPixels
# Most code in this file is only designed to be run natively on a raspberry pi or other control device.
import config
import time
import board
import neopixel
import colorwheels as clr
from collections import namedtuple
from PIL import Image


Color = namedtuple("Color", "R G B")

# from neopixel import *

# Copy settings from config.py
num_pixels = config.num_pixels
rows = config.rows
columns = config.columns

# LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
# LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
# LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
# LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
# LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Choose an open pin connected to the Data In of the NeoPixel pixels, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, config.num_pixels, brightness=config.brightness, auto_write=False, pixel_order=ORDER)
# Create NeoPixel object with appropriate configuration.
# pixels = Adafruit_NeoPixel(config.num_pixels, config.led_pin, LED_FREQ_HZ, LED_DMA, LED_INVERT, config.brightness, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
#pixels.begin()

# TODO: save last frame state globally and only update pixels that need updated to reduce IO needed (and boost performance)

# Pixel mapping for addressing using a 2d array
# Direct matrix map generation
def direct_map():
    pixel_map = [[0 for x in range(columns)] for y in range(rows)]
    pixnum = 0
    for r in range(rows):
        for c in range(columns):
            pixel_map[r][c] = pixnum
            pixnum += 1
    return pixel_map


# Vertical zig zag map generation
def zigzag_map():
    pixel_map = [[0 for x in range(columns)] for y in range(rows)]
    pixnum = 0
    for c in range(columns):
        # top down for even columns (starting from index 0)
        if c % 2 == 0:
            for r in range(rows):
                pixel_map[r][c] = pixnum
                pixnum += 1
        # bottom up for odd columns
        else:
            pixnum += rows - 1
            for r in range(rows):
                pixel_map[r][c] = pixnum
                pixnum -= 1
            pixnum += rows + 1
    return pixel_map

# custom map pattern goes here, denote -1 for pixels that do not exist.
def custom_map():
    pixel_map = [
    [-1,-1,243,242,241,240,239,238,237,236,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,-1,227,228,229,230,231,232,233,234,235,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [-1,226,225,224,223,222,221,220,219,218,217,216,215,-1,-1,-1,-1,214,213,212,211,210],
    [-1,189,190,191,192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,208,209],
    [-1,188,187,186,185,184,183,182,181,180,179,178,177,176,175,174,173,172,171,170,169,168],
    [-1,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167],
    [-1,146,145,144,143,142,141,140,139,138,137,136,135,134,133,132,131,130,129,128,127,126],
    [-1,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125],
    [100,101,102,103,104,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [99,98,97,96,95,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [90,91,92,93,94,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [89,88,87,86,85,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [80,81,82,83,84,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [79,78,77,76,75,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [70,71,72,73,74,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1],
    [69,68,67,66,65,64,63,62,61,60,59,58,57,56,55,54,53,52,-1,-1,-1,-1],
    [34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,-1,-1,-1,-1],
    [33,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,-1,-1,-1,-1],
    [-1,-1,0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,-1,-1,-1,-1]
    ]
    return pixel_map

def check_custom_map_bounds(pixel_map):
    color = (0, 0, 255)
    for r in range(rows):
        for c in range(columns):
            if c != columns-1:
                if pixel_map[r][c+1] == -1:
                    pixels[pixel_map[r][c]] = color
            if c != 0:
                if pixel_map[r][c-1] == -1:
                    pixels[pixel_map[r][c]] = color
            if c == 0 and pixel_map[r][c] != -1:
                pixels[pixel_map[r][c]] = color
            if c == columns-1 and pixel_map[r][c] != -1:
                pixels[pixel_map[r][c]] = color
    pixels.show()


def wheel_cycle(colorwheel=clr.wheel, wait=.005):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            #pixels.setPixelColor(i, colorwheel(pixel_index & 255))
            pixels[i] = colorwheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)


# clears all pixels
def clear_pixels():
    pixels.fill((0, 0, 0))
    pixels.show()


# load and display a frame for set amount of time
def play_frame(pixel_map, source, wait, frame_number=0):
    img = Image.open(source)  # Can be many different formats.
    pic = img.load()
    rgb_img = img.convert('RGB')
    # Writes each pixel to mapped pixels
    for r in range(rows):
        for c in range(columns):
            if not pixel_map[r][c] == -1:
                #pixels.setPixelColor(, pic[c, (r + frame_number * rows)])
                pixels[pixel_map[r][c]] = rgb_img.getpixel((c, (r + frame_number * rows)))
                #print(rgb_img.getpixel((c, (r + frame_number * rows))))
                #time.sleep(.2)
    pixels.show()
    time.sleep(wait)


# draws frame ignoring black pixels, requires pixels.show() to display
def draw_frame(pixel_map, source, frame_number=0):
    img = Image.open(source)  # Can be many different formats.
    # Writes each pixel to mapped pixels
    for r in range(rows):
        for c in range(columns):
            if not (img[c, (r + frame_number * rows)] == (0, 0, 0)):
                if not pixel_map[r][c] == -1:
                    #pixels.setPixelColor(pixel_map[r][c],  pic[c, (r + frame_number * rows)])
                    pixels[pixel_map[r][c]] = pic[c, (r + frame_number * rows)]


# plays through a sequence of frames at given framerate
def play_animation(pixel_map, source, fps=16, num_loops=0):
    image = Image.open(source)
    frametime = 1 / fps
    loop_counter = 0

    for i in range(int(image.height / rows)):
        play_frame(pixel_map, source, frametime, i)

    while loop_counter < num_loops:
        for i in range(int(image.height / rows)):
            play_frame(pixel_map, source, frametime, i)

        loop_counter+=1


# Define functions which animate LEDs in various ways.
def blink_bpm(color, bpm=70):
    while True:
        pixels.fill(color)
        pixels.show()
        time.sleep((bpm/240)/2)
        clear_pixels()
        pixels.show()
        time.sleep((bpm/240)/2)


def colorWipe(color, wait_ms=20):
    clear_pixels()
    """Wipe color across display a pixel at a time."""
    for i in range(config.num_pixels):
        pixels[i] = color
        #pixels.setPixelColor(i, color)
        pixels.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    clear_pixels()
    for j in range(iterations):
        for q in range(3):
            for i in range(0, config.num_pixels-1, 3):
                #pixels.setPixelColor(i+q, color)

                pixels[i+q] = color

                #print("ERR: ", i, " ", q)
            pixels.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, config.num_pixels-1, 3):
                pixels[i+q] = (0, 0, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(wait_ms=10, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    clear_pixels()
    for j in range(256*iterations):
        for i in range(config.num_pixels):
            #pixels.setPixelColor(i, wheel((i+j) & 255))
            pixels[i] = wheel((i+j) & 255)
        pixels.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(wait_ms=10, iterations=1):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    clear_pixels()
    for j in range(256*iterations):
        for i in range(config.num_pixels):
            #pixels.setPixelColor(i, wheel((int(i * 256 / config.num_pixels) + j) & 255))
            pixels[i] = wheel((int(i * 256 / config.num_pixels) + j) & 255)
        pixels.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    clear_pixels()
    for j in range(256):
        for q in range(3):
            for i in range(0, config.num_pixels-1, 3):
                #pixels.setPixelColor(i+q, wheel((i+j) % 255))
                pixels[i+q] = wheel((i+j) % 255)
            pixels.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, config.num_pixels-1, 3):
                #pixels.setPixelColor(i+q, 0)
                pixels[i+q] = (0, 0, 0)
