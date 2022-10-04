import numpy as np
from utils import rotationMatrix

# Gravitational constant
G = 6.6743e-11


def state_to_orbital(pos, vel, central_mass):
    # standard gravitational parameter u
    u = G * central_mass
    # specific angular momentum h
    h = np.cross(pos, vel)
    # unit vector of the reference plane (z axis) K
    K = np.array([0, 0, 1])
    # ascending node vector n
    n = np.cross(K, h)
    if np.sqrt(n.dot(n)) == 0:
        if h[2] > 0:
            n = np.array([0, -1, 0])
        else:
            n = np.array([0, 1, 0])
    n_mag = np.sqrt(n.dot(n))
    # eccentricity vector of the orbit. The eccentricity vector has the magnitude of the eccentricity e
    e_vect = (np.cross(vel, h) / u) - (pos / np.sqrt(np.dot(pos, pos)))
    e = np.sqrt(np.dot(e_vect, e_vect))
    # semi-latus rectum p
    p = h.dot(h) / u
    # semi-major axis a
    if e < 1: a = p / (1 - e**2)
    elif e > 1: a = p / (e**2 - 1)
    else: a = None
    # inclination
    i = np.arccos(K.dot(h) / np.sqrt(h.dot(h)))
    # unit vector of X-axis of the reference frame (x axis)
    I = np.array([1, 0, 0])
    # longitude of ascending node Omega
    Omega = np.arccos(I.dot(n) / n_mag)
    if n[1] < 0: Omega = 2 * np.pi - Omega
    # argument of periapsis omega
    if e == 0:
        omega = np.pi / 2
    else:
        omega = np.arccos(n.dot(e_vect) / (n_mag * e))
        if e_vect[2] < 0: omega = 2 * np.pi - omega
    # true anomaly nu
    if e == 0:
        nu = 0
    else:
        nu = np.arccos(np.dot(pos, e_vect) / (np.sqrt(np.dot(pos, pos)) * e))
        if np.dot(pos, vel) < 0: nu = 2 * np.pi - nu

    return a, e, i, Omega, omega, nu


def orbital_to_state(a, e, i, Omega, omega, nu, central_mass):
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
        pass

    # 3D rotation matrices
    rot_omega = rotationMatrix([0, 0, 1], np.pi / 2 - omega)
    rot_i = rotationMatrix([0, 1, 0], -i)
    rot_Omega = rotationMatrix([0, 0, 1], 3/2 * np.pi - Omega)
    # combined
    rot_tot = rot_Omega.dot(rot_i.dot(rot_omega))
    # rotate position in the plane of orbit (x,y,0) to the reference coordinate system
    pos_initial = np.array([x, y, 0])
    pos = rot_tot.dot(pos_initial)
    # rotate velocity in the plane of orbit (x,y,0) to the reference coordinate system
    vel_initial = np.cross(h, pos_initial) / pos_initial.dot(pos_initial)
    vel = rot_tot.dot(vel_initial)
    return pos, vel


class Body:
    count = 0

    def __init__(self, pos=[0, 0, 0], vel=[0, 0, 0]):
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        Body.count += 1

    @classmethod
    def from_OrbitalEelements(cls):
        # do somethiing with args
        return 'cls(pos, vel)'

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.pos}', '{self.vel}')"


class CeleBody(Body):
    count = 0

    def __init__(self, pos=[0, 0, 0], vel=[0, 0, 0], mass=1, radius=1):
        super().__init__(pos, vel)
        self.mass = mass
        self.radius = radius
        CeleBody.count += 1

    def __repr__(self) -> str:
        return f"{super().__repr__()}"


Earth = CeleBody(mass=5.97217e24, radius=6378.137e3)

# pos = [42164, 0, 0]
# vel = [0, 3075, 0]
# a, e, i, Omega, omega, nu = state_to_orbital(pos, vel, Earth.mass)
# pos1, vel1 = orbital_to_state(a, e, i, Omega, omega, nu, Earth.mass)
# print(pos, vel)
# print(f'a {a}, e {e}, i {i}, Omega {Omega}, omega {omega}, nu {nu}')
# print(pos1, vel1)

a, e, i, Omega, omega, nu = 42164, 0.1, 1, 1, 1, 1
print(a, e, i, Omega, omega, nu)
pos1, vel1 = orbital_to_state(a, e, i, Omega, omega, nu, Earth.mass)
print(pos1, vel1)
a, e, i, Omega, omega, nu = state_to_orbital(pos1, vel1, Earth.mass)
print(a, e, i, Omega, omega, nu)
pos1, vel1 = orbital_to_state(a, e, i, Omega, omega, nu, Earth.mass)
print(pos1, vel1)
a, e, i, Omega, omega, nu = state_to_orbital(pos1, vel1, Earth.mass)
print(a, e, i, Omega, omega, nu)