class Hideout:
    def __init__(self , x , y):
        self.x = x
        self.y = y
        self.stored_treasures = {'bronze': 0, 'silver': 0, 'gold': 0}
    
    def store_treasures(self, hunter):
        for treasure_type in ['bronze', 'silver', 'gold']:
            if hunter.treasures[treasure_type] > 0:
                self.stored_treasures[treasure_type] += hunter.treasures[treasure_type]
                hunter.treasures[treasure_type] = 0
        return True