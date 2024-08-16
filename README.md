# Proyecto de Métodos Numéricos: Simulación de la Trayectoria de un Nanodron

Este proyecto forma parte de la asignatura de Métodos Numéricos y tiene como objetivo simular la trayectoria de un nanodron en el espacio utilizando ecuaciones diferenciales ordinarias (EDOs).

## Descripción

El programa permite simular el movimiento de un nanodron según las siguientes ecuaciones de movimiento:

\[
\frac {\delta x} {\delta t} = \alpha (y - x)
\]
\[
\frac {\delta y} {\delta t} = x(\beta - z)- y
\]
\[
\frac {\delta z} {\delta t} = x y - \gamma z
\]

Donde:
- \(x, y, z\) son las coordenadas del nanodron en el espacio.
- \(\alpha, \beta, \gamma\) son constantes positivas.
- \(t\) es el tiempo.

## Instalación

1. **Clonar el repositorio:**
    ```bash
    git clone https://github.com/NwDann/Proyecto-MN-IIB.git
    cd Proyecto-MN-IIB
    ```

2. **Crear un entorno virtual:**
    ```bash
    python -m venv venv
    ```

3. **Activar el entorno virtual:**
    - En Windows (PowerShell):
      ```powershell
      .\venv\Scripts\activate
      ```
    - En Windows (CMD):
      ```cmd
      venv\Scripts\activate.bat
      ```
    - En macOS/Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1. **Ejecutar la aplicación:**
    ```bash
    python main.py
    ```

2. **Ingresa los valores de \(\alpha\), \(\beta\), \(\gamma\), las coordenadas iniciales \(x, y, z\), y el tiempo de simulación cuando se te solicite.**

3. **Visualiza la trayectoria del nanodron en la gráfica generada.**

## Ejemplo

Para el caso 1:
- \(\alpha = 0.1\)
- \(\beta = 0.1\)
- \(\gamma = 0.1\)
- Coordenadas iniciales: \(x = 1\), \(y = 1\), \(z = 1\)
- Tiempo de simulación: 10 segundos

Para el caso 2:
- \(\alpha = 10\)
- \(\beta = 28\)
- \(\gamma = 8/3\)
- Coordenadas iniciales: \(x = 1\), \(y = 1\), \(z = 1\)
- Tiempo de simulación: 10 segundos

### Documentación del Código

### `metodo_euler(x, y, z, alpha, beta, gamma, numero_paso, paso)`
Esta función aplica el método de Euler para calcular la siguiente posición del dron en el espacio en función de las ecuaciones diferenciales que definen su movimiento.
- **Parámetros:**
  - `x`, `y`, `z` (float): Posiciones actuales en los ejes X, Y y Z.
  - `alpha`, `beta`, `gamma` (float): Parámetros que afectan la dinámica del sistema.
  - `numero_paso` (int): Número del paso actual en la simulación.
  - `paso` (float): Paso de tiempo que se utiliza para avanzar la simulación.
- **Retorna:**
  - Tupla con las nuevas posiciones (x_nuevo, y_nuevo, z_nuevo).
Si los nuevos valores calculados se salen de los límites numéricos (infinito o NaN), la simulación se detiene y se muestra un mensaje de error.

### `actualizar_grafico(num)`
Esta función actualiza el gráfico 3D con las posiciones del dron a lo largo de su trayectoria.
- **Parámetros:**
  - `num` (int): Número de cuadro actual en la animación.

### `iniciar_simulacion()`
Esta función inicia la simulación del vuelo del dron.
- **Acciones:**
  - Obtiene los parámetros de la simulación desde los campos de entrada.
  - Configura las condiciones iniciales de la simulación.
  - Desactiva los controles de entrada y actualiza los botones de control.
  - Inicia la animación de la simulación.

## Requisitos del Sistema

- Python 3.x
- Bibliotecas adicionales: tkinter, matplotlib, numpy, scipy
