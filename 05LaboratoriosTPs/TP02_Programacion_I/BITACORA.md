# Bitácora Técnica de Trabajo - TP02 Programación I

## Integrantes
* **Nombre y Apellido:** Clara Di Stefano, Candela Baak, Felipe Oneto.
* **Comisión:** Miercoles Noche

a) ¿Qué herramientas necesita el TP?

Intérprete de Python: Para la ejecución del entorno y el desarrollo de los scripts de control.

Entorno de desarrollo (IDE): VS Code (Visual Studio Code) para la edición, depuración y estructuración del código en archivos .py.

Consola de comandos / Terminal: Para la activación de entornos virtuales y la ejecución de los scripts de servidor y control.

Entorno virtual de Python (venv): Para el aislamiento y gestión limpia de dependencias del proyecto.

Gestor de paquetes pip: Para la instalación de librerías del proyecto.

b) ¿Qué versión de Python se requiere?
Se requiere Python 3.10 o superior, versión compatible con el entorno de simulación y el motor MuJoCo.

c) ¿Qué componentes ya están instalados en la computadora?
Sistema Operativo: Windows 10 de 64 bits.
Intérprete básico de Python y el gestor de paquetes pip.
Control de versiones: Git / GitHub Desktop.
Navegador web de uso estándar.

d) ¿Qué componentes del repositorio oficial de Unitree no son necesarios para este laboratorio?

Controladores de hardware físico (SDK de C++ de Unitree): No se necesitan los programas ni controladores para conectar la computadora a un robot físico real.

Compilación manual de MuJoCo desde código fuente: No hace falta compilar el simulador MuJoCo manualmente ni instalar archivos pesados de desarrollo en C++.

Módulos de simulación compleja o ROS (Robot Operating System): No se utilizan sistemas complejos de robótica industrial (como ROS/ROS2), ya que la simulación se ejecuta de manera directa mediante el script y la ventana gráfica local.

e) ¿Qué diferencias observan entre el TP en PDF y la versión actual del repositorio?

Firma de métodos en la API: Algunos métodos como robot.saludar() no requieren argumentos en la versión actual de la API, a diferencia de versiones o borradores previos del instructivo.   

En versiones anteriores del TP los movimientos se pedían como distancia y velocidad, o ángulo y sentido. En la versión actual del repositorio, los comandos de avanzar y girar usan velocidad y tiempo.

* Para avanzar, la distancia recorrida es la velocidad multiplicada por el tiempo.   
* Para girar, el ángulo de giro es la velocidad multiplicada por el tiempo. Además, el signo de la velocidad indica la dirección: si es positivo gira a la izquierda y si es negativo gira a la derecha

Estructura de la plantilla: La versión actual del repositorio integra la simulación web simplificada a través de un servidor ligero en server.py, lo que optimiza la puesta en marcha en comparación con el instructivo general original.

Formato de los comandos: La especificación de comandos en forma de tuplas de 1 a 3 elementos se ajusta estrictamente a los límites de seguridad definidos en la versión actual del código.  


## Registro y Análisis de Problemas

### Problema N° 1: Conexión al robot equivocado (G1 en lugar de Go2)
* **Qué se estaba intentando hacer:** Ejecutar la simulación para el perro Unitree Go2.
* **Comando ejecutado:** `INICIAR_SIMULADOR.bat`.
* **Resultado obtenido:** Se abrió la ventana 3D del humanoide G1 y al ejecutar el script decía `Conectado a Unitree G1`.
* **Causa:** quedó el proceso anterior abierto con el humanoide.
* **Solución aplicada:** Se cerró la consola del simulador y las ventanas 3D de MuJoCo, se volvió a ejecutar `INICIAR_SIMULADOR.bat` y se ingresó la opción `2` explícitamente.
* **Estado final:** RESUELTO (`[OK] Conectado a Unitree Go2`).




