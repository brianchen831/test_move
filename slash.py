import pygame

class Slash():
    def __init__(self, x, y, face_right):
        
        super().__init__()
        self.pos = [x,y]
        self.facing_right = face_right
        if self.facing_right:
            self.hitbox = pygame.Rect(self.pos[0] + 100, self.pos[1] + 55, 100, 70)
        else:
            self.hitbox = pygame.Rect(self.pos[0], self.pos[1] + 55, 100, 70)

        self.initial = pygame.time.get_ticks()
    
    def get_hitbox(self):
        return self.hitbox
    
    def set_pos(self, x, y):
        self.pos = [x, y]
        self.hitbox = pygame.Rect(self.pos[0] + 100, self.pos[1] + 55, 90, 70)
