import game.gameObject as gobj
import math


class GameField:
    def __init__(self, size_x, size_y):
        self.map = []
        for i in range(size_x):
            map_y = []
            for j in range(size_y):
                map_y.append(gobj.GameObject("Empty", -1))
            self.map.append(map_y)
        self.game_status = ""
        self.pos = None

    def get_field_size(self):  # x, y value
        return len(self.map), len(self.map[0])

    def set_clicked_pos(self, pos):
        self.pos = pos

    def get_clicked_pos(self):
        return self.pos

    def get_clicked_obj(self):
        if self.pos is None:
            return None
        else:
            return self.map[self.pos[0]][self.pos[1]]

    def move_person(self, from_tile, to_tile):
        if self.map[to_tile[0]][to_tile[1]].type == "Empty":  # Here person can stay
            self.map[to_tile[0]][to_tile[1]] = self.map[from_tile[0]][from_tile[1]]
            self.map[from_tile[0]][from_tile[1]] = gobj.GameObject("Empty", -1)  # Last status
            return True
        else:
            return False

    @staticmethod
    def near_tiles(first_pos, second_pos):
        if first_pos[1] == second_pos[1] and math.fabs(first_pos[0] - second_pos[0]) == 1:
            return True
        if math.fabs(first_pos[1] - second_pos[1]) == 1 and first_pos[0] == second_pos[0]:
            return True
        if math.fabs(first_pos[1] - second_pos[1]) == 1 and \
                (first_pos[1] % 2 if first_pos[0] + 1 == second_pos[0] else first_pos[0] - 1 == second_pos[0]):
            return True
        return False


