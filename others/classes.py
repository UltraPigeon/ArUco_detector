import math
# from pygame import *
import pygame as pg
import random

# параметры для отрисовки робота на карте
bot_speed = 15
bot_width = 50
bot_length = 50
bot_height = 25
color = (0, 255, 0)
# параметры для отрисовки стен и маркера
wall_width = 10
wall_length = 10
wall_color = (0, 0, 0)
ArUco_color = (255, 0, 0)
aruco_height = 50
# параметры экрана
win_width = 1100
win_height = 800


class Robot(pg.sprite.Sprite):  # класс для спрайта робота
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения по оси х. 0 - стоять на месте
        self.yvel = 0  # скорость перемещенияпо оси у. 0 - стоять на месте
        self.startX = x  # начальная позиция х
        self.startY = y  # начальная позиция у
        self.height = bot_height + random.randint(-15, 15)
        self.image = pg.Surface((bot_width, bot_length))
        self.image.fill(color)
        self.rect = pg.Rect(x, y, bot_width, bot_length)  # прямоугольный объект

    def update(self, left, right, down, up, walls):  # метод для движения робота
        if left:
            self.xvel = -bot_speed  # лево = x- n

        if right:
            self.xvel = bot_speed  # право = x + n

        if down:
            self.yvel = bot_speed  # вниз = у- n

        if up:
            self.yvel = -bot_speed  # вверх = у + n

        if not (left or right):  # стоим, когда нет указаний идти
            self.xvel = 0
        if not (down or up):  # стоим, когда нет указаний идти
            self.yvel = 0
        self.rect.y += self.yvel
        self.collide(0, self.yvel, walls)

        self.rect.x += self.xvel  # переносим свои положение на xvel
        self.collide(self.xvel, 0, walls)

    def collide(self, xvel, yvel, walls):
        for w in walls:
            if pg.sprite.collide_rect(self, w):  # если есть пересечение стены с роботом

                if xvel > 0:  # если движется вправо
                    self.rect.right = w.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = w.rect.right  # то не движется влево

                if yvel > 0:  # если движется вниз
                    self.rect.bottom = w.rect.top  # то не движется вниз

                if yvel < 0:  # если движется вверх
                    self.rect.top = w.rect.bottom  # то не движется вверх

    def draw_distance(self, target_list, screen, c_x, c_y):
        if len(target_list) == 1:
            dist = round(((target_list[0][1]) / 100) * 0.9, 2)
            text_font = pg.font.Font(None, 40)
            text1 = text_font.render(f'ArUco ID {target_list[0][0][1]} дистанция : {dist} м',
                                     True, 'white')
            pg.draw.rect(screen, 'black', (c_x - (win_width / 2), c_y - (win_height / 2), 600, 40))
            screen.blit(text1, (c_x - (win_width / 2), c_y - (win_height / 2) + 2))
        elif len(target_list) > 1:
            dist1 = round(((target_list[0][1]) / 100) * 0.9, 2)
            dist2 = round(((target_list[0][1]) / 100) * 0.9, 2)
            text_font = pg.font.Font(None, 40)
            text1 = text_font.render(
                f'ArUco ID {target_list[0][0][1]} дистанция : {dist1} м',
                True, 'white')
            pg.draw.rect(screen, 'black', (c_x - (win_width / 2), c_y - (win_height / 2), 600, 40))
            screen.blit(text1, (c_x - (win_width / 2), c_y - (win_height / 2) + 2))
            text_font = pg.font.Font(None, 40)
            text1 = text_font.render(
                f'ArUco ID {target_list[1][0][1]} дистанция : {dist2} м',
                True, 'white')
            pg.draw.rect(screen, 'black', (c_x - (win_width / 2), c_y - (win_height / 2) + 40, 600, 40))
            screen.blit(text1, (c_x - (win_width / 2), c_y - (win_height / 2) + 42))
        else:
            text_font = pg.font.Font(None, 40)
            text1 = text_font.render(
                f'ArUco маркеров не обнаруженно',
                True, 'white')
            pg.draw.rect(screen, 'black', (c_x - (win_width / 2), c_y - (win_height / 2), 600, 40))
            screen.blit(text1, (c_x - (win_width / 2) , c_y - (win_height / 2) + 2))

    def draw_line(self, target_list, screen, robot, camera):
        if len(target_list) >= 2:
            for t in range(2):
                pg.draw.aaline(screen, (0, 0, 255),
                            [target_list[t][0][0].rect.center[0] + camera.state[0],
                             target_list[t][0][0].rect.center[1] + camera.state[1]],
                            [robot.rect.center[0] + camera.state[0], robot.rect.center[1] + camera.state[1]]
                            )

        elif len(target_list) == 1:
            pg.draw.aaline(screen, (0, 0, 255),
                        [target_list[0][0][0].rect.center[0] + camera.state[0],
                         target_list[0][0][0].rect.center[1] + camera.state[1]],
                        [robot.rect.center[0] + camera.state[0], robot.rect.center[1] + camera.state[1]]
                        )

    def seeing_area(self, screen, c_x, c_y):  # Выводим радиус обзора
        pg.draw.circle(screen, (44, 45, 56),
                    (c_x, c_y), 300)


