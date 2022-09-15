# Bruce A. Maxwell
# CS 151S
# Fall 2015
#
# Project 11
# Collision handler
#
# Modified by Eric Aaron, Fall 2018, Spring 2019
# Updated by Bruce Maxwell, Fall 2019
#   new ball_ball collision
#   updated ball_block collision
#   removed dependency on Block object parameter positioning

import physics_objects as pho
import math

# utility math function for calculating Euclidean length of a 2D vector
def length(v):
    return math.sqrt(v[0]*v[0] + v[1]*v[1])

# utility math function for creating a unit 2D vector
def unit(v):
    l = math.sqrt(v[0]*v[0] + v[1]*v[1])
    if l > 0.0:
        return (v[0]/l, v[1]/l)
    return v


def collisionTest_ball_ball(ball1, ball2):
    """Tests if there is a collision with another ball along the path of
    the ball.  Returns the distance to the collision or 1e+6 (a big number)"""
    
    # Concept: hold ball2 still and test if ball1 will hit it
    # Ray-circle intersection
    v1 = ball1.getVelocity()
    p1 = ball1.getPosition()
    p2 = ball2.getPosition()
    r = ball1.getRadius() + ball2.getRadius()

    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]

    # quadratic equation
    a = v1[0]*v1[0] + v1[1]*v1[1]
    b = dx*v1[0] + dy*v1[1]
    c = dx*dx + dy*dy - r*r

    delta = b*b - a*c
    
    if  delta <= 0: # no intersection, imaginary roots
        return 1e+6

    deltaroot = math.sqrt(delta)
    t1 = (-b + deltaroot) / a
    t2 = (-b - deltaroot) / a

    if t1 < 0 and t2 < 0: # intersection is behind the ball
        return 1e+6

    # one of these could be negative
    tmin = min(t1, t2)

    # ball's already intersect, so move ball1 back to the boundary
    if t1 < 0 or t2 < 0:
        newpx = p1[0] + tmin*v1[0]
        newpy = p1[1] + tmin*v1[1]
        ball1.setPosition( newpx, newpy )
        return 0.0
        
    dx = tmin*v1[0]
    dy = tmin*v1[1]
    distToImpact = math.sqrt(dx*dx + dy*dy)

    return distToImpact

def collision_ball_ball(ball1, ball2, dt):
    """Main collision function for handling ball/ball collisions
    Updates the ball1's position and returns true if there was a collision.
    Returns False if there was no collision (ball1 still needs to be udpated).
    ball2's velocity is changed, but it is not updated by this function"""

    # holds ball2 steady, tests ball1's trajectory
    distToImpact = collisionTest_ball_ball(ball1, ball2)

    # get the magnitude of the velocity of ball1
    v1 = ball1.getVelocity()
    v2 = ball2.getVelocity()
    vmag1 = length( ball1.getVelocity() )

    # no collision if it's too far away
    if distToImpact > vmag1 * dt:
        return False

    # check for a stationary ball
    if vmag1 < 1e-6:
        # just update and return a collision
        ball1.update( dt )
        return True

    delta = distToImpact / (vmag1*dt)

    # don't update backwards, which can happen, strangely enough
    if delta > 0.0:
        ball1.update( delta*dt )

    p1 = ball1.getPosition()
    p2 = ball2.getPosition()
    rvec = unit( (p1[0] - p2[0], p1[1] - p2[1]) ) # reflection vector

    # create the reflection matrix R(th)M(X)R(-th)

    # update ball1's velocity
    # rotate reflection vector to the Y axis
    tvx =  rvec[0] * v1[0] + rvec[1] * v1[1]
    tvy = -rvec[1] * v1[0] + rvec[0] * v1[1]

    # mirror in X
    tvx = - tvx*ball1.getElasticity()*ball2.getElasticity() # need to add the loss factor here

    # rotate back
    vfx = rvec[0] * tvx - rvec[1] * tvy
    vfy = rvec[1] * tvx + rvec[0] * tvy

    ball1.setVelocity( vfx, vfy )

    # update ball2's velocity
    tvx =  rvec[0] * v2[0] + rvec[1] * v2[1]
    tvy = -rvec[1] * v2[0] + rvec[0] * v2[1]

    # mirror in X
    tvx = - tvx*ball1.getElasticity()*ball2.getElasticity() # need to add the loss factor here

    # rotate back
    vfx = rvec[0] * tvx - rvec[1] * tvy
    vfy = rvec[1] * tvx + rvec[0] * tvy

    ball2.setVelocity( vfx, vfy )

    # finish updating ball1
    if delta > 0.0:
        ball1.update( dt - delta*dt )
    else:
        ball1.update( dt )
		
    return True


