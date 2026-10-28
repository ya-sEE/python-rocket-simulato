"""Rocket Launch Simulator (Python, tkinter).

Straight-up flight with thrust, gravity that weakens with height, air drag,
fuel burn, and live escape velocity. Run:  python rocket_launch_simulator.py
Needs only Python 3 with tkinter (included with most Python installs).
"""
import math
import random

G = 6.674e-11        # gravity constant
M = 5.972e24         # Earth mass (kg)
R = 6.371e6          # Earth radius (m)
G0 = 9.80665         # standard gravity (m/s^2)
DRY = 25000.0        # empty rocket mass (kg)
CD, AREA = 0.3, 10.0  # drag coefficient, frontal area (m^2)


def escape_velocity(h):
    """Escape speed (m/s) at height h metres above the surface."""
    return math.sqrt(2 * G * M / (R + h))


class Sim:
    def __init__(self, thrust_kn, fuel_t, isp):
        self.thrust = thrust_kn * 1000.0
        self.fuel0 = fuel_t * 1000.0
        self.fuel = self.fuel0
        self.isp = isp
        self.h = self.v = self.t = self.max_h = self.thr_now = 0.0
        self.launched = self.done = self.escaped = self.fell = False
        self.message = ""

    def twr(self):
        return self.thrust / ((DRY + self.fuel0) * G0)

    def delta_v(self):
        return self.isp * G0 * math.log((DRY + self.fuel0) / DRY)

    def burn_time(self):
        return self.fuel0 / (self.thrust / (self.isp * G0))

    def step(self, dt=0.02):
        if not self.launched or self.done:
            return
        burning = self.fuel > 0
        force = self.thrust if burning else 0.0
        if burning:
            self.fuel = max(0.0, self.fuel - force / (self.isp * G0) * dt)
        mass = DRY + self.fuel
        g = G * M / (R + self.h) ** 2
        rho = 1.225 * math.exp(-self.h / 8500.0)
        drag = 0.5 * rho * self.v * abs(self.v) * CD * AREA
        a = (force - drag) / mass - g
        self.thr_now = force
        if self.h <= 0 and a < 0 and self.v <= 0:   # still on the pad
            self.h = self.v = 0.0
            if not burning:
                self._end("The engine ran out before liftoff.")
            return
        self.v += a * dt
        self.h += self.v * dt
        self.t += dt
        self.max_h = max(self.max_h, self.h)
        if self.h <= 0:
            self.h = 0.0
            self._end(f"Crashed back to Earth at {-self.v:,.0f} m/s. "
                      f"Highest point: {self.max_h / 1000:,.0f} km.")
        elif not self.escaped and self.h > 1000 and self.v >= escape_velocity(self.h):
            self.escaped = True
            self.message = (f"Escape velocity reached at {self.h / 1000:,.0f} km. "
                            "The rocket will not fall back.")
        elif not self.escaped and not self.fell and self.v < 0 and self.t > 2:
            self.fell = True
            self.message = (f"Highest point {self.max_h / 1000:,.1f} km. "
                            "Falling back to Earth.")
        if self.escaped and self.h > 2e8:
            self._end("Escape confirmed. 200,000 km from Earth and still climbing.")

    def _end(self, text):
        self.done = True
        self.message = text


