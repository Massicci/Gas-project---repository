"""This module provides classes to the engine to run physics for the gas game.
Version 1.0"""

import pygame
from pygame.math import Vector2
from random import sample

class Ball(object):

    def __init__(self, radius, mass, pos, speed):
        """Ball.__init__ method takes 4 arguments:
        radius: int value for radius (in pixel)
        mass: int value representing the mass of the ball
        pos: 2d vector for the position of the center of the ball
        speed: 2d vector for the speed of the ball
        """
        # Model attributes
        self.radius = radius
        self.mass = mass
        # Vector2 object - position in pixels
        self.position = pos
        # Vector2 object - speed in pixels per second
        self.speed = speed

        # Graphical attributes
        self.surf = pygame.Surface((2 * radius, 2 * radius)).convert() # convert?
        self.surf.set_colorkey((0,0,0)) # Sets black transparency
        self.circle_color = (255,0,0) # Should be passed as argument
        pygame.draw.circle(self.surf, self.circle_color,
                           (radius, radius), radius)

class Walls(object):

    def __init__(self, dimensions):
        """This method takes a 2d vector for the available area of the balls"""
        self.l = dimensions[0]
        self.h = dimensions[1]

class Mechanics(object):

    def __init__(self, width, height):
        """Mechanics class runs the physics of collisions among balls
        It takes environment's width and height as arguments"""
        # List of all existing balls
        self.ball_list = []
        # Wall istance defined for Mechanics class (Area = 800 x 800)
        self.walls = Walls((width, height))
        # Definition of event COLLISION
        # (game module must have initialized the display!
        # This module does not stand alone)
        self.collision = pygame.event.Event(pygame.USEREVENT)

    def generate_ball(self):
        # Randomize attributes and checks they are consistent
        # with other balls' positions and wall dimensions
        rand_radius = None
        rand_mass = None
        rand_pos = None
        rand_speed = None

        new_ball_collision_detected = True

        while(new_ball_collision_detected):
            rand_radius = sample(range(5, 25), 1)[0]
            rand_mass = rand_radius ** 2
            rand_pos = Vector2(sample(
                       range(rand_radius, self.walls.l - rand_radius), 1)[0],
                       sample(
                       range(rand_radius, self.walls.h - rand_radius), 1)[0])
            rand_speed = Vector2(sample(range(-75, 75), 1)[0],
                         sample(range(-75, 75), 1)[0])

            # collision check for new ball's parameters
            new_ball_collision_detected = False
            for ball_i in self.ball_list:
                oroi = ball_i.position - rand_pos
                min_distance_ri = rand_radius + ball_i.radius

                if oroi.length() < min_distance_ri:
                    new_ball_collision_detected = True

        self.ball_list.append(Ball(rand_radius,
                                   rand_mass,
                                   rand_pos,
                                   rand_speed)
                             )

    def move_balls(self, deltat):
        """Updates the position of all the balls in the list.
        The update is based on time (in milliseconds) passed from the
        previous call of tick (one call per frame)"""
        # (tick method called in the main loop in game module)
        for ball in self.ball_list:
            ball.position += ball.speed * deltat / 1000

    def manage_collisions(self):
        """Calls collide method and posts collision event on
        the event queue if a collision is detected.
        It also returns the number of collisions detected"""
        # This method is called in the game's main loop. It automatically
        # calls the collide method if a collision is detected,
        # without involving the main game loop for this call
        # The method returns the number of collisions detected (both
        # ball-ball and ball-wall collisions)
        collision_number = 0

        # Detects BALL-WALL collisions:
        for ball in self.ball_list:

            # Defining wall collision conditions:
            hit_RIGHT = (ball.position + Vector2(ball.radius, 0)).x > self.walls.l
            hit_LEFT = (ball.position + Vector2(- ball.radius, 0)).x < 0
            hit_BOTTOM = (ball.position + Vector2(0, ball.radius)).y > self.walls.h
            hit_TOP = (ball.position + Vector2(0, - ball.radius)).y < 0

            # Wall collision condition
            if (hit_RIGHT or hit_LEFT) or (hit_BOTTOM or hit_TOP):
                # Calls collide method for speed transformation
                self.collide(ball)
                collision_number += 1

        # Detects BALL-BALL collisions:
        possible_collisions = [(ball_i, ball_j)
                               for ball_i in self.ball_list
                               for ball_j in self.ball_list
                               if self.ball_list.index(ball_i) <
                                  self.ball_list.index(ball_j)
        ]

        for x_collision in possible_collisions:
            # Vector from center of the 1st ball to center of the 2nd ball
            # of the tuple x_collision about to test
            oioj = x_collision[1].position - x_collision[0].position
            # Scalar minimum distance between 1st and 2nd ball (sum of radius)
            min_distance_ij = x_collision[0].radius + x_collision[1].radius

            if oioj.length() < min_distance_ij:
                # Calls collide method to calculate resulting speeds
                self.collide(x_collision[0], x_collision[1])
                # Posts collision event in the event queue
                pygame.event.post(self.collision)
                # Increments collision_number
                collision_number += 1

        return collision_number

    # This method takes the Ball istances and calculates
    # the final state of the balls after collision, updating the balls in place.
    # !!: If only one ball is passed, the collision method defaults
    # a ball-wall collision
    def collide(self, ball1, ball2=None):
        # BALL-WALL COLLISION procedure
        if ball2 == None:
            # Checks which wall hit the ball
            # Reverses the speed component that is normal to the hit wall
            # In this simple version the hit walls can be only
            # horizontal or vertical
            # IN THIS VERSION CHECKS IF A WALL COLLISION HAPPENS AND WHICH WALL,
            # AUTOMATICALLY
            # (This part of the code is copied and paste in the
            # manage_collisions) method to check the ball-wall collision thus
            # calling the collide method. This can be optimized.

            # Defining wall collision conditions:
            hit_RIGHT = (ball1.position + Vector2(ball1.radius, 0)).x > self.walls.l
            hit_LEFT = (ball1.position + Vector2(- ball1.radius, 0)).x < 0
            hit_BOTTOM = (ball1.position + Vector2(0, ball1.radius)).y > self.walls.h
            hit_TOP = (ball1.position + Vector2(0, - ball1.radius)).y < 0

            # Speed transformation after wall collision
            if hit_RIGHT or hit_LEFT:
                ball1.speed.x = - ball1.speed.x
            elif hit_BOTTOM or hit_TOP:
                ball1.speed.y = - ball1.speed.y
            else:
                pass

        # BALL-BALL COLLISION procedure:
        else:
            # The n-t formulation allows to use 1d speed transformation formulas.
            # 1) calculation of normal vector
            o1o2 = ball2.position - ball1.position # (normal vector)
            # 2) normalization of normal and tangent vectors
            n = o1o2.normalize()
            t = n.rotate(90)
            # 3) projection of speeds on normal and tangent
            #    (Notation: i: initial, _t: projection on t, _n: projection on n)
            v1i_n = ball1.speed.dot(n) * n
            v1i_t = ball1.speed.dot(t) * t
            v2i_n = ball2.speed.dot(n) * n
            v2i_t = ball2.speed.dot(t) * t
            # 4) Calculation of final speeds (sum of n- and t-components)
            #    t-component has not varied;
            #    n-component has varied.
            m1 = ball1.mass
            m2 = ball2.mass
            v1f_n = ((m1 - m2) * v1i_n + 2 * m2 * v2i_n) / (m1 + m2)
            v2f_n = ((m2 - m1) * v2i_n + 2 * m1 * v1i_n) / (m1 + m2)
            v1f_t = v1i_t # Useless but clearer
            v2f_t = v2i_t # Useless but clearer
            # 5) Update of final speeds
            ball1.speed = v1f_n + v1f_t
            ball2.speed = v2f_n + v2f_t
