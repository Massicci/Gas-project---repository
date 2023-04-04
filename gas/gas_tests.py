from nose.tools import *
from gas.engine import *
from random import sample

pygame.init()
screen = pygame.display.set_mode((20, 20))

# Test 1
def collision1d_test():

    tb1 = Ball(10, 1, Vector2(0,0), Vector2(50,0))
    tb2 = Ball(10, 1, Vector2(20,0), Vector2(-50,0))

    testengine = Mechanics()
    testengine.collide(tb1, tb2)

    assert_equal(tb1.speed, Vector2(-50,0))
    assert_equal(tb2.speed, Vector2(50,0))

# Test 2
def collision_stop_test():

    tb1 = Ball(10, 1, Vector2(0,0), Vector2(50,0))
    tb2 = Ball(10, 1, Vector2(20,0), Vector2(0,0))

    testengine = Mechanics()
    testengine.collide(tb1, tb2)

    assert_equal(tb1.speed, Vector2(0,0))
    assert_equal(tb2.speed, Vector2(50,0))

# Test 3
def collision_masses_test():

    tb1 = Ball(10, 2, Vector2(0,0), Vector2(30,15))
    tb2 = Ball(10, 1, Vector2(20,0), Vector2(-30,15))

    testengine = Mechanics()
    testengine.collide(tb1, tb2)

    assert_equal(tb1.speed, Vector2(-10,15))
    assert_equal(tb2.speed, Vector2(50,15))

# Test 4
def collision_general_test():
    # Series of random tests (10 tests)
    # For each test checks that deltaK = 0 and deltaQ = 0
    for test in range (0, 10):
        # Ball test istances initialization with random parameters
        tb1 = Ball(sample(range(0, 100), 1)[0],
                   sample(range(0, 50), 1)[0],
                   Vector2(sample(range(0, 100), 1)[0], sample(range(0, 100), 1)[0]),
                   Vector2(sample(range(0, 20), 1)[0], sample(range(0, 20), 1)[0]))
        tb2 = Ball(sample(range(0, 100), 1)[0],
                   sample(range(0, 50), 1)[0],
                   Vector2(sample(range(0, 100), 1)[0], sample(range(0, 100), 1)[0]),
                   Vector2(sample(range(0, 20), 1)[0], sample(range(0, 20), 1)[0]))
        K1i = 1 / 2 * tb1.mass * tb1.speed.magnitude_squared()
        K2i = 1 / 2 * tb2.mass * tb2.speed.magnitude_squared()
        Q1i = tb1.mass * tb1.speed
        Q2i = tb2.mass * tb2.speed

        testengine = Mechanics()
        testengine.collide(tb1, tb2)

        K1f = 1 / 2 * tb1.mass * tb1.speed.magnitude_squared()
        K2f = 1 / 2 * tb2.mass * tb2.speed.magnitude_squared()
        Q1f = tb1.mass * tb1.speed
        Q2f = tb2.mass * tb2.speed

        assert_equal(round(K1i + K2i, 8), round(K1f + K2f, 8))
        assert_equal(Q1i + Q2i, Q1f + Q2f)

# Test 5
def generate_ball_test():
    testengine = Mechanics()

    for i in range(0, 100):
        testengine.generate_ball()

    assert_equal(len(testengine.ball_list), 100)
    assert_equal(testengine.manage_collisions(), 0)

# Test 6
def manage_collisions_test():
    testengine = Mechanics()

    testengine.generate_ball()
    # Editing ball istance in the list (normally not necessary nor raccomended)
    testengine.ball_list[0].radius = 1
    testengine.ball_list[0].mass = 1
    testengine.ball_list[0].position = Vector2(0.999, 300)

    # Second ball generated
    testengine.generate_ball()
    # Editing ball istance in the list (normally not necessary nor raccomended)
    testengine.ball_list[1].radius = 1
    testengine.ball_list[1].mass = 1
    testengine.ball_list[1].position = Vector2(2.98, 300)

    # Third ball generated
    testengine.generate_ball()
    # Editing ball istance in the list (normally not necessary nor raccomended)
    testengine.ball_list[2].radius = 1
    testengine.ball_list[2].mass = 1
    testengine.ball_list[2].position = Vector2(2.98, 301.9)

    assert_equal(testengine.manage_collisions(), 3)
