import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython import get_ipython
from IPython.display import display

# simulation parameters
total_time = 50  # total simulated time of the physical lorenz attractor
dt = 0.001  # time step of the physical lorenz attractor
initial_state = np.array([0, 1, 1.05])  # initial state of the lorenz attractor
num_steps = int(total_time / dt)
round_point_index = num_steps // 50 #the round point at where the white switches to pink green

simulation_duration_seconds = 30 # time of the video that you download
fps = 20 # fps of the video that you download

# lorenz system function (the hyperfixation)
def lorenz_system(state):
    x, y, z = state
    sigma = 10
    rho = 28
    beta = 8/3
    dxdt = sigma * (y - x)
    dydt = x * (rho-z) - y
    dzdt = x * y - beta * z
    return np.array([dxdt, dydt, dzdt])

# more calcs (short for calculator)
num_steps = int(total_time / dt)
num_frames = simulation_duration_seconds * fps
steps_per_frame = num_steps // num_frames

# simulate the initial trajectory (green/white)
trajectory_initial = np.empty((num_steps + 1, 3))
trajectory_initial[0] = initial_state
current_state_initial = initial_state

for i in range(num_steps):
    rates = lorenz_system(current_state_initial)
    next_state_initial = current_state_initial + rates * dt
    trajectory_initial[i+1] = next_state_initial
    current_state_initial = next_state_initial

# the pink trajectory!
trajectory_pink = np.empty((num_steps - round_point_index + 1, 3))
current_state_pink = np.round(trajectory_initial[round_point_index],3)
trajectory_pink[0] = current_state_pink

for i in range(num_steps - round_point_index):
    rates = lorenz_system(current_state_pink)
    next_state_pink = current_state_pink + rates * dt
    trajectory_pink[i+1] = next_state_pink
    current_state_pink = next_state_pink

# I DO IT FOR THE PLOT!!
fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(projection='3d')
ax.set_facecolor('k')
ax.set_axis_off()

# initialize the line objects for all trajectories
line_initial, = ax.plot([], [], [], lw=0.5, color='white', alpha=1)
line_green, = ax.plot([], [], [], lw=0.5, color='green', alpha=0.5)
line_pink, = ax.plot([], [], [], lw=0.5, color='pink', alpha=0.5)

# initialize the marker for the point
marker_rounding_point, = ax.plot([], [], [], 'o', color='white', alpha=1, markersize=3)
pink_marker_point, = ax.plot([], [], [], 'o', color='pink', alpha=1, markersize=3)
green_marker_point, = ax.plot([], [], [], 'o', color='green', alpha=1, markersize=3)


# anime function
def update(frame):
    current_steps = frame * steps_per_frame
    
    # make white line !
    if current_steps <= round_point_index:
      line_initial.set_data(trajectory_initial[:current_steps, 0], trajectory_initial[:current_steps, 1])
      line_initial.set_3d_properties(trajectory_initial[:current_steps, 2])
    else:
      line_initial.set_data(trajectory_initial[:round_point_index, 0], trajectory_initial[:round_point_index, 1])
      line_initial.set_3d_properties(trajectory_initial[:round_point_index, 2])

    # make green line !
    if current_steps > round_point_index:
        line_green.set_data(trajectory_initial[round_point_index:current_steps, 0], trajectory_initial[round_point_index:current_steps, 1])
        line_green.set_3d_properties(trajectory_initial[round_point_index:current_steps, 2])
    else:
        line_green.set_data([], [])
        line_green.set_3d_properties([])

    # make pink line !
    if current_steps > round_point_index:
        pink_steps = current_steps - round_point_index
        line_pink.set_data(trajectory_pink[:pink_steps, 0], trajectory_pink[:pink_steps, 1])
        line_pink.set_3d_properties(trajectory_pink[:pink_steps, 2])
    else:
        line_pink.set_data([], [])
        line_pink.set_3d_properties([])

    # make marker :p
    if current_steps > round_point_index:
         rounding_point_state = trajectory_initial[round_point_index - 1]
         marker_rounding_point.set_data([rounding_point_state[0]], [rounding_point_state[1]])
         marker_rounding_point.set_3d_properties([rounding_point_state[2]])
    else:
         marker_rounding_point.set_data([], [])
         marker_rounding_point.set_3d_properties([])

    # make pink marker :D
    if current_steps > round_point_index and (current_steps - round_point_index - 1) < len(trajectory_pink):
      pink_marker_point.set_data([trajectory_pink[current_steps - round_point_index - 1, 0]], [trajectory_pink[current_steps - round_point_index - 1, 1]])
      pink_marker_point.set_3d_properties([trajectory_pink[current_steps - round_point_index - 1, 2]])
    else:
      pink_marker_point.set_data([], [])
      pink_marker_point.set_3d_properties([]) # Also clear 3d properties when not plotting
    
    # make green marker :0
    if current_steps > round_point_index and (current_steps - round_point_index - 1) < len(trajectory_initial):
      green_marker_point.set_data([trajectory_initial[current_steps, 0]], [trajectory_initial[current_steps, 1]])
      green_marker_point.set_3d_properties([trajectory_initial[current_steps, 2]])
    else:
      green_marker_point.set_data([], [])
      green_marker_point.set_3d_properties([])


    ax.set_xlim(trajectory_initial[:, 0].min(), trajectory_initial[:, 0].max())
    ax.set_ylim(trajectory_initial[:, 1].min(), trajectory_initial[:, 1].max())
    ax.set_zlim(trajectory_initial[:, 2].min(), trajectory_initial[:, 2].max())

    return line_initial, line_green, line_pink, marker_rounding_point,

# where's the function? where the fuck the function?
ani = FuncAnimation(fig, update, frames=num_frames, blit=True)

ani.save('lorenz_attractor_animation.mp4', writer='ffmpeg', fps=fps)

plt.show()
