class GameObject:
    def __init__(self, object_type, team):
        self.type = object_type
        self.team = team  # -1 means no teamable object
