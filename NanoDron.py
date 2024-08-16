import os
import signal
import tkinter as tk
from tkinter import messagebox
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Crear ventana de tkinter con los valores de entrada
def simulador():
    # Variables globales
    global entrada_alpha, entrada_beta, entrada_gamma, entrada_x_1, entrada_y_1, entrada_z_1, entrada_x_2, entrada_y_2, entrada_z_2, entrada_tiempo, entrada_paso, canvas, ventana

    # Crear la ventana
    ventana = tk.Tk()
    ventana.title("Simulación de NanoDron")

    # Crear un frame para los valores de entrada
    marco_izquierdo = tk.Frame(ventana)
    marco_izquierdo.pack(side=tk.LEFT)
    
    # Constantes positivas
    marco_constantes = tk.LabelFrame(marco_izquierdo, text="Constantes positivas")
    marco_constantes.grid(row= 0, column=0, padx=20, pady=10)  
    tk.Label(marco_constantes, text="Alpha").grid(row=0, column=0, padx=10, pady=5)
    entrada_alpha = tk.Entry(marco_constantes)
    entrada_alpha.grid(row=1, column=0, padx=10, pady=5)
    tk.Label(marco_constantes, text="Beta").grid(row=0, column=1, padx=10, pady=5)
    entrada_beta = tk.Entry(marco_constantes)
    entrada_beta.grid(row=1, column=1, padx=10, pady=5)
    tk.Label(marco_constantes, text="Gamma").grid(row=0, column=2, padx=10, pady=5)
    entrada_gamma = tk.Entry(marco_constantes)
    entrada_gamma.grid(row=1, column=2, padx=10, pady=5)

    # Puntos iniciales
    # Punto 1
    marco_punto1 = tk.LabelFrame(marco_izquierdo, text="Punto 1")
    marco_punto1.grid(row= 1, column=0, padx=20, pady=10)
    tk.Label(marco_punto1, text="X1").grid(row=0, column=0, padx=10, pady=5)
    entrada_x_1 = tk.Entry(marco_punto1)
    entrada_x_1.grid(row=1, column=0, padx=10, pady=5)
    tk.Label(marco_punto1, text="Y1").grid(row=0, column=1, padx=10, pady=5)
    entrada_y_1 = tk.Entry(marco_punto1)
    entrada_y_1.grid(row=1, column=1, padx=10, pady=5)
    tk.Label(marco_punto1, text="Z1").grid(row=0, column=2, padx=10, pady=5)
    entrada_z_1 = tk.Entry(marco_punto1)
    entrada_z_1.grid(row=1, column=2, padx=10, pady=5)

    # Punto 2
    marco_punto2 = tk.LabelFrame(marco_izquierdo, text="Punto 2")
    marco_punto2.grid(row= 2, column=0, padx=20, pady=10)
    tk.Label(marco_punto2, text="X2").grid(row=0, column=0, padx=10, pady=5)
    entrada_x_2 = tk.Entry(marco_punto2)
    entrada_x_2.grid(row=1, column=0, padx=10, pady=5)
    tk.Label(marco_punto2, text="Y2").grid(row=0, column=1, padx=10, pady=5)
    entrada_y_2 = tk.Entry(marco_punto2)
    entrada_y_2.grid(row=1, column=1, padx=10, pady=5)
    tk.Label(marco_punto2, text="Z2").grid(row=0, column=2, padx=10, pady=5)
    entrada_z_2 = tk.Entry(marco_punto2)
    entrada_z_2.grid(row=1, column=2, padx=10, pady=5)

    # Tiempo de simulación
    marco_tiempo = tk.LabelFrame(marco_izquierdo)
    marco_tiempo.grid(row= 3, column=0, padx=20, pady=10)
    tk.Label(marco_tiempo, text="Tiempo de simulación (s)").grid(row=0, column=0, padx=10, pady=5)
    entrada_tiempo = tk.Entry(marco_tiempo)
    entrada_tiempo.grid(row=1, column=0, padx=10, pady=5)
    tk.Label(marco_tiempo, text="Tamaño del paso").grid(row=0, column=1, padx=10, pady=5)
    entrada_paso = tk.Entry(marco_tiempo)
    entrada_paso.grid(row=1, column=1, padx=10, pady=5)

    # Botón de simulación
    boton_simulacion = tk.Button(marco_izquierdo, text="Iniciar simulación", command=simular)
    boton_simulacion.grid(row=4, column=0, padx=20, pady=10)

    # Crear un frame para el gráfico de simulación
    marco_derecho = tk.Frame(ventana)
    marco_derecho.pack(side=tk.RIGHT)
    marco_grafico = tk.LabelFrame(marco_derecho, text="Gráfico de simulación")
    marco_grafico.grid(row= 2, column=0, padx=20, pady=10)
    
    # Crear un canvas para dibujar el gráfico
    canvas = tk.Canvas(marco_grafico, width=400, height=410, bg="white")
    canvas.pack()

    ventana.protocol("WM_DELETE_WINDOW", on_closing)

    ventana.mainloop()

