import pygame
from src.entity import Entity

from src.constants import PLAYER_BULLET_COOLDOWN, PLAYER_BULLET_SPEED, PLAYER_START_VECTOR, PLAYER_SPEED, PLAYER_HEALTH
from src.entities.bullet import Bullet
from src.entities.enemy import Enemy
from src.sound import player_shoot, player_hit, player_death


class Player(Entity):
    move_direction: int
    speed: int
    health: int

    def __init__(self):
        super().__init__(PLAYER_START_VECTOR.x,
                         PLAYER_START_VECTOR.y, 55, 55, 'res/player.png')
        self.move_direction = 0  # -1,0,1
        self.health = PLAYER_HEALTH
        self.speed = PLAYER_SPEED
        self.shooting = False
        self.bullet_cooldown = PLAYER_BULLET_COOLDOWN

    def move_left(self):
        self.move_direction = -1

    def move_right(self):
        self.move_direction = 1

    def stop_moving(self):
        self.move_direction = 0

    def shoot(self):
        if self.bullet_cooldown == PLAYER_BULLET_COOLDOWN and not self.expired:
            self.shooting = True

    def tick(self, delta: int, objects: 'list'):
        self.velocity.x = self.speed * self.move_direction

        # cooldown refresher
        if self.bullet_cooldown >= PLAYER_BULLET_COOLDOWN:
            self.bullet_cooldown = PLAYER_BULLET_COOLDOWN
        else:
            self.bullet_cooldown += delta

        if self.shooting:
            objects.append(Bullet(pygame.Vector2(self.x, self.y),
                                  PLAYER_BULLET_SPEED, KILL_PLAYER=False))
            player_shoot.play()
            self.shooting = False
            self.bullet_cooldown = 0

        # check collision with bullects and enemies
        for obj in objects:
            if isinstance(obj, Bullet) and obj.kill_player == True and self.colliderect(obj):
                player_hit.play()
                self.health -= 1
                print(f"-1, hp:{self.health}.")
                obj.kill()
            if isinstance(obj, Enemy) and self.colliderect(obj):
                self.health = 0
                print("You died.")

        if self.health <= 0:
            player_death.play()
            self.kill()
