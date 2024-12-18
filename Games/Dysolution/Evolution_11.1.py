#######################################################################################################################################################
##
## DYSOLUTION
##
#######################################################################################################################################################

#######################################################################################################################################################
# Summaries
""" Plot
    ----
    
    1:     The player is stuck in a dungeon they assume is underground.
    2:     There is one customizable safe floor to call home.
    3:     They are free to explore and scavenge for items and materials.
    4:     They can seek serenity, strength, or evolution.
    4.1:   SERENITY: The home is a haven of collection and creativity.
    4.1.1: It may be expanded and populated by friendly creatures.
    4.2    STRENGTH: Low floors yield high stats and strong items.
    4.2.1: There is no end to the depths.
    4.3:   EVOLUTION: Special events may alter the player.
    4.3.1: The effects may be beneficial, damaging, or superficial.
    5.     ENDGAME: There is a locked room somewhere in the dungeon.
    6.     It is only unlocked by sacrificing the player's life.
    6.1:   SERENITY: Without preparation, their life is over.
    6.2:   STRENGTH: Sufficient equipment may revive the player.
    6.3:   EVOLUTION: The player may construct a clone to sacrifice. """

""" Save Files
    ----------
    
    data_dungeon:   floor layout of previous dungeon, including (?) items and stairs
    container:      
    example:        

    data_home:      floor layout of player's home, including items and stairs
    container:      ??? may be unused
    example:        

    data_inventory: player's inventory, including what is equipped
    container:      inventory = [<__main__.Object object at ...>, <__main__.Object object at ..., ...]
    example:        {0: {'category': 'weapons', ...}, 1: {'category': 'hair', ...}}

    data_objects:   house data
    container:      data_objects_1 = [<__main__.Object object at ...>, <__main__.Object object at ...>, ...] 
    example:        {0: {'category': 'potions', ...}, 1: {'category': 'scrolls', ...}, ...}

    data_player:    player stats
    container:      [player] = [<__main__.Object object at ...>]
    example:        {0: {'category': 'player', 'x': 480, 'y': 480, ...}} """

""" Organization of code
    --------------------
    
    Startup and menus
    -----------------

    New game
    --------

    Continue game
    -------------
    
    Play game
    ---------
    
    Data/audio management
    ---------------------
    
    Audio management
    ----------------
    
    Environment management
    ----------------------
    
    Utilities
    ---------
    
    Classes
    -------
    
    WIP
    --- """

#######################################################################################################################################################
# Imports
## Game mechanics
import pygame
from pygame.locals import *
import random
import math
import textwrap

## File saving
import pickle
import os
import shutil

## Debugging
import time
import sys
import inspect

# Aesthetics
from PIL import Image, ImageFilter

#######################################################################################################################################################
#######################################################################################################################################################
# Global values
## Pygame parameters
screen_width      = 640
screen_height     = 480

tile_width        = 32
tile_height       = 32

map_width         = 640 * 2
map_height        = 480 * 2

tile_map_width    = int(map_width/tile_width)
tile_map_height   = int(map_height/tile_height)

room_max_size     = 10
room_min_size     = 4
max_rooms         = 3

## Player parameters
heal_amount       = 4
lightning_damage  = 20
lightning_range   = 5 * tile_width
confuse_range     = 8 * tile_width
confuse_num_turns = 10
fireball_radius   = 3 * tile_width
fireball_damage   = 12

level_up_base     = 200
level_up_factor   = 150

torch_radius      = 10

## GUI
message_width     = int(screen_width / 10)
message_height    = 3

## Color names
black             = pygame.color.THECOLORS["black"]
gray              = pygame.color.THECOLORS["gray90"]
white             = pygame.color.THECOLORS["white"]
red               = pygame.color.THECOLORS["orangered3"]
green             = pygame.color.THECOLORS["palegreen4"]
blue              = pygame.color.THECOLORS["blue"]
yellow            = pygame.color.THECOLORS["yellow"]
orange            = pygame.color.THECOLORS["orange"]
violet            = pygame.color.THECOLORS["violet"]
light_cyan        = pygame.color.THECOLORS["lightcyan"]
light_green       = pygame.color.THECOLORS["lightgreen"]
light_blue        = pygame.color.THECOLORS["lightblue"]
light_yellow      = pygame.color.THECOLORS["lightyellow"]

## File saving
# Data/File_{load_saves[0][10]}

## Other
message_log_toggle      = True
home_map                = []
home_object_positions   = []
objects                 = []
inventory_cache         = []
data_objects_1          = []
step_counter            = [False, 0, False, 0]
startup                 = True
file_set                = ['', '', '']
super_dig               = False
idle_animation_counter  = [0]
key_cache = K_DOWN
category_order = ["apparel", "weapons", "hair"]
hair_list, skin_list, handedness_list = ['null', 'hair'], ['player'], ['left', 'right']
hair_index, skin_index, handedness_index = 0, 0, 0
new_game_index = 0
debug = True
movement_speed_toggle, movement_speed_cache, toggle_list = 0, 1, ['Default', 'Fast']
last_press_time, cooldown_time = 0, 0.5
startup_toggle = True

## Quests
current_tasks = {'main': ['Finish the game.'],
                 'side': ['Try the beta.']}
quest_menu_index = 0

## Controls
key_0      = [K_0, K_KP0, K_ESCAPE] # back
key_1      = [K_1, K_KP1]           # stats
key_2      = [K_2, K_KP2]           # inventory (equip)
key_3      = [K_3, K_KP3]           # inventory (drop)
key_4      = [K_4, K_KP4]           # quests
key_5      = [K_5, K_KP5]           # movement speed
key_6      = [K_6, K_KP6]           # screenshot
key_UP     = [K_UP, K_w]            # movement (up)
key_DOWN   = [K_DOWN, K_s]          # movement (down)
key_LEFT   = [K_LEFT, K_a]          # movement (left)
key_RIGHT  = [K_RIGHT, K_d]         # movement (right)
key_RETURN = [K_RETURN]             # activate
key_SLASH  = [K_SLASH]              # messages

#######################################################################################################################################################
# Startup and menus
def __STARTUP_AND_MENUS__():
    pass

def main():
    """ Initializes pygame, calls initialize_images() to load tileset, ???, and opens the main menu.
        Called at startup. """

    global screen, font, blank_surface, impact_image, impact_image_pos, impact
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height),)
    pygame.display.set_caption("Evolution") # Sets game title
    font = pygame.font.SysFont('segoeuisymbol', 16, bold=True)

    # Load images
    initialize_images()
    
    # ??? Used in combat
    blank_surface = pygame.Surface((tile_width, tile_height)).convert()
    blank_surface.set_colorkey(blank_surface.get_at((0,0)))
    impact_image = get_impact_image()
    impact_image_pos = [0,0]
    impact = False
    
    main_menu() # Opens the main menu

def initialize_images():
    """ IMPORTANT. Loads images from png file and sorts them in a global dictionary. 
    
        The tileset (tileset.png) is organized in rows, with each row being a category identified below
        by the categories list. This function breaks the tileset into individual tiles and adds each tile
        to its respective category in a global dictionary for later use.
        
        image_dict:        mutable dictionary sorted by category
        image_dict_cache:  less mutable than image_dict """

    global image_dict, image_dict_cache
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    # -------------------------------------- INIT --------------------------------------
    # Initialize data containers
    categories = ['armor',
                  'clothes',
                  'dagger',
                  'blood dagger',
                  'decor',
                  'floors',
                  'hair',
                  'monsters',
                  'player',
                  'player black',
                  'player cyborg',
                  'potions',
                  'scrolls',
                  'shield',
                  'shovel',
                  'super shovel',
                  'stairs',
                  'sword',
                  'blood sword',
                  'walls']
    image_dict       = {category: [] for category in categories}
    image_dict_cache = {category: [] for category in categories}

    rogue_tiles = pygame.image.load('Data/tileset.png').convert_alpha()
    rows        = rogue_tiles.get_height() // tile_height
    columns     = rogue_tiles.get_width() // tile_width
    
    # -------------------------------------- APPLY --------------------------------------
    # Sort images and import as subsurfaces
    for row in range(rows):
        row_images, row_images_cache = [], []
        for col in range(columns):
            x           = col * tile_width
            y           = row * tile_height
            image       = rogue_tiles.subsurface(x, y, tile_width, tile_height).convert_alpha()
            image_cache = rogue_tiles.subsurface(x, y, tile_width, tile_height).convert_alpha()
            row_images.append(image)
            row_images_cache.append(image_cache)
        image_dict[categories[row]] = row_images
        image_dict_cache[categories[row]] = row_images_cache
    image_dict['null'] = image_dict['scrolls'][3:8]
    image_dict_cache['null'] = image_dict_cache['scrolls'][3:8]

def main_menu():
    """ Manages the menu. Handles player input. Only active when the main menu is open.
        Called by main(), file_menu(), and character_creation(). Indirectly called by play_game(). """
    
    global startup, load_saves, new_game_index, game_title, startup_toggle
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    # -------------------------------------- INIT --------------------------------------
    # Initialize time and music
    clock = pygame.time.Clock()
    audio_control(new_track=menu_music)
    
    # Load background image
    background_image = pygame.image.load("Data/image_main.png").convert()
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))  # Scale to fit the screen

    # Initialize title
    title_font = pygame.font.SysFont('segoeuisymbol', 40, bold=True)
    game_title = title_font.render("EVOLUTION", True, green)  # Sets game title
    game_title_pos = (int((screen_width - game_title.get_width())/2), 85)
    
    # Initialize cursor
    cursor_img = pygame.Surface((16, 16)).convert()
    cursor_img.set_colorkey(cursor_img.get_at((0, 0)))
    pygame.draw.polygon(cursor_img, green, [(0, 0), (16, 8), (0, 16)], 0)
    cursor_img_pos = [50, 304]
    
    # Initialize menu options
    menu_choices = ["NEW GAME", "LOAD", "SAVE", "CONTROLS", "QUIT"]
    menu_choices_surfaces = []  # To store rendered text surfaces
    for i in range(len(menu_choices)):
        if i == 0:
            color = green
        elif i == len(menu_choices) - 1:
            color = red
        else:
            color = gray
        menu_choices_surfaces.append(font.render(menu_choices[i], True, color))
    
    choice, choices_length = 0, len(menu_choices) - 1

    if startup_toggle:
        
        # Initialize alpha for fade effect
        alpha = 0  # Starting alpha value for fade-in
        fade_speed = 5  # Speed of fading in

        # -------------------------------------- FADE IN --------------------------------------
        # Fade-in loop
        fade_surface = pygame.Surface((screen_width, screen_height))
        fade_surface.fill(black)
        
        while alpha < 255:
            clock.tick(30)
            fade_surface.set_alpha(255 - alpha)  # Adjust alpha to create the fade-in effect
            
            # Set menu background to the custom image
            screen.blit(background_image, (0, 0))

            # Draw the menu elements during the fade
            y = 300
            for menu_choice_surface in menu_choices_surfaces:
                screen.blit(menu_choice_surface, (80, y))
                y += 24
            screen.blit(game_title, game_title_pos)
            screen.blit(cursor_img, cursor_img_pos)

            # Apply the fade effect
            screen.blit(fade_surface, (0, 0))
            
            pygame.display.flip()
            
            # Increase alpha for the next frame
            alpha += fade_speed
            
        startup_toggle = False

    else:
        # Set menu background to the custom image
        screen.blit(background_image, (0, 0))

        # Draw the menu elements during the fade
        y = 300
        for menu_choice_surface in menu_choices_surfaces:
            screen.blit(menu_choice_surface, (80, y))
            y += 24
        screen.blit(game_title, game_title_pos)
        screen.blit(cursor_img, cursor_img_pos)

        pygame.display.flip()

    # -------------------------------------- MENU --------------------------------------
    # Allow player to select menu option
    while True:
        clock.tick(30)

        # Called when the user inputs a command
        for event in pygame.event.get():

            if event.type == KEYDOWN:
            
                # >>RESUME<<
                if event.key in key_0:
                    play_game()
                
                # >>SELECT MENU ITEM<<
                elif event.key in key_UP:
                    cursor_img_pos[1] -= 24
                    choice -= 1
                    if choice < 0:
                        choice = choices_length
                        cursor_img_pos[1] = 304 + (len(menu_choices) - 1) * 24
                elif event.key in key_DOWN:
                    cursor_img_pos[1] += 24
                    choice += 1
                    if choice > choices_length:
                        choice = 0
                        cursor_img_pos[1] = 304
                
                elif event.key in key_RETURN:

                    # >>NEW GAME<<
                    if choice == 0:
                        new_game_index = 0  # prevents returning to character creation menu after initialization
                        character_creation()
                    
                    # >>LOAD<<
                    if choice == 1:  
                        file_menu("Load Character")
                        if startup:
                            new_game(True)
                            startup = False
                        new_game(False)
                        play_game()
                    
                    # >>SAVE<<
                    if (choice == 2) and (game_state == 'playing'):
                    
                        # Choose a save file
                        file_menu("Save Character")

                        # Save stats and inventory
                        save_objects_to_file(load_saves[0], data_source=[player])
                        save_objects_to_file(load_saves[4], data_source=inventory)
                        
                        # Save image for loading screen
                        screenshot(cache=True, save=True, blur=True)
                        
                        # Save current floor
                        if player.dungeon_level == 0:
                            save_floor(load_saves[1])
                            save_objects_to_file(load_saves[2], data_source=data_objects_1)
                        else:
                            save_floor(load_saves[3])
                            save_objects_to_file(f"Data/File_{load_saves[0][10]}/data_dungeon_obj.pkl", data_source=objects)
                        
                    # >>CONTROLS<<
                    if choice == 3:
                        new_menu(header='Controls', 
                                 options=['Move:                                       Arrow keys or WASD',
                                          'Descend stairs or grab item:    Enter',
                                          'Ascend stairs to home:            Shift',
                                          'Check stats:                             1',
                                          'Use item in inventory:              2',
                                          'Drop item from inventory:        3',
                                          'Open questlog:                        4',
                                          'Toggle movement speed:         5',
                                          'Take screenshot:                      6',
                                          'Unused:                                   7',
                                          'Unused:                                   8',
                                          'Unused:                                   9',
                                          'Toggle messages:                     /'])
                    
                    # >>QUIT<<
                    elif choice == 4:
                        pygame.quit()
                        sys.exit()

        # -------------------------------------- RENDER --------------------------------------
        # Set menu background to the custom image
        screen.blit(background_image, (0, 0))
        
        # Renders menu to update cursor location
        y = 300
        for menu_choice_surface in menu_choices_surfaces:
            screen.blit(menu_choice_surface, (80, y))
            y += 24
        screen.blit(game_title, game_title_pos)
        screen.blit(cursor_img, cursor_img_pos)
        pygame.display.flip()

