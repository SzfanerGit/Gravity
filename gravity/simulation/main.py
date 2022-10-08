import numpy as np
from transformations import orbital_to_state, state_to_orbital

# Gravitational constant
G = 6.6743e-11

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