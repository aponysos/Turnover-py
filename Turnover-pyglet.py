import pyglet
from pyglet.window import key
from pyglet.graphics import *
from pyglet.gl import *
import random

max_row = 6
max_col = 5
rate = 0.4

ST_NONE = 0
ST_BLACK = 1
MOVES = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # left, up, right, down
SQUARE_SIZE = 20
PADDING = 4

window = pyglet.window.Window()

################################################################################################


def init_squares():
    global squares, selected, cur
    squares = [[
        ST_BLACK if (not is_on_boundary(col, row)
                     and random.random() < rate) else ST_NONE
        for col in range(max_col)] for row in range(max_row)]
    selected = []
    cur = (0, 0)


def is_on_boundary(col, row):
    return col == 0 or col == max_col-1 or row == 0 or row == max_row-1

################################################################################################


def draw_board():
    #draw_lines()
    draw_squares_bg([(col, row) for col in range(max_col)
                     for row in range(max_row)])
    draw_selected_and_current_squares()


def draw_lines():
    for col in range(max_col + 1):
        draw_line((col, 0), (col, max_row))
    for row in range(max_row + 1):
        draw_line((0, row), (max_col, row))


def draw_squares_bg(sq):
    for pos in sq:
        draw_bg(pos)


def draw_selected_and_current_squares():
    draw_squares_bg(selected)
    for pos in selected:
        draw_tip(pos, False)
    draw_tip(cur, True)


def draw_line(pos1, pos2):
    xy1, xy2 = pos2xy(pos1), pos2xy(pos2)
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                         ('v2i', xy1 + xy2)
                         )


def draw_bg(pos):
    xy1, xy2 = pos2xy(pos), pos2xy((pos[0]+1, pos[1]))
    xy3, xy4 = pos2xy((pos[0]+1, pos[1]+1)), pos2xy((pos[0], pos[1]+1))
    #glColor3B(0, 0, 255, 0, 255, 0)
    pyglet.graphics.draw(4, pyglet.gl.GL_POLYGON,
                         ('v2i', xy1 + xy2 + xy3 + xy4),
                         )


def draw_tip(pos, is_cur):
    pass


def pos2xy(pos):
    return (pos[0] * SQUARE_SIZE, window.height - pos[1] * SQUARE_SIZE)


################################################################################################


def on_enter_keypress():
    print("on_enter_keypress")


def on_esc_keypress():
    print("on_esc_keypress")


def on_dir_keypress(dir):
    print("on_dir_keypress: %d" % dir)


################################################################################################
init_squares()


@window.event
def on_draw():
    window.clear()
    draw_board()


@window.event
def on_key_press(symbol, modifiers):
    if (symbol == key.ENTER):
        on_enter_keypress()
    elif (symbol == key.ESCAPE):
        on_esc_keypress()
    elif (symbol >= key.LEFT and symbol <= key.DOWN):
        on_dir_keypress(symbol - key.LEFT)


################################################################################################
pyglet.app.run()
