import pygame
from support import import_csv_layout, import_cut_graphics
from settings import tile_size, screen_height
from tiles import Tile, StaticTile, Crate, Coin, PalmTree
from enemy import Enemy
from decoration import Sky, Water

class Level:
    def __init__(self, level_data, surface):
        # General setup
        self.display_surface = surface
        self.world_shift = 0

        # Player setup
        player_layout = import_csv_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # Terrain setup
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")

        # Crates
        crate_layout = import_csv_layout(level_data["crates"])
        self.crate_sprites = self.create_tile_group(crate_layout, "crates")

        # Grass setup
        grass_layout = import_csv_layout(level_data["grass"])
        self.grass_sprites = self.create_tile_group(grass_layout, "grass")

        # Coins
        coin_layout = import_csv_layout(level_data["coins"])
        self.coin_sprites = self.create_tile_group(coin_layout, "coins")

        # Foreground palm trees
        fg_palm_layout = import_csv_layout(level_data["fg palms"])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, "fg palms")

        # Background palm trees
        bg_palm_layout = import_csv_layout(level_data["bg palms"])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, "bg palms")

        # Enemies
        enemy_layout = import_csv_layout(level_data["enemies"])
        self.enemy_sprites = self.create_tile_group(enemy_layout, "enemies")

        #  Constraint
        constraint_layout = import_csv_layout(level_data["constraint"])
        self.constraint_sprites = self.create_tile_group(constraint_layout, "constraint")

        # Decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 40, level_width)

    def player_setup(self, layout):
        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                x = column_index * tile_size
                y = row_index * tile_size
                if value == "0":
                    print("player goes here")
                if value == "1":
                    hat_surface = pygame.image.load("../pirate-jump/assets/2 - Level/graphics/character/hat.png").convert_alpha()
                    sprite = StaticTile(tile_size, x, y, hat_surface)
                    self.goal.add(sprite)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for column_index, value in enumerate(row):
                if value != "-1":
                    x = column_index * tile_size
                    y = row_index * tile_size

                    if type == "terrain":
                        terrain_tile_list = import_cut_graphics(
                            "../pirate-jump/assets/2 - Level/graphics/terrain/terrain_tiles.png"
                            )
                        tile_surface = terrain_tile_list[int(value)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == "grass":
                        grass_tile_list = import_cut_graphics(
                            "../pirate-jump/assets/2 - Level/graphics/decoration/grass/grass.png"
                            )
                        tile_surface = grass_tile_list[int(value)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == "crates":
                        sprite = Crate(tile_size, x, y)

                    if type == "coins":
                        if value == "0":
                            sprite = Coin(tile_size, x, y, "../pirate-jump/assets/2 - Level/graphics/coins/gold")
                        if value == "1":
                            sprite = Coin(tile_size, x, y, "../pirate-jump/assets/2 - Level/graphics/coins/silver")

                    if type == "fg palms":
                        if value == "0":
                            sprite = PalmTree(tile_size, x, y, "../pirate-jump/assets/2 - Level/graphics/terrain/palm_small", 38)
                        if value == "1":
                            sprite = PalmTree(tile_size, x, y, "../pirate-jump/assets/2 - Level/graphics/terrain/palm_large", 64)

                    if type == "bg palms":
                        sprite = PalmTree(tile_size, x, y, "../pirate-jump/assets/2 - Level/graphics/terrain/palm_bg", 64)

                    if type == "enemies":
                        sprite = Enemy(tile_size, x, y)

                    if type == "constraint":
                        sprite = Tile(tile_size, x, y)

                    sprite_group.add(sprite)

        return sprite_group

    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def run (self):
        # Will start running the level

        # Decoration
        self.sky.draw(self.display_surface)

        # Background palms
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        # Terrain
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)

        # Enemy
        self.enemy_sprites.update(self.world_shift)
        self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # Crate
        self.crate_sprites.update(self.world_shift)
        self.crate_sprites.draw(self.display_surface)

        # Grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # Coins
        self.coin_sprites.update(self.world_shift)
        self.coin_sprites.draw(self.display_surface)

        # Foreground palms
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # Player sprites
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # Water
        self.water.draw(surface, shift)
