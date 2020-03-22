import game.magic


class Player:  # Users constant (not a playable hero)
    def __init__(self, type, team, hp, mp1, mp2, mp3):
        self.type = type
        self.team = team
        self.hp = hp
        self.mp1 = mp1
        self.mp2 = mp2
        self.mp3 = mp3

    def cast_magic(self, craft_ingridients, light_or_dark, ench_or_invoke, field, target_tile):
        # if you can cast it
        if self.bp > 0:
            self.bp -= 1
            if light_or_dark == "dark" and ench_or_invoke == ("ench", 1) and craft_ingridients == (1, 1, 1):
                game.Magic.test(field, target_tile)
