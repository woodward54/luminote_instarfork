# General configuration shared globally


#led_pin = 18
# Grid layout
# Currently it's reccomended to make the width (columns) to larger dimention as some functions are not fully aspect ratio agnostic yet
rows = 19
columns = 22
matrixmap = 'custom'  # use 'direct' for direct map

# LED configuration
# RGB/GRB and GPIO pin selection can be done directly in animations.py
# The number of pixels (only needs to be manually configured if using non-standard pixel mapping)
num_pixels = 244

# LED brightness (color accuracy will fade the more this is turned down due to the nature of how these LEDs work)
brightness = .50

# Font for text drawing
font = 'resources/visitor1.ttf'

# For music analysis
music_path = 'music/example.mp3'
