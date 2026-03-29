"""
gui.py - Interfaz gráfica Pygame: Gato + Árbol Minimax
Ejecutar: python gui.py   |   Requiere: pip install pygame

Mejoras del árbol:
  - Tamaño calculado de abajo hacia arriba (leaf-up): cada nodo
    ocupa exactamente el espacio que sus hijos necesitan.
  - Canvas virtual ilimitado con scroll X+Y (rueda / Shift+rueda).
  - Mini-tablero integrado dentro de cada nodo.
  - Slider para controlar la profundidad visible (1-4).
"""

import pygame
import sys
import math
from utils import terminal, result, actions, players, utility, PLAYER_X, PLAYER_O
from minimax import ai_play, min_value, max_value


def get_winner(board):
    if not terminal(board):
        return None
    u = utility(board)
    if u == 1:  return PLAYER_X
    if u == -1: return PLAYER_O
    return None


# ══════════════════════════════════════════════════════════════
#  CONSTANTES
# ══════════════════════════════════════════════════════════════
WIN_W, WIN_H  = 1280, 720
LEFT_W        = 360
RIGHT_X       = LEFT_W
RIGHT_W       = WIN_W - LEFT_W

CELL          = 100
BOARD_X       = (LEFT_W - CELL * 3) // 2
BOARD_Y       = 170

NODE_W        = 88
NODE_H        = 74
NODE_RX       = 8
H_PAD         = 16
V_GAP         = 52
LEGEND_H      = 26

BG_L          = (15, 15, 26)
BG_R          = (11, 11, 20)
DIV           = (45, 45, 72)
GRID_C        = (55, 55, 90)
TEXT_P        = (218, 218, 238)
TEXT_M        = (100, 100, 140)

COL_X         = (99,  179, 237)
COL_O         = (252, 129, 129)
COL_WIN       = (72,  199, 142)

C_MAX         = (22,  44, 105)
C_MIN         = (105, 22,  55)
C_TX          = (18,  85,  50)
C_TO          = (115, 22,  38)
C_TD          = (42,  42,  65)
C_TRUNC       = (35,  35,  60)
BORDER_N      = (140, 140, 185)
EDGE_N        = (55,  55,  88)
EDGE_B        = (72,  199, 142)

BTN_BG        = (32,  32,  62)
BTN_HV        = (52,  52,  92)
BTN_TX        = (200, 200, 230)

SLIDER_X      = 30
SLIDER_W      = LEFT_W - 60
SLIDER_Y      = WIN_H - 110
SLIDER_H      = 6
THUMB_R       = 9
DEPTH_MIN     = 1
DEPTH_MAX     = 4


# ══════════════════════════════════════════════════════════════
#  ÁRBOL MINIMAX
# ══════════════════════════════════════════════════════════════
def build_tree(board, depth=0, max_depth=2):
    is_term = terminal(board)
    node = dict(
        board=([r[:] for r in board]), is_term=is_term,
        value=None, children=[], depth=depth,
        is_best=False, action=None, truncated=False,
        cx=0.0, cy=0.0, subtree_w=0,
    )
    if is_term:
        node["value"] = utility(board)
        return node
    if depth >= max_depth:
        cur = players(board)
        node["value"] = (max_value(board) if cur == PLAYER_X
                         else min_value(board))
        node["truncated"] = True
        return node

    cur = players(board)
    best_val = -math.inf if cur == PLAYER_X else math.inf
    best_idx = None
    for action in sorted(actions(board)):
        cb    = result(board, action)
        child = build_tree(cb, depth + 1, max_depth)
        child["action"] = action
        node["children"].append(child)
        v = child["value"]
        if v is None:
            continue
        if cur == PLAYER_X and v > best_val:
            best_val, best_idx = v, len(node["children"]) - 1
        elif cur == PLAYER_O and v < best_val:
            best_val, best_idx = v, len(node["children"]) - 1

    node["value"] = best_val
    if best_idx is not None:
        node["children"][best_idx]["is_best"] = True
    return node


def _measure(node):
    if not node["children"]:
        node["subtree_w"] = NODE_W
        return NODE_W
    total = sum(_measure(c) for c in node["children"])
    total += H_PAD * (len(node["children"]) - 1)
    node["subtree_w"] = max(total, NODE_W)
    return node["subtree_w"]


def _place(node, x_center, y_top):
    node["cx"] = x_center
    node["cy"] = y_top + NODE_H / 2
    if not node["children"]:
        return
    total_w = (sum(c["subtree_w"] for c in node["children"])
               + H_PAD * (len(node["children"]) - 1))
    x = x_center - total_w / 2
    child_y = y_top + NODE_H + V_GAP
    for c in node["children"]:
        _place(c, x + c["subtree_w"] / 2, child_y)
        x += c["subtree_w"] + H_PAD


