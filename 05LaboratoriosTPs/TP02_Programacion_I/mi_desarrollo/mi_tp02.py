# =====================================================================
#  TP02 - Programacion I
#  Controlador de misiones
#
#  ESTE ES EL ARCHIVO DONDE ESCRIBIS TU PROGRAMA.
#
#  Antes de ejecutarlo:
#    1. Abri INICIAR_SIMULADOR (elegi G1 o Go2)
#    2. Espera a que aparezca la ventana con el robot
#    3. Recien ahi ejecuta este archivo
#
#  Nombre y apellido:  .....................................
#  Comision:           .....................................
# =====================================================================

from robot import ErrorDeSeguridad, Robot

from misiones import MISION_BASICA, MISION_CON_ERRORES, MISION_CUADRADO

MISION_PROPIA_INVALIDA= [
    ("avanzar", 0.15, 2.0),       # Válido
    ("girar", 0.4, 1.5),          # Válido
    ("volar", 0.8, 2.0),          # INVÁLIDO (Comando desconocido)
    ("avanzar", 0.1, 1.0),        # Válido
    ("girar", 0.8, 3.0),          # INVÁLIDO (Ángulo 0.8 > 0.5 rad/s)
    ("saludo",),                  # Válido
    ("detenerse",)                # Válido
]

MISION_PROPIA_VALIDA = [
    ("avanzar", 0.15, 2.0),   # Avanza 2s a velocidad moderada
    ("girar", 0.3, 1.5),      # Gira a la izquierda 1.5s
    ("avanzar", 0.1, 3.0),    # Avanza 3s a velocidad baja
    ("girar", -0.3, 1.5),     # Gira a la derecha (signo negativo) 1.5s
    ("saludo",),              # Ejecuta pose de saludo
    ("detenerse",)            # Se detiene s
]
# =====================================================================
# CONSTANTES GLOBALES
# =====================================================================
VELOCIDAD_MAX = 0.2    # m/s
ANGULO_MAX = 0.5       # radianes/s
BATERIA_MIN = 15       # Porcentaje mínimo
COMANDOS_VALIDOS = ("avanzar", "girar", "detenerse", "saludo")
TIEMPO_MAX= 10.0
# =====================================================================
#  PARTE 1 - Validar un comando
# =====================================================================
def comando_es_valido(comando):
    """Decide si un comando se puede ejecutar. Devuelve True o False.

    Un comando es una tupla. El primer elemento dice que hacer:

        ("avanzar", velocidad, tiempo)    velocidad en m/s, tiempo en s
        ("girar", velocidad, tiempo)      velocidad en rad/s, tiempo en s
        ("detenerse",)
        ("saludar",)

    Cosas que conviene revisar:
      - que la tupla no este vacia
      - que el nombre del comando sea uno de los cuatro validos
      - que tenga la cantidad de datos que corresponde
        (avanzar y girar llevan dos; detenerse y saludar, ninguno)
      - que velocidad y tiempo sean numeros de verdad, no textos
      - que el tiempo no sea negativo
    """
    # TU CODIGO ACA
    pass
   
    # Que no esté vacía y sea tupla o lista
    if not isinstance(comando, (tuple, list)) or len(comando) == 0:
        return False

    tipo = comando[0]

    # Que el nombre del comando sea uno de los cuatro válidos
    if tipo not in COMANDOS_VALIDOS:
        return False

    # Validar "avanzar" ("avanzar", velocidad, tiempo)
    if tipo == "avanzar":
        if len(comando) < 3:
            return False
        velocidad, tiempo = comando[1], comando[2]
        if not (isinstance(velocidad, (int, float)) and isinstance(tiempo, (int, float))):
            return False
        if not (0 < velocidad <= VELOCIDAD_MAX and tiempo > 0):
            return False

    # Validar "girar" -> ("girar", velocidad, tiempo)
    elif tipo == "girar":
        if len(comando) < 3:
            return False
        vel_angular, tiempo = comando[1], comando[2]
        if not (isinstance(vel_angular, (int, float)) and isinstance(tiempo, (int, float))):
            return False
        if not (abs(vel_angular) <= ANGULO_MAX and tiempo > 0):
            return False

    # Validar "detenerse" y "saludo" (o "saludar")
    elif tipo in ("detenerse", "saludo", "saludar"):
        if len(comando) != 1:
            return False

    return True

