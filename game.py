import random
import os
from hunter import Hunter
from knights import Knight
from treasure import Treasure
from hideout import Hideout

class Game:
    def __init__(self):
        self.hunter = Hunter()
        self.grid_size = 20
        self.treasures = []
        self.hideouts = []
        self.knights = []
        self.game_over = False
        self.generate_treasures(10)
        self.generate_hideouts(4)
        self.generate_knights(4)
    
    def generate_treasures(self, count):
        for _ in range(count):
            x, y = random.randint(0, 19), random.randint(0, 19)
            while (x == self.hunter.x and y == self.hunter.y) or any(t['x'] == x and t['y'] == y for t in self.treasures):
                x, y = random.randint(0, 19), random.randint(0, 19)
            self.treasures.append({'x': x, 'y': y, 'obj': Treasure()})
    
    def generate_hideouts(self, count):
        for _ in range(count):
            x, y = random.randint(0, 19), random.randint(0, 19)
            while (x == self.hunter.x and y == self.hunter.y) or any(h.x == x and h.y == y for h in self.hideouts):
                x, y = random.randint(0, 19), random.randint(0, 19)
            self.hideouts.append(Hideout(x, y))
    
    def generate_knights(self, count):
        for _ in range(count):
            x, y = random.randint(0, 19), random.randint(0, 19)
            while (x == self.hunter.x and y == self.hunter.y) or any(k.x == x and k.y == y for k in self.knights):
                x, y = random.randint(0, 19), random.randint(0, 19)
            self.knights.append(Knight(x, y))
    
    def display(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Knights of Eldoria ===")
        print(f"Health: {self.hunter.health}%")
        print(f"Carrying: Bronze({self.hunter.treasures['bronze']}) Silver({self.hunter.treasures['silver']}) Gold({self.hunter.treasures['gold']})")
        print(f"Stored: Bronze({sum(h.stored_treasures['bronze'] for h in self.hideouts)}) "
              f"Silver({sum(h.stored_treasures['silver'] for h in self.hideouts)}) "
              f"Gold({sum(h.stored_treasures['gold'] for h in self.hideouts)})")
        print(f"Knights remaining: {len([k for k in self.knights if k.active])}")
        print("Use WASD to move, Q to quit, H to store treasures in hideout")
        print()
        
        for y in range(self.grid_size):
            row = []
            for x in range(self.grid_size):
                if x == self.hunter.x and y == self.hunter.y:
                    row.append('H')
                elif any(t['x'] == x and t['y'] == y for t in self.treasures):
                    row.append('T')
                elif any(h.x == x and h.y == y for h in self.hideouts):
                    row.append('X')
                elif any(k.x == x and k.y == y and k.active for k in self.knights):
                    row.append('K')
                else:
                    row.append('.')
            print(' '.join(row))
    
    def check_treasure(self):
        for treasure in self.treasures[:]:
            if treasure['x'] == self.hunter.x and treasure['y'] == self.hunter.y:
                treasure['obj'].apply_effect(self.hunter)
                self.treasures.remove(treasure)
                print(f"\nFound {treasure['obj'].type} treasure! Health: {self.hunter.health}%")
                input("Press Enter to continue...")
                return True
        return False
    
    def check_hideout(self):
        for hideout in self.hideouts:
            if hideout.x == self.hunter.x and hideout.y == self.hunter.y:
                if sum(self.hunter.treasures.values()) > 0:
                    hideout.store_treasures(self.hunter)
                    print("\nStored all carried treasures in this hideout!")
                    print(f"Now carrying: {self.hunter.treasures}")
                    print(f"This hideout contains: {hideout.stored_treasures}")
                    input("Press Enter to continue...")
                    return True
                else:
                    print("\nYou're not carrying any treasures to store!")
                    print(f"This hideout contains: {hideout.stored_treasures}")
                    input("Press Enter to continue...")
                    return True
        return False
    
    def update_knights(self):
        """Update all knights and check for hunter encounters"""
        for knight in self.knights[:]:
            if not knight.active:
                continue
                
            knight.update([self.hunter], self.hideouts)

            if knight.x == self.hunter.x and knight.y == self.hunter.y:
                print("\nA knight has caught you!")
                if self.hunter.health <= 0:
                    print("You have been defeated!")
                    self.game_over = True
                input("Press Enter to continue...")
    
    def play(self):
        while not self.game_over:
            self.display()
            self.update_knights()
            if self.game_over:
                break
            
            move = input("Your move (W/A/S/D/H/Q): ").lower()
            
            if move == 'q':
                self.game_over = True
                print("\nThanks for playing Knights of Eldoria!")
                break
            elif move == 'h':
                self.check_hideout()
                continue
            
            dx, dy = 0, 0
            if move == 'w':
                dy = -1
            elif move == 's':
                dy = 1
            elif move == 'a':
                dx = -1
            elif move == 'd':
                dx = 1
            else:
                print("Invalid move! Use W/A/S/D to move, H to store, or Q to quit.")
                input("Press Enter to continue...")
                continue
            
            if not self.hunter.move(dx, dy):
                print("Can't move there - out of bounds!")
                input("Press Enter to continue...")
                continue
            
            self.check_treasure()
            self.check_hideout()
            if self.hunter.health <= 0:
                self.game_over = True
                print("\nYou have been defeated by the knights!")
                print("Game Over!")
                break
                
            if not self.treasures and sum(self.hunter.treasures.values()) == 0:
                self.game_over = True
                total_stored = sum(sum(h.stored_treasures.values()) for h in self.hideouts)
                print("\nCongratulations! You've stored all treasures!")
                print(f"Final health: {self.hunter.health}%")
                print(f"Total treasures stored: {total_stored}")
                print("Thanks for playing Knights of Eldoria!")