def collisionTest_ball_block(ball, block):
    """Test if a ball is colliding with any side of a block, and indicate
    which side. Sends out a line along the ball's velocity vector and
    compares it with all four sides of the object."""

    # get the trajectory and position of the ball
    v = unit( ball.getVelocity() )
    ballP = ball.getPosition()
    radius = ball.getRadius()

    # get the position of the block
    blockP = block.getPosition()

    # a variation on Liang-Barsky clipping
    # expands the block by the size of the ball before testing
    dx = block.getWidth()
    dy = block.getHeight()

    p = ( -v[0], v[0], -v[1], v[1] )
    q = (ballP[0] - (blockP[0] - dx*0.5 - radius),
         (blockP[0] + dx*0.5 + radius) - ballP[0],
         ballP[1] - (blockP[1] - dy*0.5 - radius),
         (blockP[1] + dy*0.5 + radius) - ballP[1] )

    # for all four cases
    tmin = -1e+6
    tmax = 1e+6
    side = -1
    sidemax = -1
    for i in range(4):
        if p[i] == 0.0: # no collision for this side of the block, motion is parallel to it
            if q[i] < 0: # outside the boundary of the box, no collision
                return 1e+6,0
            continue

        tk = q[i] / p[i]

        if p[i] < 0: # outside moving in
            if tk > tmin:
                tmin = tk
                side = i
        else:
            if tk < tmax:
                tmax = tk
                sidemax = i

        if tmax <= tmin: # no intersection with the box
            return 1e+6,0

    if tmin < 0 and tmax < 0: # both intersections behind the ball
        tmin = 1e+6
    elif tmin < 0 and tmax > 0: # ball is intersecting the block
        #print("ball is intersecting")

        # move the ball back along its velocity to the intersection point
        if v[0] == 0.0 and v[1] == 0.0:
            v = (1.0, 0.0)
            tmin = (blockP[0] - 0.5*dx - radius) - ballP[0]

        # move it to the closest side and set distance to impact to 0
        if -tmin < tmax:
            #print("setting position using tmin and velocity %.2f %d" % (tmin, side))
            ball.setPosition( ballP[0] + (tmin+1e-3)*v[0], ballP[1] + (tmin+1e-3)*v[1])
        else:
            #print("setting position using tmax and velocity %.2f %d" % (tmax, sidemax))
            ball.setPosition( ballP[0] + (tmax+1e-3)*v[0], ballP[1] + (tmax+1e-3)*v[1])
        tmin = 0

    # tmin is the closest intersection on side i
    # 0: coming up from below
    # 1: coming down from above
    # 2: coming from the left
    # 3: coming from the right
    return (tmin, side)

def collision_ball_block(ball, block, dt):
    """Main collision code for ball/block interactions.
    Updates the ball's position and returns true if there was a collision.                                     
    Returns False if there was no collision (ball still needs to be udpated)."""

    # get distance to impact
    distToImpact, side = collisionTest_ball_block( ball, block )

    # check if the impact is farther away than one step
    vmag = length( ball.getVelocity() )
    if vmag == 0.0 or distToImpact > vmag * dt:
        return False

    # update the ball prior to the collision
    delta = distToImpact / (vmag * dt)
    ball.update( delta * dt )

    # modify the velocities
    v = ball.getVelocity()
    if side == 0 or side == 1: # left or right wall, so adjust x
        ball.setVelocity( -v[0]*ball.getElasticity()*block.getElasticity(), v[1]  )
    elif side == 2 or side == 3: # top or bottom wall, so adjust y
        ball.setVelocity( v[0], -v[1]*ball.getElasticity()*block.getElasticity()  )

    # update the ball post-collision
    ball.update( (1 - delta) * dt )

    return True