# =====================================================================
#  PARTE 2 - Ejecutar un comando
# =====================================================================
def ejecutar_comando(robot, comando):
    """Ejecuta UN comando en el robot. Devuelve un texto con lo que paso.

    Ordenes que podes usar:

        robot.avanzar(velocidad=..., tiempo=...)
        robot.girar(velocidad=..., tiempo=...)
        robot.detenerse()
        robot.saludar()

    Ojo: aunque el comando parezca valido, el robot puede rechazarlo
    igual (por ejemplo, si la velocidad supera el limite de la materia).
    Eso llega como un ErrorDeSeguridad y conviene atraparlo.
    """
    # TU CODIGO ACA
    tipo = comando[0]

    # 1. Caso Avanzar: ("avanzar", velocidad, tiempo)
    if tipo == "avanzar":
        velocidad, tiempo = comando[1], comando[2]
        robot.avanzar(velocidad, tiempo)

    # 2. Caso Girar: ("girar", vel_angular, tiempo)
    elif tipo == "girar":
        vel_angular, tiempo = comando[1], comando[2]
        robot.girar(vel_angular, tiempo)

    # 3. Caso Detenerse: ("detenerse",)
    elif tipo == "detenerse":
        robot.detenerse()

    # 4. Caso Saludo / Saludar: ("saludo",) o ("saludar",)
    elif tipo in ("saludo", "saludar"):
        robot.saludar()

    return True


# =====================================================================
#  PARTE 3 - Recorre la mision entera
# =====================================================================
import time

def ejecutar_mision(robot, mision, historial):
    """Recorre la lista de comandos, uno por uno.

    Por cada comando:
      - si NO es valido, lo rechaza y sigue con el siguiente
      - si es valido, lo ejecuta
      - en los dos casos, guarda en 'historial' que fue lo que paso

    Un comando invalido NO tiene que cortar la mision.
    """
    # TU CODIGO ACA
    pass
    print(f"\n=== Iniciando misión: {len(mision)} comando(s) ===")
    inicio = time.time()

    for cmd in mision:
        tipo = cmd[0]
        params = cmd[1:] if len(cmd) > 1 else ()

        # Validacion y ejecucion
        if comando_es_valido(cmd):
            ejecutar_comando(robot, cmd)
            historial.append({"comando": cmd, "ejecutado": True, "motivo": "OK"})
            print(f" [OK] {tipo} ejecutado correctamente")
        else:
            historial.append({"comando": cmd, "ejecutado": False, "motivo": "Inválido"})
            print(f" [OMITIDO] {tipo}: Parámetros fuera de rango o comando desconocido")

    # duración total
    duracion_total = round(time.time() - inicio, 2)
    historial.append({"_duracion": duracion_total})
    print(f"=== Misión finalizada ({duracion_total}s) ===\n")

# =====================================================================
#  PARTE 4 - El reporte final
# =====================================================================
def generar_reporte(historial):
    """Muestra por pantalla un resumen de la mision.

    Tiene que decir, como minimo:
      - cuantos comandos se ejecutaron bien
      - cuantos se rechazaron
      - cual fue el motivo de cada rechazo
    """
    # TU CODIGO ACA
    pass
    ejecutados = sum(1 for r in historial if r.get("ejecutado"))
    omitidos = sum(1 for r in historial if "comando" in r and not r.get("ejecutado"))
    
    # 2. Calcula la distancia total recorrida (velocidad * tiempo solo en los ejecutados)
    distancia = 0.0
    for r in historial:
        if r.get("ejecutado") and isinstance(r.get("comando"), (tuple, list)):
            cmd = r["comando"]
            if cmd[0] == "avanzar" and len(cmd) >= 3:
                velocidad, tiempo = cmd[1], cmd[2]
                distancia += velocidad * tiempo
                
    distancia = round(distancia, 2)
    
    # 3. Obtiene la duración guardada en la clave _duracion
    duracion = next((r["_duracion"] for r in historial if "_duracion" in r), 0)
    
    # 4. Impresión del reporte
    print("=" * 35)
    print("        REPORTE DE MISIÓN")
    print("=" * 35)
    print(f" Comandos recibidos : {ejecutados + omitidos}")
    print(f" Comandos ejecutados: {ejecutados}")
    print(f" Comandos omitidos  : {omitidos}")
    print(f" Distancia recorrida: {distancia} m")
    print(f" Duración estimada  : {duracion} s")
    print("=" * 35)

# =====================================================================
#  PROGRAMA PRINCIPAL
# =====================================================================
def main():
    robot = Robot()
    robot.conectar()

    historial = []

    try:
        # Empeza probando con MISION_BASICA.
        # Cuando funcione, proba con MISION_CON_ERRORES: esa tiene
        # comandos invalidos a proposito.
        ejecutar_mision(robot, MISION_PROPIA_VALIDA, historial)
        generar_reporte(historial)
    finally:
        robot.detenerse()
        robot.desconectar()


if __name__ == "__main__":
    main()
