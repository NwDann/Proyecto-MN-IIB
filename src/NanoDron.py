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
    """
    Crea la interfaz gráfica de la simulación del NanoDron utilizando Tkinter.

    La interfaz permite ingresar los valores de las constantes (alpha, beta, gamma),
    las coordenadas iniciales de dos puntos en el espacio (X1, Y1, Z1 y X2, Y2, Z2),
    y los parámetros de tiempo de simulación y tamaño del paso.

    La interfaz también incluye un gráfico 3D que muestra la trayectoria simulada
    de los dos puntos en el espacio a lo largo del tiempo.
    """
    
    # Variables globales
    global entrada_alpha, entrada_beta, entrada_gamma, entrada_x_1, entrada_y_1 
    global entrada_z_1, entrada_x_2, entrada_y_2, entrada_z_2, entrada_tiempo
    global entrada_paso, canvas, marco_constantes, marco_punto1, marco_punto2 
    global marco_tiempo, boton_simular, boton_parar, tiempo_transcurrido, ventana

    # Crear la ventana
    ventana = tk.Tk()
    ventana.title("Simulación de NanoDron")

    # Crear un frame para los valores de entrada
    marco_izquierdo = tk.Frame(ventana)
    marco_izquierdo.pack(side=tk.LEFT)
    
    # Validar los valores de entrada
    flotantes_positivos = (ventana.register(validar_entradas), '%P', 'p')
    flotantes_positivos_negativos = (ventana.register(validar_entradas), '%P', 'n')

    # Constantes positivas
    marco_constantes = tk.LabelFrame(marco_izquierdo, text="Constantes positivas")
    marco_constantes.grid(row= 0, column=0, padx=20, pady=10)  
    tk.Label(marco_constantes, text="Alpha").grid(row=0, column=0, padx=10, pady=5)
    entrada_alpha = tk.Entry(marco_constantes, validate='key', validatecommand=flotantes_positivos)
    entrada_alpha.grid(row=1, column=0, padx=10, pady=5)
    tk.Label(marco_constantes, text="Beta").grid(row=0, column=1, padx=10, pady=5)
    entrada_beta = tk.Entry(marco_constantes, validate='key', validatecommand=flotantes_positivos)
    entrada_beta.grid(row=1, column=1, padx=10, pady=5)
    tk.Label(marco_constantes, text="Gamma").grid(row=0, column=2, padx=10, pady=5)
    entrada_gamma = tk.Entry(marco_constantes, validate='key', validatecommand=flotantes_positivos)
    entrada_gamma.grid(row=1, column=2, padx=10, pady=5)

    # Puntos iniciales
    # Punto 1
    marco_punto1 = tk.LabelFrame(marco_izquierdo, text="Punto 1")
    marco_punto1.grid(row= 1, column=0, padx=20, pady=10)
    tk.Label(marco_punto1, text="X1").grid(row=0, column=0, padx=10, pady=5)
    entrada_x_1 = tk.Entry(marco_punto1, validate='key', validatecommand=flotantes_positivos_negativos)
    entrada_x_1.grid(row=1, column=0, padx=10, pady=5)
    tk.Label(marco_punto1, text="Y1").grid(row=0, column=1, padx=10, pady=5)
    entrada_y_1 = tk.Entry(marco_punto1, validate='key', validatecommand=flotantes_positivos_negativos)
    entrada_y_1.grid(row=1, column=1, padx=10, pady=5)
    tk.Label(marco_punto1, text="Z1").grid(row=0, column=2, padx=10, pady=5)
    entrada_z_1 = tk.Entry(marco_punto1, validate='key', validatecommand=flotantes_positivos_negativos)
    entrada_z_1.grid(row=1, column=2, padx=10, pady=5)

    # Punto 2
    marco_punto2 = tk.LabelFrame(marco_izquierdo, text="Punto 2")
    marco_punto2.grid(row= 2, column=0, padx=20, pady=10)
    tk.Label(marco_punto2, text="X2").grid(row=0, column=0, padx=10, pady=5)
    entrada_x_2 = tk.Entry(marco_punto2, validate='key', validatecommand=flotantes_positivos_negativos)
    entrada_x_2.grid(row=1, column=0, padx=10, pady=5)
    tk.Label(marco_punto2, text="Y2").grid(row=0, column=1, padx=10, pady=5)
    entrada_y_2 = tk.Entry(marco_punto2, validate='key', validatecommand=flotantes_positivos_negativos)
    entrada_y_2.grid(row=1, column=1, padx=10, pady=5)
    tk.Label(marco_punto2, text="Z2").grid(row=0, column=2, padx=10, pady=5)
    entrada_z_2 = tk.Entry(marco_punto2, validate='key', validatecommand=flotantes_positivos_negativos)
    entrada_z_2.grid(row=1, column=2, padx=10, pady=5)

    # Tiempo de simulación
    marco_tiempo = tk.LabelFrame(marco_izquierdo)
    marco_tiempo.grid(row= 3, column=0, padx=20, pady=10)
    tk.Label(marco_tiempo, text="Tiempo de simulación (s)").grid(row=0, column=0, padx=10, pady=5)
    entrada_tiempo = tk.Entry(marco_tiempo, validate='key', validatecommand=flotantes_positivos)
    entrada_tiempo.grid(row=1, column=0, padx=10, pady=5)
    tk.Label(marco_tiempo, text="Tamaño del paso").grid(row=0, column=1, padx=10, pady=5)
    entrada_paso = tk.Entry(marco_tiempo, validate='key', validatecommand=flotantes_positivos)
    entrada_paso.grid(row=1, column=1, padx=10, pady=5)

    # Marco para los botones de simulación
    marco_botones = tk.Frame(marco_izquierdo)
    marco_botones.grid(row= 4, column=0, padx=20, pady=10)
    boton_simular = tk.Button(marco_botones, text="Iniciar simulación", command=procesar_informacion)
    boton_simular.grid(row=0, column=0, padx=10)
    boton_parar = tk.Button(marco_botones, text="Parar simulación", command=parar, state=tk.DISABLED)
    boton_parar.grid(row=0, column=1, padx=10)

    # Crear un frame para el gráfico de simulación
    marco_derecho = tk.Frame(ventana)
    marco_derecho.pack(side=tk.RIGHT)
    marco_grafico = tk.LabelFrame(marco_derecho, text="Gráfico de simulación")
    marco_grafico.grid(row= 0, column=0, padx=20, pady=10)
    tiempo_transcurrido = tk.Label(marco_grafico, text="Tiempo transcurrido: 0.00 s", font=('', 10, 'bold'))
    tiempo_transcurrido.grid(row=0, column=0, columnspan=2, pady=10)
    
    # Crear un canvas para dibujar el gráfico
    canvas = tk.Canvas(marco_grafico, width=448, height=448, bg="white")
    canvas.grid(row=1, column=0)
    
    ventana.protocol("WM_DELETE_WINDOW", on_closing)
    ventana.mainloop()

