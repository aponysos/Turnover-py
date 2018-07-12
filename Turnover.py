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
cur = (0, 0)

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

        self.sprite_cur = Sprite(image='sq-cur.png', position=pos2xy(0, 0))
        self.add(self.sprite_cur)

    def on_key_press(self, key, modifiers):
        if (key == pyglet.window.key.ENTER):
            on_enter_keypress()
        elif (key == pyglet.window.key.ESCAPE):
            on_esc_keypress()
            return True
        elif (key >= pyglet.window.key.LEFT and key <= pyglet.window.key.DOWN):
            on_dir_keypress(key - pyglet.window.key.LEFT)


################################################################################################


def on_enter_keypress():
    print("on_enter_keypress")


def on_esc_keypress():
    print("on_esc_keypress")


def on_dir_keypress(dir):
    print("on_dir_keypress: %d" % dir)


################################################################################################


def init_squares():
    global max_col, max_row
    global squares, selected, cur
    squares = [[
        ST_BLACK if (not is_on_boundary(col, row)
                     and random.random() < rate) else ST_NONE
        for row in range(max_row)] for col in range(max_col)]
    selected = []
    cur = (0, 0)


def is_on_boundary(col, row):
    global max_col, max_row
    return col == 0 or col == max_col-1 or row == 0 or row == max_row-1


def pos2xy(col, row):
    global WINDOW_WIDTH, WINDOW_HEIGHT
    return (col * SQUARE_SIZE + WINDOW_PADDING, WINDOW_HEIGHT - row * SQUARE_SIZE - WINDOW_PADDING)

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