def dxdt(x, y, alpha):
    return alpha * (y - x)

def dydt(x, y, z, beta):
    return (x * (beta - z)) - y

def dzdt(x, y, z, gamma):
    return x * y - gamma * z

def metodo_euler(x, y, z, alpha, beta, gamma, paso):
    x_nuevo = x + dxdt(x, y, alpha) * paso
    y_nuevo = y + dydt(x, y, z, beta) * paso
    z_nuevo = z + dzdt(x, y, z, gamma) * paso
    return x_nuevo, y_nuevo, z_nuevo

def actualizar_grafico(num):
    trayectoria1.set_data(x1[:num], y1[:num])
    trayectoria1.set_3d_properties(z1[:num])
    punto1.set_data(x1[num-1:num], y1[num-1:num])
    punto1.set_3d_properties(z1[num-1:num])
    trayectoria2.set_data(x2[:num], y2[:num])
    trayectoria2.set_3d_properties(z2[:num])
    punto2.set_data(x2[num-1:num], y2[num-1:num])
    punto2.set_3d_properties(z2[num-1:num])

    return trayectoria1, punto1, trayectoria2, punto2,

# Función para deshabilitar todos los widgets de entrada
def disable_inputs(ventana):
    for widget in ventana.winfo_children():
        if isinstance(widget, (tk.Entry, tk.Button)):
            widget.config(state='disabled')

def simular():
    # Variables globales
    global trayectoria1, punto1, trayectoria2, punto2, x1, y1, z1, x2, y2, z2, animacion

    # Valores de entrada
    entries = [entrada_alpha, entrada_beta, entrada_gamma, entrada_x_1, entrada_y_1, entrada_z_1, entrada_x_2, entrada_y_2, entrada_z_2, entrada_tiempo, entrada_paso]
    for entry in entries:
        if not entry.get():
            messagebox.showerror("Error", "Todos los campos son requeridos")
            return
    
    # Obtener los valores de entrada
    alpha = float(entrada_alpha.get())
    beta = float(entrada_beta.get())
    gamma = float(entrada_gamma.get())
    x01 = float(entrada_x_1.get())
    y01 = float(entrada_y_1.get())
    z01 = float(entrada_z_1.get())
    x02 = float(entrada_x_2.get())
    y02 = float(entrada_y_2.get())
    z02 = float(entrada_z_2.get())
    tiempo = float(entrada_tiempo.get())
    paso = float(entrada_paso.get())

    # Numero de pasos
    numero_pasos = int(tiempo / paso)

    # Incializar las coordenadas
    x1 = np.zeros(numero_pasos)
    y1 = np.zeros(numero_pasos)
    z1 = np.zeros(numero_pasos)
    x2 = np.zeros(numero_pasos)
    y2 = np.zeros(numero_pasos)
    z2 = np.zeros(numero_pasos)    
    x1[0], y1[0], z1[0] = x01, y01, z01
    x2[0], y2[0], z2[0] = x02, y02, z02

    for i in range(1, numero_pasos):
       x1[i], y1[i], z1[i] = metodo_euler(x1[i-1], y1[i-1], z1[i-1], alpha, beta, gamma, paso)
       x2[i], y2[i], z2[i] = metodo_euler(x2[i-1], y2[i-1], z2[i-1], alpha, beta, gamma, paso)
    
    # Calcular los puntos minimos y maximos para ajustar el gráfico en el canvas
    min_x = min(min(x1), min(x2))
    min_y = min(min(y1), min(y2))
    min_z = min(min(z1), min(z2))
    max_x = max(max(x1), max(x2))
    max_y = max(max(y1), max(y2))
    max_z = max(max(z1), max(z2))
    
    # Crear plt figure 3d y colocarlo en el canvas
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.set_xlim(max_x, min_x)
    ax.set_ylim(max_y, min_y)
    ax.set_zlim(min_z, max_z)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.view_init(elev=15, azim=35)
    
    # Dibujar la trayectoria y puntos
    trayectoria1, = ax.plot([], [], [], label='Trayectoria del cuerpo 1', color='blue')
    punto1, = ax.plot([], [], [], 'o', label='Cuerpo 1', color='red')
    trayectoria2, = ax.plot([], [], [], label='Trayectoria del cuerpo 2', color='green')
    punto2, = ax.plot([], [], [], 'o', label='Cuerpo 2', color='orange')

    # Leyenda
    ax.legend(loc='best', fontsize='small', ncol=2)

    # Animacion
    animacion = FuncAnimation(fig, actualizar_grafico, frames=numero_pasos, interval=paso*1000, blit=True)
    
    # Integrar la figura de Matplotlib en el canvas de Tkinter
    canvas_figura = FigureCanvasTkAgg(fig, master=canvas)
    canvas_figura.draw()
    canvas_figura.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH) 

def on_closing():
    os.kill(os.getpid(), signal.SIGTERM)

# Llamar a la función para dibujar la ventana
simulador()