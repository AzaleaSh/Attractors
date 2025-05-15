# Modeling Attractors and Chaos Theory
Modeling attractors using dynamical systems, Python, and Matplotlib

Hi all this was a fun little project. Essentially the code here is made to model the famous Lorenz Attractor. Developed by Edward Lorenz in the 1960s, this system of three relatively simple differential equations is a perfect example of deterministic chaos. I wrote this in a Juniper Notebook (.ipynb) and exported it to Github. You will need a few packages if you plan to reproduce this. 

The Lorenz system is a simplified mathematical model based on atmospheric convection. Despite its simplicity, its behavior is complex and unpredictable over longer periods. A key characteristic it demonstrates is sensitivity to initial conditions. This is also more popularly termed as the "butterfly effect" – the idea that a very small change in the initial state of the system can lead to drastically different outcomes over time.

## So how does my script mirror that?

My script specifically highlights the "butterfly effect" by simulating and animating two paths through the Lorenz system:

1. **The Initial Trajectory (White/Green):** This is the "standard" path, calculated starting from a specific initial state (`initial_state`) using numerical integration (`dt` time step).
2.  **The Perturbed Trajectory (Pink):** This path starts at a specific point along the *first* trajectory (`round_point_index`), but its starting coordinates are deliberately rounded to three decimal points. This rounding introduces a tiny, almost imperceptible difference in the initial conditions for this second trajectory.

The animation then shows both trajectories evolving simultaneously from the "rounding point" onwards.

The key visual takeaway is that while the pink and green paths branches off from the same point, because of the chaotic nature of the Lorenz system, that tiny initial difference (the rounding) is rapidly amplified, causing the pink trajectory to diverge significantly from the green trajectory over time. This visual separation is a direct demonstration of sensitivity to initial conditions.

## Technical Info

* The `lorenz_system` function defines the differential equations with standard parameters ($\sigma=10, \rho=28, \beta=8/3$).
* The script calculates all points for both trajectories beforehand using a basic Euler integration method.
* `matplotlib.animation.FuncAnimation` is used to create the animation. An `update` function is called for each frame to progressively reveal more of the calculated trajectory points, switching colors and showing the second path appear and diverge after the designated `round_point_index`.
