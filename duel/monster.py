
class Monster:
    #Todo: Load level and scaling dependent stats found in the database and primar_name
    def __init__(self, primar_stats, level):
        self.primar_name
        self.level = level
        self.scale
        self.max_health_points
        self.health_points
        self.powers
        self.experience_boundary
        self.current_experience

    #Todo: Load current pre-created monster in database
    def __init__(self, monster):
        self.primar_name
        self.level
        self.scale
        self.max_health_points
        self.health_points
        self.powers
        self.experience_boundary
        self.current_experience

def is_alive(self):
        return self.health_points

def need_to_level_up(self):
    return self.current_experience >= self.experience_boundary

def level_up(self):
    while self.need_to_level_up():
        self.level += 1
        self.current_experience = self.experience_boundary - self.current_experience
        self.update_stats()

def update_stats(self):
    #Todo: add rescaling state
    pass