class Wall(pg.sprite.Sprite):  # класс для спрайта стены
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((wall_width, wall_length))
        self.image.fill(wall_color)
        self.rect = pg.Rect(x, y, wall_width, wall_length)


class ArUco(Wall):  # подкласс для арукомаркеров
    def __init__(self, x, y):
        Wall.__init__(self, x, y)
        self.aruco_height = aruco_height + random.randint(- 20, 20)

    def draw_id(self, camera, screen, id):
        x = self.rect.centerx + camera.state[0]
        y = self.rect.centery + camera.state[1]
        text_font = pg.font.Font(None, 20)
        text1 = text_font.render(
            f'ID : {id}', True, 'red')
        screen.blit(text1, (x - 20, y - 20))

    def chek_robot(self, robot, walls, target_list, aruc):
        v = pg.Vector3(robot.rect.centerx - self.rect.centerx,
                    robot.rect.centery - self.rect.centery,
                    robot.height - aruc[0].aruco_height)
        distance_to_marker = v.magnitude()
        z = robot.height - aruc[0].aruco_height
        distance_to_wall = (distance_to_marker ** 2 - z ** 2) ** 0.5
        if distance_to_wall <= 300:
            vision = True
            k = 0
            x1 = float(self.rect.centerx)
            y1 = float(self.rect.centery)
            while vision:
                chek_rect = pg.Rect(x1, y1, 1, 1)
                x1 = int(0.005 * v.x * k) + x1
                y1 = int(0.005 * v.y * k) + y1
                k += 1
                for w in walls:
                    if chek_rect.colliderect(w.rect):
                        vision = False
                        break
                    elif chek_rect.colliderect(robot.rect):
                        distance_to_wall = round(distance_to_wall, 2)
                        target_aruco = [aruc, distance_to_wall + (distance_to_wall * random.uniform(-0.05, 0.005))]
                        target_list.append(target_aruco)
                        vision = False
                        break

    def triang(self, target_list, screen, camera, robot):
        pg.draw.aaline(screen, 'blue',
                       [self.rect.centerx + camera.state[0],
                        self.rect.centery + camera.state[1]],
                       [target_list[1][0][0].rect.center[0] + camera.state[0],
                        target_list[1][0][0].rect.center[1] + camera.state[1]]
                       )
        v = pg.Vector2(self.rect.centerx - target_list[1][0][0].rect.center[0],
                       self.rect.centery - target_list[1][0][0].rect.center[1])
        v2 = pg.Vector2(self.rect.centerx - robot.rect.centerx, self.rect.centery - robot.rect.centery)
        a = round(v.magnitude(), 2)
        c = round(target_list[0][1], 2)
        b = round(target_list[1][1], 2)
        # angle_a = math.cos((a ** 2 + b ** 2 - c ** 2) / (2 * a * c))
        angle_a = (a ** 2 + b ** 2 - c ** 2) / (2 * a * b)
        k = math.radians(pg.math.Vector2(v).angle_to((v2)))
        v3 = v2
        v3 = v3.rotate(-k)
        v3 = v3.rotate(angle_a)
        pg.draw.circle(screen, 'grey',
                       (self.rect.centerx + camera.state[0] - v3[0],
                        self.rect.centery + camera.state[1] - v3[1]), 40)
        pg.draw.circle(screen, 'grey',
                       (self.rect.centerx + camera.state[0] + v3[0],
                        self.rect.centery + camera.state[1] + v3[1]), 40)





        # print(v2)


class Left(ArUco):  # подкласс для аруко левых маркеров
    def __init__(self, x, y):
        ArUco.__init__(self, x, y)
        self.image = pg.Surface((wall_width / 5, wall_length))
        self.image.fill(ArUco_color)
        self.rect = pg.Rect(x, y, wall_width / 5, wall_length)


class Down(ArUco):  # подкласс для аруко нижних маркеров
    def __init__(self, x, y):
        ArUco.__init__(self, x, y)
        self.image = pg.Surface((wall_width, wall_length / 5))
        self.image.fill(ArUco_color)
        self.rect = pg.Rect(x, y + wall_length * (4 / 5), wall_width, wall_length / 5)


class Right(ArUco):  # подкласс для аруко правых маркеров
    def __init__(self, x, y):
        ArUco.__init__(self, x, y)
        self.image = pg.Surface((wall_width / 5, wall_length))
        self.image.fill(ArUco_color)
        self.rect = pg.Rect(x + wall_length * (4 / 5), y, wall_width / 5, wall_length)


class Up(ArUco):  # подкласс для аруко верхних маркеров
    def __init__(self, x, y):
        ArUco.__init__(self, x, y)
        self.image = pg.Surface((wall_width, wall_length / 5))
        self.image.fill(ArUco_color)
        self.rect = pg.Rect(x, y, wall_width, wall_length / 5)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = pg.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + win_width / 2, -t + win_height / 2

    # l = min(0, l)
    # l = max(-(camera.width - win_width), l)
    # # t = max(-(camera.height - win_width), t)
    # t = min(0, t)

    return pg.Rect(l, t, w, h)
