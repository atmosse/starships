# Anton Dimitrov
# CS 152 Fall 2019
# Project 11
# 11/07/2019
import graphicsPlus as gr
import random 
import math

class Thing:
	def __init__(self, win, the_type):
		self.type = the_type
		self.mass = 1
		self.position = [0, 0]
		self.velocity = [0, 0]
		self.acceleration = [0, 0]
		self.elasticity = 1 # the amount of energy retained after a collision
		self.scale = 10 # scale between simulation space and pixels
		self.win = win
		self.vis = [] # holds Zelle graphics
		self.color = (0, 0, 0) # RGB tuple
		self.drawn = False 

	#GETTERS
	def getType(self):
		return self.type 
	def getPosition(self): # return a 2-element tuple with the x,y values
		return self.position[:]
	def getVelocity(self): # returns a 2-element tuple with the x and y velocities.
		return self.velocity[:]
	def getAcceleration(self): # returns a 2-element tuple with the x and y acceleration values.
		return self.acceleration[:]
	def getMass(self): # Returns the mass of the object as a scalar value
		return self.mass
	def getElasticity(self):
		return self.elasticity
	def getColor(self):
		return self.color 

	# draw and undraw methods
	def draw(self):
		for item in self.vis:
			item.draw(self.win)
		self.drawn = True
	def undraw(self):
		for item in self.vis:
			item.undraw()
		self.drawn = False 
	
	#SETTERS
	def setVelocity(self, vx, vy): # returns a 2-element tuple with the x and y velocities.
		self.velocity[0] = vx
		self.velocity[1] = vy
	def setAcceleration(self, ax, ay): # returns a 2-element tuple with the x and y acceleration values.
		self.acceleration[0] = ax
		self.acceleration[1] = ay
	def setMass(self, m): # Returns the mass of the object as a scalar value
		self.mass = m
	def setElasticity(self, e):
		self.elasticity = e
	
	# SETTER for position and color
	def setPosition(self, px, py):
		dx = (px - self.position[0])*self.scale
		dy = - (py -self.position[1])*self.scale
		for item in self.vis:
			item.move(dx, dy)  
		self.position[0] = px
		self.position[1] = py
	def setColor(self, c):
		self.color = c
		if c != None:
			for item in self.vis:
				item.setFill(gr.color_rgb( *self.color ) ) 
	# update method
	def update(self, dt): # implement the equations of motion for the block.
		'''intakes the parameter dt, which defines the updated position of the block'''
		# update the x position using x_new = x_old + x_vel*dt + 0.5*x_acc * dt*dt
		self.position[0] = self.position[0] + self.velocity[0]*dt + 0.5*self.acceleration[0]*dt*dt
		deltaX = self.velocity[0]*dt + 0.5*self.acceleration[0]*dt*dt
		# update the y position using y_new = y_old + y_vel*dt + 0.5*y_acc * dt*dt 
		self.position[1] = self.position[1] + self.velocity[1]*dt + 0.5*self.acceleration[1]*dt*dt
		deltaY = self.velocity[1]*dt + 0.5*self.acceleration[1]*dt*dt
		# assign to dx the x velocity times dt times the scale factor (self.scale)
		dx = deltaX*self.scale
		# assign to dy the negative of the y velocity times dt times the scale factor (self.scale)
		dy = - deltaY*self.scale 
		# for each item in self.vis
		for item in self.vis:
			# call the move method of the graphics object with dx and dy as arguments..
			item.move(dx, dy)
		# update the x velocity by adding the acceleration times dt to its old value
		self.velocity[0] = self.velocity[0] + self.acceleration[0]*dt
		# update the y velocity by adding the acceleration times dt to its old value
		self.velocity[1] = self.velocity[1] + self.acceleration[1]*dt

class Ball(Thing):
	def __init__(self, win, x0 = 25, y0 = 25, radius = 1):
		Thing.__init__(self, win, "ball")
		self.radius = radius
		self.position[0] = x0
		self.position[1] = y0
		self.refresh()
		color = (random.randint(0, 250), random.randint(0, 250), random.randint(0, 250))
		self.setColor(color)
	def refresh(self):
		'''draws the object;
		undraws and redraws the object when the object moves'''
		#assign to a local variable (e.g. drawn) the value of self.drawn
		drawn = self.drawn
		if drawn: 
    		#undraw the object (use self.undraw())
			self.undraw()
		#define the self.vis list of graphics objects using the current position, radius, and window
		self.vis = [ gr.Circle(gr.Point(self.position[0]*self.scale, self.win.getHeight() - self.position[1]*self.scale), self.radius*self.scale) ]
		if drawn:
    		#draw the object
			self.draw()
	# getter and setter for radius
	def getRadius(self):
		return self.radius
	def setRadius(self, r):
		self.radius = r
		self.refresh()

