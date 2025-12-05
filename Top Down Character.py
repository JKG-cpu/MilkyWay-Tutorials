import pygame
from pygame.math import Vector2 as vector

pygame.init()

screen_width = 750
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
center_screen = (screen_width // 2, screen_height // 2)

pygame.display.set_caption("Top Down Character")

# Clock for delta time
clock = pygame.time.Clock()

# Player
player_color = "red"
player_size = 50, 50
direction = vector()
speed = 250 # Create a player speed variable + Speed is just how many pixels to move

player_surface = pygame.Surface((50, 50))
player_surface.fill(player_color)

player_rect = player_surface.get_frect(center = center_screen)

while True:
    # Make the screen one color
    screen.fill((0, 0, 0)) # You can use text like "black", RGB like (0, 0, 0, 0), or even hex values like "#000000"

    dt = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    # Getting key input
    keys = pygame.key.get_pressed()
    direction = vector()

    if keys[pygame.K_LEFT]:
        direction.x = -1
        
    if keys[pygame.K_RIGHT]:
        direction.x = 1

    if keys[pygame.K_UP]:
        direction.y = -1

    if keys[pygame.K_DOWN]:
        direction.y = 1

    # Update player position via the rect (hitbox)
    if direction:
        # If direction is changed, normalize it (need to have if direction because normalize will throw an error if the vector is (0, 0)
        direction = direction.normalize()
    player_rect.center += direction * speed * dt

    # Draw the player
    screen.blit(player_surface, player_rect)

    pygame.display.update()
