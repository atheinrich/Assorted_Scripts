##################################################################################################################
# Alex Heinrich, Eduardo Mata, Jaden Rosso, Keanu Reyna, Muath Alsawaier 
# 12/11/2020
# Programming Assignment #8
# Meteor Shower Game
# This program generates a simple game of avoidance.
##################################################################################################################


##################################################################################################################
# Imports
import pygame as pyg
import random


##################################################################################################################
# Functions
def set_speed(score, old_background):
    ''' Changes speed as score increases, then calls set_background() before returning
    both results to global script. '''
    speed = score/10 + 5
    background = set_background(speed, score, old_background)
    return speed, background

def set_background(speed, score, old_background):
    ''' Changes background color as score increases, then returns the value to set_speed(). '''
    if old_background[0] >= 230: # trigger for color 2
        if old_background[1] >= 230: # trigger for color 3
            if old_background[2] >= 230: # trigger for color reset
                background = (0,0,0) # reset color (x,y,z)
            else: background = (old_background[0], old_background[1], old_background[2] + score/300) # increase z
        else: background = (old_background[0], old_background[1] + score/200, old_background[2]) # increase y
    else: background = (old_background[0] + score/100, old_background[1], old_background[2]) # increase x  
    return background

def draw_meteors(met_list, met_dim, screen, color):
    ''' Draws each meteor in met_list when called by global script. '''
    for met in met_list:
        pyg.draw.rect(screen, color, (met[0], met[1], met_dim, met_dim))
    
def drop_meteors(met_list, met_dim, width):
    ''' Adds a new meteor to the game screen at a random interval. '''
    if random.randint(0, 9) == 1: # sets the chance of spawning a meteor
        met_x, met_y = random.randint(0, width), random.randint(-50, 0) # avoids overlap with y position
        met_pos = [met_x, met_y] # sets meteor position
        met_list.append(met_pos) # adds meteor to list

def update_meteor_positions(met_list, height, score, speed):
    ''' Adjusts the y-position of each meteor in met_list. When a meteor reaches the end of the
    screen, this function deletes it from the list. '''
    met_list_copy = met_list[:] # creates a copy of met_list
    for i in range(len(met_list_copy)):
        met_list_copy[i][-1] += speed
        if met_list_copy[i][-1] >= height:
            del met_list[i]
            score += 1
    return score

def detect_collision(met_pos, player_pos, player_dim):
    ''' Called by collision_check() for comparing each meteor position to that of the player.
    Note: met_pos=[x1,y1]; player_pos=[x2,y2]; player_dim=num; met_dim=num. '''
    if (player_pos[0]-player_dim/2) <= met_pos[0] <= (player_pos[0]+player_dim) and (player_pos[1]-player_dim/2) <= met_pos[1] <= (player_pos[1]+player_dim/2):
        return True
    else:
        return False

def collision_check(met_list, player_pos, player_dim):
    ''' Called by the global script to send meteor positions to detect_collision(). '''
    for met_pos in met_list:
        if detect_collision(met_pos, player_pos, player_dim) == True:
            return True
    return False

def escape():
    ''' Closes pygame abruptly. '''
    pyg.quit()


##################################################################################################################
# Global scripts
pyg.init()                                        # initialize pygame
    
width = 800                                       # set width of game screen in pixels
height = 600                                      # set height of game screen in pixels
player_color = (255,0,0)                          # rgb color of player
met_color = (244,208,63)                          # rgb color of meteors
background = (0,0,156)                            # initialize background colot (r,g,b)

player_dim = 50                                   # player size in pixels
player_pos = [width/2, height-2*player_dim]       # initial location of player

met_dim = 20                                      # meteor size in pixels
met_list = []                                     # initialize list of meteor positions

screen = pyg.display.set_mode((width, height))    # initialize game screen
game_over = False                                 # initialize game_over
score = 0                                         # initialize score
clock = pyg.time.Clock()                          # initialize clock

my_font = pyg.font.SysFont("monospace", 35)       # initialize system font

while not game_over:                              # play until game_over=True; update player_pos
    for event in pyg.event.get():                 # loop through events in queue
        if event.type == pyg.KEYDOWN:             # checks for key press
            x = player_pos[0]                     # assign current x position
            y = player_pos[1]                     # assign curren y position
            if event.key == pyg.K_LEFT or event.key == ord('a'):           # checks if left arrow
                x -= player_dim                   # moves player left
                if x < 0:                         # sets boundary
                   x = 0                   
            elif event.key == pyg.K_RIGHT or event.key == ord('d'):        # checks if right arrow
                x += player_dim                   # moves player right
                if x > width - player_dim:        # sets boundary
                   x = width - player_dim                       
            elif event.key == pyg.K_UP or event.key == ord('w'):           # moves player up
                if y < player_dim:                # sets boundary
                   y = player_dim 
                y -= player_dim
            elif event.key == pyg.K_DOWN or event.key == ord('s'):         # moves player down
                if y > height - 2*player_dim:     # sets boundary
                   y = height - 2*player_dim 
                y += player_dim
            elif event.key == pyg.K_ESCAPE:       # exit game
                escape()
            player_pos = [x, y]                   # reset player position

    screen.fill(background)                       # refresh screen bg color
    drop_meteors(met_list, met_dim, width)        # self-explanatory; read prompt
    speed, background = set_speed(score, background) # sets speed and background color
    score = update_meteor_positions(met_list, height, score, speed)
                                                  # read prompt
    text = "Score: " + str(score)                 # create score text
    label = my_font.render(text, 1, met_color)    # render text into label
    screen.blit(label, (width-250, height-40))    # blit label to screen at
                                                  # given position
    draw_meteors(met_list, met_dim, screen, met_color) # draw meteors
    pyg.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_dim, player_dim)) # draw player

    if collision_check(met_list, player_pos, player_dim): # check for collisions
        game_over = True                       
    
    clock.tick(60)                                 # set frame rate
    pyg.display.update()                           # update screen characters

print('GAME OVER\nFinal score:', score)            # final score
label = my_font.render("GAME OVER", 12, met_color) # render text into label
screen.blit(label, (40, height-40))                # blit label to screen
pyg.display.update()
pyg.time.delay(1200)                               # delays exit of window

pyg.display.quit()
pyg.quit()                                         # leave pygame


##################################################################################################################
