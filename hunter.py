import random

class Hunter:
    def __init__(self):
        self.x = random.randint(0, 19)
        self.y = random.randint(0, 19)
        self.health = 100
        self.steps_without_health = 0
        self.carrying_treasure = None 
        self._stored_treasures = {'bronze': 0, 'silver': 0, 'gold': 0}
        self.memory = {
            'treasures': [],  
            'hideouts': []    
        }
        self.skill = random.choice(['navigation', 'endurance', 'stealth'])

    @property
    def treasures(self):
        """Public interface for accessing stored treasures"""
        return {
            'bronze': self._stored_treasures['bronze'],
            'silver': self._stored_treasures['silver'],
            'gold': self._stored_treasures['gold']
        }

    def move(self, dx, dy):
        """Move the hunter in the specified direction if healthy enough"""
        if self.health <= 0:
            return False
            
        new_x = self.x + dx
        new_y = self.y + dy
        
        if 0 <= new_x < 20 and 0 <= new_y < 20:
            self.x = new_x
            self.y = new_y
            self.health -= 2
            if self.health <= 6:
                self.seek_rest()
            return True
        return False

    def scan_area(self, grid):
        """Scan adjacent cells for treasures and hideouts"""
        directions = [(-1,-1), (-1,0), (-1,1),
                     (0,-1),          (0,1),
                     (1,-1),  (1,0), (1,1)]
        
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < 20 and 0 <= ny < 20:
                cell = grid[nx][ny]
                if cell == 'hideout' and (nx, ny) not in self.memory['hideouts']:
                    self.memory['hideouts'].append((nx, ny))
                elif cell in ['bronze', 'silver', 'gold']:
                    if not any(t[0] == nx and t[1] == ny for t in self.memory['treasures']):
                        self.memory['treasures'].append((nx, ny, cell))

    def collect_treasure(self, grid):
        """Collect treasure from current cell if available"""
        if self.carrying_treasure is None and grid[self.x][self.y] in ['bronze', 'silver', 'gold']:
            self.carrying_treasure = grid[self.x][self.y]
            grid[self.x][self.y] = None
            self.memory['treasures'] = [t for t in self.memory['treasures'] 
                                      if t[0] != self.x or t[1] != self.y]

    def deposit_treasure(self, grid):
        """Deposit carried treasure at a hideout"""
        if self.carrying_treasure is not None and grid[self.x][self.y] == 'hideout':
            self._stored_treasures[self.carrying_treasure] += 1
            self.carrying_treasure = None

    def seek_rest(self):
        """Move toward nearest hideout when health is critical"""
        if not self.memory['hideouts']:
            return 
        closest = min(self.memory['hideouts'], 
                     key=lambda h: abs(h[0]-self.x) + abs(h[1]-self.y))
        dx = 1 if closest[0] > self.x else -1 if closest[0] < self.x else 0
        dy = 1 if closest[1] > self.y else -1 if closest[1] < self.y else 0
        
        self.move(dx, dy)

    def rest(self):
        """Recover health while at a hideout"""
        self.health = min(100, self.health + 1)

    def update(self, grid):
        """Perform one simulation step update"""
        if self.health <= 0:
            self.steps_without_health += 1
            if self.steps_without_health > 3:
                return False
            return True
        self.scan_area(grid)
        if self.carrying_treasure is not None:
            if grid[self.x][self.y] == 'hideout':
                self.deposit_treasure(grid)
            else:
                self.seek_hideout()
        else:
            if grid[self.x][self.y] in ['bronze', 'silver', 'gold']:
                self.collect_treasure(grid)
            else:
                self.explore()
        if self.health <= 6 and grid[self.x][self.y] == 'hideout':
            self.rest()
            
        return True

    def seek_hideout(self):
        """Move toward nearest hideout when carrying treasure"""
        self.seek_rest()

    def explore(self):
        """Move randomly to explore the grid"""
        dx, dy = random.choice([(0,1), (1,0), (0,-1), (-1,0)])
        self.move(dx, dy)