class Block(Thing):
	def __init__(self, win, px = 25, py = 25, dx=5, dy=5):
		Thing.__init__(self, win, "block")
		self.position[0] = px
		self.position[1] = py
		self.width = dx
		self.height = dy	
		self.reshape()
		self.color = (random.randint(0, 250), random.randint(0, 250), random.randint(0, 250))
		self.setColor(self.color)
	def reshape(self):
		'''draws the object;
		undraws and redraws the object when the object moves'''
		if self.drawn:
			self.undraw()

		self.vis = [ gr.Rectangle(gr.Point( (self.position[0] - self.width/2)*self.scale, self.win.getHeight() - (self.position[1] + self.height/2)*self.scale) , 
                                  gr.Point( (self.position[0] + self.width/2)*self.scale, self.win.getHeight() - (self.position[1] - self.height/2)*self.scale) )  ]
		if self.drawn:
			self.draw()
	
	# SETTERS AND GETTERS for WIDTH AND HEIGHT
	def getWidth(self):
		return self.width
	def getHeight(self):
		return self.height
	def setWidth(self, w):
		self.width = w
	def setHeight(self, h):
		self.height = h

# equilateral triangle class 
class Hexagon(Thing):
	def __init__(self, win, x0 = 25, y0 = 25, width = 5, height = 5):
		Thing.__init__(self, win, "hexagon")
		# treated as block for collision
		self.width = width
		self.height = height
		self.position[0] = x0
		self.position[1] = y0
		self.refresh()
		self.color = (random.randint(0, 250), random.randint(0, 250), random.randint(0, 250))
		self.setColor(self.color)

	def refresh(self):
		'''draws the object;
		undraws and redraws the object when the object moves'''
		#assign to a local variable (e.g. drawn) the value of self.drawn
		drawn = self.drawn
		if drawn: 
    		#undraw the object (use self.undraw())
			self.undraw()
			
		hexPoints = ( gr.Point((self.position[0] - self.width/2)*self.scale, self.win.getHeight() - self.position[1]*self.scale ),
					  gr.Point((self.position[0] - self.width/4)*self.scale, self.win.getHeight() - (self.position[1] + self.height/2)*self.scale ),
					  gr.Point((self.position[0] + self.width/4)*self.scale, self.win.getHeight() - (self.position[1] + self.height/2)*self.scale ),
					  gr.Point((self.position[0] + self.width/2)*self.scale, self.win.getHeight() - self.position[1]*self.scale ),
					  gr.Point((self.position[0] + self.width/4)*self.scale, self.win.getHeight() - (self.position[1] - self.height/2)*self.scale ),
					  gr.Point((self.position[0] - self.width/4)*self.scale, self.win.getHeight() - (self.position[1] - self.height/2)*self.scale ) )
					  
		self.vis = [ gr.Polygon(*hexPoints)]
		if drawn:
    		#draw the object
			self.draw()
			
	# SETTERS AND GETTERS for side
	def getWidth(self):
		return self.width
	def setWidth(self, w):
		self.width = w
	# GETTER and SETTER for height
	def getHeight(self):
		return self.height
	def setHeight(self, h):
		self.height = h