def layout_tree(root, available_w):
    _measure(root)
    total_w = max(root["subtree_w"] + 40, available_w)
    _place(root, total_w / 2, V_GAP // 2 + 10)

    def max_y(n):
        m = n["cy"] + NODE_H / 2
        for c in n["children"]:
            m = max(m, max_y(c))
        return m

    return int(total_w), int(max_y(root)) + 24


# ══════════════════════════════════════════════════════════════
#  DIBUJO DEL ÁRBOL
# ══════════════════════════════════════════════════════════════
def val_str(v):
    if v is None: return "?"
    if v ==  1:   return "+1"
    if v == -1:   return "-1"
    return "0"


def val_color(v):
    if v ==  1: return (72,  199, 142)
    if v == -1: return (252, 100, 100)
    return (160, 160, 190)


def node_bg(node):
    if node["is_term"]:
        v = node["value"]
        return C_TX if v == 1 else (C_TO if v == -1 else C_TD)
    if node["truncated"]:
        return C_TRUNC
    return C_MAX if players(node["board"]) == PLAYER_X else C_MIN


def draw_mini_board(surf, board, rx, ry, rw, rh):
    cs = rw // 3
    for i in range(3):
        for j in range(3):
            cx = rx + j * cs + cs // 2
            cy = ry + i * cs + cs // 2
            v  = board[i][j]
            if v == PLAYER_X:
                r = cs // 2 - 2
                pygame.draw.line(surf, COL_X, (cx-r, cy-r), (cx+r, cy+r), 2)
                pygame.draw.line(surf, COL_X, (cx+r, cy-r), (cx-r, cy+r), 2)
            elif v == PLAYER_O:
                pygame.draw.circle(surf, COL_O, (cx, cy), cs // 2 - 2, 2)
    for k in range(1, 3):
        pygame.draw.line(surf, GRID_C,
            (rx + k*cs, ry), (rx + k*cs, ry + rh), 1)
        pygame.draw.line(surf, GRID_C,
            (rx, ry + k*cs), (rx + rw, ry + k*cs), 1)


def draw_edges(surf, node):
    px, py = int(node["cx"]), int(node["cy"])
    for c in node["children"]:
        cx, cy = int(c["cx"]), int(c["cy"])
        col = EDGE_B if c["is_best"] else EDGE_N
        w   = 2      if c["is_best"] else 1
        pygame.draw.line(surf, col,
            (px, py + NODE_H // 2),
            (cx, cy - NODE_H // 2), w)
        draw_edges(surf, c)


def draw_nodes(surf, node, font_val, font_act):
    cx = int(node["cx"])
    cy = int(node["cy"])
    x0 = cx - NODE_W // 2
    y0 = cy - NODE_H // 2

    bg  = node_bg(node)
    bor = EDGE_B if node["is_best"] else BORDER_N
    bw  = 2      if node["is_best"] else 1

    pygame.draw.rect(surf, bg,  (x0, y0, NODE_W, NODE_H), border_radius=NODE_RX)
    pygame.draw.rect(surf, bor, (x0, y0, NODE_W, NODE_H), bw, border_radius=NODE_RX)

    # Valor minimax (arriba)
    v  = node["value"]
    vt = font_val.render(val_str(v), True, val_color(v))
    surf.blit(vt, vt.get_rect(centerx=cx, top=y0 + 4))

    # Mini-tablero (parte inferior del nodo)
    mb_m  = 4
    mb_top = y0 + 21
    mb_sz  = NODE_W - mb_m * 2
    draw_mini_board(surf, node["board"],
                    x0 + mb_m, mb_top, mb_sz, mb_sz)

    # Acción (encima del nodo)
    if node["action"]:
        at = font_act.render(str(node["action"]), True, TEXT_M)
        surf.blit(at, at.get_rect(centerx=cx, bottom=y0 - 3))

    for c in node["children"]:
        draw_nodes(surf, c, font_val, font_act)


def draw_tree_panel(surf, root, sx, sy, cw, ch,
                    font_val, font_act, font_leg):
    pygame.draw.rect(surf, BG_R, (RIGHT_X, 0, RIGHT_W, WIN_H))
    pygame.draw.line(surf, DIV, (RIGHT_X, 0), (RIGHT_X, WIN_H), 1)

    # Leyenda fija
    items = [(C_MAX,"MAX X"), (C_MIN,"MIN O"), (C_TX,"+1 X"),
             (C_TO,"-1 O"),  (C_TD,"0 Emp"), (EDGE_B,"Mejor")]
    lx = RIGHT_X + 8
    for col, label in items:
        if lx + 80 > WIN_W:
            break
        pygame.draw.rect(surf, col, (lx, 7, 10, 10), border_radius=2)
        lt = font_leg.render(label, True, TEXT_M)
        surf.blit(lt, (lx + 13, 6))
        lx += lt.get_width() + 22

    hint = font_leg.render("Rueda=scroll vertical  |  Shift+Rueda=horizontal",
                           True, TEXT_M)
    surf.blit(hint, hint.get_rect(right=WIN_W - 8, top=6))

    if root is None:
        msg = font_leg.render(
            "Haz tu primer movimiento para ver el árbol", True, TEXT_M)
        surf.blit(msg, msg.get_rect(
            center=(RIGHT_X + RIGHT_W // 2, WIN_H // 2)))
        return

    vp_h = WIN_H - LEGEND_H
    canvas = pygame.Surface((max(cw, RIGHT_W), max(ch, vp_h)))
    canvas.fill(BG_R)
    draw_edges(canvas, root)
    draw_nodes(canvas, root, font_val, font_act)

    vp = pygame.Rect(RIGHT_X, LEGEND_H, RIGHT_W, vp_h)
    surf.set_clip(vp)
    surf.blit(canvas, (RIGHT_X - sx, LEGEND_H - sy))
    surf.set_clip(None)

    # Scrollbars
    if cw > RIGHT_W:
        ratio = RIGHT_W / cw
        bw = max(30, int(RIGHT_W * ratio))
        bx = RIGHT_X + int(sx / cw * RIGHT_W)
        pygame.draw.rect(surf, (60,60,90),
            (bx, WIN_H - 5, bw, 4), border_radius=2)
    if ch > vp_h:
        ratio = vp_h / ch
        bh = max(30, int(vp_h * ratio))
        by = LEGEND_H + int(sy / ch * vp_h)
        pygame.draw.rect(surf, (60,60,90),
            (WIN_W - 5, by, 4, bh), border_radius=2)


# ══════════════════════════════════════════════════════════════
#  TABLERO PRINCIPAL
# ══════════════════════════════════════════════════════════════
def draw_depth_slider(surf, depth_val, font):
    label = font.render(f"Profundidad árbol: {depth_val}", True, TEXT_M)
    surf.blit(label, (SLIDER_X, SLIDER_Y - 22))
    pygame.draw.rect(surf, (40,40,65),
        (SLIDER_X, SLIDER_Y, SLIDER_W, SLIDER_H), border_radius=3)
    ratio  = (depth_val - DEPTH_MIN) / (DEPTH_MAX - DEPTH_MIN)
    fill_w = int(SLIDER_W * ratio)
    pygame.draw.rect(surf, (72,120,200),
        (SLIDER_X, SLIDER_Y, fill_w, SLIDER_H), border_radius=3)
    tx = SLIDER_X + fill_w
    ty = SLIDER_Y + SLIDER_H // 2
    pygame.draw.circle(surf, (130,170,230), (tx, ty), THUMB_R)
    pygame.draw.circle(surf, (80,110,180),  (tx, ty), THUMB_R, 2)
    for d in range(DEPTH_MIN, DEPTH_MAX + 1):
        r2 = (d - DEPTH_MIN) / (DEPTH_MAX - DEPTH_MIN)
        pygame.draw.circle(surf, (60,60,90),
            (SLIDER_X + int(SLIDER_W * r2), ty), 3)


def slider_val_from_x(mx):
    ratio = max(0.0, min(1.0, (mx - SLIDER_X) / SLIDER_W))
    return round(DEPTH_MIN + ratio * (DEPTH_MAX - DEPTH_MIN))


def slider_hit(mx, my):
    ty = SLIDER_Y + SLIDER_H // 2
    return (SLIDER_X <= mx <= SLIDER_X + SLIDER_W
            and abs(my - ty) < THUMB_R + 8)


def draw_board_panel(surf, board, game_over, human_mark,
                     font_title, font_sub, font_sm, depth_val):
    pygame.draw.rect(surf, BG_L, (0, 0, LEFT_W, WIN_H))

    t = font_title.render("GATO · MINIMAX", True, TEXT_P)
    surf.blit(t, t.get_rect(center=(LEFT_W // 2, 38)))

    if game_over:
        w     = get_winner(board)
        msg   = f"¡Ganó {w}!" if w else "Empate"
        color = (COL_X if w == PLAYER_X else COL_O) if w else TEXT_M
    else:
        cur      = players(board)
        is_human = cur == human_mark
        ai_m     = PLAYER_O if human_mark == PLAYER_X else PLAYER_X
        msg      = f"Tu turno ({human_mark})" if is_human \
                   else f"IA pensando... ({ai_m})"
        color    = (COL_X if human_mark == PLAYER_X else COL_O) if is_human \
                   else (COL_X if ai_m == PLAYER_X else COL_O)

    surf.blit(font_sub.render(msg, True, color),
              font_sub.render(msg, True, color).get_rect(
                  center=(LEFT_W // 2, 80)))
    ley = font_sm.render(
        f"Tú: {human_mark}   IA: {'O' if human_mark=='X' else 'X'}",
        True, TEXT_M)
    surf.blit(ley, ley.get_rect(center=(LEFT_W // 2, 105)))

    for k in range(1, 3):
        pygame.draw.line(surf, GRID_C,
            (BOARD_X+k*CELL, BOARD_Y), (BOARD_X+k*CELL, BOARD_Y+CELL*3), 3)
        pygame.draw.line(surf, GRID_C,
            (BOARD_X, BOARD_Y+k*CELL), (BOARD_X+CELL*3, BOARD_Y+k*CELL), 3)
    pygame.draw.rect(surf, GRID_C, (BOARD_X, BOARD_Y, CELL*3, CELL*3), 2)

    for i in range(3):
        for j in range(3):
            v  = board[i][j]
            cx = BOARD_X + j*CELL + CELL//2
            cy = BOARD_Y + i*CELL + CELL//2
            if v == PLAYER_X:
                r = 30
                pygame.draw.line(surf, COL_X, (cx-r,cy-r), (cx+r,cy+r), 5)
                pygame.draw.line(surf, COL_X, (cx+r,cy-r), (cx-r,cy+r), 5)
            elif v == PLAYER_O:
                pygame.draw.circle(surf, COL_O, (cx, cy), 30, 5)

    if game_over:
        for seg in _win_segments(board):
            pygame.draw.line(surf, COL_WIN, seg[0], seg[1], 6)

    draw_depth_slider(surf, depth_val, font_sm)


def _win_segments(board):
    segs = []
    for i in range(3):
        if board[i][0] and board[i][0]==board[i][1]==board[i][2]:
            y = BOARD_Y + i*CELL + CELL//2
            segs.append(((BOARD_X+10,y),(BOARD_X+CELL*3-10,y)))
        if board[0][i] and board[0][i]==board[1][i]==board[2][i]:
            x = BOARD_X + i*CELL + CELL//2
            segs.append(((x,BOARD_Y+10),(x,BOARD_Y+CELL*3-10)))
    if board[0][0] and board[0][0]==board[1][1]==board[2][2]:
        segs.append(((BOARD_X+10,BOARD_Y+10),
                     (BOARD_X+CELL*3-10,BOARD_Y+CELL*3-10)))
    if board[0][2] and board[0][2]==board[1][1]==board[2][0]:
        segs.append(((BOARD_X+CELL*3-10,BOARD_Y+10),
                     (BOARD_X+10,BOARD_Y+CELL*3-10)))
    return segs


# ══════════════════════════════════════════════════════════════
#  PANTALLA SELECCIÓN
# ══════════════════════════════════════════════════════════════
def draw_select(surf, font_lg, font_sm, hx, ho):
    surf.fill(BG_L)
    t = font_lg.render("GATO  ·  MINIMAX", True, TEXT_P)
    surf.blit(t, t.get_rect(center=(WIN_W//2, 200)))
    s = font_sm.render("Elige tu ficha para comenzar", True, TEXT_M)
    surf.blit(s, s.get_rect(center=(WIN_W//2, 258)))

    bx = pygame.Rect(WIN_W//2-155, 300, 140, 52)
    bo = pygame.Rect(WIN_W//2+15,  300, 140, 52)
    for rect, label, hov in [(bx,"Jugar como X",hx),(bo,"Jugar como O",ho)]:
        pygame.draw.rect(surf, BTN_HV if hov else BTN_BG, rect, border_radius=8)
        pygame.draw.rect(surf, DIV, rect, 1, border_radius=8)
        lt = font_sm.render(label, True, BTN_TX)
        surf.blit(lt, lt.get_rect(center=rect.center))

    note = font_sm.render("X siempre mueve primero", True, TEXT_M)
    surf.blit(note, note.get_rect(center=(WIN_W//2, 378)))
    return bx, bo


# ══════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Gato – Visualizador Minimax")
    clock  = pygame.time.Clock()

    font_lg  = pygame.font.SysFont("segoeui", 34, bold=True)
    font_sub = pygame.font.SysFont("segoeui", 18, bold=True)
    font_sm  = pygame.font.SysFont("segoeui", 14)
    font_val = pygame.font.SysFont("segoeui", 13, bold=True)
    font_act = pygame.font.SysFont("segoeui", 10)
    font_leg = pygame.font.SysFont("segoeui", 11)

    state      = "select"
    board      = None
    human_mark = PLAYER_X
    game_over  = False
    tree_root  = None
    canvas_w   = RIGHT_W
    canvas_h   = WIN_H
    sx = sy    = 0
    ai_pending = False
    depth_val  = 1
    dragging   = False

    btn_r = pygame.Rect(LEFT_W//2 - 75, WIN_H - 50, 150, 34)

    def rebuild():
        nonlocal tree_root, canvas_w, canvas_h, sx, sy
        if board and not terminal(board):
            tree_root       = build_tree(board, max_depth=depth_val)
            canvas_w, canvas_h = layout_tree(tree_root, RIGHT_W)
            sx = sy         = 0
        else:
            tree_root = None

    while True:
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if state == "select":
                bx = pygame.Rect(WIN_W//2-155, 300, 140, 52)
                bo = pygame.Rect(WIN_W//2+15,  300, 140, 52)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if bx.collidepoint(mx, my):
                        human_mark = PLAYER_X
                        board      = [[None]*3 for _ in range(3)]
                        game_over  = False
                        state      = "playing"
                        rebuild()
                    elif bo.collidepoint(mx, my):
                        human_mark = PLAYER_O
                        board      = [[None]*3 for _ in range(3)]
                        game_over  = False
                        state      = "playing"
                        ai_pending = True

            elif state == "playing":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if btn_r.collidepoint(mx, my):
                        state = "select"; tree_root = None
                        sx = sy = 0; ai_pending = False; dragging = False
                        continue
                    if mx < LEFT_W and slider_hit(mx, my):
                        dragging = True
                    elif not game_over and not ai_pending and not dragging:
                        cur = players(board)
                        if cur == human_mark:
                            col = (mx - BOARD_X) // CELL
                            row = (my - BOARD_Y) // CELL
                            if 0 <= row < 3 and 0 <= col < 3 and board[row][col] is None:
                                board = result(board, (row, col))
                                if terminal(board):
                                    game_over = True; tree_root = None
                                else:
                                    rebuild(); ai_pending = True

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    dragging = False

                if event.type == pygame.MOUSEMOTION and dragging:
                    nv = slider_val_from_x(mx)
                    if nv != depth_val:
                        depth_val = nv; rebuild()

                if event.type == pygame.MOUSEWHEEL and mx > RIGHT_X:
                    mods = pygame.key.get_mods()
                    vp_h = WIN_H - LEGEND_H
                    if mods & pygame.KMOD_SHIFT:
                        sx = max(0, min(sx - event.y * 30,
                                        max(0, canvas_w - RIGHT_W)))
                    else:
                        sy = max(0, min(sy - event.y * 30,
                                        max(0, canvas_h - vp_h)))

        if state == "playing" and ai_pending and not game_over:
            ai_pending = False
            move = ai_play(board)
            if move:
                board = result(board, move)
            if terminal(board):
                game_over = True; tree_root = None
            else:
                rebuild()

        # ── Render ──────────────────────────────────────────
        if state == "select":
            bx = pygame.Rect(WIN_W//2-155, 300, 140, 52)
            bo = pygame.Rect(WIN_W//2+15,  300, 140, 52)
            draw_select(screen, font_lg, font_sm,
                        bx.collidepoint(mx,my), bo.collidepoint(mx,my))

        elif state == "playing":
            draw_board_panel(screen, board, game_over, human_mark,
                             font_sub, font_sub, font_sm, depth_val)

            hov = btn_r.collidepoint(mx, my)
            pygame.draw.rect(screen, BTN_HV if hov else BTN_BG,
                             btn_r, border_radius=8)
            pygame.draw.rect(screen, DIV, btn_r, 1, border_radius=8)
            screen.blit(font_sm.render("Nuevo juego", True, BTN_TX),
                        font_sm.render("Nuevo juego", True, BTN_TX)
                        .get_rect(center=btn_r.center))

            draw_tree_panel(screen, tree_root, sx, sy, canvas_w, canvas_h,
                            font_val, font_act, font_leg)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()