### Problema N° 2: Constantes de límites desfasadas con la especificación del robot Go2
* **Qué se estaba intentando hacer:** Validar y ejecutar la misión de prueba en el simulador del robot Unitree Go2.
* **Comando ejecutado:** `EJECUTAR_MI_CODIGO.bat`
* **Comportamiento observado:** Al ejecutar el script, el robot se conectaba (`[OK] Conectado a Unitree Go2`) indicando en consola los límites permitidos (`0.2 m/s`, `0.5 rad/s`), pero se desconectaba inmediatamente sin ejecutar acciones (`[OK] Desconectado`).
* **Causa:** En el archivo `mi_tp02.py`, las constantes globales estaban desalineadas con la API real del robot (`VELOCIDAD_MAX = 0.5` en lugar de `0.2`, `ANGULO_MAX = 180` en lugar de `0.5` rad/s y la presencia innecesaria de `DISTANCIA_MAX`).
* **Solución aplicada:** Se actualizaron las constantes globales en `mi_tp02.py` para coincidir con la especificación de la simulación (`VELOCIDAD_MAX = 0.2`, `ANGULO_MAX = 0.5`, `TIEMPO_MAX = 10.0`) y se eliminó la validación por distancia.
* **Estado final:** RESUELTO. Las constantes quedaron correctamente alineadas con los límites del Go2, permitiendo que la función `ejecutar_mision()` inicie el despacho de comandos.




### Problema N° 3: Error de argumento inesperado en `robot.avanzar()`
* **Qué se estaba intentando hacer:** Ejecutar el comando "avanzar" de la misión sobre la instancia del robot.
* **Comando ejecutado:** `EJECUTAR_MI_CODIGO.bat`
* **Comportamiento observado:** La consola lanzó un `TypeError: Robot.avanzar() got an unexpected keyword argument 'duracion'` al intentar ejecutar el primer comando.
* **Causa:** Se llamó a `robot.avanzar(velocidad=velocidad, duracion=tiempo)` usando el parámetro nombrado `duracion=`, pero la firma del método en la librería del robot no reconoce esa palabra clave.
* **Solución aplicada:** Se cambió el llamado a argumentos posicionales directos: `robot.avanzar(velocidad, tiempo)`.
* **Estado final:** RESUELTO.



### Problema N° 4: Exceso de argumentos en `robot.girar()`
* **Qué se estaba intentando hacer:** Ejecutar la orden de giro de la misión.
* **Comando ejecutado:** `EJECUTAR_MI_CODIGO.bat`
* **Comportamiento observado:** `TypeError: Robot.girar() takes from 1 to 3 positional arguments but 4 were given`.
* **Causa:** Se le pasaban 3 parámetros (`abs(vel_angular)`, `tiempo`, `sentido`), pero la API del robot solo espera 2 parámetros (`vel_angular`, `tiempo`), determinando el sentido automáticamente según el signo positivo o negativo de la velocidad angular.
* **Solución aplicada:** Se simplificó la llamada a `robot.girar(vel_angular, tiempo)` sin calcular el sentido de forma explícita ni agregar parámetros extra.
* **Estado final:** RESUELTO.



### Problema N° 5: Exceso de argumentos en `robot.saludar()`
* **Qué se estaba intentando hacer:** Invocar el saludo del robot mediante `robot.saludar("saludo")`.
* **Comando ejecutado:** `EJECUTAR_MI_CODIGO.bat`
* **Comportamiento observado:** `TypeError: Robot.saludar() takes 1 positional argument but 2 were given`.
* **Causa:** El método `saludar()` de la librería del Go2 no requiere parámetros de entrada. Al pasarle una cadena de texto, Python contó 2 argumentos (la instancia `self` y la cadena).
* **Solución aplicada:** Se eliminó la cadena de texto de los paréntesis, dejando la llamada limpia como `robot.saludar()`.
* **Estado final:** RESUELTO. La misión propia ejecutó correctamente los 6 comandos.




**Verificación Final y Resultados:**

* **Misión Básica:**Se ejecutó exitosamente la misión de prueba completa (`MISION_BASICA`) comprobando en la ventana 3D de MuJoCo el desplazamiento, giro y pose de saludo del robot. La consola confirmó la ejecución de 4/4 comandos, registrando una distancia recorrida de 0.8 m y una duración estimada de 7.75 s.

* **Misión con Errores:** Se probó la ejecución de `MISION_CON_ERRORES` modificando la llamada en el bloque principal (`main`). Se verificó el correcto funcionamiento del filtro de validación: el controlador detectó los comandos con parámetros fuera de rango e inválidos, los omitió de la ejecución física registrándolos en el historial y continuó con la misión sin interrupciones ni fallos en el simulador.

