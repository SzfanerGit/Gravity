import numpy as np
from gravity.simulation import G


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


def state_to_orbital(r_vect, v_vect, central_mass):
    # 0.standard gravitational parameter u
    u = G * central_mass

    # 1. position r and velocity v
    r = np.sqrt(np.dot(r_vect, r_vect))
    v = np.sqrt(np.dot(v_vect, v_vect))
    v_r = np.dot(r_vect / r, v_vect) # radial velocity
    v_p = np.sqrt(v**2 - v_r**2) # azimuthal velocity

    # 2. specific angular momentum h
    h_vect = np.cross(r_vect, v_vect)
    h = np.sqrt(np.dot(h_vect, h_vect))
    
    # 3. inclination i
    try:
        i = np.arccos(h_vect[2] / h)
    except:
        i = 0

    # 4. unit vector of the reference plane (z axis) K
    K_vect = np.array((0, 0, 1))
    # ascending node vector n
    n_vect = np.cross(K_vect, h_vect)
    n = np.sqrt(np.dot(n_vect, n_vect))
    # Right Ascension of ascending node Omega
    try:
        Omega = np.arccos(n_vect[0] / n)
    except:
        Omega = 3 / 2 * np.pi
    if n_vect[1] < 0: Omega = 2 * np.pi - Omega

    # 5. eccentricity vector of the orbit. The eccentricity vector has the magnitude of the eccentricity e
    try:
        e_vect = (np.cross(v_vect, h_vect) / u) - (r_vect / r)
    except:
        e_vect = [0, 0, 0]
    e = np.sqrt(np.dot(e_vect, e_vect))

    # 6. argument of periapsis omega
    try:
        omega = np.arccos(np.dot(n_vect, e_vect) / (n * e))
    except:
        omega = 1 / 2 * np.pi
    if e_vect[2] < 0: omega = 2 * np.pi - omega

    # 7. true anomaly nu
    try:
        nu = np.arccos(np.dot(r_vect / r, e_vect / e))
    except:
        nu = 0
    if v_r < 0: nu = 2 * np.pi - nu

    # if e == 0:
    #     omega = np.pi / 2
    # else:
    #     pass # omega = ...
    # if n == 0: # TODO analise
    #     if h_vect[2] > 0:
    #         n_vect = np.array([0, -1, 0])
    #     else:
    #         n_vect = np.array([0, 1, 0])
    # n = np.sqrt(np.dot(n_vect, n_vect))
    # semi-latus rectum p
    p = h**2 / u
    # semi-major axis a
    a = p / (1 - e**2)

    return a, e, i, Omega, omega, nu


def orbital_to_state(a, e, i, Omega, omega, nu, central_mass):
    '''
    Derrives state vectors (position x, y, z and velocity v_x, v_y, v_z)
    from Keplerian/orbital elements

    has few flaws: does not work with some edge cases like
    parabolic orbits

    TODO need some testing and debuging, especially for velocity vect
    '''
    # standard gravitational parameter
    u = G * central_mass
    # check ellipticity of an orbit
    # ellipse    
    if e < 1:
        # eccentric anomaly
        temp1 = np.sqrt(1 + e) * np.cos(nu / 2)
        temp2 = np.sqrt(1 - e) * np.sin(nu / 2)
        E = 2 * np.arctan2(temp2, temp1)
        # semi-minor axis
        b = a * np.sqrt(1 - e**2)
        # x,y coordinates in the plane of the orbit
        x = a * np.cos(E)
        y = b * np.sin(E)
        # angular momentum in orbital plane
        h = np.sqrt(u * a * (1 - e**2)) * np.array([0, 0, 1]) # TODO fix vel calculations
    # hiperbola
    elif e > 1:
        # eccentric anomaly
        temp = np.sqrt((e - 1) / (e + 1)) * np.tan(nu / 2)
        E = np.log((1 + temp) / (1 - temp))
        # semi-minor axis
        b = a * np.sqrt(e**2 - 1)
        # x,y coordinates in the plane of the orbit
        x = a * (e - np.cosh(E))
        y = b * np.sinh(E)
        # angular momentum in orbital plane
        h = np.sqrt(u * a * (e**2 - 1)) * np.array([0, 0, 1])
    # parabola
    else:
        raise ValueError('e = 1 not supported')

    # 3D rotation matrices
    rot_omega = rotationMatrix([0, 0, 1], -omega)
    rot_i = rotationMatrix([1, 0, 0], -i)
    rot_Omega = rotationMatrix([0, 0, 1], -Omega)
    # combined
    rot_tot = rot_Omega @ rot_i @ rot_omega
    # rotate position in the plane of orbit (x,y,0) to the reference coordinate system
    pos_initial = np.array([x, y, 0])
    pos = rot_tot.dot(pos_initial)
    # rotate velocity in the plane of orbit (x,y,0) to the reference coordinate system
    vel_initial = np.cross(h, pos_initial) / pos_initial.dot(pos_initial)
    vel = rot_tot.dot(vel_initial)
    return pos, vel
