class Settings:
    """Class for store all settings for game Aliens attack"""

    def __init__(self):
        """initiate game settings"""
        # screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)


        self.ship_limit = 2
        self.score_scale = 1.5
        self.bullet_width = 10
        self.bullet_height = 15
        self.bullet_color = (250, 0, 0)
        self.bullets_allowed = 3


        self.fleet_drop_speed = 2
        # if this parameter will be -1 it means that fleet will change movement to left

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_setting()

    def initialize_dynamic_setting(self):
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0


        self.fleet_direction = 1



        self.alien_point = 50

    def increase_speed(self):

        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_point = int(self.alien_point * self.score_scale)