### Análisis del Error de Seguridad (`MISION_CON_ERRORES`)

* **Comando analizado:** `EJECUTAR_MI_CODIGO.bat` corriendo `MISION_CON_ERRORES`.
* **Comportamiento y excepción observada:** La consola interrumpió la ejecución lanzando el error `sim.safety.ErrorDeSeguridad: Tiempo 50.00 s: el maximo por comando en tp02-programacion-i es 10.0 s.` desde el archivo `safety.py`.
* **Análisis técnico:** La función `comando_es_valido()` no chequeó que el tiempo fuera menor a 10 segundos, por lo que dejó pasar el comando. Cuando se intentó mover al robot, el sistema de seguridad interno del simulador (`safety.py`) detectó que el tiempo (50 segundos) superaba el límite permitido y frenó el programa para proteger la simulación.
* **Conclusión:** Esto demuestra por qué es tan importante que nuestro código en `comando_es_valido()` filtre bien todos los parámetros de entrada antes de enviárselos al robot, evitando que el simulador tenga que cortar la ejecución por una falla de seguridad.


Cierre y reflexión

a) ¿Cuál fue la principal dificultad de instalación?

La principal dificultad de instalación fue el fallo por falta de reconocimiento de los módulos al ejecutar pip install mujoco y la verificación del simulador. El error ocurría porque las dependencias se intentaban instalar de forma global sin haber activado previamente el entorno virtual venv mediante el comando de activación en la terminal. Al no estar la consola posicionada en la carpeta raíz del proyecto y con el entorno virtual activo, el intérprete de Python no encontraba la librería MuJoCo ni las referencias del simulador al intentar validar la instalación.

b) ¿Qué error requirió mayor investigación?

El error que requirió mayor investigación fue la diferencia entre los parámetros indicados en el PDF original del trabajo práctico y la versión actual del repositorio. Al comenzar el desarrollo tomando como guía el instructivo en PDF, los argumentos de las funciones de movimiento y saludo no coincidían con lo que esperaba el código actual, lo que llevó bastante tiempo de depuración e investigación.

c) ¿Qué solución resultó efectiva y por qué?

La solución efectiva fue revisar las definiciones de las funciones en el repositorio actual para ajustar las llamadas, utilizando velocidad y tiempo para los movimientos e invocando robot.saludar sin argumentos entre los paréntesis. Resultó efectiva porque adaptó la lógica del script a la firma exacta requerida por la versión vigente de la API.

d) ¿Qué intento no funcionó y qué aprendieron de él?

No funcionó intentar pasarle el texto del comando como parámetro a la función robot.saludar("saludar") pensando que la API lo requería. Se hicieron varios intentos probando distintas formas de enviarle argumentos a la función sin lograr que ejecute. De esto se aprendió a revisar las firmas internas de los métodos en el código fuente de la librería y a comprender que las llamadas a la API deben ir sin parámetros adicionales cuando la función original así lo define.

e) ¿Qué diferencia encontraron entre una guía antigua y la arquitectura actual?

La guía antigua expresaba los movimientos mediante distancia y ángulo o velocidad y sentido, mientras que la arquitectura actual del repositorio utiliza velocidad y tiempo para avanzar y girar. Además, la plantilla actual simplifica la ejecución mediante un servidor local y no requiere instalar ni compilar librerías físicas pesadas de C++.

f) ¿Hasta qué nivel lograron avanzar?

Se logró avanzar hasta completar la totalidad de los niveles del trabajo práctico, logrando la implementación completa de la arquitectura Top-Down, la validación estricta de seguridad, el registro de eventos en el historial y la ejecución exitosa de la misión propia con su reporte final.

g) Si tuvieran que continuar trabajando, ¿cuál sería el próximo paso?

El próximo paso sería incorporar un sistema de lectura de archivos externos como JSON o CSV para cargar las secuencias de comandos de las misiones de forma dinamica, en lugar de dejarlas definidas fijas dentro del código. Esto permitiría ejecutar diferentes secuencias de comandos sin necesidad de modificar el código fuente del programa, además de lograr la persistencia de las misiones y del historial guardándolos directamente en el disco. O desarrollar un menú interactivo en la consola que le permita al usuario ingresar comandos manualmente uno a uno en tiempo real y ver la respuesta inmediata del simulador antes de guardarlos en el historial.