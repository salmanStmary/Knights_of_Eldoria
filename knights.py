import random
import math

class Knight:
    def __init__(self, x=None, y=None):
        self.x = x if x is not None else random.randint(0, 19)
        self.y = y if y is not None else random.randint(0, 19)
        self.energy = 100
        self.target_hunter = None
        self.garrisons = []
        self.resting = False
        self.active = True

    def scan_for_hunters(self, hunters):
        """Scan 3-cell radius for hunters and select target"""
        if self.energy <= 20 or self.resting or not self.active:
            return

        nearby_hunters = []
        for hunter in hunters:
            distance = math.sqrt((hunter.x - self.x)**2 + (hunter.y - self.y)**2)
            if distance <= 4:
                nearby_hunters.append((distance, hunter))
        
        if nearby_hunters:
            nearby_hunters.sort()
            self.target_hunter = nearby_hunters[0][1]

    def pursue(self, hunters):
        """Move toward target hunter"""
        if not self.target_hunter or self.energy <= 0 or self.resting or not self.active:
            return False

        dx = 1 if self.target_hunter.x > self.x else -1 if self.target_hunter.x < self.x else 0
        dy = 1 if self.target_hunter.y > self.y else -1 if self.target_hunter.y < self.y else 0
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        if 0 <= new_x < 20 and 0 <= new_y < 20:
            self.x = new_x
            self.y = new_y
            self.energy -= 20
            if self.x == self.target_hunter.x and self.y == self.target_hunter.y:
                self.confront_hunter(self.target_hunter)
                self.target_hunter = None
            if self.energy <= 20:
                self.retreat_to_garrison()
            
            return True
        return False

    def confront_hunter(self, hunter):
        """Either detain or challenge the caught hunter"""
        action = random.choice(['detain', 'challenge'])
        
        if action == 'detain':
            hunter.health = max(0, hunter.health - 5)
            if hunter.carrying_treasure:
                self.remember_dropped_treasure(hunter)
        else:
            hunter.health = max(0, hunter.health - 20)
            if hunter.carrying_treasure:
                self.remember_dropped_treasure(hunter)

    def remember_dropped_treasure(self, hunter):
        """Helper to handle dropped treasure memory"""
        if 'dropped_treasures' not in hunter.memory:
            hunter.memory['dropped_treasures'] = []
        hunter.memory['dropped_treasures'].append(
            (hunter.x, hunter.y, hunter.carrying_treasure))
        hunter.carrying_treasure = None

    def retreat_to_garrison(self):
        """Move toward nearest garrison"""
        if not self.garrisons:
            return
            
        closest = min(self.garrisons, 
                     key=lambda g: abs(g[0]-self.x) + abs(g[1]-self.y))
        
        dx = 1 if closest[0] > self.x else -1 if closest[0] < self.x else 0
        dy = 1 if closest[1] > self.y else -1 if closest[1] < self.y else 0
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        if 0 <= new_x < 20 and 0 <= new_y < 20:
            self.x = new_x
            self.y = new_y

    def rest(self):
        """Recover energy at garrison"""
        if self.resting:
            self.energy = min(100, self.energy + 10)
            if self.energy == 100:
                self.resting = False

    def scan_for_garrisons(self, hideouts):
        """Remember hideout locations as garrisons"""
        for hideout in hideouts:
            if (hideout.x, hideout.y) not in self.garrisons:
                self.garrisons.append((hideout.x, hideout.y))

    def update(self, hunters, hideouts):
        """Perform one simulation step"""
        self.scan_for_garrisons(hideouts)
        
        if any((self.x, self.y) == (h.x, h.y) for h in hideouts):
            self.resting = True
            self.rest()
            return
        
        self.resting = False
        self.scan_for_hunters(hunters)
        
        if self.target_hunter:
            self.pursue(hunters)
        elif self.energy <= 20:
            self.retreat_to_garrison()
        else:
            self.patrol()

    def patrol(self):
        """Random movement when idle"""
        dx, dy = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
        new_x = self.x + dx
        new_y = self.y + dy
        
        if 0 <= new_x < 20 and 0 <= new_y < 20:
            self.x = new_x
            self.y = new_y