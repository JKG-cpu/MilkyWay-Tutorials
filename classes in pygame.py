import pygame
from pygame.math import Vector2 as vector

class Entity(pygame.sprite.Sprite):
    def __init__(self, name: str, color: str | tuple[int, int, int] | tuple[int, int, int, int], pos: tuple[int, int], groups: pygame.sprite.Group) -> None:
        super().__init__(groups)

        self.name = name
        self.color = color

        self.direction = vector()
        self.speed = 250

        self.image = pygame.Surface((50, 50))
        self.image.fill(self.color)
        self.rect = self.image.get_frect(center = pos)
    
    def __str__(self) -> str:
        return f"Entity: {self.name}"

    def move(self, dt):
        self.rect.center += self.direction * self.speed * dt

    def update(self, dt):
        self.move(dt)

class Player(Entity):
    def __init__(self, name: str, color: str | tuple[int, int, int] | tuple[int, int, int, int], pos: tuple[int, int], groups: pygame.sprite.Group) -> None:
        super().__init__(name, color, pos, groups)
        
        # Change the speed to be a little bit faster than the Enemy
        self.speed = 300

    def input(self):
        new_direction = vector()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            new_direction.x = -1
    
        if keys[pygame.K_RIGHT]:
            new_direction.x = 1
        
        if keys[pygame.K_UP]:
            new_direction.y = -1
        
        if keys[pygame.K_DOWN]:
            new_direction.y = 1
        
        self.direction = new_direction.normalize() if new_direction else new_direction

    def update(self, dt):
        self.input()

        super().update(dt)

class Enemy(Entity):
    def __init__(self, name: str, color: str | tuple[int, int, int] | tuple[int, int, int, int], pos: tuple[int, int], player: Player, groups: pygame.sprite.Group) -> None:
        super().__init__(name, color, pos, groups)
        
        self.player = player
        self.distance = 200
        
    def get_clicked(self):
        mouse_pos = pygame.mouse.get_pos()
        
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                    print(self)
                            
    def check_radius(self):
        # Create a vector for each position
        enemy_position = vector(self.rect.center)
        player_position = vector(self.player.rect.center)
        
        # Calculate distance
        distance_sq = (player_position - enemy_position).length_squared()
                                
        if distance_sq < self.distance ** 2:
            # Change self.direction
            distance_vector = player_position - enemy_position
            self.direction = distance_vector.normalize() if distance_vector else distance_vector
        else:
            self.direction = vector()
                        
    def update(self, dt):
        self.get_clicked()
        self.check_radius()
        
        super().update(dt)

class AllSprites(pygame.sprite.Group):
    def __init__(self) -> None:
        super().__init__()
        self.screen = pygame.display.get_surface() # We can use this just to grab the pygame window quickly

    def draw(self, player_center) -> None:
        offset_x = -(player_center[0] - self.screen.get_width() // 2)
        offset_y = -(player_center[1] - self.screen.get_height() // 2)

        for sprite in self:
            offset_pos = sprite.rect.topleft + vector(offset_x, offset_y)
            self.screen.blit(sprite.image, offset_pos)

class Game:
    def __init__(self):
        # Init Pygame
        pygame.init()

        # Create Screen
        self.screen_width, self.screen_height = 1250, 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pygame with Classes!")

        self.clock = pygame.time.Clock()

        # Sprite Group
        self.all_sprites = AllSprites()

        # Create Player
        self.player = Player(
            name = "Player",
            color = (255, 0, 0),
            pos = (self.screen.get_width() / 2, self.screen.get_height() / 2),
            groups = self.all_sprites
        )
        
        # Create Enemy
        self.enemy = Enemy(
            name = "Enemy",
            color = (0, 255, 0),
            pos = (self.screen.get_width() / 2 + 100, self.screen.get_height() / 2),
            # Pass in the Player to the Enemy
            player = self.player,
            groups = self.all_sprites
        )
		              
    def run(self):
        while True:
            self.screen.fill((0, 0, 0))

            dt = self.clock.tick() / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)

            # Game Logic
            self.all_sprites.update(dt)

            # Draw Sprites
            self.all_sprites.draw(self.player.rect.center)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
