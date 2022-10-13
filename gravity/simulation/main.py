import os
from flask import current_app
from typing import Iterable
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from scipy.integrate import solve_ivp

from gravity.simulation import M_E, R_E
from gravity.simulation.helpers import central_body_altitude, equation, period
from gravity.simulation.transformations import orbital_to_state, state_to_orbital


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

        # initial value
        y_0 = np.hstack((self.pos, self.vel))

        # evaluation time
        t_0 = 0
        if eval_time is None:
            eval_time = period(self, self.central_body)
            if eval_time is None: eval_time = 100_000_000
            eval_time *= orbits
            print(eval_time)
        t_f = t_0 + eval_time
        t_arr = np.linspace(t_0, t_f, resolution * orbits)
        solution = solve_ivp(equation, [t_0, t_f], y_0, t_eval=t_arr, method='Radau',
                             events=central_body_altitude, args=(self.central_body,))
        self.motion = solution
        return solution


    def plot(self, show=True, fig_ref=None):
        if self.motion is None:
            self.solve_orbit()
        
        sol = self.motion.y.T
        r = sol[:, :3] # km
        r_mag = np.sqrt(np.sum(np.square(r), axis=1))
        i_min = np.argmin(r_mag, axis=0)
        i_max = np.argmax(r_mag, axis=0)
        v = sol[:, 3:] # km/s
        # altitude = np.vectorize(central_body_altitude)
        # h_surface = altitude(0, r)

        if fig_ref is None:
            # Creating spherical central body to plot
            N = 50
            phi = np.linspace(0, 2 * np.pi, N)
            theta = np.linspace(0, np.pi, N)
            theta, phi = np.meshgrid(theta, phi)

            X_c = self.central_body.radius * np.cos(phi) * np.sin(theta)
            Y_c = self.central_body.radius * np.sin(phi) * np.sin(theta)
            Z_c = self.central_body.radius * np.cos(theta)

            # Plotting Earth and Orbit
            fig = plt.figure()
            ax = plt.axes(projection='3d')
            ax.plot_surface(X_c, Y_c, Z_c, color='green', alpha=0.5)
            # View angle
            ax.view_init(30, 45)
        else:
            ax = fig_ref

        # Orbit itself
        ax.plot3D(r[:, 0], r[:, 1], r[:, 2], label='Orbit')

        # Max, min and initial distance indicators
        ax.plot(*r[i_min], 'ro')
        ax.plot(*r[i_max], 'bo')
        # movement vector indicator
        ax.plot(*r[0], 'ko')
        ax.quiver(*r[0], *v[0] * 60 * 10, color='k')

        if fig_ref is None:
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

        if show:
            plt.show()


    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.pos}', '{self.vel}')"


def plot_satelites(sat_list: Iterable[object], view_angle: Iterable[float] = (30, -45), save=False, filename='temp'):
    if len(sat_list) > 0:
        central_body = sat_list[0].central_body
        for satelite in sat_list:
            if satelite.central_body is not central_body:
                raise ValueError('All satelites are required to have the same central body')
    
    ########## Plot setup ##########
    # Creating spherical central body to plot
    N = 50
    phi = np.linspace(0, 2 * np.pi, N)
    theta = np.linspace(0, np.pi, N)
    theta, phi = np.meshgrid(theta, phi)

    X_c = central_body.radius * np.cos(phi) * np.sin(theta)
    Y_c = central_body.radius * np.sin(phi) * np.sin(theta)
    Z_c = central_body.radius * np.cos(theta)

    # Plotting Earth
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot_surface(X_c, Y_c, Z_c, color='green', alpha=0.5)
    # and Orbit
    for satelite in sat_list:
        satelite.plot(show=False, fig_ref=ax)

    # View angle
    ax.view_init(*view_angle)
    
    # Legend
    plt.title('Orbits around Earth')
    ax.set_xlabel('x [km]')
    ax.set_ylabel('y [km]')
    ax.set_zlabel('z [km]')

    # Axes limits
    xyzlim = np.array([ax.get_xlim3d(), ax.get_ylim3d(), ax.get_zlim3d()]).T
    XYZlim = np.asarray([min(xyzlim[0]), max(xyzlim[1])])
    ax.set_xlim3d(XYZlim)
    ax.set_ylim3d(XYZlim)
    ax.set_zlim3d(XYZlim * 3 / 4)

    if save:
        plot_path = os.path.join(current_app.root_path, 'static\orbit_plots', filename)
        plt.savefig(plot_path)
        # by default savefig saves as png, this could be done in a better way
        return plot_path + '.png'
    else:
        plt.show()


# position Earth at the origin
Earth = Body(mass=M_E, radius=R_E)

# LEO
Satelite1 = Body([R_E + 200, 0, 0], [0, 7.79, 0], central_body=Earth)
# GEO
Satelite2 = Body([0, 42_164, 0], [3.0746, 0, 0], central_body=Earth)
# Showcase
Satelite3 = Body([R_E * 1.5, R_E * 1.5, -R_E * 0.5], [2.5, -4.5, -1], central_body=Earth)
# plot_satelites([Satelite3,])

# Sat1 = Body([10000, 0, 0], [0, 7.0, 0], central_body=Earth)
# Sat1.plot()
# Sat2 = Body([0, 10000, 0], [2, 3, 5], central_body=Earth)
# Sat2.plot()