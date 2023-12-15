import math

import pygame
from classes.Entities.BaseEntity import BaseEntity
from classes.Item.RangedWeaponItem import RangedWeaponItem
from classes.Item.ThrowableWeaponItem import ThrowableWeaponItem
from classes.Item.WeaponItem import WeaponItem


class Character(BaseEntity):

    def __init__(self, surface, x, y, resourceLocation, textures, scale, name, meleeWeapon, rangedWeapon, singleUseItem, maxHealth):
        super().__init__(surface, x, y, resourceLocation, textures, scale, name, meleeWeapon, maxHealth)
        self.meleeWeapon = meleeWeapon
        self.rangedWeapon = rangedWeapon
        self.singleUseSlot = singleUseItem


    def draw(self):
        if isinstance(self.activeWeapon, RangedWeaponItem):
            if self.facing == 'U':
                pygame.draw.line(self.surface, "red", (self.collisionBox.baseRect.centerx, self.collisionBox.baseRect.centery),
                                 (self.collisionBox.baseRect.centerx, self.collisionBox.baseRect.centery - self.activeWeapon.weaponRange))
            elif self.facing == 'D':
                pygame.draw.line(self.surface, "red", (self.collisionBox.baseRect.centerx, self.collisionBox.baseRect.centery),
                                 (self.collisionBox.baseRect.centerx, self.collisionBox.baseRect.centery + self.activeWeapon.weaponRange))
            elif self.facing == 'L':
                pygame.draw.line(self.surface, "red", (self.collisionBox.baseRect.centerx, self.collisionBox.baseRect.centery),
                                 (self.collisionBox.baseRect.centerx - self.activeWeapon.weaponRange, self.collisionBox.baseRect.centery))
            elif self.facing == 'R':
                pygame.draw.line(self.surface, "red", (self.collisionBox.baseRect.centerx, self.collisionBox.baseRect.centery),
                                 (self.collisionBox.baseRect.centerx + self.activeWeapon.weaponRange, self.collisionBox.baseRect.centery))
        elif isinstance(self.activeWeapon, WeaponItem):
            for i in range(-45, 50, 5):
                if self.facing == 'U':
                    i += 90
                elif self.facing == 'D':
                    i += 270
                elif self.facing == 'L':
                    i += 180
                pygame.draw.line(self.surface, "red", (self.collisionBox.baseRect.centerx, self.collisionBox.baseRect.centery),
                                 (self.collisionBox.baseRect.centerx+(self.activeWeapon.weaponRange * math.cos(math.radians(i))),
                                  self.collisionBox.baseRect.centery-(self.activeWeapon.weaponRange * math.sin(math.radians(i)))))
        self.surface.blit(self.activeTexture, self.collisionBox.baseRect)

    def ticker(self, keys, dt):
        if isinstance(self.meleeWeapon, WeaponItem):
            self.meleeWeapon.ticker(self.surface, self)
        if isinstance(self.rangedWeapon, list):
            if isinstance(self.rangedWeapon[0], WeaponItem):
                self.rangedWeapon[0].ticker(self.surface, self)
        if isinstance(self.singleUseSlot, list):
            if isinstance(self.singleUseSlot[0], ThrowableWeaponItem):
                self.singleUseSlot[0].ticker(self.surface, self)
        for throwable in self.activeThrowables:
            throwable.ticker(self.surface, self)
        self.__movement(keys, dt)
        self.draw()

    def __movement(self, keys, dt):
        if keys[pygame.K_w]:
            self.facing = 'U'
            self.collisionBox.baseRect.y -= 300 * dt
            if self.activeTexture not in self.textureHandler.walkUp:
                self.activeTexture = self.textureHandler.walkUp[0]
            elif self.walkAnimationTimer == 0:
                if self.activeTexture == self.textureHandler.walkUp[0]:
                    self.activeTexture = self.textureHandler.walkUp[1]
                    self.walkAnimationTimer = 15
                elif self.activeTexture == self.textureHandler.walkUp[1]:
                    self.activeTexture = self.textureHandler.walkUp[0]
                    self.walkAnimationTimer = 15
            else:
                self.walkAnimationTimer -=1
        if keys[pygame.K_s]:
            self.facing = 'D'
            self.collisionBox.baseRect.y += 300 * dt
            if self.activeTexture not in self.textureHandler.walkDown:
                self.activeTexture = self.textureHandler.walkDown[0]
            elif self.walkAnimationTimer == 0:
                if self.activeTexture == self.textureHandler.walkDown[0]:
                    self.activeTexture = self.textureHandler.walkDown[1]
                    self.walkAnimationTimer = 15
                elif self.activeTexture == self.textureHandler.walkDown[1]:
                    self.activeTexture = self.textureHandler.walkDown[0]
                    self.walkAnimationTimer = 15
            else:
                self.walkAnimationTimer -=1
        if keys[pygame.K_a]:
            self.facing = 'L'
            self.collisionBox.baseRect.x -= 300 * dt
            if self.activeTexture not in self.textureHandler.walkLeft and not keys[pygame.K_w] and not keys[pygame.K_s]:
                self.activeTexture = self.textureHandler.walkLeft[0]
            elif self.walkAnimationTimer == 0:
                if self.activeTexture == self.textureHandler.walkLeft[0]:
                    self.activeTexture = self.textureHandler.walkLeft[1]
                    self.walkAnimationTimer = 15
                elif self.activeTexture == self.textureHandler.walkLeft[1]:
                    self.activeTexture = self.textureHandler.walkLeft[0]
                    self.walkAnimationTimer = 15
            else:
                self.walkAnimationTimer -=1
        if keys[pygame.K_d]:
            self.facing = 'R'
            self.collisionBox.baseRect.x += 300 * dt
            if self.activeTexture not in self.textureHandler.walkRight and not keys[pygame.K_w] and not keys[pygame.K_s]:
                self.activeTexture = self.textureHandler.walkRight[0]
            elif self.walkAnimationTimer == 0:
                if self.activeTexture == self.textureHandler.walkRight[0]:
                    self.activeTexture = self.textureHandler.walkRight[1]
                    self.walkAnimationTimer = 15
                elif self.activeTexture == self.textureHandler.walkRight[1]:
                    self.activeTexture = self.textureHandler.walkRight[0]
                    self.walkAnimationTimer = 15
            else:
                self.walkAnimationTimer -=1

        if not (keys[pygame.K_w] or keys[pygame.K_s] or keys[pygame.K_a] or keys[pygame.K_d]):
            if self.activeTexture in self.textureHandler.walkUp:
                self.activeTexture = self.textureHandler.idleUp
            elif self.activeTexture in self.textureHandler.walkRight:
                self.activeTexture = self.textureHandler.idleRight
            elif self.activeTexture in self.textureHandler.walkLeft:
                self.activeTexture = self.textureHandler.idleLeft
            elif self.activeTexture in self.textureHandler.walkDown:
                self.activeTexture = self.textureHandler.idleDown

        self.checkCollisions(10)


    def attack(self, event):
        if event.key == pygame.K_e:
            if isinstance(self.activeWeapon, ThrowableWeaponItem):
                self.activeWeapon.attack(self.collisionBox, self.collisionBox.baseRect.centerx, self.collisionBox.baseRect.centery, self.facing)
                self.singleUseSlot[1] -= 1
                if self.singleUseSlot[1] == 0:
                    self.singleUseSlot = None
                    self.activeWeapon = None
            elif isinstance(self.activeWeapon, RangedWeaponItem):
                self.activeWeapon.attack(self, self.collisionBox.baseRect.centerx, self.collisionBox.baseRect.centery, self.facing)
            elif isinstance(self.activeWeapon, WeaponItem):
                self.activeWeapon.attack(self.collisionBox, self.collisionBox.baseRect.centerx, self.collisionBox.baseRect.centery, self.facing)

    def changeActiveSlot(self, event):
        if event.key == pygame.K_1:
            self.activeWeapon = self.meleeWeapon
        elif event.key == pygame.K_2:
            if isinstance(self.rangedWeapon, list):
                self.activeWeapon = self.rangedWeapon[0]
            else:
                self.activeWeapon = self.rangedWeapon
        elif event.key == pygame.K_3:
            if isinstance(self.singleUseSlot, list):
                self.activeWeapon = self.singleUseSlot[0]
            else:
                self.activeWeapon = self.singleUseSlot
