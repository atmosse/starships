# Anton Dimitrov
# CS 152 Project 11
# Fall 2019
#
# Template by Bruce A Maxwell
# Fall 2018
# CS 152 Project 11
#
# Make an Asteroids-like ship move around
#
# slightly modified by Eric Aaron, Fall 2018, Spring 2019
import math
import random
import time
import graphicsPlus as gr
import physics_objects as pho
import collision as coll

def buildObstacles(win):
	'''Create all of the obstacles in the scene and put them in a list;
	each obstacle is a Thing-inheriting object (Block, Hexagon, Rotating Block, Eye)
    different obstacles have different elasticities for exciting yet balanced bounciness!'''
	hexagon = pho.Hexagon(win)
	hexagon.setPosition(25, 25)
	hexagon.elasticity = 0.5
	# rotating block
	rblock1 = pho.RotatingBlock(win, 25, 5)
	rblock1.setRotVelocity(10)
	rblock1.setAngle(20)
	rblock1.elasticity = 1.2
	# regular blocks
	block2 = pho.Block(win)
	block2.setPosition(40, 10)
	block3 = pho.Block(win)
	block3.setPosition(25, 40)
	block4 = pho.Block(win)
	block4.setPosition(10, 10)
	# eyes 
	eye1 = pho.Eye(win)
	eye1.setPosition(10, 35)
	eye1.elasticity = 0.8
	eye2 = pho.Eye(win)
	eye2.setPosition(40, 35)
	eye2.elasticity = 0.8
	
	obstacles = [hexagon, rblock1, block2, block3, block4, eye1, eye2]

    # Return the list of Things
	return obstacles
	
def StartScreen(win):
	'''Creates the initial stage that gives the players basic instructions'''
	block  = pho.Block(win, 25, 25, 50, 50)
	block.setColor((255,20,147))
	# welcome message
	welcoming = gr.Text(gr.Point(250,150), "Welcome to SpaceStar Catcher")
	welcoming.setStyle('bold italic')
	welcoming.setSize(10)
	# instructions to procede 
	exitInstruct = gr.Text(gr.Point(250,220), "You may press the Q key to quit at anytime")
	continueInstruct = gr.Text(gr.Point(250,300), "Press on the screen to create a ball and then score 10 hits")
	continueInstruct.setSize(10)
	keyUse = gr.Text(gr.Point(250,400), "Player 1: Use the W, E, and S keys	Player 2 : Use the Left, Right, and Space keys")
	keyUse.setSize(10)
	# draw start screen items 
	block.draw()
	text = [welcoming, exitInstruct, continueInstruct, keyUse]
	for item in text:
		item.draw(win)
	win.update()
	return [block, welcoming, exitInstruct, continueInstruct, keyUse]
def undrawStartScreen(win, items):
	'''Removes the start screen from the window'''
	for item in items:
		item.undraw()