def validar_entradas(value, signal):
    """
    Valida que los valores ingresados en las entradas sean números flotantes positivos
    o negativos, según el tipo de señal proporcionado.

    Args:
        value (str): El valor ingresado en la entrada.
        signal (str): Señal que indica si el valor debe ser un flotante positivo ('p')
                      o un flotante positivo o negativo ('n').

    Returns:
        bool: True si el valor es válido, False en caso contrario.
    """
    
    # Flotante positivo
    if signal == 'p':
        if value == "":
            return True
    # Flotante postivos o negativo
    elif signal == 'n':
        if value == "" or value == "-":
            return True
    try:
        float(value)
        return True
    except ValueError:
        return False

def dxdt(x, y, alpha):
    """
    Calcula la derivada de x con respecto al tiempo según la ecuación dx/dt = alpha * (y - x).

    Args:
        x (float): Valor de x en un tiempo dado.
        y (float): Valor de y en un tiempo dado.
        alpha (float): Constante que determina la tasa de cambio.

    Returns:
        float: Valor de la derivada dx/dt.
    """
    
    result = alpha * (y - x)
    if not np.isfinite(result):
        result = np.clip(result, -1e308, 1e308)  # Limitar a un rango finito
    return result

def dydt(x, y, z, beta):
    """
    Calcula la derivada de y con respecto al tiempo según la ecuación dy/dt = beta * (z - y).

    Args:
        y (float): Valor de y en un tiempo dado.
        z (float): Valor de z en un tiempo dado.
        beta (float): Constante que determina la tasa de cambio.

    Returns:
        float: Valor de la derivada dy/dt.
    """
    
    result = (x * (beta - z)) - y
    if not np.isfinite(result):
        result = np.clip(result, -1e308, 1e308)  # Limitar a un rango finito
    return result

def dzdt(x, y, z, gamma):
    """
    Calcula la derivada de z con respecto al tiempo según la ecuación dz/dt = gamma * (x - z).

    Args:
        z (float): Valor de z en un tiempo dado.
        x (float): Valor de x en un tiempo dado.
        gamma (float): Constante que determina la tasa de cambio.

    Returns:
        float: Valor de la derivada dz/dt.
    """
    
    result = x * y - gamma * z
    if not np.isfinite(result):
        result = np.clip(result, -1e308, 1e308)  # Limitar a un rango finito
    return result

