# Rocket Launch Simulator

A rocket launch simulator written in Python. It shows altitude, thrust, speed, and Earth's escape velocity while the rocket flies.

Hi, I'm Yaser. I have been working on this project for years, and I have finally built my own rocket program using my creativity. I'm still looking forward to creating even more creative rockets.

## What it does

You choose the rocket, launch it straight up, and watch what happens:

- **Altitude:** how high the rocket is, and the highest point it reached
- **Speed:** how fast it is moving
- **Thrust:** the force the engine is producing right now
- **Escape velocity:** the speed needed to leave Earth's gravity for good. It is 11.19 km/s at the surface and gets smaller as the rocket climbs
- **Fuel left**, and a bar showing your speed compared with escape velocity

If the rocket passes escape velocity, the program tells you it will not fall back to Earth. If it does not, it tells you its highest point and whether it crashed.

## How to run it

1. Install [Python 3](https://www.python.org/downloads/). Tkinter, which draws the window, comes with most Python installs.
   On Linux you may need: `sudo apt install python3-tk`
2. Download `rocket_launch_simulator.py`
3. Open a terminal in that folder and run:

```
python rocket_launch_simulator.py
```

No other libraries are needed.

## How to use it

Use the sliders to set:

| Setting | What it changes |
|---|---|
| Engine thrust (kN) | How strongly the engine pushes |
| Fuel mass (tonnes) | How much fuel the rocket carries |
| Engine efficiency, Isp (s) | How much push you get from each kilogram of fuel |
| Time speed | How fast the simulation runs |

Then press **Launch**. Two presets are included:

- **Small rocket:** climbs to about 500 km, then falls back
- **Escape rocket:** passes escape velocity and keeps going

The rocket cannot lift off if its thrust is lower than its own weight, and the program warns you if that happens.

## The physics

The simulation updates every 0.02 seconds using these formulas:

- **Escape velocity:** `v = sqrt(2GM / r)`
- **Gravity:** `g = GM / r²`, which gets weaker with height
- **Fuel use:** `fuel per second = thrust / (Isp × 9.80665)`
- **Air drag:** `½ × air density × speed² × drag coefficient × area`, with air getting thinner as the rocket climbs
- **Ideal speed gain (Δv):** `Isp × 9.80665 × ln(full mass / empty mass)`

## Limits

This is a simplified model:

- The rocket flies straight up only. It does not turn sideways to enter orbit.
- The empty rocket always weighs 25 tonnes.
- It has a single stage.
- It is a learning project, not a tool for real mission planning.

## Ideas for the future

- Sideways flight and orbits
- Rockets with more than one stage
- Other planets and moons
- Graphs of altitude and speed over time

## License

MIT License. See the `LICENSE` file.
