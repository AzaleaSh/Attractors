# Modeling The Lorenz Attractors and Chaos Theory
Modeling attractors using dynamical systems, Python, and Matplotlib

https://github.com/user-attachments/assets/8c5c095f-a232-4ee7-962b-31ff2d6db6fc

Hello! This project was genuinely very fun with a lot of physics and mathematics concepts, specifically focusing on dynamical systems. I wanted to share the process and discoveries I made while modeling one of the most famous examples of deterministic chaos: the Lorenz Attractor. I will preface with that I am a high school senior, there is high chance that I am mathematically incorrect.

Developed by the meteorologist Edward Lorenz in the 1960s, this system uses three relatively simple differential equations, yet produces incredibly complex and beautiful non-deterministic behavior. I wrote this code in a Jupyter Notebook (`.ipynb`), which allowed me to visualize things interactively before exporting it all to this GitHub repository. If you want to follow along or run the code yourself, you'll need a few standard Python packages, which I'll list later.

Let's walk through the project steps, discoveries, and the math behind them!!!! :P

## The Animated Butterfly Effect (my personal favorite)

The main aspect of the excitement behind the Lorenz system is its sensitivity to initial conditions. This project's first goal was to visualize this phenomenon, often called the "butterfly effect". Simply put: a tiny change in the beginning state can lead to drastically different outcomes later on. My first step was to create an animation to show this directly.

My script does this by simulating two paths (or trajectories) through the Lorenz system at the same time:

* **The Initial Trajectory (White/Green):** This is like our "standard" path. It's calculated starting from a specific initial point (`initial_state`) using a numerical method to step through time (`dt`).
* **The Perturbed Trajectory (Pink):** This path starts at a point taken directly from the *first* trajectory at a specific time index (`round_point_index`). However, here's the crucial part: its starting coordinates are rounded to only a few decimal places. This rounding is the tiny difference in the initial condition for this second trajectory.

The animation then starts showing the first path (white/green). When it reaches the `round_point_index`, the pink path appears, starting from that slightly-rounded version of the same point, and both trajectories continue moving simultaneously from that moment forward.


### What?! Why does this happen?

This visual divergence here is the butterfly effect in action, it is due to the non-linear nature of the Lorenz equations:

$$
\begin{align*} \frac{dx}{dt} &= \sigma(y - x),  \\ \frac{dy}{dt} &= x(\rho - z) - y,  \\ \frac{dz}{dt} &= xy - \beta z \end{align*}
$$

This exponential growth of the difference means that our inability to measure or represent initial conditions with infinite precision makes long-term prediction impossible.

## Measuring the Separation - Distance vs. Time

Watching the animation is interesting, but I wanted to quantify just how fast those two paths were separating. So, the next logical step was to calculate and plot the distance between the corresponding points on the green/white and pink trajectories over time, starting from the `round_point_index` where the pink path began.

The resulting plot looks like this:

![distance_time_graph](https://github.com/user-attachments/assets/814bd5ee-b5fd-4018-ad0b-37c93c56a63e)

As you can see, the figure contains 6 subplots. Each subplot shows the distance over time for a simulation where the initial perturbation (the rounding) for the pink trajectory was different: rounding to 1, 2, 4, 6, 8, or 10 decimal places.

### Wow, Why Does This Happen????

Looking at these plots, especially as the simulation runs longer, there is something very intersting: the distance doesn't grow smoothly to infinity. It seems to fluctuate, sometimes increasing rapidly, sometimes leveling off, or even decreasing momentarily, creating a maybe oscillatory pattern?? Why would the distance between paths show this behavior when the system itself isn't periodic?

I believe that this goes back to the nature of the strange attractor. The trajectories are confined to a bounded region (the butterfly wings). They can't just fly off forever. While they diverge exponentially on the attractor, the stretching and folding mechanism means that the two trajectories, as they orbit around the two lobes of the attractor, can occasionally be brought back into relative proximity before being stretched apart again.

The oscillations in the distance reflect this dynamic. The distance increases as the trajectories move apart on a lobe or transition between lobes. It might decrease slightly or level off when the folding of the attractor brings previously separated parts of the trajectories closer together. It's not true system periodicity, though, or is it?

## Is there a Rhythm of Separation - Fourier Analysis

The apparent oscillatory behavior in the distance plot was particularly intriguing to me. It made me wonder if there was some underlying frequency to the separation process. So intro Fourier Transform!

Simply put, a Fourier Transform takes a signal (like our distance-over-time data) and breaks it down into the frequencies that make it up. It tells you which frequencies are most dominant in the signal. So, I applied a Fourier Transform to the distance data to see what frequencies were present.

Here's the Fourier Transform plot:

![fourier_transform_graph](https://github.com/user-attachments/assets/00dfc768-eb08-4e27-b655-ffd3f275a436)


### Whatttt! What Does This Peak Mean?

Looking at the plot, there's a clear peak in the frequency spectrum, roughly between 1.25 and 1.50. This peak becomes more pronounced as the initial rounding (and thus the simulation time where the trajectories are still somewhat "related") increases.

This dominant frequency is very very fascinating! It could suggest that the oscillations in the distance between the trajectories are not just random wiggles but are happening with a characteristic frequency.

Soooo, what could this frequency relate to? Since the trajectories are orbiting around the two attractors of the butterfly attractor and switching between the lobes, this peak frequency could likely correspond to the average frequency of these orbital motions or the switching frequency between the lobes. This is very very interesting, especially given that the system itself is entirely chaotic! So how in the world could there possibly exist any type of periodic motion? I don't know, I have plans to look at this closer specifically by variable, also seeing how the coeffecients effect this, as it is known that some combinations of coeffiecents can yield periodic or quasiperiodic behaviors.

A quick note: I did test a few variables to ensure this was not an experimental error. I am not quite sure what this is. It does seem to have a relation to the coefficients but I am not sure what that is or entails. I will note that as rho is increased the peak of that frequency does increase.

## The Halvorsen System

Switching gears here, one cool aspect of this project was realizing how modular the code structure was. The main simulation loop just needed a function defining the system's equations (`def system(state)`).

To demonstrate this, I included another simulation of another interesting dynamical system: the **Halvorsen Attractor**. This system has a different set of equations but also exhibits chaotic behavior and has a unique strange attractor shape.

https://github.com/user-attachments/assets/b7d5ab94-9427-4eca-ad38-938ec5cdc499

The only change needed was defining a new function for the Halvorsen system's ODEs. 

## Technical Notes and How to Run

Here's a quick summary of the technical bits:

* System Definition: The `lorenz_system` function holds the core differential equations with standard parameters ($\sigma=10, \rho=28, \beta=8/3$).
* Integration: The script calculates all trajectory points beforehand using a basic Euler integration method.
* Animation Creation: `matplotlib.animation.FuncAnimation` is used to build the animation frame by frame. An `update` function tells each frame how much of the trajectories to show, handling the color changes and the appearance of the second (pink) path after the `round_point_index`.