# Main collision code for a ball and a rotated block
# Updates the ball's position and returns true if there was a collision.
# Returns False if there was no collision (ball still needs to be updated).
def collision_ball_rotating_block(ball, block, dt):

    # transform the ball the same way by subtracting the center of the
    # original block and rotating it to the same alignment (use anchor point?)
    p0 = ball.getPosition()
    bp = block.getPosition()
    b0 = block.getAnchor()
    
    # we have the 0-angle state of the block so create a faux block so the anchor is at 0, 0
    # ***** uses named fields
    fauxBlock = pho.RotatingBlock( block.win,
                           bp[0] - b0[0],
                           bp[1] - b0[1],
                           block.width,
                           block.height )
	

    # rotate the ball's velocity
    v0 = ball.getVelocity()

    theta = math.pi * block.getAngle() / 180.
    cth = math.cos( theta )
    sth = math.sin( theta )
    vtx =  v0[0] * cth + v0[1] * sth
    vty = -v0[0] * sth + v0[1] * cth

    px = p0[0] - b0[0]
    py = p0[1] - b0[1]
    pxx =  px * cth + py * sth
    pyy = -px * sth + py * cth

    ball.setPosition(pxx, pyy)
    ball.setVelocity(vtx, vty)

    # test if there is a collision
    distToImpact, side = collisionTest_ball_block( ball, fauxBlock )

    if distToImpact < 0: # back up the ball, and there was a collision
        distToImpact = 0.0

    # set the ball back to its original position
    ball.setPosition(p0[0],p0[1])
    ball.setVelocity(v0[0],v0[1])
            
    acc = ball.getAcceleration()
    tvx = v0[0] + acc[0] * dt
    tvy = v0[1] + acc[1] * dt
    vmag = length( (tvx, tvy) )

    if distToImpact > 0.0 and vmag == 0.0 or distToImpact > vmag * dt:
        return False

    # if there was a collision, update the ball to the collision point
    # set the ball back to its original velocity and update
    distToImpact = min(0.0, distToImpact)
    delta = distToImpact / vmag 
    ball.update( delta )
    
    # if there was a collision, re-align the new velocity with the block
    v0 = ball.getVelocity()

    # convert velocities to the collision space
    vtx =  v0[0] * cth + v0[1] * sth
    vty = -v0[0] * sth + v0[1] * cth

    # need to give it a boost or a sink if the block is rotating based on the moment arm from the center of rotation
    dx = pxx # transformed distance between anchor and the ball
    dy = pyy 
    dist = length( (dx, dy) )
    rotvel = math.pi * block.getRotVelocity() / 180.
    linvel = dist*2.*math.pi * rotvel / (2. * math.pi)

    if side == 0: # left side of the block, so x velocity has to be negative
        vtx = math.copysign(vtx * ball.getElasticity()*block.getElasticity(), -1)
        hsin = dy/dist # length of the moment arm hitting the ball
        velmod = -hsin * linvel # modify the linear velocity
        #print 'left:', hsin, linvel, vtx, velmod, vtx + velmod 
        vtx += velmod

    elif side == 1: # right side of the block
        vtx = math.copysign(vtx * ball.getElasticity()*block.getElasticity(), 1)
        hsin = dy/dist # length of the moment arm hitting the ball
        velmod = -hsin * linvel # modify the linear velocity
        #print 'right:', hsin, linvel, vtx, velmod, vtx + velmod 
        vtx += velmod
        
    elif side == 2: # bottom side
        vty = math.copysign(vty * ball.getElasticity()*block.getElasticity(), -1)
        hsin = dx/dist
        velmod = hsin * linvel
        #print 'bottom:', hsin, linvel, vty, velmod, vty + velmod 
        vty += velmod

    else: # top side
        vty = math.copysign(vty * ball.getElasticity()*block.getElasticity(), 1)
        hsin = dx/dist
        velmod = hsin * linvel
        #print 'top:', hsin, linvel, vty, velmod, vty + velmod 
        vty += velmod
        
    # rotate the velocity back
    vttx = vtx * cth - vty * sth
    vtty = vtx * sth + vty * cth

    ball.setVelocity(vttx, vtty)

    ball.update( (1 - delta) * dt )

    return True


###### students add code below this  ################

###### collision_router and helper functions go here  ################
collision_router = {}

collision_router[ ('ball', 'ball') ] = collision_ball_ball
collision_router[ ('ball', 'block') ] = collision_ball_block
collision_router[ ('ball', 'hexagon') ] = collision_ball_block
collision_router[ ('ball', 'ring') ] = collision_ball_ball
collision_router[ ('ball', 'rotating block') ] = collision_ball_rotating_block

collision_router[ ('ring', 'ball') ] = collision_ball_ball
collision_router[ ('ring', 'block') ] = collision_ball_block
collision_router[ ('ring', 'hexagon') ] = collision_ball_block
collision_router[ ('ring', 'patrick') ] = collision_ball_ball
collision_router[ ('ring', 'rotating block') ] = collision_ball_rotating_block



def collision(thing1, thing2, dt):
    '''intakes a Ball object and a Thing-inheriting object as well as time-lapse;
    using the collision_router dictionary, determines the type of collision; 
    runs the appropriate collision function with the parameters'''
    return collision_router[ (thing1.getType(), thing2.getType()) ](thing1, thing2, dt)