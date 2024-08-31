from collections import deque

class Estado:
    def __init__(self, misioneros, canibales, bote, camino=None):
        # Inicializa el estado con el número de misioneros y caníbales en la orilla
        # actual, la posición del bote ('izquierda' o 'derecha'), y el camino recorrido
        self.misioneros = misioneros
        self.canibales = canibales
        self.bote = bote
        self.camino = camino or []

    def es_valido(self):
        # Verifica si el estado es válido:
        # 1. Los números de misioneros y caníbales están en el rango permitido (0-3).
        # 2. No hay más caníbales que misioneros en ninguna orilla.
        if not (0 <= self.misioneros <= 3 and 0 <= self.canibales <= 3):
            return False
        if (self.misioneros and self.misioneros < self.canibales) or \
           (3 - self.misioneros and 3 - self.misioneros < 3 - self.canibales):
            return False
        return True

    def es_meta(self):
        # Verifica si el estado es la solución final del problema:
        # Todos los misioneros y caníbales están en la orilla derecha y el bote también.
        return self.misioneros == 0 and self.canibales == 0 and self.bote == 'derecha'

    def proximos_estados(self):
        # Genera todos los posibles estados futuros a partir del estado actual:
        # Los movimientos posibles incluyen 1 o 2 misioneros, 1 o 2 caníbales, o ambos.
        movimientos = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        delta_bote = -1 if self.bote == 'izquierda' else 1
        proximos = []

        for m, c in movimientos:
            m_nuevo = self.misioneros + delta_bote * m
            c_nuevo = self.canibales + delta_bote * c
            if 0 <= m_nuevo <= 3 and 0 <= c_nuevo <= 3:
                nuevo_bote = 'derecha' if self.bote == 'izquierda' else 'izquierda'
                nuevo_estado = Estado(m_nuevo, c_nuevo, nuevo_bote, self.camino + [(m, c, nuevo_bote)])
                if nuevo_estado.es_valido():
                    proximos.append(nuevo_estado)

        return proximos

    def __repr__(self):
        # Representación del estado en formato legible.
        return f"({self.misioneros}, {self.canibales}, {self.bote})"

def bfs():
    # Función que implementa la búsqueda en anchura (BFS) para encontrar la solución.
    estado_inicial = Estado(3, 3, 'izquierda')
    cola = deque([estado_inicial])  # Inicializa la cola con el estado inicial.
    visitados = set()  # Conjunto para almacenar los estados ya visitados.

    while cola:
        estado_actual = cola.popleft()  # Extrae el primer estado de la cola.

        if estado_actual.es_meta():
            # Si el estado actual es la solución, retorna el camino que lleva a él.
            return estado_actual.camino

        clave_estado = (estado_actual.misioneros, estado_actual.canibales, estado_actual.bote)
        if clave_estado in visitados:
            # Si el estado ya ha sido visitado, continúa con el siguiente estado.
            continue
        visitados.add(clave_estado)

        # Agrega todos los próximos estados válidos a la cola para su posterior exploración.
        cola.extend(estado for estado in estado_actual.proximos_estados() if (estado.misioneros, estado.canibales, estado.bote) not in visitados)

    return None

# Ejecutar BFS para encontrar la solución
solucion = bfs()

if solucion:
    # Imprime la solución encontrada
    print("Solución encontrada:")
    for paso in solucion:
        print(f"Mover {paso[0]} misionero(s) y {paso[1]} caníbal(es) a la orilla {paso[2]}.")
else:
    # Imprime un mensaje si no se encontró ninguna solución
    print("No se encontró solución.")

