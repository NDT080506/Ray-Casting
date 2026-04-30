import pygame as pg
from settings import *
import math

class Raycasting():

    def __init__(self, game):
        self.game = game
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures


    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray,  values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2, SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        texture_vert, texture_hort = 1, 1
        ray_angle = self.game.player.angle - HALF_FOV + 0.0001
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            #horizontals
            y_hort, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hort = (y_hort - oy) / sin_a
            x_hort = ox + depth_hort * cos_a

            delta_depth_hort = dy / sin_a
            dx = delta_depth_hort * cos_a

            for i in range(MAX_DEPTH):
                tile_hort = int(x_hort), int(y_hort)
                if tile_hort in self.game.map.world_map:
                    texture_hort = self.game.map.world_map[tile_hort]
                    break
                x_hort += dx
                y_hort += dy
                depth_hort += delta_depth_hort

            #verticles
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            
            delta_depth_vert = dx / cos_a
            dy = delta_depth_vert * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth_vert

            #depth, texture wall
            if depth_vert < depth_hort:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else 1 - y_vert
            else:
                depth, texture = depth_hort, texture_hort
                x_hort %= 1
                offset = x_hort if sin_a < 0 else 1 - x_hort

            #remove fish ball's effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            #projection
            proj_height = SCREEN_DIST / (depth + 0.0001)


            #Bốn phương trình suy giảm để mô tả càng xa thì ánh sáng càng yếu
            # 1. Phương trình suy giảm tuyến tính: f(x) = a - bx
            # 2. Phương trình suy giảm nghịch đảo: f(x) = A / (1 + k(x^n)). Hay được sử dụng cho làm game
            # 3. Phương trình suy giảm mũ: f(x) = A(e^(-kx))
            # 4. Phương trình suy giảm theo bình phương khoảng cách: f(x) = A/(r^2)
            #color = [255 / (1 + depth ** 5 * 0.0002)] * 3


            #ray casting result
            self.ray_casting_result.append((depth, proj_height, texture, offset))
            
            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()