def Gameplay(win):
	'''draws the Start Screen and undraws it when the user clicks inside the window;
	on the spot clicked, a ball is created and the game begins with the while loop;
	when a player reaches 10 points, the loop/game ends;
	the string with the winning player is returned'''
	# score points 
	score_p1 = 0
	score_p2 = 0
	# variable used in rotation
	gamma = 10
	# variable used in acceleration
	delta = 1
	# world wrap variables 
	winWidth = 50
	winHeight = 50
	# framing
	dt = 0.01
	frame = 0
	# draw the obstacles defined in buildObstacles()
	obstacles = buildObstacles(win)
	for item in obstacles:
		item.draw()
	# make one ship for each player, draw it (2-player game extension #1)
	ship1 = pho.Ship(win, 20, 25)
	ship1.draw()
	ship1.setRotVelocity(20)
	ship2 = pho.Ship(win, 30, 25)
	ship2.draw()
	ship2.setRotVelocity(20)
	# display the start screen with instructions
	startItems = StartScreen(win)
	# make a ball 	
	click = win.getMouse()
	ball = pho.Ball(win)
	ball.setPosition(click.getX()/ball.scale, (win.getHeight() - click.getY())/ball.scale)
	ball.setVelocity(random.random()*10, random.random()*10)
	ball.setAcceleration(0, -10)
	ball.draw()	
	while True:
		# exit start screen upon clicking the mouse
		if click:
			undrawStartScreen(win, startItems)
		key = win.checkKey()
		# exit game upon pressing 'q'
		if key == 'q':
			break
		#_____________________________________________________________________________PLAYER 1 SHIP MOVEMENT 
		# if the user hits the 'a' key (spin left)
		if key == 'a':
        	# set the rotational velocity to the old rotational velocity plus gamma
			ship1.setRotVelocity(ship1.getRotVelocity() + gamma)
        	# call the ship's setFlickerOn method with no arguments
			ship1.setFlickerOn()
    	# elif the user hits the 'd' key (spin right )
		elif key == 'd':
        	# set the rotational velocity to the old rotational veloity minus gamma
			ship1.setRotVelocity(ship1.getRotVelocity() - gamma)
        	# call the ship's setFlickerOn method with no arguments
			ship1.setFlickerOn()
		# elif the user types 'w' (acceleration)
		elif key == 'w': 
        	# assign to a the ship's current angle (getAngle)
			a1 = ship1.getAngle()
        	# assign to theta the result of multiplying a by math.pi and dividing by 180
			theta = a1*math.pi/100
        	# assign to v the ship's current velocity (getVelocity)
			v1 = ship1.getVelocity()
        	# set the ship's velocity to it's new values
        	#   The new X velocity is v_new_x = v_old_x + cos(theta) * delta
			v1_new_x = v1[0] + math.cos(theta)*delta
        	#   The new Y velocity is v_new_y = v_old_y + sin(theta) * delta
			v1_new_y = v1[1] + math.sin(theta)*delta
			ship1.setVelocity(v1_new_x, v1_new_y)
        	# call the ship's setFlickerOn method with no arguments
			ship1.setFlickerOn()
		# assign to moveit the value False
		moveit1 = False
    	# assign to p the ship's current position.  You might want to cast it to a list.
		p1 = list(ship1.getPosition())
    	# if the x coordinate is less than 0
		if p1[0] < 0:
        	# add winWidth to the x coordinate
			p1[0] = p1[0] + winWidth
        	# assign to moveit the value True
			moveit1 = True
    	# elif the x coordinate is greater than winWidth
		elif p1[0] > winWidth:
        	# subtract winWidth from the x coordinate
			p1[0] = p1[0] - winWidth 
        	# assign to moveit the value True
			moveit1 = True
    	# if the y coordinate is less than 0
		if p1[1] < 0:
        	# add winHeight to the y coordinate
			p1[1] = p1[1] + winHeight
        	# assign to moveit the value True
			moveit1 = True
    	# elif the y coordinate is greater than winHeight
		elif p1[1] > winHeight:
        	# subtract winHeight from the y coordinate
			p1[1] = p1[1] - winHeight
        	# assign to moveit the value True
			moveit1 = True
    	# if moveit:
		if moveit1:
        	# set the ship's position to p
			ship1.setPosition(p1[0], p1[1])							
		#__________________________________________________________________________PLAYER 2 SHIP MOVEMENT
		# if the user hits the 'Left' key
		if key == 'Left':
        	# set the rotational velocity to the old rotational velocity plus gamma
			ship2.setRotVelocity(ship2.getRotVelocity() + gamma)
        	# call the ship's setFlickerOn method with no arguments
			ship2.setFlickerOn()
    	# elif the user hits the 'Right' key
		elif key == 'Right':
        	# set the rotational velocity to the old rotational veloity minus gamma
			ship2.setRotVelocity(ship2.getRotVelocity() - gamma)
        	# call the ship's setFlickerOn method with no arguments
			ship2.setFlickerOn()
		# elif the user hits 'Up' (acceleration)
		elif key == 'Up': 
        	# assign to a the ship's current angle (getAngle)
			a2 = ship2.getAngle()
        	# assign to theta the result of multiplying a by math.pi and dividing by 180
			theta = a2*math.pi/100
        	# assign to v the ship's current velocity (getVelocity)
			v2 = ship2.getVelocity()
        	# set the ship's velocity to it's new values
        	#   The new X velocity is v_new_x = v_old_x + cos(theta) * delta
			v2_new_x = v2[0] + math.cos(theta)*delta
        	#   The new Y velocity is v_new_y = v_old_y + sin(theta) * delta
			v2_new_y = v2[1] + math.sin(theta)*delta
			ship2.setVelocity(v2_new_x, v2_new_y)
        	# call the ship's setFlickerOn method with no arguments
			ship2.setFlickerOn()
		# assign to moveit the value False
		moveit2 = False
    	# assign to p the ship's current position.  You might want to cast it to a list.
		p2 = list(ship2.getPosition())
    	# if the x coordinate is less than 0
		if p2[0] < 0:
        	# add winWidth to the x coordinate
			p2[0] = p2[0] + winWidth
        	# assign to moveit the value True
			moveit2 = True
    	# elif the x coordinate is greater than winWidth
		elif p2[0] > winWidth:
        	# subtract winWidth from the x coordinate
			p2[0] = p2[0] - winWidth
        	# assign to moveit the value True
			moveit2 = True
    	# if the y coordinate is less than 0
		if p2[1] < 0:
        	# add winHeight to the y coordinate
			p2[1] = p2[1] + winHeight
        	# assign to moveit the value True
			moveit2 = True
    	# elif the y coordinate is greater than winHeight
		elif p2[1] > winHeight:
        	# subtract winHeight from the y coordinate
			p2[1] = p2[1] - winHeight
        	# assign to moveit the value True
			moveit2 = True
    	# if moveit:
		if moveit2:
        	# set the ship's position to p
			ship2.setPosition(p2[0], p2[1])
		# address collision between ships
		coll.collision(ship1, ship2, dt)
		# move ships + rotating block
		ship1.update(dt)
		ship2.update(dt)
		obstacles[1].rotate(4)
		#____________________________________________________________BALL INTERACTION WITH OBSTACLES AND SHIPS
		# if the ball is out of bounds, re-launch it randomly 
		(ball_px, ball_py) = ball.getPosition()
		if ball_px*ball.scale < ball.radius*ball.scale or ball_px*ball.scale >  win.getWidth() - ball.radius*ball.scale or ball_py*ball.scale < ball.radius*ball.scale or ball_py*ball.scale > win.getHeight() - ball.radius*ball.scale:
			# reposition the ball 
			ball.setPosition(random.randint(5, 45), random.randint(15,45))
		# collisions
		# if the player 1 collides with the ball
		if coll.collision(ball, ship1, dt):
			# add one point to player 1's score
			score_p1 += 1
			ball.setColor((255, 0, 0))
		# if the player 2 collides with the ball
		elif coll.collision(ball, ship2, dt):
			# add one point to player 2's score
			score_p2 += 1
			ball.setColor((0, 0, 255))
		# assign to collided (with obstacles) the value False
		collided = False
        # for each item in the shapes list
		for item in obstacles:
            # if the result of calling the collision function with the ball and the obstacle item is True
			if coll.collision(ball, item, dt):
				collided = True	
        # if collided is equal to False
		if collided == False:
            # call the update method of the ball with dt as the time step
			ball.update(dt)
			
		# update window
		frame += 1
		if frame % 10 == 0:
			win.update()
			time.sleep(0.5*dt)
			
		# if either player scores 10, game is finished 
		if score_p1 == 10:
			winner = "Player 1"
			break
		elif score_p2 == 10:
			winner = "Player 2"
			break
	# undraw everything after game ends 
	ship1.undraw()
	ship2.undraw()
	ball.undraw()
	for item in obstacles:
		item.undraw()
	# return the winning player 
	return winner
		
