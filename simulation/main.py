import numpy as np
from simulation import G

class CeleBody:

    count = 0

    def __init__(self, mass, radius, pos=[0, 0, 0], vel=[0, 0, 0], acc=[0, 0, 0]):
        self.mass = mass
        self.radius = radius
        self.pos = np.array(pos)
        self.vel = np.array(vel)
        self.acc = np.array(acc)
        CeleBody.count += 1

    def __repr__(self) -> str:
        return f"CeleBody('{self.mass}', '{self.radius}', '{self.pos}', '{self.vel}', '{self.acc}')"


class Satelite(CeleBody):
    count = 0

    def __init__(self, small_mass=1, fuel=0, pos=[1, 0, 0], vel=[0, 0, 0], acc=[0, 0, 0]):
        super().__init__(None, None, pos, vel, acc)
        self.small_mass = small_mass
        self.fuel = fuel
        Satelite.count += 1

    def __repr__(self) -> str:
        return f"{super().__repr__()}"


class Earth(CeleBody):
    count = 0

    def __init__(self, pos=[1, 0, 0], vel=[0, 0, 0], acc=[0, 0, 0], mass=None, radius=None):
        super().__init__(mass, radius, pos, vel, acc)
        Earth.count += 1