class Ring(Thing):
	def __init__(self, win, x0 = 25, y0 = 25, radius = 2):
		Thing.__init__(self, win, "ring")
		# threated as circle
		self.bubbleRadius = 1
		self.radius = radius
		self.position[0] = x0
		self.position[1] = y0
		self.refresh()
		self.color = (random.randint(0, 250), random.randint(0, 250), random.randint(0, 250))
		self.setColor(self.color)
	def refresh(self):
		'''draws the object;
		undraws and redraws the object when the object moves'''
		#assign to a local variable (e.g. drawn) the value of self.drawn
		drawn = self.drawn
		if drawn: 
    		#undraw the object (use self.undraw())
			self.undraw()
			
		self.vis = [gr.Circle(gr.Point( (self.position[0] - self.radius)*self.scale, self.win.getHeight() - (self.position[1] + self.radius/2)*self.scale), self.bubbleRadius*self.scale),
					gr.Circle(gr.Point( (self.position[0] - self.radius)*self.scale, self.win.getHeight() - (self.position[1] - self.radius/2)*self.scale), self.bubbleRadius*self.scale),
					gr.Circle(gr.Point( (self.position[0] + self.radius)*self.scale, self.win.getHeight() - (self.position[1] + self.radius/2)*self.scale), self.bubbleRadius*self.scale),
					gr.Circle(gr.Point( (self.position[0] + self.radius)*self.scale, self.win.getHeight() - (self.position[1] - self.radius/2)*self.scale), self.bubbleRadius*self.scale),
					gr.Circle(gr.Point( self.position[0]*self.scale, self.win.getHeight() - (self.position[1] + self.radius)*self.scale), self.bubbleRadius*self.scale),
					gr.Circle(gr.Point( self.position[0]*self.scale, self.win.getHeight() - (self.position[1] - self.radius)*self.scale), self.bubbleRadius*self.scale)]
		if drawn:
    		#draw the object
			self.draw()
	def getRadius(self):
		return self.radius + 1 
	def setRadius(self, r):
		self.radius = r
		self.refresh()

class Patrick(Thing):
	def __init__(self, win, x0 = 25, y0 = 25, radius = 4, color = None):
		Thing.__init__(self, win, "patrick")
		self.radius = radius
		self.position[0] = x0
		self.position[1] = y0
		self.refresh()
		self.color = color
		self.setColor(self.color)

	def refresh(self):
		'''draws the object;
		undraws and redraws the object when the object moves'''
		#assign to a local variable (e.g. drawn) the value of self.drawn
		drawn = self.drawn
		if drawn: 
    		#undraw the object (use self.undraw())
			self.undraw()
			
		starPoints = ( gr.Point((self.position[0] - self.radius)*self.scale, self.win.getHeight() - self.position[1]*self.scale ),
					  gr.Point((self.position[0] + self.radius)*self.scale, self.win.getHeight() - self.position[1]*self.scale ),
					  gr.Point((self.position[0] - self.radius/2)*self.scale, self.win.getHeight() - (self.position[1] - self.radius)*self.scale ),
					  gr.Point(self.position[0]*self.scale, self.win.getHeight() - (self.position[1] + self.radius)*self.scale ),
					  gr.Point((self.position[0] + self.radius/2)*self.scale, self.win.getHeight() - (self.position[1] - self.radius)*self.scale ),
					  
					  gr.Point((self.position[0] - self.radius)*self.scale, self.win.getHeight() - self.position[1]*self.scale ) )
					  
		self.vis = [ gr.Polygon(*starPoints)]
		if drawn:
    		#draw the object
			self.draw()
			
	def getRadius(self):
		return self.radius + 1 
	def setRadius(self, r):
		self.radius = r
		self.refresh()
		
class Eye(Thing):
	def __init__(self, win, px = 25, py = 25, dx=5, dy=5, radius = 2):
		Thing.__init__(self, win, "block")
		self.radius = radius
		self.position[0] = px
		self.position[1] = py
		self.width = dx
		self.height = dy	
		self.reshape()
	def reshape(self):
		'''draws the object;
		undraws and redraws the object when the object moves'''
		if self.drawn:
			self.undraw()

		self.vis = [ gr.Rectangle(gr.Point( (self.position[0] - self.width/2)*self.scale, self.win.getHeight() - (self.position[1] + self.height/2)*self.scale) , 
                                  gr.Point( (self.position[0] + self.width/2)*self.scale, self.win.getHeight() - (self.position[1] - self.height/2)*self.scale) ),
					 gr.Circle(gr.Point(self.position[0]*self.scale, self.win.getHeight() - self.position[1]*self.scale), self.radius*self.scale),
					 gr.Circle(gr.Point(self.position[0]*self.scale, self.win.getHeight() - self.position[1]*self.scale), self.radius*self.scale/2)   ]
		self.vis[0].setFill("white")
		self.vis[1].setFill("black")
		self.vis[2].setFill("red")
		if self.drawn:
			self.draw()
	
	# SETTERS AND GETTERS for WIDTH AND HEIGHT
	def getWidth(self):
		return self.width
	def getHeight(self):
		return self.height
	def setWidth(self, w):
		self.width = w
	def setHeight(self, h):
		self.height = h
	def getRadius(self):
		return self.radius + 1 
	def setRadius(self, r):
		self.radius = r
		self.refresh()

