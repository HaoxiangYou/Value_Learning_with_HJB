import jax.numpy as jnp
from common.dynamics.dynamics import Dynamics
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Rectangle, Circle
from common.configs.dynamics.cartpole_config import CartpoleDynamicsConfig

class Cartpole(Dynamics):

    def __init__(self, config: CartpoleDynamicsConfig) -> None:
        super().__init__(config)
        self.mc = config.mc
        self.mp = config.mp
        self.l = config.l
        self.g = config.g
    
    def get_M(self, x: jnp.ndarray) -> jnp.ndarray:
        return jnp.array([
            [self.mc+self.mp, self.mp*self.l*jnp.cos(x[1])],
            [self.mp*self.l*jnp.cos(x[1]), self.mp*self.l**2]
        ])
    
    def get_C(self, x: jnp.ndarray) -> jnp.ndarray:
        return jnp.array([
            [0, -self.mp*self.l*x[3]*jnp.sin(x[1])],
            [0, 0]
        ])

    def get_G(self, x: jnp.ndarray) -> jnp.ndarray:
        return jnp.array([0, self.mp*self.g*self.l*jnp.sin(x[1])])

    def get_B(self) -> jnp.ndarray:
        return jnp.array([1,0])
    
    def states_wrap(self, x: jnp.ndarray) -> jnp.ndarray:
        assert x.shape == (4,)
        x1_wrapped = jnp.remainder(x[1] + jnp.pi, 2*jnp.pi) - jnp.pi
        return jnp.array([x[0], x1_wrapped, x[2], x[3]])
        
    def plot_trajectory(self, ts:jnp.ndarray, xs:jnp.ndarray, 
                    cart_width=0.4, cart_height=0.2, pole_radius=0.05, x_range=jnp.array([-2, 2]), y_range=jnp.array([-1,3])):
    
        fig = plt.figure()
        ax = plt.axes()

        def draw_frame(i):
            pole_x = xs[i,0] + self.l * jnp.cos(xs[i,1]-jnp.pi/2) 
            pole_y = self.l * jnp.sin(xs[i,1]-jnp.pi/2) 
            
            ax.clear()
            ax.axis('equal')
            ax.set_xlim(x_range + xs[i,0])
            ax.set_ylim(y_range)
            
            ax.hlines(y=0, xmin=x_range[0]*2 + xs[i,0], xmax=x_range[1]*2 + xs[i,0], colors="k", linestyles="-")
            ax.hlines(y=self.l, xmin=x_range[0]*2 + xs[i,0], xmax=x_range[1]*2 + xs[i,0], colors="r", linestyles="--")
            
            cart = Rectangle([xs[i,0]-cart_width/2, -cart_height/2], cart_width, cart_height, color="b")
            pole = Circle([pole_x, pole_y], pole_radius, color="g")
            ax.add_patch(cart)
            ax.add_patch(pole)

            ax.plot([xs[i,0], pole_x], [0, pole_y], "k")
            ax.set_title("{:.1f}s".format(ts[i]))

        anim = animation.FuncAnimation(fig, draw_frame, frames=ts.shape[0], repeat=False, interval=self.dt*1000)

        return anim, fig
    
if __name__ == "__main__":

    config = CartpoleDynamicsConfig(mc=1, mp=1, l=1, g=1, dt=0.05, seed=0,
                                    x0_mean=[0, 3.14, 0, 0],
                                    x0_std=[2.4, 0.05, 0, 0],
                                    umin=[-5],
                                    umax=[5])

    cartpole = Cartpole(config)
    t0 = 0
    tf = 5
    t = jnp.arange(t0, tf, cartpole.dt)
    x0 = cartpole.get_initial_state()

    xs = [x0]
    us = []

    for i in range(1, t.shape[0]):
        us.append(0)
        xs.append(cartpole.simulate(xs[i-1],us[i-1]))

    xs = jnp.array(xs)
    us = jnp.array(us)
    xs.at[:,1].set(jnp.arctan2(jnp.sin(xs[:,1]), jnp.cos(xs[:,1])))

    anim, fig = cartpole.plot_trajectory(t, xs)

    plt.show()
    plt.close()
