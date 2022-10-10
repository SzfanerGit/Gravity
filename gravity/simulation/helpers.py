from time import time
import numpy as np

from __init__ import G


def timer(func):
    '''
    Measures and prints out sensibly formated time taken to run the function.
    Usage:

    @timer
    def function():
        ...

    '''
    def wrapper(*args, **kwargs):
        start_time = time()
        result = func(*args, **kwargs)
        delta_time = time() - start_time

        # for propper rounding s
        min = int(delta_time // 60)
        s = int(((delta_time % 60) + 0.5 ) // 1)
        ms = int(1e3 * ((delta_time % 1) + 5e-4) // 1)

        time_str = ''
        if min:
            time_str = str(min) + 'min '

        if s:
            time_str += str(s) + 's'
        elif min:
            pass
        elif ms:
            time_str = str(ms) + 'ms'
        else:
            time_str = '<1ms'
        print('runtime of "' + func.__name__ + '":', time_str)
        return result
    return wrapper


def rotationMatrix(axis, angle):
    # create rotation matrix around specified axis and by given angle
    
    # normailse rotation axis vector
    u = np.array(axis) / np.sqrt(np.dot(axis, axis))
    # shorthands
    ux, uy, uz = u[0], u[1], u[2]
    c = np.cos(angle)
    s = np.sin(angle)
    matrix = np.array([[c + ux**2 * (1 - c), ux * uy * (1 - c) - uz * s, ux * uz * (1 - c) + uy * s],
                       [uy * ux * (1 - c) + uz * s, c + uy**2 * (1 - c), uy * uz * (1 - c) - ux * s],
                       [uz * ux * (1 - c) - uy * s, uz * uy * (1 - c) + ux * s, c + uz**2 * (1 - c)]])
    return matrix


def equation(t, y, central_body):
    """Evaluate classical equation of motion for 2-body problem.
    Frame of reference is inertial and centered on central body
    for both position and velocity.
    
    scipy.integrate.solve_ivp requires diff. eqs. in this form
    f(t, y) where in this example y = (pos123, vel123) (6 components)
    """
    # Gravitational parameter
    u = G * central_body.mass
    # position and velocity vector unpacking
    r = y[:3]
    v = y[3:]
    r_mag = np.sqrt(np.dot(r, r))
    # acceleration calculation
    acc = - u * r / r_mag**3
    # creating derrivative of y (r_dot = v, v_dot = acc)
    y_dot = np.hstack((v, acc))

    return y_dot


def central_body_altitude(t, y, central_body, terminal=True):
    """Height above central body surface. 
    If there is no radius then it treats it as 0.

    Terminate solve_ivp on collision.
    """
    r = y[:3]
    r_mag = np.sqrt(np.dot(r, r))
    try:
        return r_mag - central_body.radius
    except:
        return r_mag
