import CA_FINAL as ca
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import matplotlib.cm as cm



def animation_func(iterationsres, steps, terrain):
    """ Creates animation object for given grid states.
    
    Arguments:
        iterationsres {list} -- list with numpy grid states
        steps {int} -- [description]
        terrain {numpy grid} -- background terrain grid
    
    Returns:
        matplotlib.animation object -- returns animation object
    """
    sns.set_style('dark')

    fig, ax = plt.subplots()
    ax.imshow(terrain[:, 0:199], cmap='Greens')
    ax = plt.imshow(iterationsres[0], cmap='Blues',vmin=-1,vmax=1, interpolation='none')

    def animate(i):
        ax.set_array(iterationsres[i])
        return ax,

    anim = animation.FuncAnimation(fig, animate, frames=steps, interval=20, blit=True)

    return anim
    

size = 200
slope = 0.0001
water = 0.1
caz = ca.CA(size=size, slope=slope, mu=0.0004, gamma=0.0002, rho=0.02, time_limit=size, delta_water=water, viz=True)

for x in range(20):
    terrain = caz.initialize_terrain()
    path = caz.create_path_from_start()
    new_path = []
    for val in path:
        new_val = np.ma.masked_where(val < 0.01, val)
        new_path.append(new_val)
    anim = animation_func(new_path, len(path), terrain)
    anim.save(f"animations/anim_river_water_high_{water}_{x}.mp4", fps=60, extra_args=['-vcodec', 'libx264'])
    caz = ca.CA(size=size, slope=slope, mu=0.0004, gamma=0.0002, rho=0.02, time_limit=size, viz=True)
