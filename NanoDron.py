import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import simpledialog, ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Definir las ecuaciones de movimiento
def dx_dt(x, y, alpha):
    print('x', x)
    print('y', y)
    print('alpha', alpha)    
    result = alpha * (y - x)
    print('alpha', result)
    return result

def dy_dt(y, z, beta):
    print('y', y)
    print('z', z)
    print('beta', beta)
    # Calcular z * (beta - z)
    try:
        z_term = z * (beta - z)
    except OverflowError:
        print('Overflow in z * (beta - z)')
        return np.inf if z > 0 else -np.inf
    
    print('z_term:', z_term)
    
    # Calcular el resultado final
    result = z_term - y
    print('result:', result)
    return result

def dz_dt(x, y, z, gamma):    
    print('x', x)
    print('y', y)
    print('z', z)
    print('gamma', gamma)    
    result = x * y - gamma * z
    print('result_gamma', result)
    return result

# Definir el método de Euler
def euler_method(x0, y0, z0, dt, num_steps, alpha, beta, gamma):
    x = np.zeros(num_steps)
    y = np.zeros(num_steps)
    z = np.zeros(num_steps)

    x[0] = x0
    y[0] = y0
    z[0] = z0

    for i in range(1, num_steps):
        x[i] = x[i-1] + dt * dx_dt(x[i-1], y[i-1], alpha)
        y[i] = y[i-1] + dt * dy_dt(y[i-1], z[i-1], beta)
        z[i] = z[i-1] + dt * dz_dt(x[i-1], y[i-1], z[i-1], gamma)

        # Control de estabilidad
        if np.isinf(x[i]) or np.isinf(y[i]) or np.isinf(z[i]) or np.isnan(x[i]) or np.isnan(y[i]) or np.isnan(z[i]):
            print(f"Desbordamiento numérico en el paso {i}")
            break

        # Limitar los valores a un rango específico
        if abs(x[i]) > 1.5 or abs(y[i]) > 1.5 or abs(z[i]) > 1.5:
            print(f"Valor fuera de rango en el paso {i}")
            break

    return x, y, z

# Variable global para la animación
ani = None

# Función para iniciar la simulación
def start_simulation():

    # Validar que todos los campos estén llenos
    entries = [entry_alpha, entry_beta, entry_gamma, entry_x0_1, entry_y0_1, entry_z0_1, entry_x0_2, entry_y0_2, entry_z0_2, entry_time]
    for entry in entries:
        if not entry.get():
            messagebox.showerror("Input Error", "All fields must be filled out")
            return

    global ani

    # Detener la animación anterior si existe
    if ani is not None:
        ani.event_source.stop()
        ani = None

    # Obtener los valores ingresados por el usuario
    try:
        alpha = float(entry_alpha.get())
        beta = float(entry_beta.get())
        gamma = float(entry_gamma.get())
        x0_1 = float(entry_x0_1.get())
        y0_1 = float(entry_y0_1.get())
        z0_1 = float(entry_z0_1.get())
        x0_2 = float(entry_x0_2.get())
        y0_2 = float(entry_y0_2.get())
        z0_2 = float(entry_z0_2.get())
        time = float(entry_time.get())
    except ValueError:
        messagebox.showerror("Input Error", "Invalid input. Please enter valid numbers or fractions.")
        return
    
    # Tamaño del paso de integración y número de pasos
    dt = 0.001
    num_steps = int(time / dt)

    # Resolver el sistema de ecuaciones utilizando el método de Euler para ambos puntos iniciales
    x1, y1, z1 = euler_method(x0_1, y0_1, z0_1, dt, num_steps, alpha, beta, gamma)
    x2, y2, z2 = euler_method(x0_2, y0_2, z0_2, dt, num_steps, alpha, beta, gamma)

    # Determinar si min(x1) o min(x2) es menor
    min_x = min(min(x1), min(x2))
    min_y = min(min(y1), min(y2))
    min_z = min(min(z1), min(z2))
    max_x = max(max(x1), max(x2))
    max_y = max(max(y1), max(y2))
    max_z = max(max(z1), max(z2))

    # Limpiar el gráfico
    ax = fig.add_subplot(111, projection='3d')
    ax.clear()
    ax.set_xlim([min_x, max_x])
    ax.set_ylim([min_y, max_y])
    ax.set_zlim([min_z, max_z])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Actualizar el gráfico con los nuevos datos
    def update(num):
        line1.set_data(x1[:num], y1[:num])
        line1.set_3d_properties(z1[:num])
        point1.set_data(x1[num-1:num], y1[num-1:num])
        point1.set_3d_properties(z1[num-1:num])
        line2.set_data(x2[:num], y2[:num])
        line2.set_3d_properties(z2[:num])
        point2.set_data(x2[num-1:num], y2[num-1:num])
        point2.set_3d_properties(z2[num-1:num])
        time_label.config(text=f"Time: {num * dt:.2f} s")
        return line1, point1, line2, point2

    ani = FuncAnimation(fig, update, frames=num_steps, interval=dt*1000, blit=True)
    canvas.draw()

