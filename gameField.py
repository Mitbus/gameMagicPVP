import game.gameObject as gobj
import math


class WrongFieldSizeException(Exception):
    pass


class GameField:
    def __init__(self, size_x, size_y, field_type):
        self.map = []
        for i in range(size_x):
            map_y = []
            for j in range(size_y):
                map_y.append(gobj.GameObject("Empty", None, stayable_type=True))
            self.map.append(map_y)
        self.game_status = ""
        self.pos = None
        self.field_type = field_type
        if field_type == "hex":
            if size_y != size_x or size_x % 2 == 0:
                raise WrongFieldSizeException
            radius = int(size_x / 2)
            print(radius)
            for i in range(size_x):
                for j in range(size_y):
                    dist = GameField.tiles_dist((i, j), (radius, radius))
                    if dist > radius:
                        self.map[i][j].field_type = "No tile"
                        self.map[i][j].stayable_type = False



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
        if self.map[to_tile[0]][to_tile[1]].stayable_type and self.map[to_tile[0]][to_tile[1]].hero is None:  # Here person can stay
            self.map[to_tile[0]][to_tile[1]].hero = self.map[from_tile[0]][from_tile[1]].hero
            self.map[from_tile[0]][from_tile[1]].hero = None  # Last status
            return True
        else:
            return False

    @staticmethod
    def near_tiles(first_pos, second_pos):
        if first_pos[1] == second_pos[1] and math.fabs(first_pos[0] - second_pos[0]) == 1:
            return True
        if math.fabs(first_pos[1] - second_pos[1]) == 1 and first_pos[0] == second_pos[0]:
            return True
        if math.fabs(first_pos[1] - second_pos[1]) == 1:
            if first_pos[1] % 2 and first_pos[0] + 1 == second_pos[0]:
                return True
            if not first_pos[1] % 2 and first_pos[0] - 1 == second_pos[0]:
                return True
        return False

    @staticmethod
    def tiles_route(first_pos, second_pos):
        route = [first_pos]
        if first_pos == second_pos:
            return route
        cur_pos = first_pos
        while not GameField.near_tiles(cur_pos, second_pos):
            dx = second_pos[0] - cur_pos[0]
            if math.fabs(second_pos[1] - cur_pos[1]) % 2:
                if cur_pos[1] % 2:
                    dx -= 0.5
                else:
                    dx += 0.5
            dy = (second_pos[1] - cur_pos[1]) * 0.75
            if dy == 0:
                if dx > 0:
                    cur_pos = (cur_pos[0] + 1, cur_pos[1])
                else:
                    cur_pos = (cur_pos[0] - 1, cur_pos[1])
            else:
                ctg = dx / dy
                if dy > 0:
                    if ctg >= math.sqrt(3):
                        cur_pos = (cur_pos[0] + 1, cur_pos[1])
                    elif ctg <= -math.sqrt(3):
                        cur_pos = (cur_pos[0] - 1, cur_pos[1])
                    elif ctg >= 0:
                        if cur_pos[1] % 2:
                            cur_pos = (cur_pos[0] + 1, cur_pos[1] + 1)
                        else:
                            cur_pos = (cur_pos[0], cur_pos[1] + 1)
                    else:
                        if cur_pos[1] % 2:
                            cur_pos = (cur_pos[0], cur_pos[1] + 1)
                        else:
                            cur_pos = (cur_pos[0] - 1, cur_pos[1] + 1)
                else:
                    if ctg >= math.sqrt(3):
                        cur_pos = (cur_pos[0] - 1, cur_pos[1])
                    elif ctg <= -math.sqrt(3):
                        cur_pos = (cur_pos[0] + 1, cur_pos[1])
                    elif ctg >= 0:
                        if cur_pos[1] % 2:
                            cur_pos = (cur_pos[0], cur_pos[1] - 1)
                        else:
                            cur_pos = (cur_pos[0] - 1, cur_pos[1] - 1)
                    else:
                        if cur_pos[1] % 2:
                            cur_pos = (cur_pos[0] + 1, cur_pos[1] - 1)
                        else:
                            cur_pos = (cur_pos[0], cur_pos[1] - 1)
            route.append(cur_pos)
        route.append(second_pos)
        return route

    @staticmethod
    def tiles_dist(first_pos, second_pos):
        return len(GameField.tiles_route(first_pos, second_pos)) - 1





