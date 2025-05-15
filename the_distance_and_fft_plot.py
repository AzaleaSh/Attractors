import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import numpy.fft as fft

# here are my presets
dt = .001 # how small your change in time is
total_time = 1000 # the total simulated time
initial_state = np.array([0, 1, 1.05]) # for a true lorenz attractor it will be 0, 1, 1,05

# mathematical !
def lorenz_system(state):
    x,y,z = state
    sigma = 10
    rho = 28
    beta = 8/3
    dxdt = sigma * (y - x)
    dydt = x * (rho-z) - y
    dzdt = x * y - beta * z
    return np.array([dxdt, dydt, dzdt])

num_steps = int(total_time / dt)
round_point_index = num_steps // 1000  # point at which the number will round and begin the second line set

# define the initial trajectory
trajectory_initial = np.empty((num_steps + 1, 3))
trajectory_initial[0] = initial_state
current_state_initial = initial_state

# let us fill up the array!
for i in range(num_steps):
    rates = lorenz_system(current_state_initial)
    next_state_initial = current_state_initial + rates * dt
    trajectory_initial[i+1] = next_state_initial
    current_state_initial = next_state_initial

rounding_precisions = [1, 2, 4, 6, 8, 10] # our 6 different rounding points of 2, 4, 6, and 8 decimal places


# DO IT FOR THE PLOT !!! The distance plots!
fig_distance, axes_distance = plt.subplots(3, 2, figsize=(12, 10))
axes_distance = axes_distance.flatten()

for i, precision in enumerate(rounding_precisions):
    trajectory_pink = np.empty((num_steps - round_point_index + 1, 3))
    current_state_pink = np.round(trajectory_initial[round_point_index], precision)
    trajectory_pink[0] = current_state_pink

    for j in range(num_steps - round_point_index):
        rates = lorenz_system(current_state_pink)
        next_state_pink = current_state_pink + rates * dt
        trajectory_pink[j+1] = next_state_pink
        current_state_pink = next_state_pink

    min_len = min(len(trajectory_initial[round_point_index:]), len(trajectory_pink))
    distances = np.linalg.norm(trajectory_initial[round_point_index:round_point_index + min_len] - trajectory_pink[:min_len], axis=1)

    time_distance = np.arange(min_len) * dt
    axes_distance[i].plot(time_distance, distances, color = "pink") # y'all i had to do it in PINK :pppp
    axes_distance[i].set_title(f'Distance vs Time (Rounding to {precision} decimals)')
    axes_distance[i].set_xlabel('Time (seconds)')
    axes_distance[i].set_ylabel('Distance (arbitrary units)')
    axes_distance[i].set_yscale('log')
    axes_distance[i].grid(True)

plt.tight_layout()
plt.show

#WHAT ?!?!??! COULD THEIR BE PERIODIC BEHAVIOR?!?!?!?
# alright lets run it back but do it in an fft 
# !!!

fig_fft_distance, axes_fft_distance = plt.subplots(3, 2, figsize=(12, 10))
axes_fft_distance = axes_fft_distance.flatten()

# iterate through the distances for each precision value and perform the eff-eff-tee
for i, precision in enumerate(rounding_precisions):
    trajectory_pink = np.empty((num_steps - round_point_index + 1, 3))
    current_state_pink = np.round(trajectory_initial[round_point_index], precision)
    trajectory_pink[0] = current_state_pink

    for j in range(num_steps - round_point_index):
        rates = lorenz_system(current_state_pink)
        next_state_pink = current_state_pink + rates * dt
        trajectory_pink[j+1] = next_state_pink
        current_state_pink = next_state_pink

    min_len = min(len(trajectory_initial[round_point_index:]), len(trajectory_pink))
    distances = np.linalg.norm(trajectory_initial[round_point_index:round_point_index + min_len] - trajectory_pink[:min_len], axis=1)

    # alright here is the reel deel
    fft_distance = fft.fft(distances)

    # the reel frequent deel
    frequencies_distance = fft.fftfreq(min_len, dt)

    # AND YOU KNOW I HAD TO DO IT FOR THE PLOT.
    axes_fft_distance[i].plot(frequencies_distance[:min_len // 2], np.abs(fft_distance[:min_len // 2]))
    axes_fft_distance[i].set_title(f'Fourier Transform of Distance (Rounding to {precision} decimals)')
    axes_fft_distance[i].set_xlabel('Frequency (Hz)')
    axes_fft_distance[i].set_ylabel('Magnitude')
    axes_fft_distance[i].grid(True)
    axes_fft_distance[i].set_xlim(0, 2)
    axes_fft_distance[i].set_ylim(0, 1000000)

plt.tight_layout()
plt.show()