# Project 10
class RotatingBlock(Thing):
	def __init__(self, win, x0=25, y0=25, width=10, height=3, Ax=None, Ay=None):
		Thing.__init__(self, win, 'rotating block')
		self.pos = [x0, y0]
		self.width = width 
		self.height = height
		if Ax != None and Ay != None:
		    self.anchor = [Ax, Ay]
		else:
		    self.anchor = [x0, y0]
		#self.setAnchor( 20, 25 )
		self.points = [
					   [-width/2, -height/2], 
					   [width/2, -height/2], 
					   [width/2, height/2],
					   [-width/2, height/2]
					   ]
		self.angle = 0.0
		self.rvel = 0.0
		self.drawn = False
		self.refresh()
		
	def refresh(self):
		'''draws rendered object;
		if drawn, undraws, renders, then draws again;
		if not drawn, renders'''
		drawn = self.drawn
		if drawn:
			self.undraw()
		self.render()
		if drawn:
			self.draw()
			
	def rotate(self, rot):
		'''updates the angle of rotation;
		refreshes the image'''
		self.angle += rot
		self.refresh()
	
			
	def render(self):
		'''updates position of vertex points based on given angle of rotation;
		therefore, sets up the math needed for the rotation effect'''
		# angle of rotation
		Theta = self.angle*math.pi/180.0
		pts = []
		for vertex in self.points:
			# assign to x and y the results of adding the vertex to self.pos and subtracting self.anchor
			x = self.pos[0] + vertex[0] - self.anchor[0]
			y = self.pos[1] + vertex[1] - self.anchor[1]
			# assign to xt the calculation x * cos(Theta) - y * sin(Theta)
			xt = x * math.cos(Theta) - y * math.sin(Theta)
			# assign to yt the calculation x * sin(Theta) + y * cos(Theta)
			yt = x * math.sin(Theta) + y * math.cos(Theta)
			# assign to x and y the result of adding xt and yt to self.anchor
			x = xt + self.anchor[0]
			y = yt + self.anchor[1]
			# append to pts a Point object with coordinates (self.scale*x, self.win.getHeight() - self.scale*y)
			pts.append(gr.Point(self.scale*x, self.win.getHeight() - self.scale*y))
			# assign to self.vis a list with a Zelle graphics Line object using the Point objects in pts
		self.vis = [ gr.Polygon(pts[0], pts[1], pts[2], pts[3]) ]

	def update(self, dt): # implement the equations of motion for the block.
		'''intakes the parameter dt, which defines the updated position of the block'''
		# change in angle during time step
		da = self.rvel*dt
		if da != 0:
			self.rotate(da)
		# update the x position using x_new = x_old + x_vel*dt + 0.5*x_acc * dt*dt
		self.position[0] = self.position[0] + self.velocity[0]*dt + 0.5*self.acceleration[0]*dt*dt
		deltaX = self.velocity[0]*dt + 0.5*self.acceleration[0]*dt*dt
		# update the y position using y_new = y_old + y_vel*dt + 0.5*y_acc * dt*dt 
		self.position[1] = self.position[1] + self.velocity[1]*dt + 0.5*self.acceleration[1]*dt*dt
		deltaY = self.velocity[1]*dt + 0.5*self.acceleration[1]*dt*dt
		# assign to dx the x velocity times dt times the scale factor (self.scale)
		dx = deltaX*self.scale
		# assign to dy the negative of the y velocity times dt times the scale factor (self.scale)
		dy = - deltaY*self.scale 
		# for each item in self.vis
		for item in self.vis:
			# call the move method of the graphics object with dx and dy as arguments..
			item.move(dx, dy)
		# update the x velocity by adding the acceleration times dt to its old value
		self.velocity[0] = self.velocity[0] + self.acceleration[0]*dt
		# update the y velocity by adding the acceleration times dt to its old value
		self.velocity[1] = self.velocity[1] + self.acceleration[1]*dt
		
	# setter and getter for angle
	def setAngle(self, a):
		self.angle = a
		self.refresh()
	def getAngle(self):
		return self.angle
	# rotate method
	def rotate(self, rot):
		self.angle += rot
		self.refresh()
	# setters and getters for rotation anchor points
	def setAnchor(self, px, py):
		self.anchor[0] = px
		self.anchor[1] = py	
	def getAnchor(self):
		return self.anchor[:]	
	# setters and getters for rotation velocity
	def setRotVelocity(self, v):
		self.rvel = v
	def getRotVelocity(self):
		return self.rvel
	# setters and getters for width and height
	def getWidth(self):
		return self.width
	def getHeight(self):
		return self.height
	def setWidth(self, w):
		self.width = w
	def setHeight(self, h):
		self.height = h

