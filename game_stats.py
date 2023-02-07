class GameStats:
    """monitorin statistic data in game"""

    def __init__(self, ai_game):
        """initializon statistic data"""
        self.settings = ai_game.settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        """ initializon dynamic statistic data """
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1

