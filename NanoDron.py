import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.integrate import solve_ivp
from fractions import Fraction
import tkinter as tk
from tkinter import simpledialog, ttk, messagebox

def nanodron_equations(t, state, alpha, beta, gamma):
    x, y, z = state
    dxdt = alpha * (y - x)
    dydt = x * (beta - z) - y
    dzdt = x * y - gamma * z
    return [dxdt, dydt, dzdt]

def simulate_and_animate(alpha, beta, gamma, initial_conditions, t_final, canvas, ax):
    t_span = (0, t_final)
    t_eval = np.linspace(0, t_final, 1000)
    
    solution = solve_ivp(nanodron_equations, t_span, initial_conditions, args=(alpha, beta, gamma), t_eval=t_eval)
    
    x = solution.y[0]
    y = solution.y[1]
    z = solution.y[2]
    
    ax.clear()
    line, = ax.plot([], [], [], lw=2)
    point, = ax.plot([], [], [], 'o')

    ax.set_xlim(np.min(x), np.max(x))
    ax.set_ylim(np.min(y), np.max(y))
    ax.set_zlim(np.min(z), np.max(z))
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Trajectory with alpha={alpha}, beta={beta}, gamma={gamma}')
    
    def update(num, x, y, z, line, point):
        line.set_data(x[:num], y[:num])
        line.set_3d_properties(z[:num])
        point.set_data(x[num-1:num], y[num-1:num])
        point.set_3d_properties(z[num-1:num])
        return line, point
    
    ani = FuncAnimation(ax.figure, update, len(t_eval), fargs=[x, y, z, line, point], interval=10, blit=False)
    
    canvas.draw()

def start_simulation():
    entries = [alpha_entry, beta_entry, gamma_entry, x0_entry, y0_entry, z0_entry, t_final_entry]
    for entry in entries:
        if not entry.get():
            messagebox.showerror("Input Error", "All fields must be filled out")
            return
    
    try:
        alpha = float(Fraction(alpha_entry.get()))
        beta = float(Fraction(beta_entry.get()))
        gamma = float(Fraction(gamma_entry.get()))
        x0 = float(Fraction(x0_entry.get()))
        y0 = float(Fraction(y0_entry.get()))
        z0 = float(Fraction(z0_entry.get()))
        t_final = float(Fraction(t_final_entry.get()))
    except ValueError:
        messagebox.showerror("Input Error", "Invalid input. Please enter valid numbers or fractions.")
        return
    
    initial_conditions = [x0, y0, z0]
    simulate_and_animate(alpha, beta, gamma, initial_conditions, t_final, canvas, ax)

def validate_float_or_fraction(P):
    if P == "" or P == "-" or P == "/":
        return True
    if P.count('-') > 1 or P.count('/') > 1:
        return False
    if '-' in P and P.index('-') != 0:
        return False
    if '/' in P and P.index('/') == 0:
        return False
    try:
        float(Fraction(P))
        return True
    except ValueError:
        return False

root = tk.Tk()
root.title("NanoDron Simulation")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

vcmd = (root.register(validate_float_or_fraction), '%P')

ttk.Label(frame, text="Alpha:").grid(row=0, column=0, sticky=tk.W)
alpha_entry = ttk.Entry(frame, validate="key", validatecommand=vcmd)
alpha_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Beta:").grid(row=1, column=0, sticky=tk.W)
beta_entry = ttk.Entry(frame, validate="key", validatecommand=vcmd)
beta_entry.grid(row=1, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Gamma:").grid(row=2, column=0, sticky=tk.W)
gamma_entry = ttk.Entry(frame, validate="key", validatecommand=vcmd)
gamma_entry.grid(row=2, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Initial X:").grid(row=3, column=0, sticky=tk.W)
x0_entry = ttk.Entry(frame, validate="key", validatecommand=vcmd)
x0_entry.grid(row=3, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Initial Y:").grid(row=4, column=0, sticky=tk.W)
y0_entry = ttk.Entry(frame, validate="key", validatecommand=vcmd)
y0_entry.grid(row=4, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Initial Z:").grid(row=5, column=0, sticky=tk.W)
z0_entry = ttk.Entry(frame, validate="key", validatecommand=vcmd)
z0_entry.grid(row=5, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Simulation Time:").grid(row=6, column=0, sticky=tk.W)
t_final_entry = ttk.Entry(frame, validate="key", validatecommand=vcmd)
t_final_entry.grid(row=6, column=1, sticky=(tk.W, tk.E))

start_button = ttk.Button(frame, text="Start Simulation", command=start_simulation)
start_button.grid(row=7, column=0, columnspan=2, pady=10)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

root.mainloop()