import game.gameObject as gobj


class GameField:
    def __init__(self, size_x, size_y):
        self.map = []
        for i in range(size_x):
            map_y = []
            for j in range(size_y):
                map_y.append(gobj.GameObject("Empty"))
            self.map.append(map_y)
        self.map[0][0] = gobj.GameObject("Player")

    def get_field_size(self):  # x, y value
        return len(self.map), len(self.map[0])
