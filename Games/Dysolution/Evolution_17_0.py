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
## Other
home_map                = []
home_object_positions   = []
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

#######################################################################################################################################################
# Startup
def __STARTUP__():
    pass

## Initialization
def main():
    """ Initializes pygame, calls initialize_images() to load tileset, ???, and opens the main menu.
        Called at startup. """

    global blank_surface, impact_image, impact_image_pos, impact
    
    global pyg, mech, img, aud, player_obj
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    # Initialize basics
    pyg  = Pygame()
    mech = Mechanics()
    img  = Images()
    aud  = Audio()
    player_obj = Player()
    
    #with open("player_obj.pkl", "wb") as file:
    #    pickle.dump(player_obj, file)
    
    #with open("player_obj.pkl", "rb") as file:
    #    player_obj = pickle.load(file)
    
    # ??? Used in combat
    blank_surface = pygame.Surface((pyg.tile_width, pyg.tile_height)).convert()
    blank_surface.set_colorkey(blank_surface.get_at((0,0)))
    impact_image = get_impact_image()
    impact_image_pos = [0,0]
    impact = False
    
    main_menu() # Opens the main menu

## Gameplay and utility
def new_game(new):
    """ Initializes NEW GAME. Does not handle user input. Resets player stats, inventory, map, and rooms.
        Called when starting a new game or loading a previous game.

        new:  creates player as Object with Fighter stats, calls make_home(), then loads initial inventory
        else: calls load_objects_from_file() to load player, inventory, and current floor """
    
    global player, camera, game_state, player_action
    global inventory
    global data_objects_1, home_object_positions, new_game_trigger, save_objects
    global active_effects_cache, friendly, teleport, inventory_cache, dig, step_counter
    global questlog
    if debug: print(f"{debug_call()[0]:<30}{new}")

    # -------------------------------------- INIT --------------------------------------
    game_state                            = 'dead' # as opposed to 'playing'
    inventory                             = []
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
        friend_quest(init=True)

        # Generate new player
        fighter_component = Fighter(hp=100, defense=100, power=100, exp=0, death_function=player_death)
        obj = Object(
              name        = 'player',
              image       = img.dict['player'][0],
              x           = pyg.tile_width*10,
              y           = pyg.tile_height*7,
              category    = "player",
              blocks      = True,
              fighter     = fighter_component,
              hp          = 100,
              defense     = 100,
              power       = 100,
              tile        = True,
              player_lvl  = 1,
              dungeon_lvl = 0)
        player_obj.obj = obj
        
        # Generate questlog and default quests
        questlog = Questlog()
        
        # Generate map and sets the player in a room
        build_home()
        place_player(env=player_obj.home, loc=player_obj.home.center)
    
    # -------------------------------------- LOAD --------------------------------------
    else:
        load_objects_from_file(load_saves[0])
        load_objects_from_file(load_saves[2], data_objects_1)
        load_objects_from_file(load_saves[4], inventory)
        inventory_cache = inventory.copy()
        if player_obj.obj.dungeon_lvl != 0:
            load_floor(load_saves[3], aud.home[0], load_objects_file='Data/data_dungeon_obj.pkl')
        else:
            load_floor(load_saves[1], aud.home[0], load_objects_file=load_saves[2], home=True)
            #load_floor('screenshot_hidden.pkl', aud.home[0], home=True, load_objects_file='screenshot_objects.pkl')
    
    camera = Camera(player_obj.obj)
    camera.update()
    
    game_state = 'playing' # as opposed to 'dead'
    player_action = 'didnt-take-turn' 
    
    pyg.update_gui() # places health and dungeon level on the pyg.screen
    message('Welcome!', pyg.red)
    
    # -------------------------------------- NEW --------------------------------------
    # Sets initial inventory
    if new:
    
        # Create items
        armor = create_objects('clothes', [0, 0])
        shovel = create_objects('shovel', [0, 0])
        dagger = create_objects('dagger', [0, 0])
        hair = create_objects('wig', [0, 0])
        
        # Add to inventory
        inventory.append(armor)
        inventory.append(dagger)
        inventory.append(shovel)
        inventory.append(hair)
        inventory_cache.append('armor')
        inventory_cache.append('dagger')
        inventory_cache.append('shovel')
        inventory_cache.append('hair')
        step_counter[3] = shovel
        dagger.equipment.equip()
        armor.equipment.equip()
        hair.equipment.equip()
    
    sort_inventory()

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

## Classes
class Pygame:
    """ Pygame stuff. Does not need to be saved, but update_gui should be run after loading a new file. """

    def __init__(self):
        
        # Graphics parameters
        self.screen_width      = 640
        self.screen_height     = 480
        self.tile_width        = 32
        self.tile_height       = 32
        self.map_width         = 640 * 2
        self.map_height        = 480 * 2
        self.tile_map_width    = int(self.map_width/self.tile_width)
        self.tile_map_height   = int(self.map_height/self.tile_height)

        # Graphics overlays
        self.msg_toggle        = True # Boolean; shows or hides messages
        self.msg               = []   # list of font objects; messages to be rendered
        self.gui_toggle        = True # Boolean; shows or hides GUI
        self.gui               = None # font object; stats to be rendered

        # Colors
        self.black             = pygame.color.THECOLORS['black']
        self.gray              = pygame.color.THECOLORS['gray90']
        self.white             = pygame.color.THECOLORS['white']
        self.red               = pygame.color.THECOLORS['orangered3']
        self.green             = pygame.color.THECOLORS['palegreen4']
        self.blue              = pygame.color.THECOLORS['blue']
        self.yellow            = pygame.color.THECOLORS['yellow']
        self.orange            = pygame.color.THECOLORS['orange']
        self.violet            = pygame.color.THECOLORS['violet']
        self.light_cyan        = pygame.color.THECOLORS['lightcyan']
        self.light_green       = pygame.color.THECOLORS['lightgreen']
        self.light_blue        = pygame.color.THECOLORS['lightblue']
        self.light_yellow      = pygame.color.THECOLORS['lightyellow']
        
        # Controls
        self.key_0             = [K_0,     K_KP0, K_ESCAPE] # back
        self.key_1             = [K_1,     K_KP1]           # stats
        self.key_2             = [K_2,     K_KP2]           # inventory (equip)
        self.key_3             = [K_3,     K_KP3]           # inventory (drop)
        self.key_4             = [K_4,     K_KP4]           # quests
        self.key_5             = [K_5,     K_KP5]           # movement speed
        self.key_6             = [K_6,     K_KP6]           # screenshot
        self.key_UP            = [K_UP,    K_w]             # movement (up)
        self.key_DOWN          = [K_DOWN,  K_s]             # movement (down)
        self.key_LEFT          = [K_LEFT,  K_a]             # movement (left)
        self.key_RIGHT         = [K_RIGHT, K_d]             # movement (right)
        self.key_RETURN        = [K_RETURN]                 # activate
        self.key_SLASH         = [K_SLASH]                  # messages
        
        # Pygame initialization
        pygame.init()
        pygame.display.set_caption("Evolution") # Sets game title
        self.screen            = pygame.display.set_mode((self.screen_width, self.screen_height),)
        self.font              = pygame.font.SysFont('segoeuisymbol', 16, bold=True)
        self.clock             = pygame.time.Clock()

    def update_gui(self):
        self.gui = self.font.render('HP: '            + str(player_obj.obj.fighter.hp) + '/' + str(player_obj.obj.fighter.max_hp) +  ' '*60 + 
                                    'Dungeon level: ' + str(player_obj.obj.dungeon_lvl),
                                    True, pyg.yellow)

class Mechanics:
    """ Game parameters. Does not need to be saved. """
    
    def __init__(self):
        
        self.room_max_size     = 10
        self.room_min_size     = 4
        self.max_rooms         = 3

        ## Player parameters
        self.heal_amount       = 4
        self.lightning_damage  = 20
        self.lightning_range   = 5 * pyg.tile_width
        self.confuse_range     = 8 * pyg.tile_width
        self.confuse_num_turns = 10
        self.fireball_radius   = 3 * pyg.tile_width
        self.fireball_damage   = 12

        self.level_up_base     = 200
        self.level_up_factor   = 150

        self.torch_radius      = 10

        ## GUI
        self.message_width     = int(pyg.screen_width / 6)
        self.message_height    = 3

    def next_level(self):
        """ Advances player to the next level. """
        if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
        
        message('You take a moment to rest, and recover your strength.', pyg.violet)
        player_obj.obj.fighter.heal(int(player_obj.obj.fighter.max_hp / 2))  #heal the player by 50%
        
        # Change music and dungeon level
        player_obj.obj.dungeon_lvl = player_obj.obj.dungeon_lvl + 1
        aud.control(new_track=aud.dungeons[player_obj.obj.dungeon_lvl])
        
        # Generate dungeon
        time.sleep(0.5)
        message('After a rare moment of peace, you descend deeper into the heart of the dungeon...', pyg.red)
        build_dungeon_level()
        
        # Place player and update screen
        place_player(env=player_obj.dungeons[-1], loc=player_obj.dungeons[-1].center)
        camera.update()
        time.sleep(0.5)
        pyg.update_gui()

class Images:
    """ Loads images from png file and sorts them in a global dictionary. One save for each file.

        The tileset (tileset.png) is organized in rows, with each row being a category identified below
        by the categories list. This function breaks the tileset into individual tiles and adds each tile
        to its respective category in a global dictionary for later use.
        
        img.dict:        mutable dictionary sorted by category
        img.dict_cache:  less mutable than img.dict """
    
    def __init__(self):
        
        # Data containers
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
        self.dict       = {category: [] for category in categories}
        self.dict_cache = {category: [] for category in categories}

        rogue_tiles = pygame.image.load('Data/tileset.png').convert_alpha()
        rows        = rogue_tiles.get_height() // pyg.tile_height
        columns     = rogue_tiles.get_width() // pyg.tile_width
    
        # Sort images and import as subsurfaces
        for row in range(rows):
            row_images, row_images_cache = [], []
            for col in range(columns):
                x           = col * pyg.tile_width
                y           = row * pyg.tile_height
                image       = rogue_tiles.subsurface(x, y, pyg.tile_width, pyg.tile_height).convert_alpha()
                image_cache = rogue_tiles.subsurface(x, y, pyg.tile_width, pyg.tile_height).convert_alpha()
                row_images.append(image)
                row_images_cache.append(image_cache)
            self.dict[categories[row]] = row_images
            self.dict_cache[categories[row]] = row_images_cache
        self.dict['null'] = self.dict['scrolls'][3:8]
        self.dict_cache['null'] = self.dict_cache['scrolls'][3:8]

class Audio:
    """ Manages audio. One save for each file. """

    def __init__(self):
        
        # Initialize music player
        pygame.mixer.init()
        
        self.menu = []
        self.home = []
        self.dungeons = [None]

        self.menu.append(pygame.mixer.Sound("Data/music_menu.mp3"))
        self.home.append(pygame.mixer.Sound("Data/music_home.mp3"))
        self.dungeons.append(pygame.mixer.Sound("Data/music_dungeon_1.mp3"))
        self.dungeons.append(pygame.mixer.Sound("Data/music_dungeon_2.mp3"))

        # Start music
        self.current_track = self.menu[0]
        self.current_track.play()

        self.shuffle = False

    def control(self, new_track=None):
        
        if self.shuffle:
            pass
        elif (new_track is not None) and (new_track is not self.current_track):
            #for i in range(len(track_list)):
            #    if (track_list[i] == current_track):
            #        current_track.stop()
            pygame.mixer.fadeout(4000)
            new_track.play(fade_ms=4000)
            self.current_track = new_track

