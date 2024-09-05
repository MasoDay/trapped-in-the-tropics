import pygame
from settings import vertical_tile_number, tile_size, screen_width
from tiles import AnimatedTile, StaticTile
from support import import_folder
from random import choice, randint

class Sky:
    def __init__(self, horizon):
        self.top = pygame.image.load("../pirate-jump/assets/2 - Level/graphics/decoration/sky/sky_top.png").convert()
        self.middle = pygame.image.load("../pirate-jump/assets/2 - Level/graphics/decoration/sky/sky_middle.png").convert()
        self.bottom = pygame.image.load("../pirate-jump/assets/2 - Level/graphics/decoration/sky/sky_bottom.png").convert()
        self.horizon = horizon

        # Stretch tiles
        self.top = pygame.transform.scale(self.top, (screen_width, tile_size))
        self.middle = pygame.transform.scale(self.middle, (screen_width, tile_size))
        self.bottom = pygame.transform.scale(self.bottom, (screen_width, tile_size))

    def draw(self, surface):
        for row in range(vertical_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.top, (0, y))
            elif row == self.horizon:
                surface.blit(self.middle, (0, y))
            else:
                surface.blit(self.bottom, (0, y))

class Water:
    def __init__(self, top, level_width):
        water_start_point = -screen_width
        water_tile_width = 192
        tile_x_amount = int((level_width + screen_width) / water_tile_width)
        self.water_sprites = pygame.sprite.Group()

        for tile in range(tile_x_amount):
            x = tile * water_tile_width + water_start_point
            y = top
            sprite = AnimatedTile(192, x, y, "../pirate-jump/assets/2 - Level/graphics/decoration/water")
            self.water_sprites.add(sprite)

    def draw(self, surface, shift):
        self.water_sprites.update(shift)
        self.water_sprites.draw(surface)

class Clouds:
    def __init__(self, horizon, level_width, cloud_number):
        cloud_surface_list = import_folder("../pirate-jump/assets/2 - Level/graphics/decoration/clouds")
        minimum_x = -screen_width
        maximum_x = level_width + screen_width
        minimum_y = 0
        maximum_y = horizon
        self.cloud_sprites = pygame.sprite.Group()

        for cloud in range(cloud_number):
            cloud = choice(cloud_surface_list)
            x = randint(minimum_x, maximum_x)
            y = randint(minimum_y, maximum_y)
            sprite = StaticTile(0, x, y, cloud)
            self.cloud_sprites.add(sprite)

    def draw(self, surface, shift):
        self.cloud_sprites.update(shift)
        self.cloud_sprites.draw(surface)