def new_menu(header, options, options_categories=None, position="top left", backgrounds=None):
    """ IMPORTANT. Creates cursor, background, and menu options, then returns index of choice.

        header:              (string) top line of text
        options:             (list of strings) menu choices_length
        options_categories:  used to organize inventory
        position:            choses layout preset """

    global game_title

    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    # -------------------------------------- INIT --------------------------------------
    # Initialize some temporary data containers
    choice                   = 0                      # Holds index of option pointed at by cursor
    choices_length           = len(options)-1 # Number of choices
    options_categories_cache = ""   # Holds current category
    options_render = options.copy()
    if options_categories: 
        tab_x, tab_y         = 70, 10
        options_categories_cache_2 = options_categories[0]
    else:
        tab_x, tab_y         = 0, 0

    # Set initial position of each text type
    header_position    = {"top left": [5,   10],             "center": (int((screen_width - game_title.get_width())/2), 85)}
    cursor_position    = {"top left": [50+tab_x, 38+tab_y],  "center": [50, 300]}
    options_positions  = {"top left": [80+tab_x, 34],        "center": [80, 300]}
    category_positions = {"top left": [5,   34],             "center": [80, 300]}

    # Set mutable copies of text positions
    cursor_position_mutable    = cursor_position[position].copy()
    options_positions_mutable  = options_positions[position].copy()
    category_positions_mutable = category_positions[position].copy()

    # Initialize cursor
    cursor_img = pygame.Surface((16, 16)).convert()
    cursor_img.set_colorkey(cursor_img.get_at((0,0)))
    pygame.draw.polygon(cursor_img, green, [(0, 0), (16, 8), (0, 16)], 0)
    
    # Initialize menu options
    header = font.render(header, True, yellow)
    for i in range(len(options)):
        color = gray
        options_render[i] = font.render(options[i], True, color)
    
    # Initialize backgrounds
    if backgrounds:
        for i in range(len(backgrounds)):
            backgrounds[i] = pygame.image.load(backgrounds[i]).convert()

    # -------------------------------------- MENU --------------------------------------
    # Allow player to select menu option
    while True:
        pygame.time.Clock().tick(30)
        
        # Render menu background
        if backgrounds:
            screen.fill(black)
            screen.blit(backgrounds[choice], (0, 0))
        else:
            screen.fill(black)
        
        # Render header and cursor
        screen.blit(header, header_position[position])
        screen.blit(cursor_img, cursor_position_mutable)
        
        # Render categories and options
        for i in range(len(options_render)):
            
            # Render category text if it is not present 
            if options_categories:
                if options_categories[i] != options_categories_cache:
                    options_categories_cache = options_categories[i]
                    text = font.render(f'{options_categories_cache.upper()}:', True, gray)
                    options_positions_mutable[1] += tab_y
                    screen.blit(text, (category_positions_mutable[0], options_positions_mutable[1]))
                
            # Render option text
            screen.blit(options_render[i], options_positions_mutable)
            options_positions_mutable[1] += 24
        options_positions_mutable = options_positions[position].copy()
        category_positions_mutable = category_positions[position].copy()
        pygame.display.flip()
        
        # Called when the user inputs a command
        for event in pygame.event.get():
            if event.type == KEYDOWN:

                # >>RESUME<<
                if event.key in key_0:
                    return False
                
                # >>SELECT MENU ITEM<<
                if event.key in key_UP:
                
                    # Move cursor up
                    cursor_position_mutable[1]     -= 24
                    choice                         -= 1
                    
                    # Move to lowest option
                    if choice < 0:
                        choice                     = choices_length
                        cursor_position_mutable[1] = cursor_position[position][1] + (len(options)-1) * 24
                        if options_categories:
                            cursor_position_mutable[1] += tab_y * (len(set(options_categories)) - 1)
                            options_categories_cache_2 = options_categories[choice]
                    
                    # Move cursor again if there are categories
                    elif options_categories:
                        if options_categories[choice] != options_categories_cache_2:
                            options_categories_cache_2 = options_categories[choice]
                            cursor_position_mutable[1] -= tab_y
                
                elif event.key in key_DOWN:
                
                    # Move cursor down
                    cursor_position_mutable[1]     += 24
                    choice                         += 1
                    
                    # Move to highest option
                    if choice > choices_length:
                        choice                     = 0
                        cursor_position_mutable[1] = cursor_position[position][1]
                        if options_categories:
                            options_categories_cache_2 = options_categories[choice]
                    
                    # Move cursor again if there are categories
                    elif options_categories:
                        if options_categories[choice] != options_categories_cache_2:
                            options_categories_cache_2 = options_categories[choice]
                            cursor_position_mutable[1] += tab_y
                            
                elif event.key in key_RETURN:
                    return choice
    