def main():
    import tkinter as tk

    W, H = 380, 560
    root = tk.Tk()
    root.title("Rocket Launch Simulator")
    root.configure(bg="#070d1f")

    left = tk.Frame(root, bg="#070d1f")
    left.pack(side="left", padx=10, pady=10)
    right = tk.Frame(root, bg="#070d1f")
    right.pack(side="left", padx=10, pady=10, fill="y")

    canvas = tk.Canvas(left, width=W, height=H, highlightthickness=1,
                       highlightbackground="#22325c")
    canvas.pack()
    stars = [[random.random() * W, random.random() * H, random.random() * 1.5 + 0.5]
             for _ in range(70)]

    def slider(label, lo, hi, val, res):
        s = tk.Scale(right, from_=lo, to=hi, resolution=res, orient="horizontal",
                     label=label, length=330, bg="#0f1830", fg="#e4ecfa",
                     troughcolor="#22325c", highlightthickness=0)
        s.set(val)
        s.pack(pady=2)
        return s

    thr = slider("Engine thrust (kN)", 500, 20000, 3000, 100)
    fuel = slider("Fuel mass (tonnes)", 20, 1000, 200, 10)
    isp = slider("Engine efficiency, Isp (s)", 250, 460, 350, 5)
    warp = slider("Time speed (x)", 1, 100, 5, 1)

    plan = tk.Label(right, wraplength=330, justify="left", bg="#070d1f", fg="#8d9cc0")
    plan.pack(pady=4)
    stats = tk.Label(right, justify="left", font=("Courier", 12), bg="#070d1f",
                     fg="#e4ecfa")
    stats.pack(pady=4)
    msg = tk.Label(right, wraplength=330, justify="left", bg="#070d1f", fg="#5fe0c8",
                   font=("Helvetica", 11, "bold"))
    msg.pack(pady=4)

    state = {"sim": None}

    def new_sim(*_):
        sim = Sim(thr.get(), fuel.get(), isp.get())
        state["sim"] = sim
        plan.config(text=(f"Launch weight {(DRY + sim.fuel0) / 1000:,.0f} t. "
                          f"Thrust-to-weight {sim.twr():.2f}. "
                          f"Ideal speed gain {sim.delta_v() / 1000:.1f} km/s over "
                          f"{sim.burn_time():,.0f} s. Escape needs 11.19 km/s plus losses."))
        ok = sim.twr() > 1
        launch_btn.config(state="normal" if ok else "disabled")
        msg.config(text="" if ok else "Thrust is lower than the rocket's weight.",
                   fg="#ff6b6b")

    def launch():
        sim = state["sim"]
        if not sim.launched and not sim.done:
            sim.launched = True
            launch_btn.config(state="disabled")
            msg.config(text="Liftoff.", fg="#e4ecfa")

    def preset(t, f, i, w):
        thr.set(t); fuel.set(f); isp.set(i); warp.set(w)
        new_sim()

    bar = tk.Frame(right, bg="#070d1f")
    bar.pack(pady=4)
    launch_btn = tk.Button(bar, text="Launch", command=launch, bg="#ff9a3c")
    launch_btn.pack(side="left", padx=3)
    tk.Button(bar, text="Reset", command=new_sim).pack(side="left", padx=3)
    tk.Button(bar, text="Small rocket",
              command=lambda: preset(1500, 80, 300, 5)).pack(side="left", padx=3)
    tk.Button(bar, text="Escape rocket",
              command=lambda: preset(15000, 900, 450, 20)).pack(side="left", padx=3)
    for s in (thr, fuel, isp):
        s.config(command=lambda _v: (new_sim() if not state["sim"].launched else None))

    def mix(a, b, f):
        return "#%02x%02x%02x" % tuple(int(x + (y - x) * f) for x, y in zip(a, b))

    def draw(sim):
        canvas.delete("all")
        f = min(1.0, sim.h / 100000.0)
        canvas.create_rectangle(0, 0, W, H, fill=mix((74, 163, 232), (3, 5, 14), f), width=0)
        if sim.h > 30000:
            for st in stars:
                st[1] = (st[1] + min(30, abs(sim.v) * 0.002)) % H
                canvas.create_rectangle(st[0], st[1], st[0] + st[2], st[1] + st[2],
                                        fill="white", width=0)
        ry = H * 0.5
        off = 170 * math.log10(1 + sim.h / 60.0)
        gy = ry + 95 + off
        if gy < H:
            canvas.create_rectangle(0, gy, W, H, fill="#1f3b2a", width=0)
        for d, label in ((1e3, "1 km"), (1e4, "10 km"), (1e5, "100 km"), (1e6, "1,000 km"),
                         (1e7, "10,000 km"), (1e8, "100,000 km")):
            y = ry + 95 + off - 170 * math.log10(1 + d / 60.0)
            if 0 < y < H:
                canvas.create_line(W - 30, y, W, y, fill="#cccccc")
                canvas.create_text(W - 34, y - 6, text=label, anchor="e",
                                   fill="#dddddd", font=("Helvetica", 8))
        x = W / 2
        if sim.launched and not sim.done and sim.fuel > 0:
            fl = 40 + random.random() * 30
            canvas.create_polygon(x - 12, ry + 92, x + 12, ry + 92, x, ry + 95 + fl,
                                  fill="#ff9a3c", width=0)
        canvas.create_rectangle(x - 16, ry - 60, x + 16, ry + 92, fill="#c9d4ea", width=0)
        canvas.create_polygon(x - 16, ry - 60, x, ry - 125, x + 16, ry - 60,
                              fill="#ff9a3c", width=0)
        canvas.create_polygon(x - 16, ry + 50, x - 34, ry + 95, x - 16, ry + 92,
                              fill="#3a4a73", width=0)
        canvas.create_polygon(x + 16, ry + 50, x + 34, ry + 95, x + 16, ry + 92,
                              fill="#3a4a73", width=0)
        canvas.create_oval(x - 7, ry - 37, x + 7, ry - 23, fill="#5fe0c8", width=0)

    def loop():
        sim = state["sim"]
        if sim.launched and not sim.done:
            for _ in range(max(1, round(warp.get() * 0.016 / 0.02))):
                sim.step(0.02)
        ve = escape_velocity(sim.h)
        pct = max(0, min(1, sim.v / ve)) * 100
        shown = sim.thr_now if (sim.launched and not sim.done and sim.fuel > 0) else 0
        stats.config(text=(
            f"Altitude        {sim.h / 1000:>12,.1f} km\n"
            f"Speed           {abs(sim.v) / 1000:>12,.2f} km/s\n"
            f"Thrust now      {shown / 1000:>12,.0f} kN\n"
            f"Escape velocity {ve / 1000:>12,.2f} km/s\n"
            f"Highest point   {sim.max_h / 1000:>12,.1f} km\n"
            f"Fuel left       {sim.fuel / sim.fuel0 * 100:>12,.0f} %\n"
            f"Speed vs escape {pct:>12,.0f} %"))
        if sim.message:
            msg.config(text=sim.message, fg="#5fe0c8" if sim.escaped else "#ff6b6b")
        draw(sim)
        root.after(16, loop)

    new_sim()
    loop()
    root.mainloop()


if __name__ == "__main__":
    main()
