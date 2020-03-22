class GameObject:
    def __init__(self, object_type, placed_item, stayable_type):
        self.field_type = object_type
        self.placed_item = placed_item
        self.stayable_type = stayable_type
        self.hero = None

    def set_hero(self, hero):
        self.hero = hero