def inventory_menu(header):
    """ Shows a menu with each item of the inventory as an option, then returns an item if it is chosen. """
    
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    # Generates a list of item names and a list containing the category of each item
    # options holds item names; options_categories holds item categories
    if len(inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options, options_categories = [], []
        for item in inventory:
            text = item.name
            if item.equipment and item.equipment.is_equipped: # Shows additional information in case it's equipped
                text = text + ' (on ' + item.equipment.slot + ')'
            options.append(text)
            options_categories.append(item.category)
        
    # Generates a list of items to be omitted from the menu
    hidden_menu_items, hidden_menu_counter = [], 0 # Adjust for more hidden items
    for hair in hair_list:
        hidden_menu_items.append(hair)
        
    # Remove hidden item from options and save its index with hidden_menu_counter
    options_new, categories_new = [], []
    for i in range(len(options)):
        if options[i][0:4] in hidden_menu_items:
            hidden_menu_counter = options.index(options[i]) # Adjust for more hidden items
        else:
            options_new.append(options[i])
            categories_new.append(options_categories[i])

    # Generate menu and return selected option
    index = new_menu(header, options_new, options_categories=categories_new, position="top left")

    # Adjust index to account for hidden items, then return selected item
    if type(index) == int:
        if index >= 0 and index < (len(options)-1): # Adjust for more hidden items
            if index >= hidden_menu_counter: # Adjust for more hidden items
                index += 1
            return inventory[index].item
    else:
        return None
    
def file_menu(header):
    """ Shows a menu with each item of the inventory as an option, then returns an item if it is chosen. """
    
    global load_saves, file_set
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    options = [f"File A {file_set[0]}",
               f"File B {file_set[1]}",
               f"File C {file_set[2]}"]
               
    set_file_backgrounds = ["Data/File_1/screenshot.png",
                            "Data/File_2/screenshot.png",
                            "Data/File_3/screenshot.png"]
                  
    index = new_menu(header, options, backgrounds=set_file_backgrounds)
    if type(index) != int: main_menu()
    else:                  index += 1
    
    load_saves = [f"Data/File_{index}/data_player_{index}.pkl",
                  f"Data/File_{index}/data_home_{index}.pkl",
                  f"Data/File_{index}/data_objects_{index}.pkl",
                  f"Data/File_{index}/data_dungeon_{index}.pkl",
                  f"Data/File_{index}/data_inventory_{index}.pkl"]
    file_set = ['','','']
    file_set[index-1] = ' (current)'
    return index

def debug_call():
    """ Just a print statement for debugging. Shows which function is called alongside variable details. """
    optional_data = time.strftime("%M:%S", time.localtime())
    return [inspect.currentframe().f_back.f_code.co_name, optional_data]

#######################################################################################################################################################
# Start game
def __START_GAME__():
    pass

def character_creation():
    """ Manages the character creation menu. Handles player input. Only active when menu is open.
        Called when starting a new game.
    
        HAIR:       sets hair by altering hair_index, which is used in new_game to add hair as an Object hidden in the inventory
        HANDEDNESS: mirrors player/equipment tiles, which are saved in image_dict and image_dict_cache
        ACCEPT:     runs new_game() to generate player, home, and default items, then runs play_game() """
    
    global startup, load_saves, hair_index, skin_index, handedness_index, new_game_index
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    # -------------------------------------- INIT --------------------------------------
    # Initialize time
    clock = pygame.time.Clock()

    # Initialize cursor
    cursor_img = pygame.Surface((16, 16)).convert()
    cursor_img.set_colorkey(cursor_img.get_at((0,0)))
    pygame.draw.polygon(cursor_img, green, [(0, 0), (16, 8), (0, 16)], 0)
    cursor_img_pos = [50, 304]
    
    # Set character background
    background_image = pygame.image.load("Data/room.png")
    rotation_indices = [0, 0, [0, 2, 1, 3]] # used for rotating character in menu

    # Initialize menu options
    menu_choices = ["HAIR", "HANDEDNESS", "", "ACCEPT", "BACK"]   
    for i in range(len(menu_choices)):
        if   i == len(menu_choices)-2:  color = green
        elif i == len(menu_choices)-1:  color = red
        else:                           color = gray
        menu_choices[i] = font.render(menu_choices[i], True, color)
    choice, choices_length = 0, len(menu_choices)-1
    
    # Begins with default settings (ideally)
    for i in range(4):
        image_dict['player'][i]   = image_dict_cache['player'][i]
        image_dict['dagger'][i+1] = image_dict_cache['dagger'][i+1]
    hair_index = 1
    
    # -------------------------------------- MENU --------------------------------------
    # Allow player to select menu option
    while True:
        clock.tick(30)
        
        # Prevent escape from going back to character creation
        if new_game_index == 1:
            return
        
        # Called when the user inputs a command
        for event in pygame.event.get():

            if event.type == KEYDOWN:
            
                # >>MAIN MENU<<
                if event.key in key_0:
                    main_menu()
                
                # >>SELECT MENU ITEM<<
                elif event.key in key_UP:   # Up
                    cursor_img_pos[1]     -= 24
                    choice                -= 1
                    if choice < 0:
                        choice            = choices_length
                        cursor_img_pos[1] = 304 + (len(menu_choices)-1) * 24
                    elif choice == (choices_length - 2):
                        choice = choices_length - 3
                        cursor_img_pos[1] = 304 + (len(menu_choices)-4) * 24
                elif event.key in key_DOWN: # Down
                    cursor_img_pos[1]     += 24
                    choice                += 1
                    if choice > choices_length:
                        choice            = 0
                        cursor_img_pos[1] = 304
                    elif choice == (choices_length - 2):
                        choice = choices_length - 1
                        cursor_img_pos[1] = 304 + (len(menu_choices)-2) * 24
                elif event.key in key_RETURN:
                
                    # >>HAIR<<
                    if choice == 0:
                        if hair_index < len(hair_list)-1:
                            hair_index += 1
                        else:
                            hair_index = 0
                    
                    # >>HANDEDNESS<<
                    if choice == 1:
                        if handedness_index < len(handedness_list)-1:
                            handedness_index += 1
                        else:
                            handedness_index = 0
                        player_cache = pygame.transform.flip(image_dict['player'][2], True, False)
                        dagger_cache = pygame.transform.flip(image_dict['dagger'][3], True, False)
                        hair_cache = pygame.transform.flip(image_dict_cache['hair'][3], True, False)
                        image_dict['player'][0] = pygame.transform.flip(image_dict['player'][0], True, False)
                        image_dict['player'][1] = pygame.transform.flip(image_dict['player'][1], True, False)
                        image_dict['player'][2] = pygame.transform.flip(image_dict['player'][3], True, False)
                        image_dict['player'][3] = player_cache
                        image_dict['dagger'][1] = pygame.transform.flip(image_dict['dagger'][1], True, False)
                        image_dict['dagger'][2] = pygame.transform.flip(image_dict['dagger'][2], True, False)
                        image_dict['dagger'][3] = pygame.transform.flip(image_dict['dagger'][4], True, False)
                        image_dict['dagger'][4] = dagger_cache
                        image_dict_cache['hair'][1] = pygame.transform.flip(image_dict_cache['hair'][1], True, False)
                        image_dict_cache['hair'][2] = pygame.transform.flip(image_dict_cache['hair'][2], True, False)
                        image_dict_cache['hair'][3] = pygame.transform.flip(image_dict_cache['hair'][4], True, False)
                        image_dict_cache['hair'][4] = hair_cache
                    
                    # >>ACCEPT<<
                    if choice == 3:
                        if handedness_list[handedness_index] == 'right':
                            for item in image_dict:
                                if item == 'player':
                                    player_cache = pygame.transform.flip(image_dict_cache['player'][2], True, False)
                                    image_dict_cache['player'][0] = pygame.transform.flip(image_dict_cache['player'][0], True, False)
                                    image_dict_cache['player'][1] = pygame.transform.flip(image_dict_cache['player'][1], True, False)
                                    image_dict_cache['player'][2] = pygame.transform.flip(image_dict_cache['player'][3], True, False)
                                    image_dict_cache['player'][3] = player_cache
                                elif item not in ['monsters', 'stairs', 'walls', 'floors', 'decor', 'potions', 'scrolls', 'dagger']:
                                    item_cache = pygame.transform.flip(image_dict[item][3], True, False)
                                    image_dict[item][1] = pygame.transform.flip(image_dict[item][1], True, False)
                                    image_dict[item][2] = pygame.transform.flip(image_dict[item][2], True, False)
                                    image_dict[item][3] = pygame.transform.flip(image_dict[item][4], True, False)
                                    image_dict[item][4] = item_cache
                                    item_cache = pygame.transform.flip(image_dict_cache[item][3], True, False)
                                    image_dict_cache[item][1] = pygame.transform.flip(image_dict_cache[item][1], True, False)
                                    image_dict_cache[item][2] = pygame.transform.flip(image_dict_cache[item][2], True, False)
                                    image_dict_cache[item][3] = pygame.transform.flip(image_dict_cache[item][4], True, False)
                                    image_dict_cache[item][4] = item_cache
                    
                        new_game_index += 1
                        load_saves = ["Data/File_0/data_player_0.pkl",
                                      "Data/File_0/data_home_0.pkl",
                                      "Data/File_0/data_objects_0.pkl",
                                      "Data/File_0/data_dungeon_0.pkl",
                                      "Data/File_0/data_inventory_0.pkl"]
                        startup = False
                        new_game(True)
                        play_game()
                        
                    # >>MAIN MENU<<
                    if choice == 4:
                        main_menu()
        
        # -------------------------------------- RENDER --------------------------------------
        # Implement timed rotation of character
        rotation_indices[0] += 1
        if rotation_indices[0] == 30:
            rotation_indices[0] = 0
            if rotation_indices[1] < 3:
                rotation_indices[1] += 1
            else:
                rotation_indices[1] = 0

        # Set menu background
        screen.fill(black)
        
        # Renders menu to update cursor location
        y = 300
        for menu_choice in menu_choices:
            screen.blit(menu_choice, (80, y))
            y += 24
        screen.blit(cursor_img, cursor_img_pos)
        screen.blit(background_image, (400, 200))
        screen.blit(image_dict[skin_list[skin_index]][rotation_indices[2][rotation_indices[1]]], (464, 264))
        screen.blit(image_dict_cache[hair_list[hair_index]][rotation_indices[2][rotation_indices[1]]+1], (464, 264))
        screen.blit(image_dict['dagger'][rotation_indices[2][rotation_indices[1]]+1], (464, 264))
        pygame.display.flip()

game_state = 'dead' # as opposed to 'playing'
def new_game(new):
    """ Initializes NEW GAME. Does not handle user input. Resets player stats, inventory, map, and rooms.
        Called when starting a new game or loading a previous game.

        new:  creates player as Object with Fighter stats, calls make_home(), then loads initial inventory
        else: calls load_objects_from_file() to load player, inventory, and current floor """
    
    global player, camera, game_state, player_action, active_entities
    global game_msgs, game_msgs_data, message_log, inventory
    global data_objects_1, home_object_positions, new_game_trigger, save_objects
    global active_effects_cache, friendly, teleport, inventory_cache, dig, step_counter
    global questlog
    if debug: print(f"{debug_call()[0]:<30}{new}")

    # -------------------------------------- INIT --------------------------------------
    inventory                             = []
    active_entities                       = []
    save_objects                          = []
    active_effects_cache                  = []
    inventory_cache                       = []
    friendly, teleport, dig               = False, False, False
    step_counter                          = [False, 0, False, 0]
    data_objects_1, home_object_positions = [], []
    
    # -------------------------------------- NEW --------------------------------------
    if new:
        # Clear prior data
        new_game_trigger = True
        dialogue(init=True)

        # Generate new player
        fighter_component = Fighter(hp=100, defense=100, power=100, exp=0, death_function=player_death)
        player = Object(
                    tile_width*10, tile_height*7,
                    image_dict['player'][0],
                    name = "player",
                    category = "player",
                    blocks=True,
                    fighter=fighter_component,
                    hp=100, defense=100, power=100,
                    tile=True,
                    level=1, dungeon_level=0)
        
        # Set default quests
        gathering_supplies = Quest(name='Gathering supplies',
                             content=['My bag is nearly empty.',
                                      'It would be good to have some items on hand.',
                                      '☐ Collect potions.',
                                      '☐ Find a spare shovel.'],
                             category='Main')
        finding_a_future = Quest(name='Finding a future',
                             content=['I should make my way into town.',
                                      '☐ Wander east.'],
                             category='Main')
        making_a_friend = Quest(name='Making a friend',
                             content=['I wonder who this is. Maybe I should say hello.',
                                      '☐ Say hello to the creature.',
                                      '☐ Get to know them.'],
                             category='Side')
        furnishing_a_home = Quest(name='Furnishing a home',
                             content=['My house is empty. Maybe I can spruce it up.',
                                      '☐ Use the shovel to build new rooms.',
                                      '☐ Drop items to be saved for later use.',
                                      '☐ Look for anything interesting.'],
                             category='Side')
        questlog = Questlog(quests=[gathering_supplies, finding_a_future, making_a_friend, furnishing_a_home])
        questlog.update_quests()
        
        # Generate map and sets the player in a room
        make_home()
    
    # -------------------------------------- LOAD --------------------------------------
    else:
        load_objects_from_file(load_saves[0])
        load_objects_from_file(load_saves[2], data_objects_1)
        load_objects_from_file(load_saves[4], inventory)
        inventory_cache = inventory.copy()
        if player.dungeon_level != 0:
            load_floor(load_saves[3], home_music, load_objects_file='Data/data_dungeon_obj.pkl')
        else:
            load_floor(load_saves[1], home_music, load_objects_file=load_saves[2], home=True)
            #load_floor('screenshot_hidden.pkl', home_music, home=True, load_objects_file='screenshot_objects.pkl')
    
    camera = Camera(player)
    camera.update()
    
    game_state = 'playing' # as opposed to 'dead'
    player_action = 'didnt-take-turn' 
    
    update_gui() # places health and dungeon level on the screen
    game_msgs, game_msgs_data = [], [] # holds game messages and their colors
    message_log = True
    message('Welcome!', red)
    
    # -------------------------------------- NEW --------------------------------------
    # Sets initial inventory
    if new:
    
        # Clothes
        armor_equip   = Equipment(
                        slot          = "body",
                        defense_bonus = 10,
                        name          = "clothes")
        armor         = Object(
                        x             = 0,
                        y             = 0,
                        image         = image_dict["clothes"][0],
                        name          = "clothes",
                        category      = "apparel",
                        equipment     = armor_equip,
                        appended      = "objects")
        
        # Shovel
        shovel_equip  = Equipment(
                        slot          = "right hand",
                        power_bonus   = 0,
                        timer         = True,
                        name          = "shovel")
        shovel        = Object(
                        x             = 0,
                        y             = 0,
                        image         = image_dict['shovel'][0],
                        name          = "shovel",
                        category      = "weapons",
                        equipment     = shovel_equip)

        # Dagger
        dagger_equip  = Equipment(
                        slot          = "right hand",
                        power_bonus   = 2,
                        name          = "dagger")
        dagger        = Object(
                        x             = 0,
                        y             = 0,
                        image         = image_dict['dagger'][0],
                        name          = "dagger",
                        category      = "weapons",
                        equipment     = dagger_equip)
        
        # Wig
        hair_equip    = Equipment(
                        slot          = "head",
                        power_bonus   = 0,
                        name          = hair_list[hair_index])
        hair          = Object(
                        x             = 0,
                        y             = 0,
                        image         = image_dict[hair_list[hair_index]][0],
                        name          = hair_list[hair_index],
                        category      = "hair",
                        equipment     = hair_equip)
        
        # Apply
        inventory.append(armor)
        inventory.append(dagger)
        inventory.append(shovel)
        inventory.append(hair)
        inventory_cache.append('armor')
        inventory_cache.append('dagger')
        inventory_cache.append('shovel')
        inventory_cache.append('hair')
        step_counter[3] = shovel
        dagger_equip.equip()
        armor_equip.equip()
        hair_equip.equip()
    
    sort_inventory()

#######################################################################################################################################################
# Play game
def __PLAY_GAME__():
    pass

def play_game():
    """ IMPORTANT. Processes user input and triggers monster movement. """
    
    global player_action, message_log, message_log_toggle, stairs, last_press_time
    global gui_on, questlog
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    clock = pygame.time.Clock() # Keeps track of time
    player_move = False
    pygame.key.set_repeat(250, 150)

    while True:
        clock.tick(30)
        event = pygame.event.get()
        
        #animate_sprites()
        
        if event:

            # Save and quit
            if event[0].type == QUIT:
                save_game()
                pygame.quit()
                sys.exit()
            
            # Keep playing
            if game_state == 'playing':
                if event[0].type == KEYDOWN:
                    if debug: print()
                    active_effects()
                    
                    # >>MAIN MENU<<
                    if event[0].key in key_0:
                        message_log = False
                        #screenshot(cache=True)
                        return
                    
                    if toggle_list[movement_speed_toggle] == 'Fast':
                        # Update sprites and effects
                        if (event[0].key in key_UP or event[0].key in key_DOWN or event[0].key in key_LEFT or event[0].key in key_RIGHT) and ('transformation potion' not in inventory_cache):
                            animate_sprites(event[0].key, self=True)

                        # >>MOVE/ATTACK<<
                        if event[0].key in key_UP:
                            if (player.image == image_dict['player'][1]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(0, -tile_height)
                        elif event[0].key in key_DOWN:
                            if (player.image == image_dict['player'][0]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(0, tile_height)
                        elif event[0].key in key_LEFT:
                            if (player.image == image_dict['player'][2]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(-tile_width, 0)
                        elif event[0].key in key_RIGHT:
                            if (player.image == image_dict['player'][3]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(tile_width, 0)
                    else:
                        # >>MOVE/ATTACK<<
                        if event[0].key in key_UP:
                            if (player.image == image_dict['player'][1]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(0, -tile_height)
                        elif event[0].key in key_DOWN:
                            if (player.image == image_dict['player'][0]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(0, tile_height)
                        elif event[0].key in key_LEFT:
                            if (player.image == image_dict['player'][2]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(-tile_width, 0)
                        elif event[0].key in key_RIGHT:
                            if (player.image == image_dict['player'][3]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(tile_width, 0)

                        # Update sprites and effects
                        if (event[0].key in key_UP or event[0].key in key_DOWN or event[0].key in key_LEFT or event[0].key in key_RIGHT) and ('transformation potion' not in inventory_cache):
                            animate_sprites(event[0].key, self=True)

                    # >>PICKUP/STAIRS<<
                    if event[0].key in key_RETURN:                        
                        if player.tile.item and player.tile.item.item: 
                            player.tile.item.item.pick_up()
                            player.tile.item = None # Hides icon
                        
                        elif stairs.x == player.x and stairs.y == player.y:
                            # Save house
                            if player.dungeon_level == 0:   
                                save_floor(load_saves[1])   
                                save_objects_to_file(load_saves[2], data_source=data_objects_1)
                            next_level()
                            
                    if event[0].key == K_RSHIFT and player.dungeon_level != 0: # Ascend stairs to home
                        if stairs.x == player.x and stairs.y == player.y:
                            go_home()

                    # >>VIEW STATS<<
                    if event[0].key in key_1:
                        level_up_exp = level_up_base + player.level * level_up_factor
                        new_menu(header =   'Character Information',
                                 options = ['Level:                                ' + str(player.level),
                                            'Experience:                       ' + str(player.fighter.exp),
                                            'Experience to level up:    ' + str(level_up_exp),
                                            'Maximum HP:                    ' + str(player.fighter.max_hp),
                                            'Attack:                             ' + str(player.fighter.power),
                                            'Defense:                           ' + str(player.fighter.defense)])
                            
                    # >>CHECK INVENTORY<<
                    elif event[0].key in key_2:
                        chosen_item = inventory_menu("INVENTORY:         USE ITEM")
                        if chosen_item is not None:
                            chosen_item.use()
                            update_gui()
                    
                    # >>DROP ITEM<<
                    elif event[0].key in key_3:
                        if player.tile.item:
                            message("There's already something here")
                        else:
                            chosen_item = inventory_menu('INVENTORY:         DROP ITEM')
                            if chosen_item is not None:
                                chosen_item.drop()
                                pygame.event.clear()
                    
                    # >>VIEW QUESTLOG<<
                    elif event[0].key in key_4:
                        print(f"----------{questlog.categories_type}-----------")
                        if questlog.menu_index == 0:
                            quest_index = new_menu(header='Questlog',
                                                   options=questlog.quest_names,
                                                   options_categories=questlog.categories_type)
                            if type(quest_index) == int:
                                questlog.selected_quest = questlog.quests[quest_index]
                                questlog.update_quest()
                                selected_index = new_menu(header=questlog.selected_quest.name,
                                                          options=questlog.selected_quest.content,
                                                          options_categories=questlog.categories_content)
                                if type(selected_index) != int:
                                    questlog.back_to_menu()
                        else:
                            selected_index = new_menu(header=questlog.selected_quest.name,
                                                      options=questlog.selected_quest.content,
                                                      options_categories=questlog.categories_content)
                            if type(selected_index) == int:
                                questlog.back_to_menu()
                    
                    # >>MOVEMENT SPEED<<
                    elif event[0].key in key_5 and (time.time()-last_press_time > cooldown_time):
                        movement_speed(adjust=True)
                        last_press_time = float(time.time())
                    
                    # >>SCREENSHOT<<
                    elif event[0].key in key_6:
                        screenshot(cache=True, big=True)
                    
                    # >>TOGGLE MESSAGES<<
                    elif event[0].key in key_SLASH:
                    
                        # Hide messages
                        if message_log_toggle:
                            message_log, message_log_toggle = False, False
                        
                        else:
                            # Hide messages and GUI
                            if gui_on:
                                gui_on = False
                                message_log, message_log_toggle = False, False
                            
                            # View messages and GUI
                            else:
                                gui_on = True
                                message_log, message_log_toggle = True, True
            
            else:
                # >>MAIN MENU<<
                if event[0].type == KEYDOWN:
                    if event[0].key in key_0:
                        message_log = False
                        #screenshot(cache=True)
                        return
                        
                # >>TOGGLE MESSAGES<<
                elif event[0].key in key_SLASH:
                    if message_log_toggle:
                        message_log, message_log_toggle = False, False
                    else:
                        if gui_on:
                            gui_on = False
                            message_log, message_log_toggle = False, False
                        else:
                            message_log, message_log_toggle = True, True
                            gui_on = True
            
            if event[0].type == MOUSEBUTTONDOWN: # Cursor-controlled actions?
                if event[0].button == 1:
                    player_move = True
                    message_log = False
                elif event[0].button == 3:
                    mouse_x, mouse_y = event[0].pos
                    get_names_under_mouse(mouse_x, mouse_y)
                    
            if event[0].type == MOUSEBUTTONUP:
                if event[0].button == 1:
                    player_move = False

        if player_move and game_state == 'playing': # Cursor-controlled movement
            pos = pygame.mouse.get_pos()
            x = int((pos[0] + camera.x)/tile_width)
            y = int((pos[1] + camera.y)/tile_height)
            tile = level_map[x][y]
            if tile != player.tile:
                dx = tile.x - player.x
                dy = tile.y - player.y
                distance = math.sqrt(dx ** 2 + dy ** 2) # Distance from player to target
                dx = int(round(dx / distance)) * tile_width # Restrict motion to grid
                dy = int(round(dy / distance)) * tile_height
                player_move_or_attack(dx, dy) # Triggers the chosen action

    #if game_state == 'playing' and player_action != 'didnt-take-turn': # Tab forward and unhash to allow turn-based game
        for entity in active_entities:
            if entity.ai:
                entity.ai.take_turn()
        player_action = 'didnt-take-turn'
        render_all()

def go_home():
    """ Advances player to home. """
    
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    generate_friend()
    
    message('You take a moment to rest, and recover your strength.', violet)
    player.fighter.heal(int(player.fighter.max_hp / 2)) # Heals the player by 50%
    time.sleep(0.5)
    message('You gather you belongings and head home.', red)
    if player.dungeon_level != 0:
        player.dungeon_level = 0
    
    player.x = 15*32
    player.y = 15*32
    load_floor(load_saves[1], home_music, load_objects_file=load_saves[2], home=True)
    load_objects_from_file(load_saves[2], objects)
    camera.update()
    time.sleep(0.5)
    update_gui()

def player_move_or_attack(dx, dy):
    """ Moves the player by a given amount if the path is clear. Activates floor effects. """
    
    global player_action, dig, step_counter
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    target = None

    # Find new position
    x = int((player.x + dx)/tile_width)
    y = int((player.y + dy)/tile_height)
    
    #print(f"player:\t\t{player.x}\t{player.y}\nlevel_map:\t{x}\t{y}")
    #x2 = int((player.x)/tile_width)
    #y2 = int((player.y)/tile_height)
    #print(f"(x,y):\t\t\t({x2},{y2})")
    #print(f"(player.x,player.y):\t({x2*32},{y2*32})")
    #print(f"left:\t{level_map[x2-1][y2].unbreakable}")
    #print(f"right:\t{level_map[x2+1][y2].unbreakable}")
    #print(f"up:\t{level_map[x2][y2-1].unbreakable}")
    #print(f"down:\t{level_map[x2][y2+1].unbreakable}")
    #print(f"center:\t{level_map[x2][y2].unbreakable}")
        
    # Remove (level_map[x][y].entity and dungeon_level != 0) for default
    if (level_map[x][y].entity == player and player.dungeon_level == 0) or not is_blocked(x, y):
        
        # Move player and update level_map
        player.x += dx
        player.y += dy
        player.tile.entity = None # remove player from previous position; invisible barrier otherwise
        level_map[x][y].entity = player
        player.tile = level_map[x][y]
        check_tile(x, y)
        
        # Trigger floor effects
        try:
            floor_effects(level_map[x][y].floor_effect)
        except:
            pass
        
        camera.update()
    
    # Attack target
    elif level_map[x][y].entity and player.dungeon_level != 0: 
        target = level_map[x][y].entity
        player.fighter.attack(target)
    
    # Dig tunnel
    else:
        if (dig or super_dig) and not level_map[x][y].entity: # True if shovel equipped
            
            # Move player
            if player.x >= 64 and player.y >= 64:
                if super_dig or not level_map[x][y].unbreakable:
                    player.x                    += dx
                    player.y                    += dy
                    player.tile.entity          = None
                    level_map[x][y].blocked     = False
                    level_map[x][y].block_sight = False
                    level_map[x][y].unbreakable = False
                    level_map[x][y].image  = 'floors'
                    level_map[x][y].entity      = player
                    player.tile                 = level_map[x][y]
                    check_tile(x, y) # Reveals tile
                    camera.update()
                    
                    if (step_counter[1] >= 100) and not super_dig:
                        inventory[inventory.index(step_counter[3])].item.drop()
                        player.tile.item = None # Hides icon
                        step_counter = [False, 0, False, 0]
                    else:
                        step_counter[1] += 1
                else:
                    message('The shovel strikes the wall but does not break it.', white)
    player_action = 'took-turn'

def floor_effects(floor_effect):
    if floor_effect == "fire":
        player.fighter.take_damage(10)
    pass

#######################################################################################################################################################
# Data and audio management
def __DATA_AND_AUDIO_MANAGEMENT__():
    pass

# Mutable; holds savefile information; 0 = default, 1 = Slot A, 2 = Slot B, ...
load_saves = ["Data/File_0/data_player_0.pkl",
              "Data/File_0/data_home_0.pkl",
              "Data/File_0/data_objects_0.pkl",
              "Data/File_0/data_dungeon_0.pkl",
              "Data/File_0/data_inventory_0.pkl"]

def save_objects_to_file(file, data_source):
    """ Called by:      main_menu()                         when using >>SAVE<< 
                        play_game()                         when entering dungeon
        
        Player data:    file        = "Data/File_{index}/data_player_{index}.pkl"
                        data_source = [player]
        House data:     file        = "Data/File_{index}/data_objects_{index}.pkl"
                        data_source = data_objects_1
        Inventory data: file        = "Data/File_{index}/data_inventory_{index}.pkl"
                        data_source = inventory """

    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")

    objects_data = {}
    for i, item in enumerate(data_source):
    
        if item.category == 'player':
            objects_data[i] = {
                'category':      item.category,
                'x':             item.x,
                'y':             item.y,
                'name':          item.name,
                'blocks':        item.blocks,
                'ai':            item.ai,
                'item':          item.item,
                'equipment':     item.equipment,
                'hp':            item.hp,
                'defense':       item.defense,
                'power':         item.power,
                'level':         item.level,
                'dungeon_level': item.dungeon_level}
    
        elif item.category in ['potions', 'scrolls']:
            objects_data[i] = {
                'category':          item.category,
                'x':                 item.x,
                'y':                 item.y,
                'image_num':         item.image_num,
                'name':              item.name,
                'item.use_function': item.item.use_function,
                'hp':                item.hp,
                'defense':           item.defense,
                'power':             item.power,
                'level':             item.level,
                'dungeon_level':     item.dungeon_level}

        elif item.category in ['weapons', 'apparel', 'hair']:
            objects_data[i] = {
                'category':                item.category,
                'x':                       item.x,
                'y':                       item.y,
                'image_num':               item.image_num,
                'name':                    item.name,
                'equipment.power_bonus':   item.equipment.power_bonus,
                'equipment.defense_bonus': item.equipment.defense_bonus,
                'equipment.max_hp_bonus':  item.equipment.max_hp_bonus,
                'equipment.slot':          item.equipment.slot,
                'equipment.is_equipped':   item.equipment.is_equipped,
                'equipment.timer':         item.equipment.timer,
                'equipment.name':          item.equipment.name,
                'hp':                      item.hp,
                'defense':                 item.defense,
                'power':                   item.power,
                'level':                   item.level,
                'dungeon_level':           item.dungeon_level}

        else:
            objects_data[i] = {
                'category':      item.category,
                'x':             item.x,
                'y':             item.y,
                'image_num':     item.image_num,
                'name':          item.name,
                'hp':            item.hp,
                'defense':       item.defense,
                'power':         item.power,
                'level':         item.level,
                'dungeon_level': item.dungeon_level}

    with open(file, 'wb') as f:
        pickle.dump(objects_data, f)

def save_floor(file):
    """ Called by:    main_menu()              when using >>SAVE<<
        
        House data:   file = "Data/File_{index}/data_home_{index}.pkl"
        Dungeon data: file = "Data/File_{index}/data_dungeon_{index}.pkl" """

    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")

    layout_data = {}
    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            layout_data[(row_index, col_index)] = {
                'blocked':     tile.blocked,
                'x':           tile.x,
                'y':           tile.y,
                'block_sight': tile.block_sight,
                'visible':     tile.visible,
                'unbreakable': tile.unbreakable,
                'image':       tile.image,
                'image_num': tile.image_num,
                'explored':    tile.explored}

    with open(file, 'wb') as file:
        pickle.dump(layout_data, file)

def load_objects_from_file(file, container=None):
    global player, inventory, data_objects_1, stairs
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
            
    with open(file, 'rb') as file:
        load_objects = pickle.load(file)
        for i in range(len(load_objects)):
        
            # Loads player
            if load_objects[i]['name'] == 'player':
                fighter_component = Fighter(
                            hp=load_objects[i]['hp'],
                            defense=load_objects[i]['defense'],
                            power=load_objects[i]['power'],
                            exp=0,
                            death_function=player_death)
                player = Object(
                            load_objects[i]['x'],
                            load_objects[i]['y'],
                            image_dict['player'][0],
                            "player", category="player",
                            blocks=True,
                            fighter=fighter_component,
                            hp=load_objects[i]['hp'],
                            defense=load_objects[i]['defense'],
                            power=load_objects[i]['power'],
                            level=load_objects[i]['level'],
                            dungeon_level=load_objects[i]['dungeon_level'])
                dungeon_level = player.dungeon_level

            # Loads stairs
            elif load_objects[i]['name'] == 'stairs':
                stairs = Object(
                            load_objects[i]['x'],
                            load_objects[i]['y'],
                            image_dict['stairs'][0],
                            load_objects[i]['name'],
                            category=load_objects[i]['category'])
                container.append(stairs)
                
            # Loads items
            elif load_objects[i]['category'] in ['potions', 'scrolls']:
                item_component = Item(load_objects[i]['item.use_function'])
                new_item = Object(
                            load_objects[i]['x'],
                            load_objects[i]['y'],
                            image_dict[load_objects[i]['category']][load_objects[i]['image_num']],
                            name = load_objects[i]['name'],
                            category = load_objects[i]['category'],
                            item = item_component)
                if load_objects[i]['name'] != 'friend': # prevents phantom sprites (fix)
                    container.append(new_item)
            
            # Loads equipment
            elif load_objects[i]['category'] in ['weapons', 'apparel', 'hair']:
                equipment_component = Equipment(
                            power_bonus   = load_objects[i]['equipment.power_bonus'],
                            defense_bonus = load_objects[i]['equipment.defense_bonus'],
                            max_hp_bonus  = load_objects[i]['equipment.max_hp_bonus'],
                            slot          = load_objects[i]['equipment.slot'],
                            is_equipped   = load_objects[i]['equipment.is_equipped'],
                            timer         = load_objects[i]['equipment.timer'],
                            name          = load_objects[i]['equipment.name'])
                new_equipment = Object(
                            load_objects[i]['x'],
                            load_objects[i]['y'],
                            image_dict[load_objects[i]['name']][0],
                            name = load_objects[i]['name'],
                            category = load_objects[i]['category'],
                            equipment = equipment_component)
                container.append(new_equipment)
                if load_objects[i]['equipment.is_equipped']:
                    equipment_component.equip()
    
    # Generates tiles
    if container:
        for i in range(len(container)):
            if (container[i] != 0) and (container[i].name != 'player'):
                item = container[i]
                x, y = int(container[i].x/32), int(container[i].y/32)
                objects.append(item)
                #menu(f'{x}, {y}', 'test')
                try:
                    level_map[x][y].item = item
                except:
                    print(x, y, container[i].name)

def load_floor(file, music, load_objects_file=None, home=False):
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    global level_map, objects, load_saves

    # Start music track
    audio_control(new_track=music)

    # Load floor plan
    objects = [player]
    with open(file, 'rb') as f:
        layout_data = pickle.load(f)
    level_map = []
    for row_index in range(max(layout_data.keys(), key=lambda x: x[0])[0] + 1):
        row = []
        for col_index in range(max(layout_data.keys(), key=lambda x: x[1])[1] + 1):
            tile_data = layout_data.get((row_index, col_index))
            if tile_data is not None:
                row.append(Tile(
                    tile_data['blocked'],
                    tile_data['x'],
                    tile_data['y'],
                    tile_data['block_sight'],
                    tile_data['visible'],
                    unbreakable=tile_data['unbreakable'],
                    image=tile_data['image'],
                    explored=False))
            else:
                row.append(None)
        level_map.append(row)

    # Optionally load additional objects
    if load_objects_file:
        load_objects_from_file(load_objects_file, objects)
    
    if home:
        generate_friend()

    # Place objects
    level_map[int(player.x / 32)][int(player.y / 32)].entity = player
    player.tile = level_map[int(player.x / 32)][int(player.y / 32)]
    check_tile(int(player.x / 32), int(player.y / 32))
    if file == load_saves[3]: place_objects(home=home, fresh_start=False)  # Adds content to the room

## Initialize music player
pygame.mixer.init()

## Initialize track list
menu_music = pygame.mixer.Sound("Data/music_menu.mp3")
home_music = pygame.mixer.Sound("Data/music_home.mp3")
dungeon_music_1 = pygame.mixer.Sound("Data/music_dungeon_1.mp3")
dungeon_music_2 = pygame.mixer.Sound("Data/music_dungeon_2.mp3")
track_list = [menu_music, home_music, dungeon_music_1, dungeon_music_2]

# Start music
current_track = menu_music
current_track.play()

shuffle = False

def audio_control(new_track=None):
    global current_track
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    if shuffle:
        pass
    elif (new_track is not None) and (new_track is not current_track):
        #for i in range(len(track_list)):
        #    if (track_list[i] == current_track):
        #        current_track.stop()
        pygame.mixer.fadeout(4000)
        new_track.play(fade_ms=4000)
        current_track = new_track

#######################################################################################################################################################
# Environment management
def __ENVIRONMENT_MANAGEMENT__():
    pass

def create_room(room, block_sight=False, unbreakable=False, floor_effect=None, image='floors', image_num=0):
    """ Creates tiles for a room's floor and walls.
        Takes Rectangle object as an argument with parameters for width (x2 - x1) and height (y2 - y1). """
    global level_map
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            tile = level_map[x][y]
            tile.room = room
            
            tile.blocked = False # False for path, True for barrier
            
            tile.block_sight = block_sight # False for floor, True for wall
            
            tile.floor_effect = floor_effect # sets floor effects
            
            tile.image = image
            
            tile.image_num = image_num
            
            if unbreakable:
                if (x == room.x1 + 1) or (x == room.x2 - 1) or (y == room.y1 + 1) or (y == room.y2 - 1):
                    tile.unbreakable = True                
                else:
                    tile.block_sight = False

def create_h_tunnel(x1, x2, y):
    """ Creates horizontal tunnel. min() and max() are used if x1 is greater than x2. """
    global level_map
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    for x in range(min(x1, x2), max(x1, x2) + 1):
        level_map[x][y].blocked = False
        level_map[x][y].block_sight = False
        level_map[x][y].image = 'floors'

def create_v_tunnel(y1, y2, x):
    """ Creates vertical tunnel. min() and max() are used if y1 is greater than y2. """
    global level_map
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    for y in range(min(y1, y2), max(y1, y2) + 1):
        level_map[x][y].blocked = False
        level_map[x][y].block_sight = False
        level_map[x][y].image = 'floors'

def make_home():
    """ Initializes and generates the player's home, its rooms, and its contents. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")

    global level_map, objects, stairs, new_game_trigger
    
    # Start music track
    audio_control(new_track=home_music)
    
    objects = [player] # holds objects in home
    
    # Defines the map. [[x for x in range(2)] for y in range(3)] yields [[0,1], [0,1], [0,1]], for example.
    level_map = [[ Tile(True, x, y, visible=False, image='walls') # initialize walls at each point in the map
                for y in range(0, map_height*5, tile_height) ]
                for x in range(0, map_width*5, tile_width) ]

    # Create main room
    main_room = Rectangle(10, 10, room_max_size, room_max_size) 
    create_room(main_room)
    (new_x, new_y) = main_room.center()
    
    # Create secret room
    secret_room = Rectangle(30, 30, room_min_size*2, room_min_size*2) 
    create_room(secret_room, block_sight=True, unbreakable=True)
    
    # Place player
    player.x                       = new_x * tile_width
    player.y                       = new_y * tile_height
    level_map[new_x][new_y].entity = player
    player.tile                    = level_map[new_x][new_y]
    check_tile(new_x, new_y)
    new_x, new_y                   = new_x + 3, new_y # Sets the position for the stairs
    place_objects(main_room, home=True, fresh_start=new_game_trigger) # Adds content to the room
    if new_game_trigger:
        new_game_trigger = False
    
    generate_friend()

    # Creates stairs at the center of the last room
    stairs = Object(
                new_x * tile_width,
                new_y * tile_height,
                image_dict['stairs'][0],
                name = 'stairs',
                appended = 'objects')
    level_map[new_x][new_y].item = stairs
    objects.append(stairs)
    data_objects_1.append(stairs)
    stairs.send_to_back()

def generate_friend():
    global objects
    
    # Generates friend
    x = random.randint(11, 19) # Sets random location
    y = random.randint(11, 19)
    hp_set, defense_set, power_set, exp_set = 200, 0, 0, 0
    fighter_component = Fighter(
                hp=hp_set,
                defense=defense_set,
                power=power_set,
                exp=exp_set,
                death_function=monster_death)
    ai_component = BasicMonster()             
    monster = Object(
                x*tile_width,
                y*tile_height,
                image_dict['monsters'][0],
                'friend',
                blocks=True,
                fighter=fighter_component,
                ai=ai_component,
                appended='objects')
    data_objects_1.append(monster)
    home_object_positions.append([x, y])
    objects.append(monster)
    level_map[x][y].entity = monster # Places monster?
    monster.tile = level_map[x][y]

def place_objects(room=None, home=False, fresh_start=True):
    """ Decides the chance of each monster or item appearing, then generates and places them. """
    global data_objects_1, stairs
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    if not room: # Lazy bug fix
        room = Rectangle(1,1,2,2)
    
    # Set spawn chance for [chance, dungeon_level]
    max_monsters                    = from_dungeon_level([[2, 1], [3, 4], [5, 10]]) # Maximum per room. [value, level]
    monster_chances                 = {} # Chance of spawning monster by monster type
    monster_chances['orc']          = 80 # Sets spawn chance for orcs
    monster_chances['troll']        = from_dungeon_level([[15, 2], [30, 5], [60, 10]])
    monster_chances['troll 2']      = from_dungeon_level([[1, 2], [5, 5], [10, 10]])
 
    max_items                       = from_dungeon_level([[1, 1], [2, 4]]) # Maximum per room
    item_chances                    = {} # Chance of spawning item by item type
    item_chances['healing']         = 35 # Sets spawn chance for potions
    item_chances['transformation']  = 5 # Sets spawn chance for potions

    item_chances['lightning']       = from_dungeon_level([[25, 4]])
    item_chances['fireball']        = from_dungeon_level([[25, 6]])
    item_chances['confuse']         = from_dungeon_level([[10, 2]])

    item_chances['shovel']          = 20
    item_chances['super shovel']    = 10
    item_chances['sword']           = from_dungeon_level([[10, 5]])
    item_chances['blood dagger']    = from_dungeon_level([[5, 4]])
    item_chances['blood sword']     = from_dungeon_level([[2, 1]])
    item_chances['shield']          = from_dungeon_level([[15, 8]])

    # Place items in home
    if home:
        data_objects_1, home_object_positions = [], []
        
        # Place default items for new game
        if fresh_start:
            for i in range(5): 
                x = room.x1+3+i # Sets location
                y = room.y1+1
                if i == 0:
                    item_component = Item(use_function=cast_heal)
                    item = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['potions'][0],
                                'healing potion', category="potions", image_num=0,
                                item=item_component,
                                appended='objects')
                elif i == 1:
                    item_component = Item(use_function=cast_lightning)
                    item = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['scrolls'][0],
                                'scroll of lightning bolt', category="scrolls", image_num=0,
                                item=item_component,
                                appended='objects')
                elif i == 2:
                    item_component = Item(use_function=cast_fireball)
                    item = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['scrolls'][0],
                                'scroll of fireball', category="scrolls", image_num=0,
                                item=item_component,
                                appended='objects')
                                
                elif i == 3:
                    x, y = 33, 33
                    equipment_component = Equipment(
                                slot='right hand',
                                power_bonus=6,
                                name='blood sword')
                    item = Object(
                                x*tile_width,
                                y*tile_width,
                                image_dict['blood sword'][0],
                                'blood sword', category="weapons",
                                equipment=equipment_component,
                                appended='objects')
                elif i == 4:
                    x, y = 34, 34
                    equipment_component = Equipment(
                                slot='left hand',
                                defense_bonus=3,
                                name='shield')
                    item = Object(
                                34*tile_width,
                                34*tile_width,
                                image_dict['shield'][0],
                                'shield', category="apparel",
                                equipment=equipment_component,
                                appended='objects')
                elif i == 5:
                    x, y = 0, 0
                    item_component = Item(use_function=cast_fireball)
                    item = Object(
                                0,
                                0,
                                image_dict['scroll'][-1],
                                'scroll of fireball', category="scrolls", image_num=0,
                                item=item_component,
                                appended='objects')
                data_objects_1.append(item)
                home_object_positions.append([x, y])
                objects.append(item)
                level_map[x][y].item = item

    else: # Places items and monsters in dungeon
        num_monsters = random.choice([0, 0, 0, 0, 1, max_monsters])
        num_items = random.randint(0, max_items) # Sets number of items?
        
        for i in range(num_monsters): # Places monsters
            x = random.randint(room.x1+1, room.x2-1) # Sets random location
            y = random.randint(room.y1+1, room.y2-1)
            if not is_blocked(x, y):
                choice = random_choice(monster_chances) # Sets random monster
                if choice == 'orc': # Creates an orc
                    hp_set, defense_set, power_set, exp_set = 20, 0, 4, 35
                    fighter_component = Fighter(
                                hp=hp_set,
                                defense=defense_set,
                                power=power_set,
                                exp=exp_set,
                                death_function=monster_death)
                    ai_component = BasicMonster()               
                    monster = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['monsters'][7],
                                'orc',
                                blocks=True,
                                fighter=fighter_component,
                                ai=ai_component)
                elif choice == 'troll':
                    hp_set, defense_set, power_set, exp_set = 30, 2, 8, 100
                    fighter_component = Fighter(
                                hp=hp_set,
                                defense=defense_set,
                                power=power_set,
                                exp=exp_set,
                                death_function=monster_death)
                    ai_component = BasicMonster()               
                    monster = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['monsters'][4],
                                'troll',
                                blocks=True,
                                fighter=fighter_component,
                                ai=ai_component,
                                appended='objects')
                elif choice == 'troll 2':
                    hp_set, defense_set, power_set, exp_set = 50, 5, 15, 500
                    fighter_component = Fighter(
                                hp=hp_set,
                                defense=defense_set,
                                power=power_set,
                                exp=exp_set,
                                death_function=monster_death)
                    ai_component = BasicMonster()               
                    monster = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['monsters'][6],
                                'troll 2',
                                blocks=True,
                                fighter=fighter_component,
                                ai=ai_component,
                                appended='objects')
                objects.append(monster)
                level_map[x][y].entity = monster # Places monster?
                monster.tile = level_map[x][y]

        for i in range(num_items): # Places items
            x = random.randint(room.x1+1, room.x2-1) # Sets random location
            y = random.randint(room.y1+1, room.y2-1)
            if not is_blocked(x, y):
                choice = random_choice(item_chances) # Sets random item
                item = Object(x, y, image_dict['decor'][-1], name='bug fix')
                
                if choice == 'heal': # Creates a potion
                    item_component = Item(use_function=cast_heal)
                    item = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['potions'][0],
                                'healing potion', category="potions", image_num=0,
                                item=item_component,
                                appended='objects')
                if choice == 'transformation': # Creates a potion
                    item_component = Item()
                    item = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['potions'][1],
                                'transformation potion', category="potions", image_num=1,
                                item=item_component,
                                appended='objects')
                                
                elif choice == 'lightning': # Creates a lightning scroll
                    item_component = Item(use_function=cast_lightning)
                    item = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['scrolls'][0],
                                'scroll of lightning bolt', category="scrolls", image_num=0,
                                item=item_component,
                                appended='objects')
                elif choice == 'fireball': # Creates a fireball scroll
                    item_component = Item(use_function=cast_fireball)
                    item = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['scrolls'][0],
                                'scroll of fireball', category="scrolls", image_num=0,
                                item=item_component,
                                appended='objects')
                elif choice == 'confuse': # Creates a confusion scroll
                    item_component = Item(use_function=cast_confuse)
                    item = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['scrolls'][0],
                                'scroll of confusion', category="scrolls", image_num=0,
                                item=item_component,
                                appended='objects')
                                
                elif choice == 'blood dagger': # Creates a blood dagger
                    equipment_component = Equipment(
                                slot='right hand',
                                power_bonus=4,
                                name='blood dagger')
                    item = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['blood dagger'][0],
                                'blood dagger', category="weapons",
                                equipment=equipment_component,
                                appended='objects')
                elif choice == 'sword': # Creates a sword
                    equipment_component = Equipment(
                                slot='right hand',
                                power_bonus=3,
                                name='sword')
                    item = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['sword'][0],
                                'sword', category="weapons",
                                equipment=equipment_component,
                                appended='objects')
                elif choice == 'blood sword': # Creates a blood sword
                    equipment_component = Equipment(
                                slot='right hand',
                                power_bonus=6,
                                name='blood sword')
                    item = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['blood sword'][0],
                                'blood sword', category="weapons",
                                equipment=equipment_component,
                                appended='objects')
                elif choice == 'shield': # Creates a shield
                    equipment_component = Equipment(
                                slot='left hand',
                                defense_bonus=3,
                                name='shield')
                    item = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['shield'][0],
                                'shield', category="apparel",
                                equipment=equipment_component,
                                appended='objects')
                elif choice == 'shovel':
                    equipment_component = Equipment(
                                slot='right hand',
                                power_bonus=1,
                                timer=True,
                                name='shovel')
                    item = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['shovel'][0],
                                'shovel', category="weapons",
                                equipment=equipment_component,
                                equipment_list=['right hand', 0])        
                elif choice == 'super shovel':
                    equipment_component = Equipment(
                                slot='right hand',
                                power_bonus=10,
                                name='super shovel')
                    item = Object(
                                x*tile_width,
                                y*tile_height,
                                image_dict['super shovel'][0],
                                'super shovel', category="weapons",
                                equipment=equipment_component,
                                equipment_list=['right hand', 0])                                  
                objects.append(item)
                level_map[x][y].item = item
                item.send_to_back()

def make_map():
    """ Initializes and generates the map, its rooms, and its contents. """
    global level_map, objects, stairs
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")

    # Initializations
    objects          = [player]
    rooms            = []
    room_counter     = 0
    
    # Changes map parameters based on dungeon level
    num_rooms        = int(max_rooms * player.dungeon_level)
    new_map_height   = int(map_height * player.dungeon_level)
    new_map_width    = int(map_width * player.dungeon_level)
    
    # Initializes tiles at each point in the map
    level_map        = [[ Tile(True, x, y, image='walls')
                       for y in range(0, new_map_height, tile_height) ]
                       for x in range(0, new_map_width, tile_width) ]
 
    # Creates random set of rooms and places them in the map
    for r in range(num_rooms):
        w = random.randint(room_min_size, room_max_size) # Sets a random width and height for a single room
        h = random.randint(room_min_size, room_max_size)
        x = random.randint(0, tile_map_width - w - 1) # Set a random position within the map
        y = random.randint(0, tile_map_height - h - 1)
        new_room = Rectangle(x, y, w, h) # Places the room at the random location.
 
        failed = False # Checks for room intersections. Include more values to make more hallways.
        if random.choice([0, 1, 2, 3]) != 0:
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

        if random.choice(range(player.dungeon_level)) >= player.dungeon_level*(3/4):
            create_room(new_room, image_num=5) # Sets parameters for the room's floor
        else:
            create_room(new_room, image_num=0)

        if not failed: # Completes room
            (new_x, new_y) = new_room.center() # Coordinates of the room's center
            if room_counter == 0: # Places player in the first room
                player.x                       = new_x * tile_width
                player.y                       = new_y * tile_height
                level_map[new_x][new_y].entity = player
                player.tile                    = level_map[new_x][new_y]
                check_tile(new_x, new_y)
            else: # Makes tunnel to connect to the previous room
                (prev_x, prev_y) = rooms[room_counter-1].center() # Coordinates of previous room's center
                if random.randint(0, 1) == 0:
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)
                place_objects(new_room) # Adds content to the room
            rooms.append(new_room) # Adds new room to the room list
            room_counter += 1

    # Creates stairs at the center of the last room
    stairs = Object(
                new_x * tile_width,
                new_y * tile_height,
                image_dict['stairs'][0],
                'stairs',
                appended='objects')
    level_map[new_x][new_y].item = stairs
    objects.append(stairs)
    stairs.send_to_back()

#######################################################################################################################################################
# Utilities
def __UTILITIES__():
    pass

def animate_sprites(key=key_cache, self=True):
    global idle_animation_counter, key_cache
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")

    if self == True:
        #if idle_animation_counter[0] <= 40:
        #    player.image = images[2]
        #    player.image_num = 2
        #elif 40 < idle_animation_counter[0] < 60:
        #    player.image = images[3]
        #    player.image_num = 3
        #else:
        #    idle_animation_counter[0] = 0
        #idle_animation_counter[0] += 1
        
        key_cache = key
        if key in key_UP:
            player.image = image_dict['player'][1]
        elif key in key_DOWN:
            player.image = image_dict['player'][0]
        elif key in key_LEFT:
            player.image = image_dict['player'][2]
        elif key in key_RIGHT:
            player.image = image_dict['player'][3]

def render_all(screenshot=False, visible=False):
    """ Draws tiles and stuff. Constantly runs. """
    
    global active_entities
    
    active_entities = []
    dungeon_scaling = int(player.dungeon_level / 10)
    screen.fill(black)
    
    if screenshot:
        y_range_1, y_range_2 = 0, len(level_map[0])
        x_range_1, x_range_2 = 0, len(level_map)
    else:
        y_range_1, y_range_2 = camera.tile_map_y, camera.y_range
        x_range_1, x_range_2 = camera.tile_map_x, camera.x_range
    
    # Draw visible tiles
    for y in range(y_range_1, y_range_2):
        for x in range(x_range_1, x_range_2):
            tile = level_map[x][y]
            if visible or tile.visible:
                
                # Sets wall image
                screen.blit(image_dict[tile.image][tile.image_num], (tile.x-camera.x, tile.y-camera.y))
                
                # Generates floor and entities; sets floor image
                if not tile.block_sight:
                    if tile.item:
                        screen.blit(tile.item.image, (tile.x-camera.x, tile.y-camera.y))
                        tile.item.draw(screen)
                    if tile.entity:
                        tile.entity.draw(screen)
                        active_entities.append(tile.entity)

                if tile.unbreakable:
                    screen.blit(image_dict['walls'][1], (tile.x-camera.x, tile.y-camera.y))
    if not screenshot:
        if impact:
            screen.blit(impact_image, impact_image_pos)
        

        # Print messages
        if message_log: 
           y = 10
           for msg in game_msgs:
               screen.blit(msg, (5, y))
               y += 24
        if gui_on:
            screen.blit(gui, (10,456))
        pygame.display.flip()

gui_on = True
def control_gui():
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")

    global message_log_toggle

    if message_log_toggle:
        message_log, message_log_toggle = False, False
    else:
        message_log, message_log_toggle = True, True

def update_gui():
    """ Updates health and dungeon level. """
    
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")

    global gui, gui_on
    
    gui = font.render('HP: ' + str(player.fighter.hp) + '/' + str(player.fighter.max_hp)
                        +  ' '*60 + ' Dungeon level ' + str(player.dungeon_level), True, yellow)

def message(new_msg, color = white):
    """ Initializes images to be projected with render_all. """

    global game_msgs, message_log, game_msgs_data
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")

    if not message_log:
       game_msgs = []
       game_msgs_data = []
    message_log = True
    
    new_msg_lines = textwrap.wrap(new_msg, message_width) # Splits the message among multiple lines
    for line in new_msg_lines:
        if len(game_msgs) == message_height:
            del game_msgs[0]
            del game_msgs_data[0]
        msg = font.render(line, True, color) # Adds the new message
        game_msgs.append(msg)
        game_msgs_data.append((line,color))
    render_all()
    wait_time = 0
    while wait_time < 10:
        pygame.time.Clock().tick(30)
        wait_time += 1

def active_effects():
    """ Applies effects from items and equipment. Runs constantly. """
    global friendly, teleport, dig, super_dig
    
    if 'transformation potion' in inventory_cache:
        player.image = image_dict['monsters'][0]
        friendly = True
    else:
        #player.image = images[2]
        friendly = False
        
    if step_counter[0]:
        dig = True
    else:
        dig = False
    
    try:
        if get_equipped_in_slot('right hand').name == 'super shovel':
            super_dig = True
        else:
            super_dig = False
    except:
        super_dig = False
    
    if 'scroll of lightning bolt' in inventory_cache:
        teleport = True
    else:
        teleport = False

def player_death(player):
    """ Ends the game upon death and transforms the player into a corpse. """
    global game_state
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    message('You died!', red)
    game_state         = 'dead'
    player.image       = image_dict['decor'][1]
    player.tile.entity = None
    player.tile.item   = player

def monster_death(monster):
    """ Transforms a monster into a corpse. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    message('The ' + monster.name + ' is dead! You gain ' + str(monster.fighter.exp) + ' experience points.', orange)
    monster.image       = image_dict['decor'][1]
    monster.tile.entity = None
    monster.blocks      = False
    monster.fighter     = None
    monster.ai          = None
    monster.category    = 'other'
    monster.name        = 'remains of ' + monster.name
    try:
        monster.send_to_back()
    except:
        pass
    monster.item = Item()
    monster.item.owner = monster
    if not monster.tile.item:
        monster.tile.item = monster
    pygame.event.get()

def cast_heal():
    """ Heals the player. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    if player.fighter.hp == player.fighter.max_hp:
        message('You are already at full health.', red)
        return 'cancelled'
    message('Your wounds start to feel better!', violet)
    player.fighter.heal(heal_amount)

def cast_lightning():
    """ Finds the closest enemy within a maximum range and attacks it. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    monster = closest_monster(lightning_range)
    if monster is None:  #no enemy found within maximum range
        message('No enemy is close enough to strike.', red)
        return 'cancelled'
    message('A lighting bolt strikes the ' + monster.name + ' with a loud thunder! The damage is '
        + str(lightning_damage) + ' hit points.', light_blue)
    monster.fighter.take_damage(lightning_damage)

def cast_fireball():
    """ Asks the player for a target tile to throw a fireball at. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    message('Left-click a target tile for the fireball, or right-click to cancel.', light_cyan)
    (x, y) = target_tile()
    if x is None: return 'cancelled'
    message('The fireball explodes, burning everything within ' + str(int(fireball_radius/tile_width)) + ' tiles!', orange)
    for obj in active_entities: # Damages every fighter in range, including the player
        if obj.distance(x, y) <= fireball_radius and obj.fighter:
            message('The ' + obj.name + ' gets burned for ' + str(fireball_damage) + ' hit points.', orange)
            obj.fighter.take_damage(fireball_damage)

def cast_confuse():
    """ Asks the player for a target to confuse, then replaces the monster's AI with a "confused" one. After some turns, it restores the old AI. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    message('Left-click an enemy to confuse it, or right-click to cancel.', light_cyan)
    monster = target_monster(confuse_range)
    if monster is None: return 'cancelled'
    old_ai = monster.ai
    monster.ai = ConfusedMonster(old_ai)
    monster.ai.owner = monster  #tell the new component who owns it
    message('The eyes of the ' + monster.name + ' look vacant, as he starts to stumble around!', light_green)

def closest_monster(max_range):
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    closest_enemy = None
    closest_dist = max_range + 1  #start with (slightly more than) maximum range
 
    for obj in active_entities:
        if obj.fighter and obj != player and obj.tile.visible:
            #calculate distance between this object and the player
            dist = player.distance_to(obj)
            if dist < closest_dist:  #it's closer, so remember it
                closest_enemy = obj
                closest_dist
    return closest_enemy

def target_tile(max_range=None):
    """ Returns the position of a tile left-clicked in player's field of view, or (None,None) if right-clicked. """
    global message_log
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    while True:         
        pygame.time.Clock().tick(30)
        for event in pygame.event.get(): # Processes user input
        
            if event.type == QUIT: # Quit
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN: # Cancels action for escape
                if event.key in key_0:
                    message_log = False 
                    return (None, None)
                    
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 3: # Cancels action for right-click
                    message_log = False 
                    return (None, None)
                    
                if event.button == 1: # Accepts the target if clicked in the field of view
                    mouse_x, mouse_y = event.pos
                    mouse_x += camera.x
                    mouse_y += camera.y
                    x = int(mouse_x /tile_width)
                    y = int(mouse_y /tile_height)
                    if (level_map[x][y].visible and
                        (max_range is None or player.distance(mouse_x, mouse_y) <= max_range)):
                        return (mouse_x, mouse_y)
        render_all()

def check_tile(x, y):
    """ Reveals newly explored regions. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    tile = level_map[x][y]
    if not tile.explored:
       tile.explored = True 
       old_x = x
       old_y = y
       for x in range(old_x - 1, old_x + 2):
           for y in range(old_y - 1, old_y + 2):
               level_map[x][y].visible = True
       if tile.room and not tile.room.explored:
          room = tile.room
          room.explored = True
          for x in range(room.x1 , room.x2 + 1):
              for y in range(room.y1 , room.y2 + 1):
                  level_map[x][y].visible = True       

def check_level_up():
    """ Checks if the player's experience is enough to level-up. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    level_up_exp = level_up_base + player.level * level_up_factor
    if player.fighter.exp >= level_up_exp: # Levels up
        player.level += 1
        player.fighter.exp -= level_up_exp
        message('Your battle skills grow stronger! You reached level ' + str(player.level) + '!', yellow)
        choice = None
        while choice == None: # Keeps asking until a choice is made
            choice = new_menu(header = 'Level up! Choose a stat to raise:',
                              options = ['Constitution (+20 HP, from ' + str(player.fighter.max_hp) + ')',
                                         'Strength (+1 attack, from ' + str(player.fighter.power) + ')',
                                         'Agility (+1 defense, from ' + str(player.fighter.defense) + ')'], 
                              position="center")

        if choice == 0: # Boosts health
            player.fighter.max_hp += 20
            player.fighter.hp += 20
        elif choice == 1: # Boosts power
            player.fighter.power += 1
        elif choice == 2: # Boosts defense
            player.fighter.defense += 1
        update_gui()

def from_dungeon_level(table):
    """ Returns a value that depends on the dungeon level. Runs in groups.
        The table specifies what value occurs after each level with 0 as the default. """
    
    for (value, level) in reversed(table):
        if player.dungeon_level >= level:
            return value
    return 0

def is_blocked(x, y):
    """ Checks for barriers and trigger dialogue. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    try:
        # Check for barriers
        if level_map[x][y].blocked:
            return True
            
        # Check for monsters
        if level_map[x][y].entity: 
        
            # Triggers dialogue for friend
            if level_map[x][y].entity.name in NPC_names:
                dialogue(NPC_name=level_map[x][y].entity.name)
            return True
            
        # Triggers message for hidden passages
        if level_map[x][y].unbreakable:
            message('A mysterious breeze seeps through the cracks.', white)
            pygame.event.clear()
            return True
    except:
        return True
    return False

def get_equipped_in_slot(slot):
    """ Returns the equipment in a slot, or None if it's empty. """
    
    for obj in inventory:
        if obj.equipment and obj.equipment.slot == slot and obj.equipment.is_equipped:
            return obj.equipment
    return None

def entity_flash(entity):
    """ Death animation. """
    global impact
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    impact = True
    impact_image_pos[0] = entity.x-camera.x
    impact_image_pos[1] = entity.y-camera.y
    render_all()
    impact = False
    
    #wait_time = 0
    #while wait_time < 5:
    #    pygame.time.Clock().tick(30)
    #    wait_time += 1    
    
    flash = 3
    flash_time = 2
    if entity.fighter.hp <=0:
       flash_time = 4
    entity_old_image = entity.image
    while flash_time > 1:
        pygame.time.Clock().tick(30)
        if flash:
           entity.image = blank_surface
        render_all()
        if not flash:
           flash = 6
        flash -= 1
        if flash < 1:
           flash = False
           flash_time -= 1
           entity.image = entity_old_image 
           if flash_time < 1:
              flash_time = 0
              flash = False
              entity.image = entity_old_image

def get_impact_image():
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    color = (230,230,230)
    impact_image = pygame.Surface((tile_width, tile_width)).convert()
    impact_image.set_colorkey(impact_image.get_at((0,0)))
    image = pygame.Surface((int(tile_width/2), int(tile_height/3))).convert()
    top = 0
    left = 0
    bottom = image.get_width()-1
    right = image.get_height()-1
    center_x = int(image.get_width()/2)-1
    center_y = int(image.get_height()/2)-1
    pygame.draw.line(image, color, (top,left), (bottom,right), 2)
    #pygame.draw.line(image, color, (bottom,left), (top,right), 2)
    #pygame.draw.line(image, color, (center_x,top), (center_x,bottom), 2)
    #pygame.draw.line(image, color, (left,center_y),(right,center_y), 2)
    x = int((impact_image.get_width()-image.get_width())/2)
    y = int((impact_image.get_height()-image.get_height())/2)
    impact_image.blit(image, (x,y))
    return impact_image

def next_level():
    """ Advances player to the next level. """
    global dungeon_level
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    message('You take a moment to rest, and recover your strength.', violet)
    player.fighter.heal(int(player.fighter.max_hp / 2))  #heal the player by 50%
    
    # Change music and dungeon level
    if player.dungeon_level == 0:
        audio_control(new_track=dungeon_music_1)
    elif player.dungeon_level >= 10:
        audio_control(new_track=dungeon_music_2)
    player.dungeon_level = player.dungeon_level + 1
    
    time.sleep(0.5)
    message('After a rare moment of peace, you descend deeper into the heart of the dungeon...', red)
    make_map()
    camera.update()
    time.sleep(0.5)
    update_gui()
    
def random_choice_index(chances):
    """ Chooses an option from a list of possible values, then returns its index. """
    
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    dice = random.randint(1, sum(chances))
    running_sum = 0
    choice = 0
    # Checks if the random choice corresponds to one of the possible values
    for w in chances:
        running_sum += w
        if dice <= running_sum:
            return choice
        choice += 1

def random_choice(chances_dict):
    """ Chooses one option from dictionary of chances, then returning its key. """
    
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    chances = chances_dict.values()
    strings = list(chances_dict.keys())
    return strings[random_choice_index(chances)]

def sort_inventory():
    global inventory
    
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    inventory_cache = {"sorted": [], "weapons": [], "armor": [], "potions": [], "scrolls": [], "other": []}

    # Sort by category
    for item in inventory:
        try:    inventory_cache[item.category].append(item)
        except: inventory_cache['other'].append(item)
    
    # Sort weapons by stats
    category_cache, num_cache = [], [0 ,0]
    for item in inventory_cache['weapons']:
        try: 
            num_cache[0] += item.equipment.power_bonus
            num_cache[1] += 1
        except: pass
        try:
            num_cache[0] += item.equipment.defense_bonus
            num_cache[1] += 1
        except: pass
        try:
            num_cache[0] += item.equipment.max_hp_bonus
            num_cache[1] += 1
        except: pass
        category_cache.append([num_cache[0]/num_cache[1], item])
    category_cache = sorted(category_cache, key=lambda x: x[0])
    category_cache.reverse()
    for lists in category_cache:
        inventory_cache['sorted'].append(lists[1])
    
    # Sort armor by stats
    category_cache, num_cache = [], [0 ,0]
    for item in inventory_cache['armor']:
        try:
            num_cache[0] += item.equipment.power_bonus
            num_cache[1] += 1
        except: pass
        try:
            num_cache[0] += item.equipment.defense_bonus
            num_cache[1] += 1
        except: pass
        try:
            num_cache[0] += item.equipment.max_hp_bonus
            num_cache[1] += 1
        except: pass
        category_cache.append([num_cache[0]/num_cache[1], item])
    category_cache.sort()
    category_cache.reverse()
    for lists in category_cache:
        inventory_cache['sorted'].append(lists[1])
        
    # Sort potions
    category_cache, num_cache = [], [0 ,0]
    for item in inventory_cache['potions']:
        category_cache.append([item.name, item])
    category_cache = sorted(category_cache)
    for lists in category_cache:
        inventory_cache['sorted'].append(lists[1])
        
    # Sort scrolls
    category_cache, num_cache = [], [0 ,0]
    for item in inventory_cache['scrolls']:
        category_cache.append([item.name, item])
    category_cache = sorted(category_cache)
    for lists in category_cache:
        inventory_cache['sorted'].append(lists[1])

    # Add everything else to inventory
    for item in inventory_cache['other']:
        inventory_cache['sorted'].append(item)

    inventory = inventory_cache['sorted']

#######################################################################################################################################################
# Classes
def __CLASSES__():
    pass

class Object:
    """ Defines a generic object, such as the player, a monster, an item, or stairs. """
    
    def __init__(self, x, y, image, name, blocks=False, fighter=None, hp=None, power=None, defense=None,
                ai=None, item=None, equipment=None, item_list=False, equipment_list=False,
                appended=False, tile=None, level=None, dungeon_level=None, category=None, image_num=0):
        """ Defines object and object parameters, such as name, image and image size, stats, and equipment.
            Initializes player, monster, stairs, and items. """
        
        global level_map

        # Assign object parameters
        self.x           = x                    # tile width (integer)
        self.y           = y                    # tile height (integer)
        
        self.image       = image                # tile image (integer, pulled from rogue_tiles.png)
        
        self.name        = name                 # name (string)
        
        self.blocks      = blocks               # unknown
        self.tile        = None                 # initialized tile location (?)
        
        self.fighter     = fighter              # true for player or monster
        self.level       = level
        self.hp          = hp
        self.defense     = defense
        self.power       = power
        self.counter     = 0

        self.ai          = ai                   # true for monsters
        self.item        = item                 # true for usable items
        self.equipment   = equipment            # true for wearable items
        self.dungeon_level = dungeon_level
        
        self.category    = category
        self.image_num   = image_num

        # Lets player and monsters fight
        if self.fighter:
            self.fighter.owner = self
        
        # Lets monsters control themselves
        if self.ai:
            self.ai.owner = self
        
        # Lets items be usable
        if self.item:
            self.item.owner = self
            
        # Lets items be wearable
        if self.equipment: # Lets the Equipment component know who owns it
            self.equipment.owner = self
            self.item            = Item()
            self.item.owner      = self
            
    def move(self, dx, dy):
        """ Moves the player by the given amount if the destination is not blocked. """
        
        x = int((self.x + dx)/tile_width)
        y = int((self.y + dy)/tile_height)
        if not is_blocked(x, y):
            self.x                 += dx
            self.y                 += dy
            self.tile.entity       = None
            level_map[x][y].entity = self
            self.tile              = level_map[x][y]

    def move_towards(self, target_x, target_y):
        """ Moves object towards target. """
        
        dx       = target_x - self.x
        dy       = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx       = int(round(dx / distance)) * tile_width # Restricts to map grid
        dy       = int(round(dy / distance)) * tile_height
        self.move(dx, dy)
 
    def distance_to(self, other):
        """ Returns the distance to another object. """
        
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
      
    def distance(self, x, y):
        """ Returns the distance to some coordinates. """
        
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)      
      
    def send_to_back(self):
        """ Lets this object be drawn first, so all others appear above it if they're on the same tile. """
        
        global objects
        
        objects.remove(self)

        objects.insert(0, self)
       
    def draw(self, surface):
        """ Draws the object at its position. """
        
        surface.blit(self.image, (self.x-camera.x, self.y-camera.y))

class Fighter:
    """ Defines combat-related properties and methods (monster, player, NPC).
        Used by fighter_component, attack(), cast_lightning(), cast_fireball(), player_move_or_attack(), take_turn(),
        next_level(), go_home(), and cast_heal(). Can call player_death() and monster_death(). """
    
    def __init__(self, hp, defense, power, exp, death_function=None):
        """ Defines fighter stats. """
        
        self.max_hp         = hp                # initial health (integer)
        self.hp             = hp                # current health (integer)
        self.defense        = defense           # defense stat (integer)
        self.power          = power             # attack stat (integer)
        self.exp            = exp               # experience gained (integer, zero for player)
        self.death_function = death_function    # player death or monster death

    def save(self, filename):
        data = {
            'max_hp':         self.max_hp,
            'hp':             self.hp,
            'defense':        self.defense,
            'power':          self.power,
            'exp':            self.exp,
            'death_function': self.death_function}
        with open(filename, 'wb') as file:
            pickle.dump(data, file)
    
    def attack(self, target):
        """ Calculates and applies attack damage.
            Used by player_move_or_attack() and take_turn() for monsters. """
        
        if self.owner.name != target.name:                  # prevents self-inflicted damage
            damage = self.power - target.fighter.defense    # accounts for defense stats
            if damage > 0:                                  # damages the target
                message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')
                target.fighter.take_damage(damage)
            else:
                message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')

    def take_damage(self, damage):
        """ Applies damage if possible.
            Used by attack(), cast_lightning(), and cast_fireball().
            Calls player_death() or monster_death() if applicable. """
        
        if damage > 0:
            self.hp -= damage
            entity_flash(self.owner)
            if self.owner == player:
               update_gui()
            if self.hp <= 0:                    # checks for death
                self.hp = 0
                update_gui()
                function = self.death_function  # kills player or monster
                if function is not None:
                    function(self.owner)
                if self.owner != player:        # gives experience to the player
                    player.fighter.exp += self.exp
                    check_level_up()
    
    def heal(self, amount):
        """ Heals player by the given amount without going over the maximum.
            Used when leveling up, going home, or using a health item. """
        
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

class Item:
    """ Defines an item that can be picked up and used. """
    
    def __init__(self, use_function=None):
        self.use_function = use_function

    def pick_up(self):
        """ Adds an item to the player's inventory and removes it from the map. """
        
        global inventory_cache
        
        if len(inventory) >= 26:
            message('Your inventory is full, cannot pick up ' + self.owner.name + '.', red)
        else:
            inventory.append(self.owner)
            inventory_cache.append(self.owner.name)
            if self.owner in data_objects_1:
                index = data_objects_1.index(self.owner)
                data_objects_1.pop(index) # Removes item from home
                #home_object_positions.pop(index)
            objects.remove(self.owner)
            message('You picked up a ' + self.owner.name + '!', green)
            equipment = self.owner.equipment # Automatically equips item if possible
            if equipment and get_equipped_in_slot(equipment.slot) is None:
               equipment.equip()
       
        sort_inventory()

    def drop(self):
        """ Unequips item before dropping if the object has the Equipment component, then adds it to the map at
            the player's coordinates and removes it from their inventory.
            Dropped items are only saved if dropped in home. """
        
        if self.owner.equipment:
            self.owner.equipment.dequip()
        if player.dungeon_level == 0: # Saves dropped items at home
            data_objects_1.append(self.owner)
            home_object_positions.append([int(player.x/tile_width), int(player.y/tile_height)])
        objects.append(self.owner)
        inventory.remove(self.owner)
        #inventory_cache.remove(self.owner.name)
        self.owner.x = player.x
        self.owner.y = player.y
        player.tile.item = self.owner
        message('You dropped a ' + self.owner.name + '.', yellow)   

    def use(self):
        """ Equips of unequips an item if the object has the Equipment component. """
        
        global step_counter
        
        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return
        if self.use_function is None:
            message('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function() != 'cancelled':
                inventory.remove(self.owner) # Destroys item after use

class Equipment:
    """ Defines an object that can be equipped and yield bonuses. Automatically adds the Item component. """
    
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0, timer=False, name=None, is_equipped=False):
        """ Defines equipment and equipment parameters. """
        
        self.power_bonus   = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus  = max_hp_bonus
        self.slot          = slot
        self.is_equipped   = False
        self.timer         = timer
        self.name          = name

    def toggle_equip(self):
        """ Toggles the equip/unequip status. """
        
        if self.is_equipped:
            self.dequip()
        else:
            self.equip()

    def equip(self):
        """ Unequips object if the slot is already being used. """
        
        global step_counter, images
        
        old_equipment = get_equipped_in_slot(self.slot)
        if old_equipment is not None:
            old_equipment.dequip()
        self.is_equipped       = True
        player.fighter.power   += self.power_bonus
        player.fighter.defense += self.defense_bonus
        player.fighter.max_hp  += self.max_hp_bonus
        
        if self.name not in hair_list:
            message('Equipped ' + self.owner.name + ' on ' + self.slot + '.', light_green)
        
        if self.timer:
            step_counter[0] = True
            step_counter[1] += 1
            step_counter[3] = self.owner
        
        # Update player sprite
        for i in range(4):
            image_dict['player'][i] = image_dict_cache['player'][i]
        
        def custom_sort(item):
            try:
                return category_order.index(item.category)
            except ValueError:
                return len(category_order)
        sorted_inventory = sorted(inventory, key=custom_sort)
        
        for i in range(len(inventory)):
            if sorted_inventory[i].category in ["weapons", "apparel", "hair"]:
                if sorted_inventory[i].equipment.is_equipped:
                    for j in range(4):
                        overlay_image = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
                        overlay_image.blit(image_dict['player'][j], (0, 0))
                        overlay_image.blit(image_dict[sorted_inventory[i].name][j+1], (0, 0))
                        image_dict['player'][j] = overlay_image
        animate_sprites(key_cache)
        camera.update()

    def dequip(self):
        """ Unequips an object and shows a message about it. """
        
        global images
        
        if not self.is_equipped: return
        self.is_equipped       = False
        player.fighter.power   -= self.power_bonus
        player.fighter.defense -= self.defense_bonus
        player.fighter.max_hp  -= self.max_hp_bonus
        if player.fighter.hp > player.fighter.max_hp:
           player.fighter.hp = player.fighter.max_hp 
        message('Dequipped ' + self.owner.name + ' from ' + self.slot + '.', light_yellow)

        if self.timer:
            step_counter[0] = False
            
        # Update player sprite
        for i in range(4):
            image_dict['player'][i] = image_dict_cache['player'][i]
            
        def custom_sort(item):
            try:
                return category_order.index(item.category)
            except ValueError:
                return len(category_order)
        sorted_inventory = sorted(inventory, key=custom_sort)

        for i in range(len(inventory)):
            if sorted_inventory[i].category in ["weapons", "apparel", "hair"]:
                if sorted_inventory[i].equipment.is_equipped:
                    for j in range(4):
                        overlay_image = pygame.Surface((tile_width, tile_height), pygame.SRCALPHA)
                        overlay_image.blit(image_dict['player'][j], (0, 0))
                        overlay_image.blit(image_dict[sorted_inventory[i].name][j+1], (0, 0))
                        image_dict['player'][j] = overlay_image
        animate_sprites(key_cache)
        camera.update()

class BasicMonster:
    """ Defines the AI for a basic monster. """
    
    def take_turn(self):
        """ Lets a basic monster takes its turn. """
        
        monster = self.owner
        if monster.tile.visible:
            distance = monster.distance_to(player)
            if distance < 128:
                if (player.dungeon_level != 0) and (friendly == False):
                    if distance >= 64: # Moves towards player if far away
                        monster.move_towards(player.x, player.y)
                    elif player.fighter.hp > 0: # Attacks player once per 3 turns
                        if monster.counter == 0:
                            monster.fighter.attack(player)
                        elif monster.counter == 10:
                            monster.counter = -1
                        monster.counter += 1
                else:
                    if distance >= 100:
                        monster.move_towards(player.x, player.y)

class Tile:
    """ Defines a tile of the map and its parameters. Sight is blocked if a tile is blocked. 
        Used in make_home() and make_map(). """
    
    def __init__(self, blocked, x, y, block_sight=None, visible=False, explored=False, unbreakable=False, image=None, image_num=0):
        self.blocked = blocked
        if block_sight is None: block_sight = blocked # blocked makes walls, None makes floor
        self.block_sight = block_sight
        self.x           = x
        self.y           = y
        self.visible     = visible # True makes everything visible
        self.explored    = explored # True makes everything hidden
        self.room        = None
        self.entity      = None
        self.item        = None
        self.unbreakable = unbreakable
        self.image       = image
        self.image_num = image_num

class Rectangle:
    """ Defines rectangles on the map. Used to characterize a room. """
    
    def __init__(self, x, y, w, h):
        """ Defines a rectangle and its size. """
        
        self.x1       = x
        self.y1       = y
        self.x2       = x + w
        self.y2       = y + h
        self.explored = False # False for visible, True for hidden

    def center(self):
        """ Finds the center of the rectangle. """
        
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return (center_x, center_y)
 
    def intersect(self, other):
        """ Returns true if this rectangle intersects with another one. """
        
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)        

class Camera:
    """ Defines a camera to follow the player. """
    
    def __init__(self, target):
        """ Defines a camera and its parameters. """
        
        self.target          = target
        self.width           = screen_width
        self.height          = screen_height + tile_height
        self.x               = self.target.x - int(self.width / 2)
        self.y               = self.target.y - int(self.height / 2)
        self.center_x        = self.x + int(self.width / 2)
        self.center_y        = self.y + int(self.height / 2)
        self.right           = self.x + self.width
        self.bottom          = self.y + self.height
        self.tile_map_x      = int(self.x / tile_width)
        self.tile_map_y      = int(self.y / tile_height)
        self.tile_map_width  = int(self.width / tile_width)
        self.tile_map_height = int(self.height / tile_height)
        self.x_range         = self.tile_map_x + self.tile_map_width
        self.y_range         = self.tile_map_y + self.tile_map_height
        self.fix_position()
        
    def update(self):
        """ ? """
        
        if self.target.x != self.center_x:
            x_move          = self.target.x - self.center_x
            self.x          += x_move
            self.center_x   += x_move
            self.right      += x_move
            self.tile_map_x = int(self.x / tile_width)
            self.x_range    = self.tile_map_x + self.tile_map_width
        #if self.y > 0 and  self.target.y < self.center_y \
        #or self.bottom < map_height and  self.target.y > self.center_y:
        if self.target.y != self.center_y:   
            y_move          = self.target.y - self.center_y
            self.y          += y_move
            self.center_y   += y_move
            self.bottom     += y_move
            self.tile_map_y = int(self.y / tile_height)
            self.y_range    = self.tile_map_y + self.tile_map_height
        self.fix_position()

    def fix_position(self):
        """ ? """
        
        if player.dungeon_level != 0:
            if self.x < 0:
               self.x          = 0
               self.center_x   = self.x + int(self.width / 2)
               self.right      = self.x + self.width
               self.tile_map_x = int(self.x / tile_width)
               self.x_range    = self.tile_map_x + self.tile_map_width
            elif self.right > map_width:
               self.right      = map_width
               self.x          = self.right - self.width
               self.center_x   = self.x + int(self.width / 2)
               self.tile_map_x = int(self.x / tile_width)
               self.x_range    = self.tile_map_x + self.tile_map_width
            if self.y < 0:
               self.y          = 0
               self.center_y   = self.y + int(self.height / 2)
               self.bottom     = self.y + self.height
               self.tile_map_y = int(self.y / tile_height)
               self.y_range    = self.tile_map_y + self.tile_map_height
            elif self.bottom > map_height:
               self.bottom     = map_height
               self.y          = self.bottom - self.height
               self.center_y   = self.y + int(self.height / 2)
               self.tile_map_y = int(self.y / tile_height)
               self.y_range    = self.tile_map_y + self.tile_map_height

class Questlog:
    
    def __init__(self, quests, achievements=None):
        self.selected_quest = quests[0]
        self.menu_index = 0

        self.quests = quests
        self.categories_type = []
        self.main_quests = []
        self.side_quests = []
        self.achievements = achievements

    def back_to_menu(self):
        if self.menu_index == 0:
            self.menu_index += 1
        else:
            self.menu_index = 0
    
    def update_quests(self):
        self.main_quests = []
        self.side_quests = []
        self.quest_names = []
        self.categories = []
        
        for quest in self.quests:
            if quest.category == 'Main':
                self.main_quests.append(quest)
            else:
                self.side_quests.append(quest)
            self.quest_names.append(quest.name)
            self.categories_type.append(quest.category)
            
    def update_quest(self, name=None):
        self.categories_content = []
        
        for i in range(len(self.selected_quest.content)):
            if self.selected_quest.content[i][0] not in ['☐', '☑']:
                self.categories_content.append('Notes')
            else:
                self.categories_content.append('Objectives')
        
        if name:
            for i in range(len(self.quests)):
                if self.quests[i].name == name:
                    for j in range(len(self.quests[i].content)):
                        if (j != 0) and (self.quests[i].content[j][0] == '☐'):
                            self.quests[i].content[j] = self.quests[i].content[j].replace('☐', '☑', 1)
                            break
   
class Quest:

    def __init__(self, name='', content=[], category='main'):
        """ name       : string; title of quest
            content    : list of strings; notes and checklists
            category   : string in ['main', 'side']; organizes quest priority
            finished   : Boolean; notes if the quest has been completed """

        self.name = name
        self.content = content
        self.category = category
        self.finished = False

#######################################################################################################################################################
# WIP
def __WIP__():
    pass

def make_tutorial():
    """ Initializes and generates the player's home, its rooms, and its contents. """
    
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    global level_map, objects, stairs, new_game_trigger
    
    # Start music track
    audio_control(new_track=home_music)
    
    objects = [player] # holds objects in home
    
    # Defines the map. [[x for x in range(2)] for y in range(3)] yields [[0,1], [0,1], [0,1]], for example.
    level_map = [[ Tile(True, x, y, visible=False, image='walls') # initialize walls at each point in the map
                for y in range(0, map_height*5, tile_height) ]
                for x in range(0, map_width*5, tile_width) ]
    
    # Create main room
    main_room = Rectangle(10, 10, room_max_size, room_max_size) 
    create_room(main_room)
    (new_x, new_y) = main_room.center()
    
    # Create secret room
    secret_room = Rectangle(30, 30, room_min_size*2, room_min_size*2) 
    create_room(secret_room, block_sight=True, unbreakable=True)
    
    # Place player
    player.x                       = new_x * tile_width
    player.y                       = new_y * tile_height
    level_map[new_x][new_y].entity = player
    player.tile                    = level_map[new_x][new_y]
    check_tile(new_x, new_y)
    new_x, new_y                   = new_x + 3, new_y # Sets the position for the stairs
    place_objects(main_room, home=True, fresh_start=new_game_trigger) # Adds content to the room
    if new_game_trigger:
        new_game_trigger = False

def dialogue(init=False, NPC_name=None):
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")

    global friend_messages, friend_level, NPC_names

    # -------------------------------------- INIT --------------------------------------
    # Initialize dialogue
    if init:
        
        # Set NPC names
        NPC_names = ['friend']
        
        # Initialize friend dialogue
        friend_messages, friend_level = {}, 1
        
        # Friend: level 1
        cache_list = []
        for i in range(34):
            if i < 30:
                cache_list.append("Who is this, anyways?")
                cache_list.append("")
                cache_list.append("")
            else:
                cache_list.append("Your new friend seems bored.")
                cache_list.append("Your new friend gazes deeply into the distance.")
                cache_list.append("Your new friend looks nervous.")
                cache_list.append("You give your new friend a playful nudge.")
        friend_messages['level 1'] = cache_list
        
        # Friend: level 2
        cache_list = []
        for i in range(34):
            if i < 30:
                cache_list.append("Your friend looks happy to see you.")
                cache_list.append("")
                cache_list.append("")
            else:
                cache_list.append("Why are you here?")
                cache_list.append("Your friend seems friendlier now.")
                cache_list.append("Who is this, anyways?")
                cache_list.append("You give your friend a playful nudge.")
        friend_messages['level 2'] = cache_list

        # Friend: level 3
        cache_list = []
        for i in range(34):
            if i < 30:
                cache_list.append("Your friend seems excited.")
                cache_list.append("")
                cache_list.append("")
            else:
                cache_list.append("Your friend feels calmer in your presence.")
                cache_list.append("Your friend fidgets but seems content.")
                cache_list.append("Who is this, anyways?")
                cache_list.append("You give your friend a playful nudge.")
        friend_messages['level 3'] = cache_list
    
    # -------------------------------------- QUEST --------------------------------------
    elif NPC_name == 'friend':
        
        # Increase friendship
        friend_level += 0.1
        if friend_level == 1.1:
            message("☑ You say hello to your new friend.", white)
            questlog.update_quest(name="Making a friend")
        
        if int(friend_level) <= 3:
            message(friend_messages[f'level {int(friend_level)}'][random.randint(0, len(friend_messages[f'level {int(friend_level)}']))], white)
        else:
            if random.randint(0,10) != 1:
                message(friend_messages[f'level {int(friend_level)}'][random.randint(0, len(friend_messages[f'level {int(friend_level)}']))], white)
            else:
            
                # Start quest
                message("Woah! What's that?", white)
                x = lambda dx : int((player.x + dx)/tile_width)
                y = lambda dy : int((player.y + dy)/tile_height)

                found = False
                for i in range(3):
                    if found:
                        break
                    x_test = x(tile_width*(i-1))
                    for j in range(3):
                        y_test = y(tile_height*(j-1))
                        if not level_map[x_test][y_test].entity:
                            item_component = Item(use_function=mysterious_note)
                            item = Object(
                                        0,
                                        0,
                                        image_dict['scrolls'][0],
                                        name="mysterious note", category="scrolls", image_num=0,
                                        item=item_component,
                                        appended='objects')
                            data_objects_1.append(item)
                            home_object_positions.append([x_test, y_test])
                            objects.append(item)
                            level_map[x_test][y_test].item = item
                            found = True
                            break
        pygame.event.clear()

def mysterious_note():
    global questlog

    note_text = ["ξνμλ λξ ξλι ξγθιβξ ξ θθ.", "Ηκρσ σρσ λβνξθι νθ.", "Ψπθ αβνιθ πθμ."]
    new_menu(header="mysterious note", options=note_text, position="top left")
    message('Quest added!', green)
    mysterious_note = Quest(name='Mysterious note',
                         content=['My green friend dropped this. It has a strange encryption.',
                                  'ξνμλ λξ ξλι ξγθιβξ ξ θθ,', 'Ηκρσ σρσ λβνξθι νθ,', 'Ψπθ αβνιθ πθμ.',
                                  '☐ Keep an eye out for more mysterious notes.'],
                         category='Main')

def movement_speed(adjust=False, move=False):
    global movement_speed_toggle
    
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    if adjust:
        if movement_speed_toggle == len(toggle_list)-1: 
            movement_speed_toggle = 0
        else:
            movement_speed_toggle += 1
        
        if toggle_list[movement_speed_toggle] == 'Default':
            pygame.key.set_repeat(250, 150)
            message(f"Movement speed: Default", blue)
        elif toggle_list[movement_speed_toggle] == 'Slow':
            pygame.key.set_repeat(0, 0)
            message(f"Movement speed: Fixed", white)
        else:
            pygame.key.set_repeat(175, 150)
            message(f"Movement speed: Fast", red)

def screenshot(lvl_width=1, lvl_height=1, cache=False, save=False, blur=False, big=False):
    """ Takes a screenshot.
        cache:  saves a regular screenshot under Data/Cache/screenshot.png
        save:   moves regular cached screenshot to Data/File_#/screenshot.png 
        blur:   adds a blur effect """
    
    global screen, gui_on, message_log, message_log_toggle, screenshot_time_counter
    
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}\tcache={cache}\tsave={save}\tbig={big}")

    gui_on, message_log, message_log_toggle = False, False, False
    
    # Takes a screenshot whenever the menu is opened
    if cache:
        render_all()
        
        # Saves regular screenshot in Data
        destination_folder = 'Data/Cache'
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        destination_path = os.path.join(destination_folder, "screenshot.png")
        
        pygame.image.save(screen, destination_path)
    
    if save:
        render_all()
        
        # Moves cached screenshot to Data/File_{index}
        destination_folder = f"Data/File_{load_saves[0][10]}"
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        destination_path = os.path.join(destination_folder, "screenshot.png")
        
        shutil.move("Data/Cache/screenshot.png", destination_path)
        
        # Adds an effect: blur
        if blur:
            image_before = Image.open(f"Data/File_{load_saves[0][10]}/screenshot.png")
            image_after  = image_before.filter(ImageFilter.BLUR)
            image_after.save(f"Data/File_{load_saves[0][10]}/screenshot.png")
            print("BLURRED................")
    
    # Takes a screenshot of the entire map, not just the screen
    if big:
        camera_cache = [camera.x, camera.y]
            
        # Generate full screen with visible tiles
        screen = pygame.display.set_mode((len(level_map[0])*16, len(level_map)*16),)
        render_all(screenshot=True, visible=True)
        camera.x = 0
        camera.y = 0
        camera.update()
        
        # Save as is
        pygame.image.save(screen, "screenshot_visible.png") # pygame.Surface((map_width, map_height))
        destination_folder = "Data/Cache"
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        destination_path = os.path.join(destination_folder, "screenshot_visible.png")
        shutil.move("screenshot_visible.png", destination_path)
        #save_floor('screenshot_visible.pkl')
        
        if player.dungeon_level == 0:
            save_objects_to_file('screenshot_objects.pkl', data_source=data_objects_1)
        else:
            save_objects_to_file('screenshot_objects.pkl', data_source=objects)
        destination_folder = "Data/Cache"
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        destination_path = os.path.join(destination_folder, "screenshot_objects.pkl")
        shutil.move("screenshot_objects.pkl", destination_path)
        
        screen = pygame.display.set_mode((screen_width, screen_height),)
        render_all()
        camera.x = camera_cache[0]
        camera.y = camera_cache[1]
        camera.update()
    gui_on, message_log, message_log_toggle = True, True, True

#######################################################################################################################################################
# Global scripts
if __name__ == "__main__":
    main()

#######################################################################################################################################################