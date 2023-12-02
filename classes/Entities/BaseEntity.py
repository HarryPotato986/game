from classes.BaseObject import BaseObject
from classes.CollisionBox import CollisionBox
from classes.Entities.EntityTextureHandler import EntityTextureHandler


class BaseEntity(BaseObject):

    def __init__(self, surface, x, y, resourceLocation, textures, scale, name, weapon, maxHealth):
        self.textureHandler = EntityTextureHandler(resourceLocation, textures[0], textures[1], textures[2], textures[3], textures[4], textures[5], textures[6], textures[7], scale)
        super().__init__(surface, x, y, self.textureHandler.idleDown.get_width(), self.textureHandler.idleDown.get_height())
        self.activeTexture = self.textureHandler.idleDown
        self.walkAnimationTimer = 15
        self.weapon = weapon
        self.facing = 'D'
        self.name = name
        self.maxHealth = maxHealth
        self.health = maxHealth


    def draw(self):
        self.surface.blit(self.activeTexture, self.collisionBox.baseRect)

    def hit(self, facing, knockback):
        if facing == 'U':
            self.collisionBox.baseRect.y -= knockback
        elif facing == 'D':
            self.collisionBox.baseRect.y += knockback
        elif facing == 'L':
            self.collisionBox.baseRect.x -= knockback
        elif facing == 'R':
            self.collisionBox.baseRect.x += knockback
        self.checkCollisions(knockback+1)
        print(self.name + ": Hit!")

    def checkCollisions(self, collisionTolerance):
        entityRect = self.collisionBox.baseRect
        if entityRect.right > self.surface.get_width():
            entityRect.right = self.surface.get_width()
        if entityRect.left < 0:
            entityRect.left = 0
        if entityRect.bottom > self.surface.get_height():
            entityRect.bottom = self.surface.get_height()
        if entityRect.top < 0:
            entityRect.top = 0
        for otherBox in CollisionBox.activeBoxs:
            if otherBox != self.collisionBox and entityRect.colliderect(otherBox.baseRect):
                if abs(otherBox.baseRect.top - entityRect.bottom) < collisionTolerance:
                    entityRect.bottom = otherBox.baseRect.top
                if abs(otherBox.baseRect.bottom - entityRect.top) < collisionTolerance:
                    entityRect.top = otherBox.baseRect.bottom
                if abs(otherBox.baseRect.right - entityRect.left) < collisionTolerance:
                    entityRect.left = otherBox.baseRect.right
                if abs(otherBox.baseRect.left - entityRect.right) < collisionTolerance:
                    entityRect.right = otherBox.baseRect.left
