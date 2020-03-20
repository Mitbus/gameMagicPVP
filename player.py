class Player:  # Users constant (not a playable hero)
    def __init__(self, team_color, hp, bp, max_bp, mp1, mp2, mp3):
        self.team = team_color
        self.hp = hp
        self.bp = bp
        self.max_bp = max_bp
        self.mp1 = mp1
        self.mp2 = mp2
        self.mp3 = mp3
