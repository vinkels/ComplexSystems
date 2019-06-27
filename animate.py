import CA_FINAL as ca
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import matplotlib.cm as cm



def animation_func(iterationsres, steps, terrain):
    """ Function used to animate the simulation. """
    sns.set_style('dark')

    fig, ax = plt.subplots()
    ax.imshow(terrain[:, 0:199], cmap='Greens')
    # mycmap = cm.get_cmap('hot')
    # mycmap.set_under('w')
    # im = plt.imshow(iterationsres[0], extent=[0, 1, 0, 1], cmap='Blues')
    # masked_data = np.ma.masked_where(iterationsres[0] < 0.01, iterationsres[0])
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
    anim.save(f"anim_river_water_high_{water}_{x}.mp4", fps=60, extra_args=['-vcodec', 'libx264'])
    caz = ca.CA(size=size, slope=slope, mu=0.0004, gamma=0.0002, rho=0.02, time_limit=size, viz=True)

# masked_data = np.ma.masked_where(path < 0.01, path)
# print(np.min(path), np.max(path))
# fig, ax = plt.subplots()
# ax.imshow(terrain[:, 0:199], cmap='Greens')
# ax.imshow(masked_data, cmap='Blues',vmin=-1,vmax=1, interpolation='none')
# plt.show()