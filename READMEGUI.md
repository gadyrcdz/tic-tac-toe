# Gato · Visualizador Minimax

Juego de Gato (Tic-Tac-Toe) con visualización interactiva del árbol de decisiones Minimax, construido con Python y Pygame.

---

## Requisitos

- Python 3.8 o superior
- Pygame

```bash
pip install pygame
```

---

## Estructura de archivos

```
├── gui.py        # Interfaz gráfica (este archivo es el punto de entrada)
├── minimax.py    # Algoritmo Minimax (min_value, max_value, ai_play)
├── utils.py      # Lógica del juego (tablero, jugadores, acciones, utilidad)
└── README.md
```

---

## Cómo ejecutar

```bash
python visualizador.py
```

---

## Cómo jugar

### 1. Pantalla de inicio

Al abrir el programa verás dos botones:

- **Jugar como X** — tú mueves primero (X siempre abre la partida)
- **Jugar como O** — la IA abre con X y tú respondes como O

### 2. Pantalla de juego

La ventana se divide en dos paneles:

**Panel izquierdo — Tablero**

- Haz clic en cualquier celda vacía para colocar tu ficha.
- La IA responde automáticamente después de tu movimiento.
- El juego indica de quién es el turno en la parte superior.
- Al terminar la partida se resalta la línea ganadora (o se muestra "Empate").
- El botón **Nuevo juego** te regresa a la pantalla de inicio.

**Panel derecho — Árbol Minimax**

Muestra el árbol de decisiones que la IA genera a partir del estado actual del tablero. Cada nodo representa un posible estado futuro del juego.

---

## El árbol Minimax

### ¿Qué significa cada nodo?

Cada nodo contiene:

- **Valor minimax** (+1, 0, -1) en la parte superior
- **Mini-tablero** con el estado del juego en ese punto
- **Acción** que llevó a ese estado (coordenada fila, columna), mostrada encima del nodo

### Colores de los nodos

| Color | Significado |
|-------|-------------|
| Azul oscuro | Turno de X — nodo MAX (X intenta maximizar) |
| Rojo oscuro | Turno de O — nodo MIN (O intenta minimizar) |
| Verde oscuro | Estado terminal — X gana (+1) |
| Rojo intenso | Estado terminal — O gana (-1) |
| Gris | Estado terminal — Empate (0) |

### Colores de las aristas

| Color | Significado |
|-------|-------------|
| Gris | Movimiento posible |
| Verde | Mejor movimiento — el camino que la IA elige |

### Valores minimax

- **+1** — X gana en esa rama
- **0** — empate en esa rama
- **-1** — O gana en esa rama

---

## Control de profundidad

En la parte inferior del panel izquierdo hay un **slider de profundidad** (1 a 4).

- **Profundidad 1** — solo se muestran los movimientos inmediatos disponibles
- **Profundidad 2** — se muestran dos niveles de decisiones
- **Profundidad 3 / 4** — árbol más completo; puede volverse muy ancho al inicio de la partida

Los nodos que llegan al límite de profundidad sin ser terminales muestran el valor minimax calculado internamente (aunque no se expandan visualmente).

Arrastra el slider mientras juegas para explorar distintos niveles del árbol.

---

## Navegación del árbol

| Acción | Efecto |
|--------|--------|
| Rueda del ratón (en panel derecho) | Scroll vertical |
| Shift + Rueda del ratón | Scroll horizontal |

Las barras de scroll finas en los bordes del panel indican la posición actual.

---