def metodo_euler(x, y, z, alpha, beta, gamma, numero_paso, paso):
    """
    Aplica el método de Euler para calcular las nuevas coordenadas (x, y, z) de un punto en el espacio.

    Utiliza las ecuaciones diferenciales definidas para dx/dt, dy/dt y dz/dt, con las constantes alpha, 
    beta y gamma para determinar la tasa de cambio.

    Args:
        x (float): Coordenada actual en el eje X.
        y (float): Coordenada actual en el eje Y.
        z (float): Coordenada actual en el eje Z.
        alpha (float): Constante que afecta la tasa de cambio de x.
        beta (float): Constante que afecta la tasa de cambio de y.
        gamma (float): Constante que afecta la tasa de cambio de z.
        numero_paso (int): Número del paso actual en la simulación.
        paso (float): Tamaño del paso de tiempo en la simulación.

    Returns:
        tuple: Nuevas coordenadas (x_nuevo, y_nuevo, z_nuevo) después de aplicar el método de Euler,
        o None si ocurre un desbordamiento numérico.
    """
    
    x_nuevo = x + dxdt(x, y, alpha) * paso
    y_nuevo = y + dydt(x, y, z, beta) * paso
    z_nuevo = z + dzdt(x, y, z, gamma) * paso

    # Control de estabilidad
    if np.isinf(x_nuevo) or np.isinf(y_nuevo) or np.isinf(z_nuevo) or np.isnan(x_nuevo) or np.isnan(y_nuevo) or np.isnan(z_nuevo):
        mensage = f"Desbordamiento numérico en el paso {numero_paso}. Con valores x: {x_nuevo}, y: {y_nuevo}, z: {z_nuevo}"
        messagebox.showerror("Error", message=mensage)
        habilitar_deshabilitar_entradas('normal')
        boton_simular.config(text="Iniciar simulación", state=tk.NORMAL)
        return

    return x_nuevo, y_nuevo, z_nuevo

def actualizar_grafico(num):
    """
    Actualiza el gráfico 3D con las trayectorias y posiciones actuales de los puntos en cada frame de la simulación.

    Mueve las trayectorias y los puntos en el gráfico para representar el progreso de la simulación. También actualiza
    la etiqueta que muestra el tiempo transcurrido y controla el estado de los botones en la interfaz una vez que la 
    simulación termina.

    Args:
        num (int): El número actual del frame en la simulación.

    Returns:
        tuple: Los objetos de Matplotlib (trayectoria1, punto1, trayectoria2, punto2) actualizados para el frame actual.
    """
    
    trayectoria1.set_data(x1[:num], y1[:num])
    trayectoria1.set_3d_properties(z1[:num])
    punto1.set_data(x1[num-1:num], y1[num-1:num])
    punto1.set_3d_properties(z1[num-1:num])
    trayectoria2.set_data(x2[:num], y2[:num])
    trayectoria2.set_3d_properties(z2[:num])
    punto2.set_data(x2[num-1:num], y2[num-1:num])
    punto2.set_3d_properties(z2[num-1:num])
    tiempo_transcurrido.config(text=f"Tiempo transcurrido: {num * paso:.2f} s")

    # Emitir cuando haya transcurrido el tiempo de simulación
    if (num + 1) == len(x1):
        habilitar_deshabilitar_entradas('normal')
        boton_simular.config(text="Iniciar simulación", state=tk.NORMAL)    
        boton_parar.config(state=tk.DISABLED)

    return trayectoria1, punto1, trayectoria2, punto2,

# Función para habilitar o deshabilitar todos los widgets de entrada
def habilitar_deshabilitar_entradas(action):
    """
    Habilita o deshabilita todos los campos de entrada (Entry) en los marcos de la interfaz gráfica.

    Esta función recorre todos los widgets en los marcos `marco_constantes`, `marco_punto1`, `marco_punto2` 
    y `marco_tiempo`, y cambia el estado de los campos de entrada (Entry) según el valor del parámetro `action`.
    Esto permite desactivar los campos de entrada mientras la simulación está en curso y volver a activarlos 
    cuando la simulación finaliza.

    Args:
        action (str): Estado a aplicar a los campos de entrada. Puede ser 'normal' para habilitarlos o 'disabled' 
        para deshabilitarlos.
    """
    
    for widget in marco_constantes.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.config(state=action)
    for widget in marco_punto1.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.config(state=action)
    for widget in marco_punto2.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.config(state=action)
    for widget in marco_tiempo.winfo_children():
        if isinstance(widget, tk.Entry):
            widget.config(state=action)

