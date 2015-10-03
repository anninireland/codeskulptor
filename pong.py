# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_HEIGHT = PAD_HEIGHT/2
LEFT = False
RIGHT = True
paddle1_pos = 200
paddle2_pos = 200
paddle1_vel = 0
paddle2_vel = 0
ball_pos = [WIDTH/2,HEIGHT/2]
ball_vel = [0.5,-2.0]
score_p1 = 0
score_p2 = 0

# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH/2,HEIGHT/2]
    if direction is LEFT:
        ball_vel[0] = random.randrange(-5,-3)
        ball_vel[1] = random.randrange(-5,-3)
    if direction is RIGHT:
        ball_vel[0] = random.randrange(3,5)
        ball_vel[1] = random.randrange(-5,-3)
                
# define event handlers
def new_game():	
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    global ball_pos, ball_vel # these are vectors stored as lists
    global score_p1, score_p2
    score_p1 = 0
    score_p2 = 0
    spawn_ball(RIGHT)

def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel += 4
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel -= 4  
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += 4
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel -= 4 

def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel -= 4
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel += 4
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel -= 4
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel += 4       
  
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, score_p1, score_p2
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # Draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

    # draw paddles
    canvas.draw_line((0,paddle1_pos - HALF_PAD_HEIGHT),(0,paddle1_pos + HALF_PAD_HEIGHT), 16, "Yellow")
    canvas.draw_line((600,paddle2_pos - HALF_PAD_HEIGHT),(600,paddle2_pos + HALF_PAD_HEIGHT), 16, "Yellow")

    # draw scores
    canvas.draw_text(str(score_p1), (WIDTH*0.25, 40), 36, 'Red')
    canvas.draw_text(str(score_p2), (WIDTH*0.75, 40), 36, 'Red')    
    
    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # reflect off the top and bottom walls
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]

    # reset ball when it touches gutter 			# check if it hits paddle 
    if ball_pos[0] <= BALL_RADIUS+PAD_WIDTH: 		# check left paddle
        if ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT:
                ball_pos[0] = BALL_RADIUS + PAD_WIDTH
                ball_vel[0] = -ball_vel[0]*1.1
            else:
                score_p2 += 1
                spawn_ball(RIGHT)
        else:
            score_p2 += 1
            spawn_ball(RIGHT)

    if ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS:	# check right paddle
        if ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT:
                ball_pos[0] = WIDTH - PAD_WIDTH - BALL_RADIUS
                ball_vel[0] = - ball_vel[0]*1.1
            else:
                score_p1 += 1
                spawn_ball(LEFT)      
        else:
            score_p1 += 1
            spawn_ball(LEFT)

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos += paddle1_vel
    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel
    paddle2_pos += paddle2_vel
    
    if paddle1_pos <= HALF_PAD_HEIGHT:		#	keep paddle on screen
        paddle1_pos = HALF_PAD_HEIGHT
        
    if paddle1_pos >= 400 - HALF_PAD_HEIGHT:
        paddle1_pos = 400 - HALF_PAD_HEIGHT
            
    if paddle2_pos <= HALF_PAD_HEIGHT:		
        paddle2_pos = HALF_PAD_HEIGHT
        
    if paddle2_pos >= 400 - HALF_PAD_HEIGHT:
        paddle2_pos = 400 - HALF_PAD_HEIGHT
                    
# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Reset', new_game)
# start frame
new_game()
frame.start()