class Player:
    """ Manages player file. One save for each file. """

    def __init__(self, env=None):
        """ Holds everything regarding the player.
            Parameters
            ----------
            env      : Environment object; current environment
            home     : Environment object; player's home
            dungeons : list of Environment objects; dungeon levels """
        
        self.env      = None
        self.home     = Environment(size='medium', soundtrack=[aud.home[0]])
        self.dungeons = []
        self.handedness = None
    
    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("home", None)
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        #self.home = Environment(size='medium', soundtrack=[aud.home[0]])

#######################################################################################################################################################
# Player actions
def main_menu():
    """ Manages the menu. Handles player input. Only active when the main menu is open.
        Called by main(), file_menu(), and character_creation(). Indirectly called by play_game(). """
    
    global startup, load_saves, new_game_index, game_title, startup_toggle
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    # -------------------------------------- INIT --------------------------------------
    # Initialize time and music
    aud.control(new_track=aud.menu[0])
    
    # Load background image
    background_image = pygame.image.load("Data/image_main.png").convert()
    background_image = pygame.transform.scale(background_image, (pyg.screen_width, pyg.screen_height))  # Scale to fit the pyg.screen

    # Initialize title
    title_font = pygame.font.SysFont('segoeuisymbol', 40, bold=True)
    game_title = title_font.render("EVOLUTION", True, pyg.green)  # Sets game title
    game_title_pos = (int((pyg.screen_width - game_title.get_width())/2), 85)
    
    # Initialize cursor
    cursor_img = pygame.Surface((16, 16)).convert()
    cursor_img.set_colorkey(cursor_img.get_at((0, 0)))
    pygame.draw.polygon(cursor_img, pyg.green, [(0, 0), (16, 8), (0, 16)], 0)
    cursor_img_pos = [50, 304]
    
    # Initialize menu options
    menu_choices = ["NEW GAME", "LOAD", "SAVE", "CONTROLS", "QUIT"]
    menu_choices_surfaces = []  # To store rendered text surfaces
    for i in range(len(menu_choices)):
        if i == 0:
            color = pyg.green
        elif i == len(menu_choices) - 1:
            color = pyg.red
        else:
            color = pyg.gray
        menu_choices_surfaces.append(pyg.font.render(menu_choices[i], True, color))
    
    choice, choices_length = 0, len(menu_choices) - 1

    if startup_toggle:
        
        # Initialize alpha for fade effect
        alpha = 0  # Starting alpha value for fade-in
        fade_speed = 5  # Speed of fading in

        # -------------------------------------- FADE IN --------------------------------------
        # Fade-in loop
        fade_surface = pygame.Surface((pyg.screen_width, pyg.screen_height))
        fade_surface.fill(pyg.black)
        
        while alpha < 255:
            pyg.clock.tick(30)
            fade_surface.set_alpha(255 - alpha)  # Adjust alpha to create the fade-in effect
            
            # Set menu background to the custom image
            pyg.screen.blit(background_image, (0, 0))

            # Draw the menu elements during the fade
            y = 300
            for menu_choice_surface in menu_choices_surfaces:
                pyg.screen.blit(menu_choice_surface, (80, y))
                y += 24
            pyg.screen.blit(game_title, game_title_pos)
            pyg.screen.blit(cursor_img, cursor_img_pos)

            # Apply the fade effect
            pyg.screen.blit(fade_surface, (0, 0))
            
            pygame.display.flip()
            
            # Increase alpha for the next frame
            alpha += fade_speed
            
        startup_toggle = False

    else:
        # Set menu background to the custom image
        pyg.screen.blit(background_image, (0, 0))

        # Draw the menu elements during the fade
        y = 300
        for menu_choice_surface in menu_choices_surfaces:
            pyg.screen.blit(menu_choice_surface, (80, y))
            y += 24
        pyg.screen.blit(game_title, game_title_pos)
        pyg.screen.blit(cursor_img, cursor_img_pos)

        pygame.display.flip()

    # -------------------------------------- MENU --------------------------------------
    # Allow player to select menu option
    while True:
        pyg.clock.tick(30)

        # Called when the user inputs a command
        for event in pygame.event.get():

            if event.type == KEYDOWN:
            
                # >>RESUME<<
                if event.key in pyg.key_0:
                    play_game()
                
                # >>SELECT MENU ITEM<<
                elif event.key in pyg.key_UP:
                    cursor_img_pos[1] -= 24
                    choice -= 1
                    if choice < 0:
                        choice = choices_length
                        cursor_img_pos[1] = 304 + (len(menu_choices) - 1) * 24
                elif event.key in pyg.key_DOWN:
                    cursor_img_pos[1] += 24
                    choice += 1
                    if choice > choices_length:
                        choice = 0
                        cursor_img_pos[1] = 304
                
                elif event.key in pyg.key_RETURN:

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
                        save_objects_to_file(load_saves[0], data_source=[player_obj.obj])
                        save_objects_to_file(load_saves[4], data_source=inventory)
                        
                        # Save image for loading pyg.screen
                        screenshot(cache=True, save=True, blur=True)
                        
                        # Save current floor
                        if player_obj.obj.dungeon_lvl == 0:
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
        pyg.screen.blit(background_image, (0, 0))
        
        # Renders menu to update cursor location
        y = 300
        for menu_choice_surface in menu_choices_surfaces:
            pyg.screen.blit(menu_choice_surface, (80, y))
            y += 24
        pyg.screen.blit(game_title, game_title_pos)
        pyg.screen.blit(cursor_img, cursor_img_pos)
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
    header_position    = {"top left": [5,   10],             "center": (int((pyg.screen_width - game_title.get_width())/2), 85)}
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
    pygame.draw.polygon(cursor_img, pyg.green, [(0, 0), (16, 8), (0, 16)], 0)
    
    # Initialize menu options
    header = pyg.font.render(header, True, pyg.yellow)
    for i in range(len(options)):
        color = pyg.gray
        options_render[i] = pyg.font.render(options[i], True, color)
    
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
            pyg.screen.fill(pyg.black)
            pyg.screen.blit(backgrounds[choice], (0, 0))
        else:
            pyg.screen.fill(pyg.black)
        
        # Render header and cursor
        pyg.screen.blit(header, header_position[position])
        pyg.screen.blit(cursor_img, cursor_position_mutable)
        
        # Render categories and options
        for i in range(len(options_render)):
            
            # Render category text if it is not present 
            if options_categories:
                if options_categories[i] != options_categories_cache:
                    options_categories_cache = options_categories[i]
                    text = pyg.font.render(f'{options_categories_cache.upper()}:', True, pyg.gray)
                    options_positions_mutable[1] += tab_y
                    pyg.screen.blit(text, (category_positions_mutable[0], options_positions_mutable[1]))
                
            # Render option text
            pyg.screen.blit(options_render[i], options_positions_mutable)
            options_positions_mutable[1] += 24
        options_positions_mutable = options_positions[position].copy()
        category_positions_mutable = category_positions[position].copy()
        pygame.display.flip()
        
        # Called when the user inputs a command
        for event in pygame.event.get():
            if event.type == KEYDOWN:

                # >>RESUME<<
                if event.key in pyg.key_0:
                    return False
                
                # >>SELECT MENU ITEM<<
                if event.key in pyg.key_UP:
                
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
                
                elif event.key in pyg.key_DOWN:
                
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
                            
                elif event.key in pyg.key_RETURN:
                    return choice

def character_creation():
    """ Manages the character creation menu. Handles player input. Only active when menu is open.
        Called when starting a new game.
    
        HAIR:       sets hair by altering hair_index, which is used in new_game to add hair as an Object hidden in the inventory
        HANDEDNESS: mirrors player/equipment tiles, which are saved in img.dict and img.dict_cache
        ACCEPT:     runs new_game() to generate player, home, and default items, then runs play_game() """
    
    global startup, load_saves, hair_index, skin_index, handedness_index, new_game_index
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    # -------------------------------------- INIT --------------------------------------
    # Initialize cursor
    cursor_img = pygame.Surface((16, 16)).convert()
    cursor_img.set_colorkey(cursor_img.get_at((0,0)))
    pygame.draw.polygon(cursor_img, pyg.green, [(0, 0), (16, 8), (0, 16)], 0)
    cursor_img_pos = [50, 304]
    
    # Set character background
    background_image = pygame.image.load("Data/room.png")
    rotation_indices = [0, 0, [0, 2, 1, 3]] # used for rotating character in menu

    # Initialize menu options
    menu_choices = ["HAIR", "HANDEDNESS", "", "ACCEPT", "BACK"]   
    for i in range(len(menu_choices)):
        if   i == len(menu_choices)-2:  color = pyg.green
        elif i == len(menu_choices)-1:  color = pyg.red
        else:                           color = pyg.gray
        menu_choices[i] = pyg.font.render(menu_choices[i], True, color)
    choice, choices_length = 0, len(menu_choices)-1
    
    # Begins with default settings (ideally)
    for i in range(4):
        img.dict['player'][i]   = img.dict_cache['player'][i]
        img.dict['dagger'][i+1] = img.dict_cache['dagger'][i+1]
    hair_index = 1
    
    # -------------------------------------- MENU --------------------------------------
    # Allow player to select menu option
    while True:
        pyg.clock.tick(30)
        
        # Prevent escape from going back to character creation
        if new_game_index == 1:
            return
        
        # Called when the user inputs a command
        for event in pygame.event.get():

            if event.type == KEYDOWN:
            
                # >>MAIN MENU<<
                if event.key in pyg.key_0:
                    main_menu()
                
                # >>SELECT MENU ITEM<<
                elif event.key in pyg.key_UP:   # Up
                    cursor_img_pos[1]     -= 24
                    choice                -= 1
                    if choice < 0:
                        choice            = choices_length
                        cursor_img_pos[1] = 304 + (len(menu_choices)-1) * 24
                    elif choice == (choices_length - 2):
                        choice = choices_length - 3
                        cursor_img_pos[1] = 304 + (len(menu_choices)-4) * 24
                elif event.key in pyg.key_DOWN: # Down
                    cursor_img_pos[1]     += 24
                    choice                += 1
                    if choice > choices_length:
                        choice            = 0
                        cursor_img_pos[1] = 304
                    elif choice == (choices_length - 2):
                        choice = choices_length - 1
                        cursor_img_pos[1] = 304 + (len(menu_choices)-2) * 24
                elif event.key in pyg.key_RETURN:
                
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
                        player_cache = pygame.transform.flip(img.dict['player'][2], True, False)
                        dagger_cache = pygame.transform.flip(img.dict['dagger'][3], True, False)
                        hair_cache = pygame.transform.flip(img.dict_cache['hair'][3], True, False)
                        img.dict['player'][0] = pygame.transform.flip(img.dict['player'][0], True, False)
                        img.dict['player'][1] = pygame.transform.flip(img.dict['player'][1], True, False)
                        img.dict['player'][2] = pygame.transform.flip(img.dict['player'][3], True, False)
                        img.dict['player'][3] = player_cache
                        img.dict['dagger'][1] = pygame.transform.flip(img.dict['dagger'][1], True, False)
                        img.dict['dagger'][2] = pygame.transform.flip(img.dict['dagger'][2], True, False)
                        img.dict['dagger'][3] = pygame.transform.flip(img.dict['dagger'][4], True, False)
                        img.dict['dagger'][4] = dagger_cache
                        img.dict_cache['hair'][1] = pygame.transform.flip(img.dict_cache['hair'][1], True, False)
                        img.dict_cache['hair'][2] = pygame.transform.flip(img.dict_cache['hair'][2], True, False)
                        img.dict_cache['hair'][3] = pygame.transform.flip(img.dict_cache['hair'][4], True, False)
                        img.dict_cache['hair'][4] = hair_cache
                    
                    # >>ACCEPT<<
                    if choice == 3:
                        if handedness_list[handedness_index] == 'right':
                            for item in img.dict:
                                if item == 'player':
                                    player_cache = pygame.transform.flip(img.dict_cache['player'][2], True, False)
                                    img.dict_cache['player'][0] = pygame.transform.flip(img.dict_cache['player'][0], True, False)
                                    img.dict_cache['player'][1] = pygame.transform.flip(img.dict_cache['player'][1], True, False)
                                    img.dict_cache['player'][2] = pygame.transform.flip(img.dict_cache['player'][3], True, False)
                                    img.dict_cache['player'][3] = player_cache
                                elif item not in ['monsters', 'stairs', 'walls', 'floors', 'decor', 'potions', 'scrolls', 'dagger']:
                                    item_cache = pygame.transform.flip(img.dict[item][3], True, False)
                                    img.dict[item][1] = pygame.transform.flip(img.dict[item][1], True, False)
                                    img.dict[item][2] = pygame.transform.flip(img.dict[item][2], True, False)
                                    img.dict[item][3] = pygame.transform.flip(img.dict[item][4], True, False)
                                    img.dict[item][4] = item_cache
                                    item_cache = pygame.transform.flip(img.dict_cache[item][3], True, False)
                                    img.dict_cache[item][1] = pygame.transform.flip(img.dict_cache[item][1], True, False)
                                    img.dict_cache[item][2] = pygame.transform.flip(img.dict_cache[item][2], True, False)
                                    img.dict_cache[item][3] = pygame.transform.flip(img.dict_cache[item][4], True, False)
                                    img.dict_cache[item][4] = item_cache
                    
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
        pyg.screen.fill(pyg.black)
        
        # Renders menu to update cursor location
        y = 300
        for menu_choice in menu_choices:
            pyg.screen.blit(menu_choice, (80, y))
            y += 24
        pyg.screen.blit(cursor_img, cursor_img_pos)
        pyg.screen.blit(background_image, (400, 200))
        pyg.screen.blit(img.dict[skin_list[skin_index]][rotation_indices[2][rotation_indices[1]]], (464, 264))
        pyg.screen.blit(img.dict_cache[hair_list[hair_index]][rotation_indices[2][rotation_indices[1]]+1], (464, 264))
        pyg.screen.blit(img.dict['dagger'][rotation_indices[2][rotation_indices[1]]+1], (464, 264))
        pygame.display.flip()

