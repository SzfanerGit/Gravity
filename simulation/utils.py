from time import time


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