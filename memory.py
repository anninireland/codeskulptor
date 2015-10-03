# implementation of card game - Memory

import simplegui
import random

DECK = [0,1,2,3,4,5,6,7,0,1,2,3,4,5,6,7]
exposed = []
turns = 0
state = 0
posA = ''
posB = ''

# helper function to initialize globals
def new_game():
    global DECK, exposed, state, turns
    state = 0
    turns = 0
    label.set_text('Turns = '+str(turns))
    random.shuffle(DECK)
    exposed = [False] * 16
    
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global DECK, exposed, state, posA, posB, turns 
    clicked = pos[0] // 50
    if exposed[clicked] == False:
        exposed[clicked] = True 
        
        if state == 0:
            state = 1
            posA = clicked
        elif state == 1:
            turns += 1
            state = 2
            posB = clicked            
        else:
            if DECK[posA] == DECK[posB]:
                exposed[posA] = 'matched'
                exposed[posB] = 'matched'
            if DECK[posA] != DECK[posB]:
                exposed[posA] = False
                exposed[posB] = False       
            posA = clicked
#            turns += 1
            posB = ''
            state = 1

# cards are logically 50x100 pixels in size    
def draw(canvas):
    global DECK, exposed
    point = 15
    x = 0
    label.set_text('Turns = '+str(turns))
    for i in range(0,16):
        if exposed[i] == False:
            canvas.draw_polygon([(x,0),(x+50,0),(x+50,100),(x,100)],5,'Red','Green')
        else:
            canvas.draw_text(str(DECK[i]), (point,60), 48, 'white')
        point += 50
        x += 50 

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

