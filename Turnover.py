import cocos
import random

max_row = 6
max_col = 5
rate = 0.4

ST_NONE = 0
ST_BLACK = 1
MOVES = [(-1, 0), (0, -1), (1, 0), (0, 1)]
SZ = 20
PADDING = 4

class Turnover(cocos.layer.Layer):
    squares = []
    selected = []
    cur = (0, 0)

    def __init__(self):
        super(Turnover, self).__init__()

        self.init_squares()

        label = cocos.text.Label( \
            '\n'.join([str(row) for row in self.squares]), \
            font_name='Times New Roman', \
            font_size=32, \
            anchor_x='center', anchor_y='center', \
            multiline=True, width=240 \
        )
        label.position = 320, 240
        self.add(label)

    def init_squares(self):
        self.squares = [[ \
            ST_BLACK if (not self.is_on_boundary(row, col) and random.random() < rate) else ST_NONE \
            for col in range(max_col)] for row in range(max_row)]

    def is_on_boundary(self, row, col):
        return row == 0 or col == 0 or row == max_row-1 or col == max_col-1


cocos.director.director.init()
turnover_layer = Turnover()
main_scene = cocos.scene.Scene(turnover_layer)
cocos.director.director.run(main_scene)