def EndScreen(win, winner):
	'''Creates the final stage that shows the winner;
	based on the button pressed, the player:
	Q - playAgain = False
	R - playsAgain = True
	the results (playAgain) is returned'''
	block  = pho.Block(win, 25, 25, 50, 50)	
	block.setColor((0,255,0))
	# winner announced 
	winnerString = "Winner is {}!".format(winner)
	winnerText = gr.Text(gr.Point(250,150), winnerString)
	winnerText.setStyle('bold italic')
	winnerText.setSize(15)
	# instructions 
	againInstruct = gr.Text(gr.Point(250,300), "Press R to play again") # play again extension #2
	againInstruct.setSize(10)
	quitGame = gr.Text(gr.Point(250,400), "Press Q to quit")
	quitGame.setSize(10)
	# draw start screen items 
	block.draw()
	text = [winnerText, againInstruct, quitGame]
	for item in text:
		item.draw(win)
		
	# update window with the end screen announcement + instructions
	win.update()
	
	# Press Q to exit or Press R to play again (extension #2)
	while True:
		key = win.checkKey()
		# if Q, does not play again / playAgain = False
		if key == 'q':
			playAgain = False
			break
		# if R, plays again / playAgain = True 
		elif key == 'r':
			playAgain = True
			break
		time.sleep(0.05)
	# at the end, undraw the visuals in this screen 
	for item in text:
		item.undraw()
	block.undraw()
	return playAgain

def main():
	'''creates the window for the simulation'''
	# make a window
	win = gr.GraphWin('SpaceStar Catcher', 500, 500, False)
	# always play the first game 
	playAgain = True
	while playAgain:
		# winner variable holds the string with the winning player
		winner = Gameplay(win) 
		# playing again depends on the button pressed by the player (Q to exit, R to play again)
		playAgain = EndScreen(win, winner)
if __name__ == "__main__":
	main()
