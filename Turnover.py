import pyglet
import cocos
from cocos.director import director
from cocos.scene import Scene
from cocos.sprite import Sprite
import random

max_row = 6
max_col = 4
rate = 0.4

squares = []
selected = []
cur_col, cur_row = (0, 0)

ST_NONE = 0
ST_BLACK = 1
MOVES = [(-1, 0), (0, -1), (1, 0), (0, 1)]  # left, up, right, down

WINDOW_WIDTH = 0
WINDOW_HEIGHT = 0
WINDOW_PADDING = 100
SQUARE_SIZE = 20
SQUARE_PADDING = 4

################################################################################################


class BackgroundLayer(cocos.layer.ColorLayer):
    def __init__(self):
        super(BackgroundLayer, self).__init__(r=255, g=255, b=255, a=255)


class SquaresLayer(cocos.layer.Layer):
    def __init__(self):
        super(SquaresLayer, self).__init__()

        for col, row in [(col, row) for col in range(max_col) for row in range(max_row)]:
            if squares[col][row] == ST_BLACK:
                image_file = 'sq-black.png'
            else:
                image_file = 'sq-white.png'
            sprite = Sprite(image=image_file, position=pos2xy(col, row))
            self.add(sprite)


class TipsLayer(cocos.layer.Layer):
    def __init__(self):
        super(TipsLayer, self).__init__()
        self.is_event_handler = True

        self.sprite_cur = None
        self.sprite_selected = []
        self.update_tips()

    def on_key_press(self, key, modifiers):
        if (key == pyglet.window.key.ENTER):
            on_enter_keypress()
        elif (key == pyglet.window.key.ESCAPE):
            on_esc_keypress()
        elif (key >= pyglet.window.key.LEFT and key <= pyglet.window.key.DOWN):
            on_dir_keypress(key)

        self.update_tips()

        if key == pyglet.window.key.ESCAPE:
            return True

    def update_tips(self):
        for sp in self.sprite_selected:
            self.remove(sp)

        self.sprite_selected = []
        for s in selected:
            sprite = Sprite(image='sq-sel.png', position=pos2xy(s[0], s[1]))
            self.sprite_selected.append(sprite)
            self.add(sprite)

        if self.sprite_cur != None:
            self.remove(self.sprite_cur)
        self.sprite_cur = Sprite(
            image='sq-cur.png', position=pos2xy(cur_col, cur_row))
        self.add(self.sprite_cur)

################################################################################################


def on_enter_keypress():
    print("on_enter_keypress")

    if (is_selecting()):
        if (is_done()):
            pass
    else:
        selected.append((cur_col, cur_row))


def on_esc_keypress():
    print("on_esc_keypress")

    cancel_selecting()


def on_dir_keypress(key):
    print("on_dir_keypress: %d" % key)

    global cur_col, cur_row
    dir = key - pyglet.window.key.LEFT
    next_col = cur_col + MOVES[dir][0]
    next_row = cur_row + MOVES[dir][1]

    if (not check_bound(next_col, next_row)):
        return

    if (is_selecting()):
        i = index_of_selected(next_col, next_row)
        if i < 0:
            selected.append((next_col, next_row))
        elif i == len(selected) - 2:
            selected.pop()
        else:
            return

    cur_col, cur_row = next_col, next_row


################################################################################################


def init_squares():
    global max_col, max_row
    global squares, selected, cur_col, cur_row
    squares = [[
        ST_BLACK if (not is_on_boundary(col, row)
                     and random.random() < rate) else ST_NONE
        for row in range(max_row)] for col in range(max_col)]
    selected = []
    cur_col, cur_row = (0, 0)


def check_bound(col, row):
    global max_col, max_row
    return col >= 0 and col < max_col and row >= 0 and row < max_row


def is_on_boundary(col, row):
    global max_col, max_row
    return col == 0 or col == max_col-1 or row == 0 or row == max_row-1


def pos2xy(col, row):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    return (col * SQUARE_SIZE + WINDOW_PADDING, WINDOW_HEIGHT - row * SQUARE_SIZE - WINDOW_PADDING)


def is_selecting():
    global selected
    return len(selected) > 0


def cancel_selecting():
    global selected
    selected = []


def is_done():
    return False


def index_of_selected(col, row):
    for i, s in enumerate(selected):
        if (col == s[0] and row == s[1]):
            return i
    return -1

################################################################################################


def main():
    director.init()
    global WINDOW_WIDTH, WINDOW_HEIGHT
    WINDOW_WIDTH, WINDOW_HEIGHT = director.get_window_size()

    init_squares()

    background_layer = BackgroundLayer()
    squares_layer = SquaresLayer()
    tips_layer = TipsLayer()

    main_scene = Scene(background_layer, squares_layer, tips_layer)
    director.run(main_scene)


if __name__ == '__main__':
    main()
