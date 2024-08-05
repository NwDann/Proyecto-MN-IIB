import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp
import tkinter as tk
from tkinter import simpledialog

def nanodron_equations(t, state, alpha, beta, gamma):
    x, y, z = state
    dxdt = alpha * (y - x)
    dydt = x * (beta - z) - y
    dzdt = x * y - gamma * z
    return [dxdt, dydt, dzdt]

def simulate_and_animate(alpha, beta, gamma, initial_conditions, t_final):
    t_span = (0, t_final)
    t_eval = np.linspace(0, t_final, 1000)
    
    solution = solve_ivp(nanodron_equations, t_span, initial_conditions, args=(alpha, beta, gamma), t_eval=t_eval)
    
    x = solution.y[0]
    y = solution.y[1]
    z = solution.y[2]
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
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
    
    ani = FuncAnimation(fig, update, len(t_eval), fargs=[x, y, z, line, point], interval=10, blit=False)
    
    plt.show()

def get_input():
    root = tk.Tk()
    root.withdraw()
    
    alpha = float(simpledialog.askstring("Input", "Enter the value of alpha:", parent=root))
    beta = float(simpledialog.askstring("Input", "Enter the value of beta:", parent=root))
    gamma = float(simpledialog.askstring("Input", "Enter the value of gamma:", parent=root))
    
    x0 = float(simpledialog.askstring("Input", "Enter the initial x coordinate:", parent=root))
    y0 = float(simpledialog.askstring("Input", "Enter the initial y coordinate:", parent=root))
    z0 = float(simpledialog.askstring("Input", "Enter the initial z coordinate:", parent=root))
    
    t_final = float(simpledialog.askstring("Input", "Enter the simulation time (seconds):", parent=root))
    
    return alpha, beta, gamma, [x0, y0, z0], t_final

if __name__ == "__main__":
    alpha, beta, gamma, initial_conditions, t_final = get_input()
    simulate_and_animate(alpha, beta, gamma, initial_conditions, t_final)
