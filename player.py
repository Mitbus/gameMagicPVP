import game.magic


class Player:  # Users constant (not a playable hero)
    def __init__(self, type, team, hp, dmg, mp1, mp2, mp3):
        self.type = type
        self.team = team
        self.hp = hp
        self.dmg = dmg
        self.mp1 = mp1
        self.mp2 = mp2
        self.mp3 = mp3

    def cast_magic(self, craft_ingridients, light_or_dark, ench_or_invoke, field, target_tile):
        # if you can cast it
        if craft_ingridients[0] <= self.mp1 and craft_ingridients[1] <= self.mp2:
            if light_or_dark == "dark" and ench_or_invoke == ("ench", 1) and craft_ingridients == (1, 1, 1):
                game.Magic.test(field, target_tile)

    def get_dmg_is_dead(self, dmg):  # returns true if dead
        self.hp -= dmg
        return self.hp <= 0
