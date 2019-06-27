import CA_FINAL as ca
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation


# def show_state_over_time(states_over_time, L):
#     '''
#     @param states_over_time: a TxLxL array for T time steps and a system size of LxL.
#     '''
#     assert np.ndim(states_over_time) == 100
    
#     num_time_steps = np.shape(states_over_time)[0]
    
#     # First set up the figure, the axis, and the plot element we want to animate
#     fig = plt.figure()
#     im = plt.imshow(np.random.randint(3, size=(L,L)), animated=True)
    
#     # animation function. This is called sequentiallybrew install ffmpeg
#     def animate(i):
#         im.set_array(states_over_time[i])
#         return im,
#     Writer = animation.writers['ffmpeg']
#     # call the animator.  blit=True means only re-draw the parts that have changed.
#     # ani = matplotlib.animation.FuncAnimation(fig, animate, frames=17, repeat=True)
#     anim = animation.FuncAnimation(fig, animate, frames=num_time_steps, interval=200, blit=True)

#     # save the animation as an mp4.  This requires ffmpeg or mencoder to be
#     # installed.  The extra_args ensure that the x264 codec is used, so that
#     # the video can be embedded in html5.  You may need to adjust this for
#     # your system: for more information, see
#     # http://matplotlib.sourceforge.net/api/animation_api.html
#     # with moviewriter.saving(states_over, 'myfile.mp4', dpi=100):
#     # for j in range(n):
#     #     update_figure(n)
#     #     moviewriter.grab_frame()
#     anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

#     return HTML(anim.to_html5_video())
# #     rc('animation', html='html5')
# #     return anim

# if __name__ == "__main__":
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import seaborn as sns
import matplotlib.cm as cm



# FFMpegWriter = manimation.writers['ffmpeg']
# metadata = dict(title='Movie Test', artist='Matplotlib',
#                 comment='Movie support!')
# writer = FFMpegWriter(fps=15, metadata=metadata)

# fig = plt.figure()
# l, = plt.plot([], [], 'k-o')

# plt.xlim(-5, 5)
# plt.ylim(-5, 5)

# x0, y0 = 0, 0

# with writer.saving(fig, "writer_test.mp4", 100):
#     for i in range(len(path_list)):
#         x0 += 0.1 * np.random.randn()
#         y0 += 0.1 * np.random.randn()
#         l.set_data(x0, y0)
#         writer.grab_frame()

def animation_func(iterationsres, steps):
    """ Function used to animate the simulation. """
    sns.set_style('dark')

    fig = plt.figure()

    mycmap = cm.get_cmap('hot')
    mycmap.set_under('w')
    im = plt.imshow(iterationsres[0], extent=[0, 1, 0, 1], cmap=mycmap, vmin=0.001
                    , animated=True)


    def animate(i):
        im.set_array(iterationsres[i])
        return im,

    anim = animation.FuncAnimation(fig, animate, frames=steps, interval=20, blit=True)

    anim.save("anim_river.mp4", fps=60, extra_args=['-vcodec', 'libx264'])
    plt.show()

# show_state_over_time(path_list, L=size)

size = 200
slope = 0.0001
water = 0.0008
ca = ca.CA(size=size, slope=slope, mu=0.0004, gamma=0.0002, rho=0.02, time_limit=size, delta_water=water, viz=True)
terrain = ca.initialize_terrain()
path_list = ca.create_path_from_start()
animation_func(path_list, 100)
