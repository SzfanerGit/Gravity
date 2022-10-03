from time import time
import numpy as np


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