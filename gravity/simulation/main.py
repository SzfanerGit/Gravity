import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import solve_ivp

from __init__ import M_E, R_E, G
from helpers import central_body_altitude, equation
from transformations import orbital_to_state, state_to_orbital


class Body:
    count = 0

    def __init__(self, pos=[0, 0, 0], vel=[0, 0, 0], mass=1, radius=1, central_body=None):
        self.pos = np.array(pos) # km
        self.vel = np.array(vel) # km/s
        self.mass = mass # kg
        self.radius = radius # km
        self.central_body = central_body
        self.motion = None
        Body.count += 1

    @classmethod
    def from_OrbitalEelements(cls, a, e, i, Omega, omega, nu):
        pos, vel = orbital_to_state(a, e, i, Omega, omega, nu)
        return cls(pos, vel)


    def solve_orbit(self, eval_time=None, orbits=1, resolution=1_000):
        # Exeption
        if self.central_body is None or self.central_body.mass <= 0:
            raise RuntimeError("need central reference body with positive mass")
        
        # Gravitational parameter
        u = G * self.central_body.mass

        # initial value
        y_0 = np.hstack((self.pos, self.vel))

        # evaluation time
        t_0 = 0
        if eval_time is None:
            eval_time = 100_000 * orbits # TODO calculate orbital time
        t_f = t_0 + eval_time
        t_arr = np.linspace(t_0, t_f, resolution * orbits)
        solution = solve_ivp(equation, [t_0, t_f], y_0, t_eval=t_arr, method='Radau',
                             events=central_body_altitude, args=(self.central_body,))
        self.motion = solution
        return solution


    def plot(self):
        if self.motion is None:
            self.solve_orbit()
        
        sol = self.motion.y.T
        r = sol[:, :3] # km
        r_mag = np.sqrt(np.sum(np.square(r), axis=1))
        i_min = np.argmin(r_mag, axis=0)
        i_max = np.argmax(r_mag, axis=0)
        v = sol[:, 3:] # km/s
        v_0_mag = np.sqrt(np.dot(v[0, :], v[0, :]))
        # altitude = np.vectorize(central_body_altitude)
        # h_surface = altitude(0, r)

        # Setting up Spherical Earth to Plot
        N = 50
        phi = np.linspace(0, 2 * np.pi, N)
        theta = np.linspace(0, np.pi, N)
        theta, phi = np.meshgrid(theta, phi)

        X_E = R_E * np.cos(phi) * np.sin(theta)
        Y_E = R_E * np.sin(phi) * np.sin(theta)
        Z_E = R_E * np.cos(theta)

        # Plotting Earth and Orbit
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        ax.plot_surface(X_E, Y_E, Z_E, color='green', alpha=0.5)
        ax.plot3D(r[:, 0], r[:, 1], r[:, 2], label="Orbit")

        # Max, min and initial distance indicators
        ax.plot(*r[i_min], 'ro', label="Perigee")
        ax.plot(*r[i_max], 'bo', label="Apogee")
        # movement vector indicator
        ax.plot(*r[0], 'ko' , label="Initial")
        ax.quiver(*r[0], *v[0] * 60 * 10, color='k')

        # View angle
        ax.view_init(30, 145)

        # Legend
        plt.title('Orbits around Earth')
        ax.set_xlabel('x [km]')
        ax.set_ylabel('y [km]')
        ax.set_zlabel('z [km]')
        ax.legend()

        # Axes limits
        xyzlim = np.array([ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()]).T
        XYZlim = np.asarray([min(xyzlim[0]), max(xyzlim[1])])
        ax.set_xlim3d(XYZlim)
        ax.set_ylim3d(XYZlim)
        ax.set_zlim3d(XYZlim * 3/4)

        plt.show()


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.pos}', '{self.vel}')"


# position Earth at the origin
Earth = Body(mass=M_E, radius=R_E)

Satelite1 = Body([8000, 0, 6000], [0.1, 5, 5], central_body=Earth)
Satelite1.solve_orbit()
Satelite1.plot()
