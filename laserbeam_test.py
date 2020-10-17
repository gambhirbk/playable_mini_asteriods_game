from laserbeam import LaserBeam

params = {
    'SPACE': {'w': 100, 'h': 200},
    'x': 50,
    'y': 75,
    'x_vel': 5,
    'y_vel': 7.5,
}


def test_constructor():
    # Test minimal required constructor args
    a = LaserBeam(params['SPACE'],
                  params['x'], params['y'],
                  params['x_vel'], params['y_vel'])
    assert a.SPACE['w'] == 100 and \
        a.SPACE['h'] == 200 and \
        a.x_vel == params['x_vel'] * a.LASER_SPEED_FACTOR and \
        a.y_vel == params['y_vel'] * a.LASER_SPEED_FACTOR and \
        a.x == params['x'] + params['x_vel'] and \
        a.y == params['y'] + params['y_vel'] and \
        hasattr(a, "radius") and \
        hasattr(a, "lifespan") and \
        hasattr(a, "diam")