def play_game():
    """ IMPORTANT. Processes user input and triggers monster movement. """
    
    global player_action, msg_toggle, stairs, last_press_time
    global gui_toggle, questlog
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    player_move = False
    pygame.key.set_repeat(250, 150)

    while True:
        pyg.clock.tick(30)
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
                    print(f"({player_obj.obj.x}, {player_obj.obj.y}), ({int(player_obj.obj.x/pyg.tile_width)}, {int(player_obj.obj.y/pyg.tile_height)})")
                        
                    # >>MAIN MENU<<
                    if event[0].key in pyg.key_0:
                        return
                    
                    if toggle_list[movement_speed_toggle] == 'Fast':
                        # Update sprites and effects
                        if (event[0].key in pyg.key_UP or event[0].key in pyg.key_DOWN or event[0].key in pyg.key_LEFT or event[0].key in pyg.key_RIGHT) and ('transformation potion' not in inventory_cache):
                            animate_sprites(event[0].key, self=True)

                        # >>MOVE/ATTACK<<
                        if event[0].key in pyg.key_UP:
                            if (player_obj.obj.image == img.dict['player'][1]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(0, -pyg.tile_height)
                        elif event[0].key in pyg.key_DOWN:
                            if (player_obj.obj.image == img.dict['player'][0]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(0, pyg.tile_height)
                        elif event[0].key in pyg.key_LEFT:
                            if (player_obj.obj.image == img.dict['player'][2]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(-pyg.tile_width, 0)
                        elif event[0].key in pyg.key_RIGHT:
                            if (player_obj.obj.image == img.dict['player'][3]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(pyg.tile_width, 0)
                    else:
                        # >>MOVE/ATTACK<<
                        if event[0].key in pyg.key_UP:
                            if (player_obj.obj.image == img.dict['player'][1]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(0, -pyg.tile_height)
                        elif event[0].key in pyg.key_DOWN:
                            if (player_obj.obj.image == img.dict['player'][0]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(0, pyg.tile_height)
                        elif event[0].key in pyg.key_LEFT:
                            if (player_obj.obj.image == img.dict['player'][2]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(-pyg.tile_width, 0)
                        elif event[0].key in pyg.key_RIGHT:
                            if (player_obj.obj.image == img.dict['player'][3]) or ('transformation potion' in inventory_cache):
                                player_move_or_attack(pyg.tile_width, 0)

                        # Update sprites and effects
                        if (event[0].key in pyg.key_UP or event[0].key in pyg.key_DOWN or event[0].key in pyg.key_LEFT or event[0].key in pyg.key_RIGHT) and ('transformation potion' not in inventory_cache):
                            animate_sprites(event[0].key, self=True)

                    # >>PICKUP/STAIRS<<
                    if event[0].key in pyg.key_RETURN:
                        if player_obj.env.map[int(player_obj.obj.x/pyg.tile_width)][int(player_obj.obj.y/pyg.tile_height)].item:
                            if player_obj.obj.tile.item and player_obj.obj.tile.item.item: 
                                player_obj.obj.tile.item.item.pick_up()
                                player_obj.obj.tile.item = None # Hides icon
                            
                            elif player_obj.env.map[int(player_obj.obj.x/pyg.tile_width)][int(player_obj.obj.y/pyg.tile_height)].item.name == 'stairs': 
                                
                                # Save house
                                if player_obj.obj.dungeon_lvl == 0:   
                                    save_floor(load_saves[1])   
                                    save_objects_to_file(load_saves[2], data_source=data_objects_1)
                                mech.next_level()
                            
                    if event[0].key == K_RSHIFT and player_obj.obj.dungeon_lvl != 0: # Ascend stairs to home
                        if player_obj.env.map[int(player_obj.obj.x/pyg.tile_width)][int(player_obj.obj.y/pyg.tile_height)].item:
                            if player_obj.env.map[int(player_obj.obj.x/pyg.tile_width)][int(player_obj.obj.y/pyg.tile_height)].item.name == 'stairs':
                                go_home()

                    # >>VIEW STATS<<
                    if event[0].key in pyg.key_1:
                        level_up_exp = mech.level_up_base + player_obj.obj.player_lvl * mech.level_up_factor
                        new_menu(header =   'Character Information',
                                 options = ['Level:                                ' + str(player_obj.obj.player_lvl),
                                            'Experience:                       ' + str(player_obj.obj.fighter.exp),
                                            'Experience to level up:    ' + str(level_up_exp),
                                            'Maximum HP:                    ' + str(player_obj.obj.fighter.max_hp),
                                            'Attack:                             ' + str(player_obj.obj.fighter.power),
                                            'Defense:                           ' + str(player_obj.obj.fighter.defense)])
                            
                    # >>CHECK INVENTORY<<
                    elif event[0].key in pyg.key_2:
                        chosen_item = inventory_menu("INVENTORY:         USE ITEM")
                        if chosen_item is not None:
                            chosen_item.use()
                            pyg.update_gui()
                    
                    # >>DROP ITEM<<
                    elif event[0].key in pyg.key_3:
                        if player_obj.obj.tile.item:
                            message("There's already something here")
                        else:
                            chosen_item = inventory_menu('INVENTORY:         DROP ITEM')
                            if chosen_item is not None:
                                chosen_item.drop()
                                pygame.event.clear()
                    
                    # >>VIEW QUESTLOG<<
                    elif event[0].key in pyg.key_4:
                        try:
                            questlog.questlog_menu()
                        except:
                            questlog = Questlog()
                            questlog.questlog_menu()
                    
                    # >>MOVEMENT SPEED<<
                    elif event[0].key in pyg.key_5 and (time.time()-last_press_time > cooldown_time):
                        movement_speed(adjust=True)
                        last_press_time = float(time.time())
                    
                    # >>SCREENSHOT<<
                    elif event[0].key in pyg.key_6:
                        screenshot(cache=True, big=True)
                    
                    # >>TOGGLE MESSAGES<<
                    elif event[0].key in pyg.key_SLASH:
                    
                        # Hide messages
                        if pyg.msg_toggle:
                            pyg.msg_toggle = False
                        
                        else:
                            # Hide messages and GUI
                            if pyg.gui_toggle:
                                pyg.gui_toggle = False
                                pyg.msg_toggle = False
                            
                            # View messages and GUI
                            else:
                                pyg.gui_toggle = True
                                pyg.msg_toggle = True
            
            else:
                # >>MAIN MENU<<
                if event[0].type == KEYDOWN:
                    if event[0].key in pyg.key_0:
                        return
                        
                # >>TOGGLE MESSAGES<<
                elif event[0].key in pyg.key_SLASH:
                    if pyg.msg_toggle:
                        pyg.msg_toggle = False
                    else:
                        if pyg.gui_toggle:
                            pyg.gui_toggle = False
                            pyg.msg_toggle = False,
                        else:
                            pyg.msg_toggle = True
                            pyg.gui_toggle = True
            
            if event[0].type == MOUSEBUTTONDOWN: # Cursor-controlled actions?
                if event[0].button == 1:
                    player_move = True
                    pyg.msg_toggle = False
                elif event[0].button == 3:
                    mouse_x, mouse_y = event[0].pos
                    get_names_under_mouse(mouse_x, mouse_y)
                    
            if event[0].type == MOUSEBUTTONUP:
                if event[0].button == 1:
                    player_move = False

        if player_move and game_state == 'playing': # Cursor-controlled movement
            pos = pygame.mouse.get_pos()
            x = int((pos[0] + camera.x)/pyg.tile_width)
            y = int((pos[1] + camera.y)/pyg.tile_height)
            tile = player_obj.env.map[x][y]
            if tile != player_obj.obj.tile:
                dx = tile.x - player_obj.obj.x
                dy = tile.y - player_obj.obj.y
                distance = math.sqrt(dx ** 2 + dy ** 2) # Distance from player to target
                dx = int(round(dx / distance)) * pyg.tile_width # Restrict motion to grid
                dy = int(round(dy / distance)) * pyg.tile_height
                player_move_or_attack(dx, dy) # Triggers the chosen action

    #if game_state == 'playing' and player_action != 'didnt-take-turn': # Tab forward and unhash to allow turn-based game
        for entity in player_obj.env.active_entities:
            if entity.ai:
                entity.ai.take_turn()
        player_action = 'didnt-take-turn'
        render_all()

#######################################################################################################################################################
# Play game
def __PLAY_GAME__():
    pass

def go_home():
    """ Advances player to home. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    message('You take a moment to rest, and recover your strength.', pyg.violet)
    player_obj.obj.fighter.heal(int(player_obj.obj.fighter.max_hp / 2)) # Heals the player by 50%
    time.sleep(0.5)
    message('You gather you belongings and head home.', pyg.red)
    if player_obj.obj.dungeon_lvl != 0:
        player_obj.obj.dungeon_lvl = 0
        
    player_obj.env = player_obj.home
    place_player(env=player_obj.env, loc=player_obj.env.center)
    camera.update()
    time.sleep(0.5)
    pyg.update_gui()

def player_move_or_attack(dx, dy):
    """ Moves the player by a given amount if the path is clear. Activates floor effects. """
    
    global player_action, dig, step_counter
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    target = None

    # Find new position
    x = int((player_obj.obj.x + dx)/pyg.tile_width)
    y = int((player_obj.obj.y + dy)/pyg.tile_height)
    
    # Remove (map[x][y].entity and dungeon_lvl != 0) for default
    if (player_obj.env.map[x][y].entity == player_obj.obj and player_obj.obj.dungeon_lvl == 0) or not is_blocked(x, y):
        
        # Move player and update map
        player_obj.obj.x += dx
        player_obj.obj.y += dy
        player_obj.obj.tile.entity = None # remove player from previous position; invisible barrier otherwise
        player_obj.env.map[x][y].entity = player_obj.obj
        player_obj.obj.tile = player_obj.env.map[x][y]
        check_tile(x, y)
        
        # Trigger floor effects
        try:
            floor_effects(player_obj.env.map[x][y].floor_effect)
        except:
            pass
        
        camera.update()
    
    # Attack target
    elif player_obj.env.map[x][y].entity and player_obj.obj.dungeon_lvl != 0: 
        target = player_obj.env.map[x][y].entity
        player_obj.obj.fighter.attack(target)
    
    # Dig tunnel
    else:
        if (dig or super_dig) and not player_obj.env.map[x][y].entity: # True if shovel equipped
            
            # Move player
            if player_obj.obj.x >= 64 and player_obj.obj.y >= 64:
                if super_dig or not player_obj.env.map[x][y].unbreakable:
                    player_obj.obj.x                    += dx
                    player_obj.obj.y                    += dy
                    player_obj.obj.tile.entity          = None
                    player_obj.env.map[x][y].blocked     = False
                    player_obj.env.map[x][y].block_sight = False
                    player_obj.env.map[x][y].unbreakable = False
                    player_obj.env.map[x][y].image  = 'floors'
                    player_obj.env.map[x][y].entity      = player_obj.obj
                    player_obj.obj.tile                 = player_obj.env.map[x][y]
                    check_tile(x, y) # Reveals tile
                    camera.update()
                    
                    if (step_counter[1] >= 100) and not super_dig:
                        inventory[inventory.index(step_counter[3])].item.drop()
                        player_obj.obj.tile.item = None # Hides icon
                        step_counter = [False, 0, False, 0]
                    else:
                        step_counter[1] += 1
                else:
                    message('The shovel strikes the wall but does not break it.', pyg.white)
    player_action = 'took-turn'

def floor_effects(floor_effect):
    if floor_effect == "fire":
        player_obj.obj.fighter.take_damage(10)
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
                'player_lvl':    item.player_lvl,
                'dungeon_lvl':   item.dungeon_lvl}
    
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
                'player_lvl':        item.player_lvl,
                'dungeon_lvl':       item.dungeon_lvl}

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
                'player_lvl':              item.player_lvl,
                'dungeon_lvl':             item.dungeon_lvl}

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
                'player_lvl':    item.player_lvl,
                'dungeon_lvl':   item.dungeon_lvl}

    with open(file, 'wb') as f:
        pickle.dump(objects_data, f)

def save_floor(file):
    """ Called by:    main_menu()              when using >>SAVE<<
        
        House data:   file = "Data/File_{index}/data_home_{index}.pkl"
        Dungeon data: file = "Data/File_{index}/data_dungeon_{index}.pkl" """

    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")

    layout_data = {}
    for row_index, row in enumerate(player_obj.env.map):
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
                fighter_component          = Fighter(
                            hp             = load_objects[i]['hp'],
                            defense        = load_objects[i]['defense'],
                            power          = load_objects[i]['power'],
                            exp            = 0,
                            death_function = player_death)
                obj                     = Object(
                            name           = "player",
                            image          = img.dict['player'][0],
                            x              = load_objects[i]['x'],
                            y              = load_objects[i]['y'],
                            category       = 'player',
                            blocks         = True,
                            fighter        = fighter_component,
                            hp             = load_objects[i]['hp'],
                            defense        = load_objects[i]['defense'],
                            power          = load_objects[i]['power'],
                            player_lvl     = load_objects[i]['player_lvl'],
                            dungeon_lvl    = load_objects[i]['dungeon_lvl'])
                dungeon_lvl = player_obj.obj.dungeon_lvl
                player_obj.obj = obj

            # Loads stairs
            elif load_objects[i]['name'] == 'stairs':
                stairs = Object(
                            name     = load_objects[i]['name'],
                            image    = img.dict['stairs'][0],
                            x        = load_objects[i]['x'],
                            y        = load_objects[i]['y'],
                            category = load_objects[i]['category'])
                container.append(stairs)
                
            # Loads items
            elif load_objects[i]['category'] in ['potions', 'scrolls']:
                item_component = Item(load_objects[i]['item.use_function'])
                new_item = Object(
                            name     = load_objects[i]['name'],
                            image    = img.dict[load_objects[i]['category']][load_objects[i]['image_num']],
                            x        = load_objects[i]['x'],
                            y        = load_objects[i]['y'],
                            category = load_objects[i]['category'],
                            item     = item_component)
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
                            img.dict[load_objects[i]['name']][0],
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
                #menu(f'{x}, {y}', 'test')
                try:
                    player_obj.env.map[x][y].item = item
                except:
                    print(x, y, container[i].name)

def load_floor(file, music, load_objects_file=None, home=False):
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    global map, load_saves

    # Start music track
    aud.control(new_track=music)

    # Load floor plan
    with open(file, 'rb') as f:
        layout_data = pickle.load(f)
    map = []
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
        map.append(row)

    # Optionally load additional objects
    if load_objects_file:
        load_objects_from_file(load_objects_file, objects)
    
    if home:
        generate_friend()

    # Place objects
    map[int(player_obj.obj.x / 32)][int(player_obj.obj.y / 32)].entity = player_obj.obj
    player_obj.obj.tile = map[int(player_obj.obj.x / 32)][int(player_obj.obj.y / 32)]
    check_tile(int(player_obj.obj.x / 32), int(player_obj.obj.y / 32))
    if file == load_saves[3]: place_objects(home=home, fresh_start=False)  # Adds content to the room

#######################################################################################################################################################
# Environment management
def __ENVIRONMENT_MANAGEMENT__():
    pass

def generate_friend():
    
    # Generates friend
    x = random.randint(11, 19) # Sets random location
    y = random.randint(11, 19)
    hp_set, defense_set, power_set, exp_set = 200, 0, 0, 0
    fighter_component          = Fighter(
                hp             = hp_set,
                defense        = defense_set,
                power          = power_set,
                exp            = exp_set,
                death_function = monster_death)
    ai_component = BasicMonster()             
    monster = Object(
                name    = 'friend',
                image   = img.dict['monsters'][0],
                x       = x*pyg.tile_width,
                y       = y*pyg.tile_height,
                blocks  = True,
                fighter = fighter_component,
                ai      = ai_component)
    data_objects_1.append(monster)
    home_object_positions.append([x, y])
    map[x][y].entity = monster # Places monster?
    monster.tile = map[x][y]

def place_objects(room=None, home=False, fresh_start=True):
    """ Decides the chance of each monster or item appearing, then generates and places them. """
    global data_objects_1, stairs
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    if not room: # Lazy bug fix
        room = Rectangle(1,1,2,2)
    
    # Set spawn chance for [chance, dungeon_lvl]
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
            for i in range(6): 
                x = room.x1+3+i # Sets location
                y = room.y1+1
                
                if i == 0:
                    item = create_objects('healing potion', [x, y])
                elif i == 1:
                    item = create_objects('scroll of lightning bolt', [x, y])
                elif i == 2:
                    item = create_objects('scroll of fireball', [x, y])
                elif i == 3:
                    item = create_objects('blood sword', [33, 33])
                elif i == 4:
                    item = create_objects('shield', [34, 34])
                elif i == 5:
                    item = create_objects('scroll of fireball', [0, 0])
                
                data_objects_1.append(item)
                home_object_positions.append([x, y])
                player_obj.env.map[x][y].item = item

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
                        hp            = hp_set,
                        defense       = defense_set,
                        power         = power_set,
                        exp           = exp_set,
                        death_function=monster_death)
                    ai_component = BasicMonster()               
                    monster     = Object(
                        name    = 'orc',
                        image   = img.dict['monsters'][7],
                        x       = x*pyg.tile_width,
                        y       = y*pyg.tile_height,
                        blocks  = True,
                        fighter = fighter_component,
                        ai      = ai_component)
                elif choice == 'troll':
                    hp_set, defense_set, power_set, exp_set = 30, 2, 8, 100
                    fighter_component  = Fighter(
                        hp             = hp_set,
                        defense        = defense_set,
                        power          = power_set,
                        exp            = exp_set,
                        death_function = monster_death)
                    ai_component = BasicMonster()               
                    monster     = Object(
                        name    = 'troll',
                        image   = img.dict['monsters'][4],
                        x       = x * pyg.tile_width,
                        y       = y * pyg.tile_height,
                        blocks  = True,
                        fighter = fighter_component,
                        ai      = ai_component)
                elif choice == 'troll 2':
                    hp_set, defense_set, power_set, exp_set = 50, 5, 15, 500
                    fighter_component = Fighter(
                        hp            = hp_set,
                        defense       = defense_set,
                        power         = power_set,
                        exp           = exp_set,
                        death_function=monster_death)
                    ai_component = BasicMonster()               
                    monster     = Object(
                        name    = 'troll 2',
                        image   = img.dict['monsters'][6],
                        x       = x*pyg.tile_width,
                        y       = y*pyg.tile_height,
                        blocks  = True,
                        fighter = fighter_component,
                        ai      = ai_component)
                player_obj.env.map[x][y].entity = monster # Places monster?
                monster.tile = player_obj.env.map[x][y]

        for i in range(num_items): # Places items
            x = random.randint(room.x1+1, room.x2-1) # Sets random location
            y = random.randint(room.y1+1, room.y2-1)
            if not is_blocked(x, y):
                
                # This part could be significantly optimized, but it would require changes elsewhere
                choice = random_choice(item_chances) # Sets random item
                item = Object(name='bug fix', image=img.dict['decor'][-1], x=x, y=y)
                
                if choice == 'heal': item = create_objects('healing potion', [x, y])
                
                if choice == 'transformation': item = create_objects('transformation potion', [x, y])
                
                elif choice == 'lightning': item = create_objects('scroll of lightning bolt', [x, y])
                
                elif choice == 'fireball': item = create_objects('scroll of fireball', [x, y])

                elif choice == 'confuse': item = create_objects('scroll of confusion', [x, y])

                elif choice == 'blood dagger': item = create_objects('blood dagger', [x, y])

                elif choice == 'sword': item = create_objects('sword', [x, y])

                elif choice == 'blood sword': item = create_objects('blood sword', [x, y])

                elif choice == 'shield': item = create_objects('shield', [x, y])

                elif choice == 'shovel': item = create_objects('shovel', [x, y])
      
                elif choice == 'super shovel': item = create_objects('super shovel', [x, y])
                
                player_obj.env.map[x][y].item = item

#######################################################################################################################################################
# Item effects
def cast_heal():
    """ Heals the player. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    if player_obj.obj.fighter.hp == player_obj.obj.fighter.max_hp:
        message('You are already at full health.', pyg.red)
        return 'cancelled'
    message('Your wounds start to feel better!', pyg.violet)
    player_obj.obj.fighter.heal(mech.heal_amount)

def cast_lightning():
    """ Finds the closest enemy within a maximum range and attacks it. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    monster = closest_monster(mech.lightning_range)
    if monster is None:  #no enemy found within maximum range
        message('No enemy is close enough to strike.', pyg.red)
        return 'cancelled'
    message('A lighting bolt strikes the ' + monster.name + ' with a loud thunder! The damage is '
        + str(mech.lightning_damage) + ' hit points.', pyg.light_blue)
    monster.fighter.take_damage(mech.lightning_damage)

def cast_fireball():
    """ Asks the player for a target tile to throw a fireball at. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    message('Left-click a target tile for the fireball, or right-click to cancel.', pyg.light_cyan)
    (x, y) = target_tile()
    if x is None: return 'cancelled'
    message('The fireball explodes, burning everything within ' + str(int(mech.fireball_radius/pyg.tile_width)) + ' tiles!', pyg.orange)
    for ent in player_obj.env.active_entities: # Damages every fighter in range, including the player
        if ent.distance(x, y) <= mech.fireball_radius and ent.fighter:
            message('The ' + ent.name + ' gets burned for ' + str(mech.fireball_damage) + ' hit points.', pyg.orange)
            ent.fighter.take_damage(mech.fireball_damage)

def cast_confuse():
    """ Asks the player for a target to confuse, then replaces the monster's AI with a "confused" one. After some turns, it restores the old AI. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    message('Left-click an enemy to confuse it, or right-click to cancel.', pyg.light_cyan)
    monster = target_monster(mech.confuse_range)
    if monster is None: return 'cancelled'
    old_ai = monster.ai
    monster.ai = ConfusedMonster(old_ai)
    monster.ai.owner = monster  #tell the new component who owns it
    message('The eyes of the ' + monster.name + ' look vacant, as he starts to stumble around!', pyg.light_green)

#######################################################################################################################################################
# Utilities
def __UTILITIES__():
    pass

def animate_sprites(key=key_cache, self=True):
    global idle_animation_counter, key_cache
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")

    if self == True:
        #if idle_animation_counter[0] <= 40:
        #    player_obj.obj.image = images[2]
        #    player_obj.obj.image_num = 2
        #elif 40 < idle_animation_counter[0] < 60:
        #    player_obj.obj.image = images[3]
        #    player_obj.obj.image_num = 3
        #else:
        #    idle_animation_counter[0] = 0
        #idle_animation_counter[0] += 1
        
        key_cache = key
        if key in pyg.key_UP:
            player_obj.obj.image = img.dict['player'][1]
        elif key in pyg.key_DOWN:
            player_obj.obj.image = img.dict['player'][0]
        elif key in pyg.key_LEFT:
            player_obj.obj.image = img.dict['player'][2]
        elif key in pyg.key_RIGHT:
            player_obj.obj.image = img.dict['player'][3]

def render_all(screenshot=False, visible=False):
    """ Draws tiles and stuff. Constantly runs. """
        
    dungeon_scaling = int(player_obj.obj.dungeon_lvl / 10)
    pyg.screen.fill(pyg.black)
    
    if screenshot:
        y_range_1, y_range_2 = 0, len(player_obj.env.map[0])
        x_range_1, x_range_2 = 0, len(player_obj.env.map)
    else:
        y_range_1, y_range_2 = camera.tile_map_y, camera.y_range
        x_range_1, x_range_2 = camera.tile_map_x, camera.x_range
    
    # Draw visible tiles
    for y in range(y_range_1, y_range_2):
        for x in range(x_range_1, x_range_2):
            tile = player_obj.env.map[x][y]
            if visible or tile.visible:
                
                # Sets wall image
                pyg.screen.blit(img.dict[tile.image][tile.image_num], (tile.x-camera.x, tile.y-camera.y))
                
                # Generates floor and entities; sets floor image
                if not tile.block_sight:
                    if tile.item:
                        pyg.screen.blit(tile.item.image, (tile.x-camera.x, tile.y-camera.y))
                        tile.item.draw(pyg.screen)
                    if tile.entity:
                        tile.entity.draw(pyg.screen)

                if tile.unbreakable:
                    pyg.screen.blit(img.dict['walls'][1], (tile.x-camera.x, tile.y-camera.y))
    if not screenshot:
        if impact:
            pyg.screen.blit(impact_image, impact_image_pos)
        

        # Print messages
        if pyg.msg_toggle: 
           y = 10
           for message in pyg.msg:
               pyg.screen.blit(message, (5, y))
               y += 24
        if pyg.gui_toggle:
            pyg.screen.blit(pyg.gui, (10,456))
        pygame.display.flip()

def message(new_msg, color):
    """ Initializes messages to be projected with render_all. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    # Split the message among multiple lines
    new_msg_lines = textwrap.wrap(new_msg, mech.message_width)
    
    # Update message list
    for line in new_msg_lines:
        
        # Delete older messages
        if len(pyg.msg) == mech.message_height:
            del pyg.msg[0]
        
        # Create message object
        pyg.msg.append(pyg.font.render(line, True, color))

def active_effects():
    """ Applies effects from items and equipment. Runs constantly. """
    global friendly, teleport, dig, super_dig
    
    if 'transformation potion' in inventory_cache:
        player_obj.obj.image = img.dict['monsters'][0]
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

def death(ent):
    if ent.name == 'player':
        message('You died!', pyg.red)
        game_state                 = 'dead'
        player_obj.obj.image       = img.dict['decor'][1]
        player_obj.obj.tile.entity = None
        player_obj.obj.tile.item   = player_obj.obj
        
    else:
        message('The ' + monster.name + ' is dead! You gain ' + str(monster.fighter.exp) + ' experience points.', pyg.orange)
        monster.image       = img.dict['decor'][1]
        monster.tile.entity = None
        monster.blocks      = False
        monster.fighter     = None
        monster.ai          = None
        monster.category    = 'other'
        monster.name        = 'remains of ' + monster.name

        monster.item = Item()
        monster.item.owner = monster
        if not monster.tile.item:
            monster.tile.item = monster
        pygame.event.get()

def player_death(player):
    """ Ends the game upon death and transforms the player into a corpse. """
    global game_state
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    message('You died!', pyg.red)
    game_state         = 'dead'
    player.image       = img.dict['decor'][1]
    player.tile.entity = None
    player.tile.item   = player

def monster_death(monster):
    """ Transforms a monster into a corpse. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    message('The ' + monster.name + ' is dead! You gain ' + str(monster.fighter.exp) + ' experience points.', pyg.orange)
    monster.image       = img.dict['decor'][1]
    monster.tile.entity = None
    monster.blocks      = False
    monster.fighter     = None
    monster.ai          = None
    monster.category    = 'other'
    monster.name        = 'remains of ' + monster.name

    monster.item = Item()
    monster.item.owner = monster
    if not monster.tile.item:
        monster.tile.item = monster
    pygame.event.get()


def closest_monster(max_range):
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    closest_enemy = None
    closest_dist = max_range + 1  #start with (slightly more than) maximum range
 
    for ent in player_obj.env.active_entities:
        if ent.fighter and ent != player_obj.obj and ent.tile.visible:
            #calculate distance between this object and the player
            dist = player_obj.obj.distance_to(ent)
            if dist < closest_dist:  #it's closer, so remember it
                closest_enemy = ent
                closest_dist
    return closest_enemy

def target_tile(max_range=None):
    """ Returns the position of a tile left-clicked in player's field of view, or (None,None) if right-clicked. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    while True:         
        pygame.time.Clock().tick(30)
        for event in pygame.event.get(): # Processes user input
        
            if event.type == QUIT: # Quit
                pygame.quit()
                sys.exit()
                
            if event.type == KEYDOWN: # Cancels action for escape
                if event.key in pyg.key_0:
                    pyg.msg_toggle = False 
                    return (None, None)
                    
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 3: # Cancels action for right-click
                    pyg.msg_toggle = False 
                    return (None, None)
                    
                if event.button == 1: # Accepts the target if clicked in the field of view
                    mouse_x, mouse_y = event.pos
                    mouse_x += camera.x
                    mouse_y += camera.y
                    x = int(mouse_x /pyg.tile_width)
                    y = int(mouse_y /pyg.tile_height)
                    if (player_obj.env.map[x][y].visible and
                        (max_range is None or player_obj.obj.distance(mouse_x, mouse_y) <= max_range)):
                        return (mouse_x, mouse_y)
        render_all()

def check_tile(x, y):
    """ Reveals newly explored regions. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    tile = player_obj.env.map[x][y]
    if not tile.explored:
       tile.explored = True 
       old_x = x
       old_y = y
       for x in range(old_x - 1, old_x + 2):
           for y in range(old_y - 1, old_y + 2):
               player_obj.env.map[x][y].visible = True
       if tile.room and not tile.room.explored:
          room = tile.room
          room.explored = True
          for x in range(room.x1 , room.x2 + 1):
              for y in range(room.y1 , room.y2 + 1):
                  player_obj.env.map[x][y].visible = True       

def check_level_up():
    """ Checks if the player's experience is enough to level-up. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    level_up_exp = mech.level_up_base + player_obj.obj.player_lvl * mech.level_up_factor
    if player_obj.obj.fighter.exp >= level_up_exp: # Levels up
        player_obj.obj.player_lvl += 1
        player_obj.obj.fighter.exp -= level_up_exp
        message('Your battle skills grow stronger! You reached level ' + str(player_obj.obj.level) + '!', pyg.yellow)
        choice = None
        while choice == None: # Keeps asking until a choice is made
            choice = new_menu(header = 'Level up! Choose a stat to raise:',
                              options = ['Constitution (+20 HP, from ' + str(player.fighter.max_hp) + ')',
                                         'Strength (+1 attack, from ' + str(player.fighter.power) + ')',
                                         'Agility (+1 defense, from ' + str(player.fighter.defense) + ')'], 
                              position="center")

        if choice == 0: # Boosts health
            player_obj.obj.fighter.max_hp += 20
            player_obj.obj.fighter.hp += 20
        elif choice == 1: # Boosts power
            player_obj.obj.fighter.power += 1
        elif choice == 2: # Boosts defense
            player_obj.obj.fighter.defense += 1
        pyg.update_gui()

def from_dungeon_level(table):
    """ Returns a value that depends on the dungeon level. Runs in groups.
        The table specifies what value occurs after each level with 0 as the default. """
    
    for (value, level) in reversed(table):
        if player_obj.obj.dungeon_lvl >= level:
            return value
    return 0

def is_blocked(x, y):
    """ Checks for barriers and trigger dialogue. """
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
    
    try:
        # Check for barriers
        if player_obj.env.map[x][y].blocked:
            return True
            
        # Check for monsters
        if player_obj.env.map[x][y].entity: 
        
            # Triggers dialogue for friend
            if map[x][y].entity.name in NPC_names:
                friend_quest(NPC_name=map[x][y].entity.name)
            return True
            
        # Triggers message for hidden passages
        if player_obj.env.map[x][y].unbreakable:
            message('A mysterious breeze seeps through the cracks.', pyg.white)
            pygame.event.clear()
            return True
    except:
        return True
    return False

def get_equipped_in_slot(slot):
    """ Returns the equipment in a slot, or None if it's empty. """
    
    for eq in inventory:
        if eq.equipment and eq.equipment.slot == slot and eq.equipment.is_equipped:
            return eq.equipment
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
    impact_image = pygame.Surface((pyg.tile_width, pyg.tile_width)).convert()
    impact_image.set_colorkey(impact_image.get_at((0,0)))
    image = pygame.Surface((int(pyg.tile_width/2), int(pyg.tile_height/3))).convert()
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

class Entity:
    """ Initialize pygame and audio, load images and environmnets, load player. """
    
    def __init__(self, name, image_num, x, y):
        
        # Generic parameters
        self.name = name
        self.image_num = image_num
        self.x = x
        self.y = y

        self.hp          = hp
        self.defense     = defense
        self.power       = power
        self.tile        = None

        # Player
        self.player_lvl  = player_lvl
        
        
        # Monsters
        
        
        # NPCs

class Object:
    """ Defines a generic object, such as the player, a monster, an item, or stairs. """
    
    def __init__(self, name, image, x, y, blocks=False, fighter=None, hp=None, power=None, defense=None,
                ai=None, item=None, equipment=None, item_list=False,
                appended=False, tile=None, player_lvl=None, dungeon_lvl=None, category=None, image_num=0):
        """ Defines object and object parameters, such as name, image and image size, stats, and equipment.
            Initializes player, monster, stairs, and items. """
        
        global map

        # Assign object parameters
        self.x           = x                    # tile width (integer)
        self.y           = y                    # tile height (integer)
        
        self.image       = image                # tile image (integer, pulled from rogue_tiles.png)
        
        self.name        = name                 # name (string)
        
        self.blocks      = blocks               # unknown
        self.tile        = None                 # initialized tile location (?)
        
        self.fighter     = fighter              # true for player or monster
        self.player_lvl  = player_lvl
        self.hp          = hp
        self.defense     = defense
        self.power       = power
        self.counter     = 0

        self.ai          = ai                   # true for monsters
        self.item        = item                 # true for usable items
        self.equipment   = equipment            # true for wearable items
        self.dungeon_lvl = dungeon_lvl
        
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
        
        x = int((self.x + dx)/pyg.tile_width)
        y = int((self.y + dy)/pyg.tile_height)
        if not is_blocked(x, y):
            self.x                 += dx
            self.y                 += dy
            self.tile.entity       = None
            player_obj.env.map[x][y].entity = self
            self.tile              = player_obj.env.map[x][y]

    def move_towards(self, target_x, target_y):
        """ Moves object towards target. """
        
        dx       = target_x - self.x
        dy       = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx       = int(round(dx / distance)) * pyg.tile_width # Restricts to map grid
        dy       = int(round(dy / distance)) * pyg.tile_height
        self.move(dx, dy)
 
    def distance_to(self, other):
        """ Returns the distance to another object. """
        
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)
      
    def distance(self, x, y):
        """ Returns the distance to some coordinates. """
        
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)      
       
    def draw(self, surface):
        """ Draws the object at its position. """
        
        surface.blit(self.image, (self.x-camera.x, self.y-camera.y))

class Fighter:
    """ Defines combat-related properties and methods (monster, player, NPC).
        Used by fighter_component, attack(), cast_lightning(), cast_fireball(), player_move_or_attack(), take_turn(),
        mech.next_level(), go_home(), and cast_heal(). Can call player_death() and monster_death(). """
    
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
            if self.owner == player_obj.obj:
               pyg.update_gui()
            if self.hp <= 0:                    # checks for death
                self.hp = 0
                pyg.update_gui()
                function = self.death_function  # kills player or monster
                if function is not None:
                    function(self.owner)
                if self.owner != player_obj.obj:        # gives experience to the player
                    player_obj.obj.fighter.exp += self.exp
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
            message('Your inventory is full, cannot pick up ' + self.owner.name + '.', pyg.red)
        else:
            inventory.append(self.owner)
            inventory_cache.append(self.owner.name)
            if self.owner in data_objects_1:
                index = data_objects_1.index(self.owner)
                data_objects_1.pop(index) # Removes item from home
                #home_object_positions.pop(index)
            message('You picked up a ' + self.owner.name + '!', pyg.green)
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
        if player_obj.obj.dungeon_lvl == 0: # Saves dropped items at home
            data_objects_1.append(self.owner)
            home_object_positions.append([int(player_obj.obj.x/pyg.tile_width), int(player_obj.obj.y/pyg.tile_height)])
        inventory.remove(self.owner)
        #inventory_cache.remove(self.owner.name)
        self.owner.x = player_obj.obj.x
        self.owner.y = player_obj.obj.y
        player_obj.obj.tile.item = self.owner
        message('You dropped a ' + self.owner.name + '.', pyg.yellow)   

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
    
    def __init__(self, name=None, slot=None, power_bonus=0, defense_bonus=0, max_hp_bonus=0, timer=False, is_equipped=False):
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
        player_obj.obj.fighter.power   += self.power_bonus
        player_obj.obj.fighter.defense += self.defense_bonus
        player_obj.obj.fighter.max_hp  += self.max_hp_bonus
        
        if self.name not in hair_list:
            message('Equipped ' + self.owner.name + ' on ' + self.slot + '.', pyg.light_green)
        
        if self.timer:
            step_counter[0] = True
            step_counter[1] += 1
            step_counter[3] = self.owner
        
        # Update player sprite
        for i in range(4):
            img.dict['player'][i] = img.dict_cache['player'][i]
        
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
                        overlay_image = pygame.Surface((pyg.tile_width, pyg.tile_height), pygame.SRCALPHA)
                        overlay_image.blit(img.dict['player'][j], (0, 0))
                        overlay_image.blit(img.dict[sorted_inventory[i].name][j+1], (0, 0))
                        img.dict['player'][j] = overlay_image
        animate_sprites(key_cache)
        camera.update()

    def dequip(self):
        """ Unequips an object and shows a message about it. """
        
        global images
        
        if not self.is_equipped: return
        self.is_equipped       = False
        player_obj.obj.fighter.power   -= self.power_bonus
        player_obj.obj.fighter.defense -= self.defense_bonus
        player_obj.obj.fighter.max_hp  -= self.max_hp_bonus
        if player_obj.obj.fighter.hp > player_obj.obj.fighter.max_hp:
           player_obj.obj.fighter.hp = player_obj.obj.fighter.max_hp 
        message('Dequipped ' + self.owner.name + ' from ' + self.slot + '.', pyg.light_yellow)

        if self.timer:
            step_counter[0] = False
            
        # Update player sprite
        for i in range(4):
            img.dict['player'][i] = img.dict_cache['player'][i]
            
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
                        overlay_image = pygame.Surface((pyg.tile_width, pyg.tile_height), pygame.SRCALPHA)
                        overlay_image.blit(img.dict['player'][j], (0, 0))
                        overlay_image.blit(img.dict[sorted_inventory[i].name][j+1], (0, 0))
                        img.dict['player'][j] = overlay_image
        animate_sprites(key_cache)
        camera.update()

class BasicMonster:
    """ Defines the AI for a basic monster. """
    
    def take_turn(self):
        """ Lets a basic monster takes its turn. """
        
        monster = self.owner
        if monster.tile.visible:
            distance = monster.distance_to(player_obj.obj)
            if distance < 128:
                if (player_obj.obj.dungeon_lvl != 0) and (friendly == False):
                    if distance >= 64: # Moves towards player if far away
                        monster.move_towards(player_obj.obj.x, player_obj.obj.y)
                    elif player_obj.obj.fighter.hp > 0: # Attacks player once per 3 turns
                        if monster.counter == 0:
                            monster.fighter.attack(player_obj.obj)
                        elif monster.counter == 10:
                            monster.counter = -1
                        monster.counter += 1
                else:
                    if distance >= 100:
                        monster.move_towards(player_obj.obj.x, player_obj.obj.y)

class Tile:
    """ Defines a tile of the map and its parameters. Sight is blocked if a tile is blocked. 
        Used in make_home() and make_map(). """
    
    def __init__(self, blocked, x, y, name='tile', block_sight=None, visible=False, explored=False, unbreakable=False, image=None, image_num=0):
        self.name        = name
        self.blocked     = blocked
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
        self.width           = pyg.screen_width
        self.height          = pyg.screen_height + pyg.tile_height
        self.x               = self.target.x - int(self.width / 2)
        self.y               = self.target.y - int(self.height / 2)
        self.center_x        = self.x + int(self.width / 2)
        self.center_y        = self.y + int(self.height / 2)
        self.right           = self.x + self.width
        self.bottom          = self.y + self.height
        self.tile_map_x      = int(self.x / pyg.tile_width)
        self.tile_map_y      = int(self.y / pyg.tile_height)
        self.tile_map_width  = int(self.width / pyg.tile_width)
        self.tile_map_height = int(self.height / pyg.tile_height)
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
            self.tile_map_x = int(self.x / pyg.tile_width)
            self.x_range    = self.tile_map_x + self.tile_map_width
        #if self.y > 0 and  self.target.y < self.center_y \
        #or self.bottom < pyg.map_height and  self.target.y > self.center_y:
        if self.target.y != self.center_y:   
            y_move          = self.target.y - self.center_y
            self.y          += y_move
            self.center_y   += y_move
            self.bottom     += y_move
            self.tile_map_y = int(self.y / pyg.tile_height)
            self.y_range    = self.tile_map_y + self.tile_map_height
        self.fix_position()

    def fix_position(self):
        """ ? """
        
        if player_obj.obj.dungeon_lvl != 0:
            if self.x < 0:
               self.x          = 0
               self.center_x   = self.x + int(self.width / 2)
               self.right      = self.x + self.width
               self.tile_map_x = int(self.x / pyg.tile_width)
               self.x_range    = self.tile_map_x + self.tile_map_width
            elif self.right > pyg.map_width:
               self.right      = pyg.map_width
               self.x          = self.right - self.width
               self.center_x   = self.x + int(self.width / 2)
               self.tile_map_x = int(self.x / pyg.tile_width)
               self.x_range    = self.tile_map_x + self.tile_map_width
            if self.y < 0:
               self.y          = 0
               self.center_y   = self.y + int(self.height / 2)
               self.bottom     = self.y + self.height
               self.tile_map_y = int(self.y / pyg.tile_height)
               self.y_range    = self.tile_map_y + self.tile_map_height
            elif self.bottom > pyg.map_height:
               self.bottom     = pyg.map_height
               self.y          = self.bottom - self.height
               self.center_y   = self.y + int(self.height / 2)
               self.tile_map_y = int(self.y / pyg.tile_height)
               self.y_range    = self.tile_map_y + self.tile_map_height

#######################################################################################################################################################
# Quests
class Quest:
    """ Holds quest information. """

    def __init__(self, name='', notes=[], tasks=[], category='main'):
        """ name     : string; title of quest
            content  : list of strings; notes and checklists
            category : string in ['main', 'side']; organizes quest priority
            finished : Boolean; notes if the quest has been completed """

        self.name     = name
        self.notes    = notes
        self.tasks    = tasks
        self.category = category
        self.finished = False
        
        self.content  = notes + tasks
        self.categories    = ['Notes' for i in range(len(notes))]
        self.categories    += ['Tasks' for i in range(len(tasks))]

class Questlog:
    """ Manages quest menu and modifies Quest objects. """
    
    def __init__(self):
        """ Only runs once when a new game is started.

            quests          : list of Quest objects
            quest_names     : list of strings
            categories      : list of strings; 'main' or 'side'
            main_quests     : list of Quest objects
            side_quests     : list of Quest objects
            selected_quest  : Quest object
            
            menu_index      : int; toggles questlog pages
            categories      : 
            achievements    : """
        
        # Initialize parameters
        self.menu_index = 0
        
        # Create default quests
        gathering_supplies  = Quest(name='Gathering supplies',
                                    notes=['My bag is nearly empty.',
                                           'It would be good to have some items on hand.'],
                                    tasks=['☐ Collect 3 potions.',
                                           '☐ Find a spare shovel.'],
                                    category='Main')

        finding_a_future    = Quest(name='Finding a future',
                                    notes=['I should make my way into town.'],
                                    tasks=['☐ Wander east.'],
                                    category='Main')

        making_a_friend     = Quest(name='Making a friend',
                                    notes=['I wonder who this is. Maybe I should say hello.'],
                                    tasks=['☐ Say hello to the creature.',
                                           '☐ Get to know them.'],
                                    category='Side')

        furnishing_a_home   = Quest(name='Furnishing a home',
                                    notes=['My house is empty. Maybe I can spruce it up.'],
                                    tasks=['☐ Use the shovel to build new rooms.',
                                           '☐ Drop items to be saved for later use.',
                                           '☐ Look for anything interesting.'],
                                    category='Side')

        self.quests = [gathering_supplies, finding_a_future, making_a_friend, furnishing_a_home]
        self.update_questlog()

    def back_to_menu(self):
        """ Toggle menus. """
        
        if self.menu_index == 0: self.menu_index += 1
        else:                    self.menu_index = 0
    
    def update_questlog(self):
        """ Updates data containers used in menu. """
        
        self.main_quests = []
        self.side_quests = []
        self.quest_names = []
        self.categories  = []
        
        for quest in self.quests:
            
            if quest.category == 'Main': self.main_quests.append(quest)
            else:                        self.side_quests.append(quest)
            
            self.quest_names.append(quest.name)
            self.categories.append(quest.category)

    def questlog_menu(self):
        """ Manages menu for quest titles and details. """
        
        # Show lsit of quests
        if self.menu_index == 0:
        
            # List of quests
            quest_index = new_menu(header='Questlog',
                                   options=self.quest_names,
                                   options_categories=self.categories)
            
            # Description of selected quest
            if type(quest_index) == int:
                self.selected_quest = self.quests[quest_index]
                self.update_questlog()
                selected_index = new_menu(header=self.selected_quest.name,
                                          options=self.selected_quest.content,
                                          options_categories=self.selected_quest.categories)
                
                # Go back to list of quests
                if type(selected_index) != int:
                    self.back_to_menu()
        
        # Show description of selected quest
        else:
            
            # Description of selected quest
            selected_index = new_menu(header=self.selected_quest.name,
                                      options=self.selected_quest.content,
                                      options_categories=self.selected_quest.categories)
            
            # Go back to list of quests
            if type(selected_index) == int:
                questlog.back_to_menu()

def friend_quest(init=False, NPC_name=None):
    """ Manages friend quest, including initialization and dialogue. """
    
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")

    global friend_messages, friend_level, NPC_names

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
    
    elif NPC_name == 'friend':
        
        # Increase friendship
        friend_level += 0.1
        if friend_level == 1.1:
            message("☑ You say hello to your new friend.", pyg.white)
            questlog.update_questlog(name="Making a friend")
        
        if int(friend_level) <= 3:
            message(friend_messages[f'level {int(friend_level)}'][random.randint(0, len(friend_messages[f'level {int(friend_level)}']))], pyg.white)
        else:
            if random.randint(0,10) != 1:
                message(friend_messages[f'level {int(friend_level)}'][random.randint(0, len(friend_messages[f'level {int(friend_level)}']))], pyg.white)
            else:
            
                # Start quest
                message("Woah! What's that?", pyg.white)
                x = lambda dx : int((player_obj.obj.x + dx)/pyg.tile_width)
                y = lambda dy : int((player_obj.obj.y + dy)/pyg.tile_height)

                found = False
                for i in range(3):
                    if found:
                        break
                    x_test = x(pyg.tile_width*(i-1))
                    for j in range(3):
                        y_test = y(pyg.tile_height*(j-1))
                        if not player_obj.env.map[x_test][y_test].entity:
                            item_component = Item(use_function=mysterious_note)
                            item = Object(0,
                                          0,
                                          img.dict['scrolls'][0],
                                          name="mysterious note", category="scrolls", image_num=0,
                                          item=item_component)
                            data_objects_1.append(item)
                            home_object_positions.append([x_test, y_test])
                            player_obj.env.map[x_test][y_test].item = item
                            found = True
                            break
        pygame.event.clear()

def mysterious_note():
    global questlog

    note_text = ["ξνμλ λξ ξλι ξγθιβξ ξ θθ.", "Ηκρσ σρσ λβνξθι νθ.", "Ψπθ αβνιθ πθμ."]
    new_menu(header="mysterious note", options=note_text, position="top left")
    message('Quest added!', pyg.green)
    mysterious_note = Quest(name='Mysterious note',
                         content=['My pyg.green friend dropped this. It has a strange encryption.',
                                  'ξνμλ λξ ξλι ξγθιβξ ξ θθ,', 'Ηκρσ σρσ λβνξθι νθ,', 'Ψπθ αβνιθ πθμ.',
                                  '☐ Keep an eye out for more mysterious notes.'],
                         category='Main')

#######################################################################################################################################################
# Uncategorized
def create_objects(selection, location):
    """ Creates and returns an object.
    
        Parameters
        ----------
        selection : string; name of object
        location  : list of int; coordinates of item location """

    # ----------------------- WEAPONS -----------------------
    # Shovel
    if selection == 'shovel':
        item_component  = Equipment(
            slot        = 'right hand',
            power_bonus = 0,
            timer       = True,
            name        = 'shovel')
        item_object     = Object(
            name        = 'shovel',
            image       = img.dict['shovel'][0],
            x           = location[0] * pyg.tile_width,
            y           = location[1] * pyg.tile_height,
            category    = 'weapons',
            equipment   = item_component)
    
    # Super shovel
    elif selection == 'super shovel':
        item_component  = Equipment(
            slot        = 'right hand',
            power_bonus = 10,
            name        = 'super shovel')
        item_object     = Object(
            name        = 'super shovel',
            image       = img.dict['super shovel'][0],
            x           = location[0] * pyg.tile_width,
            y           = location[1] * pyg.tile_height,
            category    = 'weapons',
            equipment   = item_component)
    
    # Dagger
    elif selection == 'dagger':
        item_component  = Equipment(
            name        = 'dagger',
            slot        = 'right hand',
            power_bonus = 2)
        item_object     = Object(
            name        = 'dagger',
            image       = img.dict['dagger'][0],
            x           = location[0] * pyg.tile_width,
            y           = location[1] * pyg.tile_height,
            category    = 'weapons',
            equipment   = item_component)
    
    # Sword
    elif selection == 'sword':
        item_component  = Equipment(
            name        = 'sword',
            slot        = 'right hand',
            power_bonus = 3)
        item_object     = Object(
            name        = 'sword',
            image       = img.dict['sword'][0],
            x           = location[0] * pyg.tile_width,
            y           = location[1] * pyg.tile_height,
            category    = 'weapons',
            equipment   = item_component)
    
    # Blood dagger
    elif selection == 'blood dagger':
        item_component  = Equipment(
            name        = 'blood dagger',
            slot        = 'right hand',
            power_bonus = 4)
        item_object     = Object(
            name        = 'blood dagger',
            image       = img.dict['blood dagger'][0],
            x           = location[0] * pyg.tile_width,
            y           = location[1] * pyg.tile_height,
            category    = 'weapons',
            equipment   = item_component)
    
    # Blood sword
    elif selection == 'blood sword':
        item_component  = Equipment(
            name        = 'blood sword',
            slot        = 'right hand',
            power_bonus = 6)
        item_object     = Object(
            name        = 'blood sword',
            image       = img.dict['blood sword'][0],
            x           = location[0] * pyg.tile_width,
            y           = location[1] * pyg.tile_height,
            category    = 'weapons',
            equipment   = item_component)

    # ----------------------- ARMOR -----------------------
    # Clothes
    elif selection == 'clothes':
        item_component    = Equipment(
            name          = 'clothes',
            slot          = 'body',
            defense_bonus = 10)
        item_object       = Object(
            name          = 'clothes',
            image         = img.dict['clothes'][0],
            x             = location[0] * pyg.tile_width,
            y             = location[1] * pyg.tile_height,
            category      = 'apparel',
            equipment     = item_component)
    
    # Wig
    elif selection == 'wig':
        item_component    = Equipment(
            name          = hair_list[hair_index],
            slot          = 'head',
            power_bonus   = 0)
        item_object       = Object(
            name          = hair_list[hair_index],
            image         = img.dict[hair_list[hair_index]][0],
            x             = location[0] * pyg.tile_width,
            y             = location[1] * pyg.tile_height,
            category      = 'hair',
            equipment     = item_component)
    
    # Shield
    elif selection == 'shield':
        item_component    = Equipment(
            name          = 'shield',
            slot          = 'left hand',
            defense_bonus = 3)
        item_object       = Object(
            name          = 'shield',
            image         = img.dict['shield'][0],
            x             = location[0] * pyg.tile_width,
            y             = location[1] * pyg.tile_height,
            category      = 'apparel',
            equipment     = item_component)

    # ----------------------- POTIONS -----------------------
    # Healing potion
    elif selection == 'healing potion':
        item_component   = Item(
            use_function = cast_heal)
        item_object      = Object(
            name         = 'healing potion',
            image        = img.dict['potions'][0],
            image_num    = 0,
            x            = location[0] * pyg.tile_width,
            y            = location[1] * pyg.tile_height,
            category     = 'potions',
            item         = item_component)
    
    # Transformation potion
    elif selection == 'transformation potion':
        item_component   = Item()
        item_object      = Object(
            name         = 'transformation potion',
            image        = img.dict['potions'][1],
            image_num    = 1,
            x            = location[0] * pyg.tile_width,
            y            = location[1] * pyg.tile_height,
            category     = 'potions',
            item         = item_component)
    
    # ----------------------- SCROLLS -----------------------
    # Scroll of lightning bolt
    elif selection == 'scroll of lightning bolt':
        item_component   = Item(
            use_function = cast_lightning)
        item_object      = Object(
            name         = 'scroll of lightning bolt',
            image        = img.dict['scrolls'][0],
            image_num    = 0,
            x            = location[0] * pyg.tile_width,
            y            = location[1] * pyg.tile_height,
            category     = 'scrolls',
            item         = item_component)
    
    # Scroll of fireball
    elif selection == 'scroll of fireball':
        item_component   = Item(
            use_function = cast_fireball)
        item_object      = Object(
            name         = 'scroll of fireball',
            image        = img.dict['scrolls'][0],
            image_num    = 0,
            x            = location[0] * pyg.tile_width,
            y            = location[1] * pyg.tile_height,
            category     = 'scrolls',
            item         = item_component)

    # Scroll of confusion
    elif selection == 'scroll of confusion':
        item_component   = Item(
            use_function = cast_confuse)
        item_object      = Object(
            name         = 'scroll of confusion',
            image        = img.dict['scrolls'][0],
            image_num    = 0,
            x            = location[0] * pyg.tile_width,
            y            = location[1] * pyg.tile_height,
            category     = 'scrolls',
            item         = item_component)
    
    # ----------------------- OTHER -----------------------
    # Stairs
    elif selection == 'stairs':
        item_object      = Object(
            name         = 'stairs',
            image        = img.dict['stairs'][0],
            x            = location[0] * pyg.tile_width,
            y            = location[1] * pyg.tile_height)
    
    else:
        print(selection)
    
    return item_object

#######################################################################################################################################################
# WIP
def __WIP__():
    pass

def save_account():    
    
    # Save environments
    with open(f"Data/File_{player_obj.file_num}/env.pkl", 'wb') as file:
        pickle.dump(player_obj.env, file)
    
    # Save player
    with open(f"Data/File_{player_obj.file_num}/obj.pkl", 'wb') as file:
        pickle.dump(player_obj.obj, file)
    
    # Apply images
    ## defaults
    ## customization (handedness)
    
def load_account():
    global player_obj
    
    with open("player_obj.pkl", "rb") as file:
        player_obj = pickle.load(file)


#######################################################################################################################################################
# World creation and management
class Environment:
    """ Generates and manages each world, such as each floor of the dungeon. """
    
    def __init__(self, size='medium', soundtrack=[None]):
        """ map  :
            soundtrack : list of pygame audio files """
        
        # Map
        size_dict = {'small': 1, 'medium': 5, 'large': 10}
        self.map  = [[Tile(True, x, y, visible=False, image='walls')
                           for y in range(0, pyg.map_height * size_dict[size], pyg.tile_height)]
                           for x in range(0, pyg.map_width  * size_dict[size], pyg.tile_width)]
        
        # Audio
        self.soundtrack = soundtrack
    
        # NPCs
        self.active_entities = []
    
    def create_room(self, rectangle_obj, block_sight=False, unbreakable=False, floor_effect=None, image='floors', image_num=0):
        """ Creates tiles for a room's floor and walls.
            Takes Rectangle object as an argument with parameters for width (x2 - x1) and height (y2 - y1). """
        
        for x in range(rectangle_obj.x1 + 1, rectangle_obj.x2):
            for y in range(rectangle_obj.y1 + 1, rectangle_obj.y2):
                tile              = self.map[x][y]
                
                tile.room         = rectangle_obj
                tile.blocked      = False # False for path, True for barrier
                tile.block_sight  = block_sight # False for floor, True for wall
                tile.floor_effect = floor_effect # sets floor effects
                tile.image        = image
                tile.image_num    = image_num
                
                if unbreakable:
                    if (x == rectangle_obj.x1 + 1) or (x == rectangle_obj.x2 - 1) or (y == rectangle_obj.y1 + 1) or (y == rectangle_obj.y2 - 1):
                        tile.unbreakable = True                
                    else:
                        tile.block_sight = False

    def create_h_tunnel(self, x1, x2, y):
        """ Creates horizontal tunnel. min() and max() are used if x1 is greater than x2. """
        if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
        
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.map[x][y].blocked = False
            self.map[x][y].block_sight = False
            self.map[x][y].image = 'floors'

    def create_v_tunnel(self, y1, y2, x):
        """ Creates vertical tunnel. min() and max() are used if y1 is greater than y2. """
        if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}")
        
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.map[x][y].blocked = False
            self.map[x][y].block_sight = False
            self.map[x][y].image = 'floors'

def build_home():
    """ Generates player's home. """
    
    # Set audio tracks
    home_soundtrack = aud.home[0]
    
    # Initialize environment
    env_home        = Environment(size='medium', soundtrack=[home_soundtrack])
    player_obj.home = env_home

    # Construct rooms
    main_room       = Rectangle(10, 10, mech.room_max_size, mech.room_max_size)
    secret_room     = Rectangle(30, 30, mech.room_min_size*2, mech.room_min_size*2)
    env_home.center = main_room.center()
    env_home.create_room(main_room)
    env_home.create_room(secret_room, block_sight=True, unbreakable=True)

    # Place items in home
    for i in range(5): 

        # Healing potion
        x, y                    = 13, 11
        item                    = create_objects('healing potion', [x, y])
        env_home.map[x][y].item = item
        
        # Lightning scroll
        x, y                    = 14, 11
        item                    = create_objects('scroll of lightning bolt', [x, y])
        env_home.map[x][y].item = item

        # Fireball scroll
        x, y                    = 15, 11
        item                    = create_objects('scroll of fireball', [x, y])
        env_home.map[x][y].item = item

        # Blood sword
        x, y                    = 33, 33
        item                    = create_objects('blood sword', [x, y])
        env_home.map[x][y].item = item

        # Shield
        x, y                    = 34, 34
        item                    = create_objects('shield', [x, y])
        env_home.map[x][y].item = item

        # Bug fix
        x, y                    = 0, 0
        item                    = create_objects('scroll of fireball', [x, y])
        env_home.map[x][y].item = item        
    
    # Generate stairs
    x, y                    = 18, 15
    stairs                  = create_objects('stairs', [x, y])
    env_home.map[x][y].item = stairs
    
    # Generate friend
    x, y                       = 18, 18
    fighter_component          = Fighter(
                hp             = 200,
                defense        = 0,
                power          = 0,
                exp            = 0,
                death_function = monster_death)
    ai_component               = BasicMonster()
    monster                    = Object(
                name           = 'friend',
                image          = img.dict['monsters'][0],
                x              = x * pyg.tile_width,
                y              = y * pyg.tile_height,
                blocks         = True,
                fighter        = fighter_component,
                ai             = ai_component)
    env_home.map[x][y].entity  = monster
    monster.tile               = env_home.map[x][y]

def build_dungeon_level():
    """ Generates a dungeon level. """
    
    # Set audio tracks
    dungeon_soundtrack = aud.dungeons[player_obj.obj.dungeon_lvl]

    # Initialize environment
    player_obj.dungeons.append(Environment(size='medium', soundtrack=[dungeon_soundtrack]))
    
    # Construct rooms
    rooms, room_counter = [], 0
    num_rooms           = int(mech.max_rooms * player_obj.obj.dungeon_lvl)
    new_map_height      = int(pyg.map_height * player_obj.obj.dungeon_lvl)
    new_map_width       = int(pyg.map_width  * player_obj.obj.dungeon_lvl)
 
    for i in range(num_rooms):
        
        # Construct room
        width    = random.randint(mech.room_min_size, mech.room_max_size)
        height   = random.randint(mech.room_min_size, mech.room_max_size)
        x        = random.randint(0,             pyg.tile_map_width  - width - 1)
        y        = random.randint(0,             pyg.tile_map_height - height - 1)
        new_room = Rectangle(x, y, width, height)

        failed = False
        if random.choice([0, 1, 2, 3]) != 0: # include more values to make more hallways (?)
            for other_room in rooms:
                if new_room.intersect(other_room):
                    failed = True
                    break

        # Set floor image
        if random.choice(range(player_obj.obj.dungeon_lvl)) >= player_obj.obj.dungeon_lvl*(3/4):
            player_obj.dungeons[-1].create_room(new_room, image_num=5)
        else:
            player_obj.dungeons[-1].create_room(new_room, image_num=0)

        # Customize room
        if not failed:
            x, y = new_room.center()[0], new_room.center()[1]
            
            # Place player in first room
            if room_counter == 0:
                player_obj.obj.x    = x * pyg.tile_width
                player_obj.obj.y    = y * pyg.tile_height
                player_obj.dungeons[-1].map[x][y].entity = player_obj.obj
                player_obj.obj.tile = player_obj.dungeons[-1].map[x][y]
                check_tile(x, y)
                player_obj.dungeons[-1].center = new_room.center()
            
            # Construct hallways
            else:
                (prev_x, prev_y) = rooms[room_counter-1].center()
                if random.randint(0, 1) == 0:
                    player_obj.dungeons[-1].create_h_tunnel(prev_x, x, prev_y)
                    player_obj.dungeons[-1].create_v_tunnel(prev_y, y, x)
                else:
                    player_obj.dungeons[-1].create_v_tunnel(prev_y, y, prev_x)
                    player_obj.dungeons[-1].create_h_tunnel(prev_x, x, y)
                
            # Place objects
            place_objects(new_room)
            
            # Prepare for next room
            rooms.append(new_room)
            room_counter += 1

    # Generate stairs
    stairs = create_objects('stairs' , [prev_x, prev_y])
    player_obj.dungeons[-1].map[prev_x][prev_y].item = stairs

def place_player(env, loc):
    """ Sets player in a new position.

        Parameters
        ----------
        env : Environment object; new environment of player
        loc : list of integers; new location of player """
    
    player_obj.env                 = env

    player_obj.obj.x                       = loc[0] * pyg.tile_width
    player_obj.obj.y                       = loc[1] * pyg.tile_height
    player_obj.obj.tile                    = player_obj.env.map[loc[0]][loc[1]]
    env.map[loc[0]][loc[1]].entity = player_obj.obj
    check_tile(loc[0], loc[1])




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
            message(f"Movement speed: Default", pyg.blue)
        elif toggle_list[movement_speed_toggle] == 'Slow':
            pygame.key.set_repeat(0, 0)
            message(f"Movement speed: Fixed", pyg.white)
        else:
            pygame.key.set_repeat(175, 150)
            message(f"Movement speed: Fast", pyg.red)

def screenshot(lvl_width=1, lvl_height=1, cache=False, save=False, blur=False, big=False):
    """ Takes a screenshot.
        cache:  saves a regular screenshot under Data/Cache/screenshot.png
        save:   moves regular cached screenshot to Data/File_#/screenshot.png 
        blur:   adds a blur effect """
    
    global gui_toggle, msg_toggle, screenshot_time_counter
    
    if debug: print(f"{debug_call()[0]:<30}{debug_call()[1]}\tcache={cache}\tsave={save}\tbig={big}")

    pyg.gui_toggle, pyg.msg_toggle = False, False
    
    # Takes a screenshot whenever the menu is opened
    if cache:
        render_all()
        
        # Saves regular screenshot in Data
        destination_folder = 'Data/Cache'
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        destination_path = os.path.join(destination_folder, "screenshot.png")
        
        pygame.image.save(pyg.screen, destination_path)
    
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
    
    # Takes a screenshot of the entire map, not just the pyg.screen
    if big:
        camera_cache = [camera.x, camera.y]
            
        # Generate full pyg.screen with visible tiles
        pyg.screen = pygame.display.set_mode((len(player_obj.env.map[0])*16, len(player_obj.env.map)*16),)
        render_all(screenshot=True, visible=True)
        camera.x = 0
        camera.y = 0
        camera.update()
        
        # Save as is
        pygame.image.save(pyg.screen, "screenshot_visible.png") # pygame.Surface((pyg.map_width, pyg.map_height))
        destination_folder = "Data/Cache"
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        destination_path = os.path.join(destination_folder, "screenshot_visible.png")
        shutil.move("screenshot_visible.png", destination_path)
        #save_floor('screenshot_visible.pkl')
        
        if player_obj.obj.dungeon_lvl == 0:
            save_objects_to_file('screenshot_objects.pkl', data_source=data_objects_1)
        else:
            save_objects_to_file('screenshot_objects.pkl', data_source=objects)
        destination_folder = "Data/Cache"
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
        destination_path = os.path.join(destination_folder, "screenshot_objects.pkl")
        shutil.move("screenshot_objects.pkl", destination_path)
        
        pyg.screen = pygame.display.set_mode((pyg.screen_width, pyg.screen_height),)
        render_all()
        camera.x = camera_cache[0]
        camera.y = camera_cache[1]
        camera.update()
    pyg.gui_toggle, pyg.msg_toggle = True, True


#######################################################################################################################################################
# Global scripts
if __name__ == "__main__":
    main()

#######################################################################################################################################################