# ship object, treated as a ball
# able to rotate
class Ship(Thing):
    def __init__(self, win, x0=0, y0=0, mass=1, radius=3):
        Thing.__init__(self, win, 'ball')
        self.setMass(mass)
        self.radius = radius
        self.setPosition(x0, y0)

        # anchor point is by default the center of the ship/circle so we don't need it
        self.angle = 0.
        self.dangle = 0.

        # visualization properties
        # This is a two-part visualization
        # the ship is a triangle
        self.bodypts = [ (radius, 0),
                         (- radius*0.5,   1.732*radius*0.5),
                         (- radius*0.5, - 1.732*radius*0.5) ]
        # the exhaust is another triangle
        self.flamepts = [ (- radius*0.5,   0.5*radius),
                          (- radius*0.5, - 0.5*radius),
                          (- radius*1.732, 0) ]

        self.scale = 10.
        self.vis = []
        self.drawn = False
        self.refresh() # call refresh to set up the vis list properly

        # these are for handling the flicker of the exhaust
        self.flickertime = 6
        self.flicker = False
        self.countdown = 0

    #########
    # these functions are identical to the rotating block
    # a smart coder would make a parent rotator class

    # draw the object into the window
    def refresh(self):
        drawn = self.drawn
        if drawn:
            self.undraw()
            
        self.render()
        
        if drawn:
            self.draw()

    # get and set the angle of the object
    # these are unique to rotators
    def getAngle(self):
        return self.angle

    # setAngle has to update the visualization
    def setAngle(self, a):
        self.angle = a
        self.refresh()

    # get and set rotational velocity
    def setRotVelocity(self, rv):
        self.dangle = rv # degrees per second

    def getRotVelocity(self):
        return self.dangle

    def getRadius(self):
        return self.radius

    def setRadius(self, r):
        self.radius = r
        self.refresh()

    # incrementally rotate by da (in degrees)
    # has to update the visualization
    def rotate(self, da):
        self.angle += da
        self.refresh()

    # special ship methods
    def setFlickerOn(self, countdown = 50):
        self.flicker = True
        self.countdown = countdown

    def setFlickerOff(self):
        self.countdown = 0
        self.flicker = False
        
    # simplified render function since the ship always rotates around its center
    def render(self):

        # get the cos and sin of the current orientation
        theta = math.pi * self.angle / 180.
        cth = math.cos(theta)
        sth = math.sin(theta)

        # rotate each point around the object's center
        pts = []
        for vertex in self.bodypts + self.flamepts:
            # move the object's center to 0, 0, which it is already in model coordinates
            xt = vertex[0]
            yt = vertex[1]

            # rotate the vertex by theta around the Z axis
            xtt = cth*xt - sth*yt
            ytt = sth*xt + cth*yt

            # move the object's center back to its original location
            pos = self.getPosition()
            xf = xtt + pos[0]
            yf = ytt + pos[1]

            # create a point with the screen space coordinates
            pts.append( gr.Point(self.scale * xf, self.win.getHeight() - self.scale * yf) )

        # make the two objects
        self.vis = [ gr.Polygon( pts[:3] ), gr.Polygon( pts[3:] ) ]
        self.vis[0].setFill("dark blue")
        self.vis[0].setOutline("dark red")
        self.vis[1].setOutline("yellow")

    # update the various state variables
    # add a unique flicker touch
    def update(self, dt):
        # update the angle based on rotational velocity
        da = self.dangle * dt
        if da != 0.0: # don't bother updating if we don't have to
            self.rotate( da )

        # flicker the flames
        # this should be a field of the object
        if self.flicker and self.countdown > 0:
            if self.countdown % self.flickertime < self.flickertime/2:
                self.vis[1].setFill( 'yellow' )
            else:
                self.vis[1].setFill( 'orange' )
            self.countdown -= 1
        else:
            self.vis[1].setFill( 'white' )

        # call the parent update for the rest of it
        Thing.update(self, dt)