import game.magic


class Player:  # Users constant (not a playable hero)
    def __init__(self, hero_type, team, hp, dmg, mp_destroy, mp_illusion, mp_call, mp_heal):
        self.type = hero_type
        self.team = team
        self.hp = hp
        self.dmg = dmg
        self.mp_destroy = mp_destroy
        self.mp_illusion = mp_illusion
        self.mp_call = mp_call
        self.mp_heal = mp_heal

    def cast_magic(self, craft_ingridients, light_or_dark, ench_or_invoke, field, target_tile):
        # if you can cast it
        if craft_ingridients[0] <= self.mp_destroy and craft_ingridients[1] <= self.mp_illusion:
            if light_or_dark == "dark" and ench_or_invoke == ("ench", 1) and craft_ingridients == (1, 1, 0, 0):
                game.Magic.test(field, target_tile)

    def get_dmg_is_dead(self, dmg):  # returns true if dead
        self.hp -= dmg
        return self.hp <= 0