# Función para detener la simulación
def stop_simulation():
    global ani
    if ani is not None:
        ani.event_source.stop()
        ani = None

# Función para validar que un valor sea un número flotante
def validate_float(P):
    if P == "" or P == "-":
        return True
    try:
        float(P)
        return True
    except ValueError:
        return False

# Crear la ventana de tkinter
root = tk.Tk()
root.title("NanoDron Simulation")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Configurar el espacio entre columnas en el frame
frame.columnconfigure(0, pad=30)
frame.columnconfigure(1, pad=30)
frame.columnconfigure(2, pad=30)
frame.columnconfigure(3, pad=30)

# Validar los valores de entrada
vcmd = (root.register(validate_float), '%P')

# Crear los frame para los valores de entrada
ttk.Label(frame, text="Alpha:").grid(row=0, column=0, sticky=tk.E)
entry_alpha = ttk.Entry(frame, validate="key", validatecommand=vcmd)
entry_alpha.grid(row=0, column=1, sticky=tk.W)

ttk.Label(frame, text="Beta:").grid(row=1, column=0, sticky=tk.E)
entry_beta = ttk.Entry(frame, validate="key", validatecommand=vcmd)
entry_beta.grid(row=1, column=1, sticky=tk.W)

ttk.Label(frame, text="Gamma:").grid(row=0, column=2, sticky=tk.E)
entry_gamma = ttk.Entry(frame, validate="key", validatecommand=vcmd)
entry_gamma.grid(row=0, column=3, sticky=tk.W)

ttk.Label(frame, text="Simulation Time (seconds):").grid(row=1, column=2, sticky=tk.E)
entry_time = ttk.Entry(frame, validate="key", validatecommand=vcmd)
entry_time.grid(row=1, column=3, sticky=tk.W)

ttk.Label(frame, text="").grid(row=2, column=0, sticky=tk.E)

ttk.Label(frame, text="Initial X1:").grid(row=3, column=0, sticky=tk.E)
entry_x0_1 = ttk.Entry(frame, validate="key", validatecommand=vcmd)
entry_x0_1.grid(row=3, column=1, sticky=tk.W)

ttk.Label(frame, text="Initial Y1:").grid(row=4, column=0, sticky=tk.E)
entry_y0_1 = ttk.Entry(frame, validate="key", validatecommand=vcmd)
entry_y0_1.grid(row=4, column=1, sticky=tk.W)

ttk.Label(frame, text="Initial Z1:").grid(row=5, column=0, sticky=tk.E)
entry_z0_1 = ttk.Entry(frame, validate="key", validatecommand=vcmd)
entry_z0_1.grid(row=5, column=1, sticky=tk.W)

ttk.Label(frame, text="Initial X2:").grid(row=3, column=2, sticky=tk.E)
entry_x0_2 = ttk.Entry(frame, validate="key", validatecommand=vcmd)
entry_x0_2.grid(row=3, column=3, sticky=tk.W)

ttk.Label(frame, text="Initial Y2:").grid(row=4, column=2, sticky=tk.E)
entry_y0_2 = ttk.Entry(frame, validate="key", validatecommand=vcmd)
entry_y0_2.grid(row=4, column=3, sticky=tk.W)

ttk.Label(frame, text="Initial Z2:").grid(row=5, column=2, sticky=tk.E)
entry_z0_2 = ttk.Entry(frame, validate="key", validatecommand=vcmd)
entry_z0_2.grid(row=5, column=3, sticky=tk.W)

# Crear los botones de inicio y parada de la simulación
start_button = ttk.Button(frame, text="Start Simulation", command=start_simulation)
start_button.grid(row=6, column=1, sticky=tk.E, pady=10, padx=20)

stop_button = ttk.Button(frame, text="Stop Simulation", command=stop_simulation)
stop_button.grid(row=6, column=2, sticky=tk.W, pady=10, padx=20)

# Crear y colocar la etiqueta del cronómetro
time_label = ttk.Label(frame, text="Time: 0.00 s")
time_label.grid(row=7, column=0, columnspan=2, pady=10)

# Crear el gráfico inicial
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([1.5, -0.5])
ax.set_ylim([1.5, -0.5])
ax.set_zlim([-0.5, 1.5])
ax.set_xticks(np.arange(-0.5, 1.6, 0.5))
ax.set_yticks(np.arange(-0.5, 1.6, 0.5))
ax.set_zticks(np.arange(-0.5, 1.6, 0.5))
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.view_init(elev=15, azim=35)
line1, = ax.plot([], [], [], label='Trayectoria del cuerpo 1', color='blue')
point1, = ax.plot([], [], [], 'ro', label='Cuerpo 1')
line2, = ax.plot([], [], [], label='Trayectoria del cuerpo 2', color='orange')
point2, = ax.plot([], [], [], 'go', label='Cuerpo 2')
ax.legend(loc='best', fontsize='small', ncol=2)

# Mostrar el gráfico en la ventana de tkinter
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)

# Iniciar el bucle principal de tkinter
root.mainloop()