def procesar_informacion():
    """
    Procesa la información ingresada en la interfaz y realiza la simulación.

    Obtiene los valores de las constantes y las coordenadas iniciales de los puntos
    desde las entradas de la interfaz para calcular las trayectorias de
    los puntos a lo largo del tiempo.

    Los resultados de la simulación se muestran en un gráfico 3D en la interfaz.
    """
    
    # Deshabilitar los widgets de entrada
    habilitar_deshabilitar_entradas('disabled')

    # Cambiar el texto del botón a "Procesando..."
    boton_simular.config(text="Procesando...", state=tk.DISABLED)
    ventana.update()  # Actualiza la interfaz para mostrar el cambio inmediatamente
    
    # Llamar a la función
    response = simular()
    if response:
        # Restaurar el texto original del botón
        boton_simular.config(text="Iniciar simulación", state=tk.DISABLED)
        boton_parar.config(state=tk.NORMAL)
    else:
        habilitar_deshabilitar_entradas('normal')
        boton_simular.config(text="Iniciar simulación", state=tk.NORMAL)

def simular():
    """
    Dibuja la trayectoria de los puntos en el gráfico 3D.
    Anima el tiempo transcurrido en la simulación y actualiza la etiqueta correspondiente.

    La animación se ejecuta en un bucle que se detiene cuando se alcanza el tiempo
    máximo de simulación o se detiene manualmente por el usuario.
    """
    
    # Variables globales
    global trayectoria1, punto1, trayectoria2, punto2, x1, y1, z1, x2, y2, z2
    global animacion, canvas_figura, paso
    
    # Valores de entrada
    entries = [entrada_alpha, entrada_beta, entrada_gamma, entrada_x_1, entrada_y_1, entrada_z_1, 
               entrada_x_2, entrada_y_2, entrada_z_2, entrada_tiempo, entrada_paso]
    for entry in entries:
        if not entry.get():
            messagebox.showerror("Error", "Todos los campos son requeridos.")
            return
    if float(entrada_paso.get()) == 0:
        messagebox.showerror("Error", "El Tamaño del paso debe ser mayor que cero.")
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
    if numero_pasos < 10:
        messagebox.showerror("Error", "Con los datos ingresados de Tiempo de simulación " +  
                             "y Tamaño del paso, se generaron menos de 10 numeros de pasos. No se puede simular.")
        return

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
       x1[i], y1[i], z1[i] = metodo_euler(x1[i-1], y1[i-1], z1[i-1], alpha, beta, gamma, i, paso)
       x2[i], y2[i], z2[i] = metodo_euler(x2[i-1], y2[i-1], z2[i-1], alpha, beta, gamma, i, paso)
          
    # Calcular los puntos minimos y maximos para ajustar el gráfico en el canvas
    min_x = min(min(x1), min(x2))
    min_y = min(min(y1), min(y2))
    min_z = min(min(z1), min(z2))
    max_x = max(max(x1), max(x2))
    max_y = max(max(y1), max(y2))
    max_z = max(max(z1), max(z2))
    
    # Crear plt figure 3d y colocarlo en el canvas    
    fig = plt.figure(figsize=(4.5, 4.5))
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.clear()
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
    animacion = FuncAnimation(fig, actualizar_grafico, frames=numero_pasos, interval=paso*1000, blit=True, repeat=False)
   
    # Si ya existe una figura, se elimina
    if 'canvas_figura' in globals():
        canvas_figura.get_tk_widget().pack_forget()  

    # Integrar la figura de Matplotlib en el canvas de Tkinter
    canvas_figura = FigureCanvasTkAgg(fig, master=canvas)
    canvas_figura.draw()
    canvas_figura.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH) 
    
    return True

def parar():
    """
    Detiene la simulación y reinicia la interfaz.

    La función reinicia los valores de la interfaz y habilita los botones de simulación.
    """
    
    global animacion
    if animacion is not None:
        animacion.event_source.stop()
        animacion = None
    habilitar_deshabilitar_entradas('normal')
    boton_simular.config(state=tk.NORMAL)
    boton_parar.config(state=tk.DISABLED)

def on_closing():
    """
    Cierra la ventana principal cuando el usuario selecciona la opción de cerrar.

    Esta función se utiliza para asegurarse de que todos los procesos se detengan
    correctamente antes de cerrar la aplicación.
    """
    
    os.kill(os.getpid(), signal.SIGTERM)

# Llamar a la función para simular
simulador()