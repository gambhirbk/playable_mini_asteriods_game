from laserbeam import LaserBeam
from asteroid import Asteroid
from spaceship import Spaceship


class GameController:
    """
    Maintains the state of the game
    and manages interactions of game elements.
    """

    def __init__(self, SPACE, fadeout):
        """Initialize the game controller"""
        self.SPACE = SPACE
        self.fadeout = fadeout

        self.spaceship_hit = False
        self.asteroid_destroyed = False
        self.asteroids = [Asteroid(self.SPACE)]
        self.laser_beams = []
        self.spaceship = Spaceship(self.SPACE)

    def update(self):
        """Updates game state on every frame"""
        self.do_intersections()

        for asteroid in self.asteroids:
            asteroid.display()

        # Laser beam handler
        # replace (or augment) the next several
        # lines. Laser beam objects should remain in the scene
        # as many frames as their lifespan allows.

        life_span_list_check = []

        for l in range(len(self.laser_beams)):
            if self.laser_beams[l].lifespan > 0:
                self.laser_beams[l].lifespan -= 1
                self.laser_beams[l].display()
            elif self.laser_beams[l].lifespan == 0:
                life_span_list_check.append(l)

        for i in range(len(life_span_list_check)):
            self.laser_beams.pop(i)

        self.spaceship.display()

        # Carries out necessary actions if game over
        if self.spaceship_hit:
            if self.fadeout <= 0:
                fill(1)
                textSize(30)
                text("YOU HIT AN ASTEROID",
                     self.SPACE['w']/2 - 165, self.SPACE['h']/2)
            else:
                self.fadeout -= 1

        if self.asteroid_destroyed:
            fill(1)
            textSize(30)
            text("YOU DESTROYED THE ASTEROIDS!!!",
                 self.SPACE['w']/2 - 250, self.SPACE['h']/2)

    def fire_laser(self, x, y, rot):
        """Add a laser beam to the game"""
        x_vel = sin(radians(rot))
        y_vel = -cos(radians(rot))
        self.laser_beams.append(
            LaserBeam(self.SPACE, x, y, x_vel, y_vel)
            )

    def handle_keypress(self, key, keycode=None):
        if (key == ' '):
            if self.spaceship.intact:
                self.spaceship.control(' ', self)
        if (keycode):
            if self.spaceship.intact:
                self.spaceship.control(keycode)

    def handle_keyup(self):
        if not self.spaceship.intact:
            self.spaceship.control('keyup')

    def do_intersections(self):
        """ intersections between 1) asteroids and laser beams
            2) asteroid and spaceship"""

        # ======================================================
        # Part 1: Intersections
        # check for intersections between asteroids and laser beams. Laser
        # beams should be removed
        # from the scene if they hit an asteroid, and the asteroid should
        # blow up

        new_list_asteroids = []
        new_list_laser_beams = []

        for j in range(len(self.laser_beams)):
            for i in range(len(self.asteroids)):
                if (
                    abs(self.laser_beams[j].x - self.asteroids[i].x)
                    < max(self.asteroids[i].radius,
                          self.laser_beams[j].radius)
                    and
                        abs(self.laser_beams[j].y - self.asteroids[i].y)
                        < max(self.asteroids[i].radius,
                              self.laser_beams[j].radius)):
                    # We've intersected an asteroid
                    new_list_asteroids.append((j, i))
                    new_list_laser_beams.append(j)

        for a in new_list_asteroids:
            self.blow_up_asteroid(a[0], a[1])

        if len(self.asteroids) == 0:
            self.asteroid_destroyed = True

        # End of code changes for Intersections
        # ======================================================

        # If the space ship still hasn't been blown up
        if self.spaceship.intact:
            # Check each asteroid for intersection
            for i in range(len(self.asteroids)):
                if (
                      abs(self.spaceship.x - self.asteroids[i].x)
                      < max(self.asteroids[i].radius, self.spaceship.radius)
                      and
                      abs(self.spaceship.y - self.asteroids[i].y)
                      < max(self.asteroids[i].radius, self.spaceship.radius)):
                    # We've intersected an asteroid
                    self.spaceship.blow_up(self.fadeout)
                    self.spaceship_hit = True

    def blow_up_asteroid(self, j, i):
        """break a large asteriod into two medium asteroids
           ,break two medium asteriods into small asteroids
           ,and disappear small asteriods when hit by laser beams"""
        # ======================================================+

        # the code to blow up an asteroid.
        # The parameters represent the indexes for the list of
        # asteroids and the list of laser beams, indicating
        # which asteroid is hit by which laser beam.

        # I'll need to:
        # A) Remove the hit asteroid from the scene
        # B) Add appropriate smaller asteroids to the scene
        # C) Make sure that the smaller asteroids are positioned
        #    correctly and flying off in the correct directions

        # Specifically. If the large asteroid is hit, it should
        # break into two medium asteroids, which should fly off
        # perpendicularly to the direction of the laser beam.

        # If a medium asteroid is hit, it should break into three
        # small asteroids, two of which should fly off perpendicularly
        # to the direction of the laser beam, and the third
        # should fly off in the same direction that the laser
        # beam had been traveling.

        # If a small asteroid is hit, it disappears.

        # Begin code changes for Problem 4, Part 2: Asteroid blow-up
        SCALAR = 0.2
        if self.asteroids[i].asize == 'Large':
            self.asteroids.append(Asteroid(self.SPACE, asize='Med',
                                  x=self.asteroids[i].x,
                                  y=self.asteroids[i].y,
                                  x_vel=self.laser_beams[j].y_vel * SCALAR,
                                  y_vel=-self.laser_beams[j].x_vel * SCALAR))
            self.asteroids.append(Asteroid(self.SPACE, asize='Med',
                                  x=self.asteroids[i].x,
                                  y=self.asteroids[i].y,
                                  x_vel=-self.laser_beams[j].y_vel * SCALAR,
                                  y_vel=self.laser_beams[j].x_vel * SCALAR))
            self.asteroids.pop(i)
            self.laser_beams.pop(j)
        elif self.asteroids[i].asize == 'Med':
            self.asteroids.append(Asteroid(self.SPACE, asize='Small',
                                  x=self.asteroids[i].x,
                                  y=self.asteroids[i].y,
                                  x_vel=self.laser_beams[j].y_vel * SCALAR,
                                  y_vel=-self.laser_beams[j].x_vel * SCALAR))
            self.asteroids.append(Asteroid(self.SPACE, asize='Small',
                                  x=self.asteroids[i].x,
                                  y=self.asteroids[i].y,
                                  x_vel=-self.laser_beams[j].y_vel * SCALAR,
                                  y_vel=self.laser_beams[j].x_vel * SCALAR))
            self.asteroids.append(Asteroid(self.SPACE, asize='Small',
                                  x=self.asteroids[i].x,
                                  y=self.asteroids[i].y,
                                  x_vel=self.laser_beams[j].x_vel * SCALAR,
                                  y_vel=self.laser_beams[j].y_vel * SCALAR))
            self.asteroids.pop(i)
            self.laser_beams.pop(j)
        else:
            self.asteroids.pop(i)
            self.laser_beams.pop(j)
