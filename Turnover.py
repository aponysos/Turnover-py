import cocos

class Turnover(cocos.layer.Layer):
    def __init__(self):
        super(Turnover, self).__init__()

        ST_NONE = 0
        ST_BLACK = 1
        MOVES = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        SZ = 20
        PADDING = 4

        self.maxx = 5
        self.maxy = 5
        self.rate = 0.5
        self.squares = []
        self.selected = []
        self.cur = (0, 0)

        label = cocos.text.Label( \
            'Hello, world', \
            font_name='Times New Roman', \
            font_size=32, \
            anchor_x='center', anchor_y='center' \
        )
        label.position = 320, 240
        self.add(label)

    def init_squares():
        pass

cocos.director.director.init()
turnover_layer = Turnover()
main_scene = cocos.scene.Scene (turnover_layer)
cocos.director.director.run(main_scene)
