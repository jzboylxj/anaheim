from suit_creator.widgets import graphics_scene


class Scene(object):

    def __init__(self):
        super().__init__()

        self.scene_width = 64000
        self.scene_height = 64000

        self.init_ui()

    def init_ui(self):
        self.gr_scene = graphics_scene.SGraphicsScene(self)
        self.gr_scene.set_scene_size(self.scene_width, self.scene_height)
