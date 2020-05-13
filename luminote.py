import config
import time
import os
from animations import blink_bpm, direct_map, zigzag_map, custom_map, wheel_cycle, clear_pixels, draw_frame, play_frame, play_animation, check_custom_map_bounds, colorWipe, theaterChase, wheel, rainbow, rainbowCycle, theaterChaseRainbow
from gpiozero import ButtonBoard
from threading import Thread, Event
from signal import pause
from collections import namedtuple
from simple_term_menu import TerminalMenu
import concurrent.futures

Color = namedtuple("Color", "R G B")

# LED mapping
if config.matrixmap == 'zigzag':
    print(f'using zigzag map with {config.columns} columns and {config.rows} rows')
    matrix_map = zigzag_map()
elif config.matrixmap == 'direct':
    print(f'using direct map with {config.columns} columns and {config.rows} rows')
    matrix_map = direct_map()
elif config.matrixmap == 'custom':
    print(f'using custom map with {config.columns} columns and {config.rows} rows and {config.num_pixels} number of pixels')
    matrix_map = custom_map()
    # TODO - check that the custom map dimensions match the config dimensions
else:
    print('pixel map not correctly specified in config.py')

# Button mapping
#btns = ButtonBoard(5, 6, 13, 19)

# Flow control
machinestate = 'default'


# Triggered on cue activation
def activate_cue(cue):
    print(f'Cue "{cue}" was activated')


# Triggered on any button press
def on_button_press(buttons):
    # Code to isolate button which caused state change event
    # if lastbuttonspressed < sum(buttons):
    #     return
    buttontotal = 0
    for button in buttons.value:
        buttontotal += button

    if buttontotal == 0:
        return

    if buttons.value[0] == 1:
        activate_cue('test0')
    if buttons.value[1] == 1:
        activate_cue('test1')
    if buttons.value[2] == 1:
        activate_cue('test2')
    if buttons.value[3] == 1:
        activate_cue('test3')






def colorMenu():

    main_menu_cursor = "> "
    main_menu_cursor_style = ("fg_red", "bold")
    main_menu_style = ("bg_red", "fg_yellow")

    edit_menu_title = "  Select a color\n"
    edit_menu_items = ["Red", "Orange", "Yellow", "Lt Green", "Green", "Paste Green", "Teel", "Lt Blue", "Blue", "Purple", "Hot Pink", "Magenta", "White"]
    edit_menu_back = False
    edit_menu = TerminalMenu(edit_menu_items,
                            edit_menu_title,
                            main_menu_cursor,
                            main_menu_cursor_style,
                            main_menu_style)
    
    os.system('clear')
    edit_sel = edit_menu.show()
    
    if edit_sel == 0:
        return Color(255, 0, 0)
    elif edit_sel == 1:
        return Color(255, 128, 0)
    elif edit_sel == 2:
        return Color(255, 255, 0)
    elif edit_sel == 3:
        return Color(128, 255, 0)
    elif edit_sel == 4:
        return Color(0, 255, 0)
    elif edit_sel == 5:
        return Color(0, 255, 128)
    elif edit_sel == 6:
        return Color(0, 255, 255)
    elif edit_sel == 7:
        return Color(0, 128, 255)
    elif edit_sel == 8:
        return Color(0, 0, 255)
    elif edit_sel == 9:
        return Color(127, 0, 255)
    elif edit_sel == 10:
        return Color(255, 0, 255)
    elif edit_sel == 11:
        return Color(255, 0, 127)
    elif edit_sel == 12:
        return Color(255, 255, 255)
        #edit_menu_back = True

#main_menu_exit = False

def main():
    main_menu_title = "LED Guitar Main Menu\n"
    main_menu_items = ["Quit", "Blackout/Clear", "Color Wipe", "Theater Chase", "Rainbow Cycle", "Rainbow Theater", "Fire", "BigOne", "Blink"]
    main_menu_cursor = "> "
    main_menu_cursor_style = ("fg_red", "bold")
    main_menu_style = ("bg_red", "fg_yellow")
    main_menu_exit = False
    

    main_menu = TerminalMenu(menu_entries=main_menu_items,
                             title=main_menu_title,
                             menu_cursor=main_menu_cursor,
                             menu_cursor_style=main_menu_cursor_style,
                             menu_highlight_style=main_menu_style,
                             cycle_cursor=True)

    
    
    while not main_menu_exit:
        os.system('clear')
        main_sel = main_menu.show()

        if main_sel == 0:
            main_menu_exit = True
            print("Quit Selected")
            #time.sleep(5)
            
        elif main_sel == 1:
            print("Clearing...")
            clear_pixels()

        elif main_sel == 2:
            #clear_pixels()
            print("Color Wipe Selected")
            # TODO sub menu to select color
            colorWipe(colorMenu(), 10)
        elif main_sel == 3:
            #clear_pixels()
            print("Theater Chase Selected")
            #tmpColor
            # sub menu to select color
            theaterChase(colorMenu(), 50, 1000)
        elif main_sel == 4:
            #clear_pixels()
            #print("Rainbow Cycle")
            rainbowCycle(1, 1000)
        elif main_sel == 5:
            #clear_pixels()
            #print("Rainbow Cycle")
            theaterChaseRainbow()
        elif main_sel == 6:
            #clear_pixels()
            #print("Rainbow Cycle")
            play_animation(matrix_map, 'img/fire.png', 20, 100)
            #rainbowCycle(10, 1000)
        elif main_sel == 7:
            #clear_pixels()
            #print("Rainbow Cycle")
            #rainbowCycle(10, 1000)
            play_animation(matrix_map, 'img/THEBIGONE_fixed.png', 50, 1000)
        elif main_sel == 8:
            blink_bpm(colorMenu())
        else:
            print('Invalid choice')



# Main
if __name__ == '__main__':
    #print('Instar LED Guitar started\nUse Ctrl+C to exit')
     
    main()
    
    

    # set ButtonBoard callback
    #btns.when_activated = on_button_press

    #pause()
    # while True:
    # check_custom_map_bounds(matrix_map)
    # play_animation(matrix_map, 'img/THEBIGONE_fixed.png', 50, 100
    # play_animation(matrix_map, 'img/THEBIGONE_fixed.png', 70, 5)
    #
    # while True:
    #     print('=============================')
    #     print('')
    #     print ('Color wipe animations.')
    #     #colorWipe(Color(255, 0, 0))  # Red wipe
    #     colorWipe(C--olor(0, 255, 0))  # Blue wipe
    #     #colorWipe(Color(0, 0, 255))  # Green wipe
    #     print ('Theater chase animations.')
    #     theaterChase(Color(127, 127, 127))  # White theater chase
    #     theaterChase(Color(127,   0,   0))  # Red theater chase
    #     theaterChase(Color(  0,   0, 127))  # Blue theater chase
    #     print ('Rainbow')
    #     rainbow()
    #
    #     print ('Rainbow Cycle')
    #     rainbowCycle()
    #
    #     print ('Theater Chase Rainbow')
    #     theaterChaseRainbow()
