import numpy as np
from simulation import G
from utils import rotationMatrix


def state_to_orbital(pos, vel, central_mass):
    # standard gravitational parameter
    u = G * central_mass
    # specific angular momentum
    h = np.cross(pos, vel)
    # unit vector of the reference plane (z axis)
    K = np.array([0, 0, 1])
    # ascending node vector
    n = np.cross(K, h)
    # eccentricity vector ev of the orbit. The eccentricity vector has the magnitude of the eccentricity e
    e_vect = np.cross(vel, h) / u + pos / np.sqrt(pos.dot(pos))
    e = np.sqrt(e_vect.dot(e_vect))
    # semi-latus rectum p
    p = h.dot(h) / u
    # semi-major axis
    if e != 1: a = p / (1 - e**2)
    else: a = None
    # inclination
    i = np.arccos(K.dot(h) / np.sqrt(h.dot(h)))
    # unit vector of X-axis of the reference frame (x axis)
    I = np.array([1, 0, 0])
    # longitude of ascending node
    Omega = np.arccos(I.dot(n) / np.sqrt(n.dot(n)))
    if n[1] < 0: Omega = 2 * np.pi - Omega
    # argument of periapsis
    omega = np.arccos(n.dot(e_vect) / (np.sqrt(n.dot(n)) * e))
    if e_vect[2] < 0: omega = 2 * np.pi - omega
    # true anomaly
    nu = np.arccos(np.dot(pos, e_vect) / (np.sqrt(np.dot(pos, pos)) * e))
    if np.dot(pos, vel) < 0: nu = 2 * np.pi - nu

    return a, e, i, Omega, omega, nu


def orbital_to_state(a, e, i, Omega, omega, nu, central_mass):
    rot_omega = rotationMatrix([0, 0, 1], omega)
    rot_i = rotationMatrix([0, 1, 0], -i)
    rot_Omega = rotationMatrix([0, 0, 1], 3/2 * np.pi - Omega)
    temp = np.sqrt((e - 1) / (e + 1)) * np.tan(nu / 2)
    E = np.log((1 + temp) / (1 - temp))
    b = a * np.sqrt(1 - e**2)
    x = a * np.cos(E)
    y = b * np.sin(E)
    pos_initial = np.array([x, y, 0])
    pos = rot_Omega * rot_i * rot_omega * pos_initial
    vel = 
    return pos, vel

class Body:
    count = 0

    def __init__(self, pos=[0, 0, 0], vel=[0, 0, 0]):
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        Body.count += 1

    @classmethod
    def from_KeplerianEelements(cls):
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