import random

class Treasure:
    def __init__(self):
        self.type = random.choices(
            ['bronze', 'silver', 'gold'],
            weights=[70, 20, 10],
            k=1
        )[0]
    
    def apply_effect(self, hunter):
        if self.type == 'bronze':
            hunter.health *= 1.03
            hunter.treasures['bronze'] += 1
        elif self.type == 'silver':
            hunter.health *= 1.07
            hunter.treasures['silver'] += 1
        elif self.type == 'gold':
            hunter.health *= 1.13
            hunter.treasures['gold'] += 1
        hunter.health = round(hunter.health, 2)