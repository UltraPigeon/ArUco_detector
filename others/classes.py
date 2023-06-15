from pygame import *
import random

# параметры для отрисовки робота на карте
bot_speed = 5
bot_width = 20
bot_length = 20
bot_height = 25
color = (0, 255, 0)
# параметры для отрисовки стен и маркера
wall_width = 10
wall_length = 10
wall_color = (0, 0, 0)
ArUco_color = (255, 0, 0)
aruco_height = 50
# параметры экрана
win_width = 800
win_height = 500


class Robot(sprite.Sprite):  # класс для спрайта робота
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.xvel = 0  # скорость перемещения по оси х. 0 - стоять на месте
        self.yvel = 0  # скорость перемещенияпо оси у. 0 - стоять на месте
        self.startX = x  # начальная позиция х
        self.startY = y  # начальная позиция у
        self.height = bot_height + random.randint(-15, 15)
        self.image = Surface((bot_width, bot_length))
        self.image.fill(color)
        self.rect = Rect(x, y, bot_width, bot_length)  # прямоугольный объект

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
            if sprite.collide_rect(self, w):  # если есть пересечение стены с роботом

                if xvel > 0:  # если движется вправо
                    self.rect.right = w.rect.left  # то не движется вправо

                if xvel < 0:  # если движется влево
                    self.rect.left = w.rect.right  # то не движется влево

                if yvel > 0:  # если движется вниз
                    self.rect.bottom = w.rect.top  # то не движется вниз

                if yvel < 0:  # если движется вверх
                    self.rect.top = w.rect.bottom  # то не движется вверх

    def draw_line(self, target_list, screen, robot, level_h):
        if len(target_list) >= 2:
            for t in range(2):
                draw.aaline(screen, (0, 0, 255),
                            [target_list[t][0][0].rect.center[0], target_list[t][0][0].rect.center[1]],
                            [robot.rect.center[0], robot.rect.center[1]]
                            )
                if t == 0:
                    text_font = font.Font(None, 40)
                    text1 = text_font.render(f'ArUco ID {target_list[t][0][1]} дистанция : {target_list[t][1]} пикселей',
                                             True, (0, 0, 0))
                    screen.blit(text1, (10, level_h * wall_length + 10))
                else:
                    text_font = font.Font(None, 40)
                    text1 = text_font.render(f'ArUco ID {target_list[t][0][1]} дистанция : {target_list[t][1]} пикселей',
                                             True, (0, 0, 0))
                    screen.blit(text1, (10, level_h * wall_length + 50))
        elif len(target_list) == 1:
            draw.aaline(screen, (0, 0, 255),
                        [target_list[0][0][0].rect.center[0], target_list[0][0][0].rect.center[1]],
                        [robot.rect.center[0], robot.rect.center[1]]
                        )
            text_font = font.Font(None, 40)
            text1 = text_font.render(f'ArUco ID {target_list[0][0][1]} дистанция : {target_list[0][1]} пикелей',
                                     True, (0, 0, 0))
            screen.blit(text1, (10, level_h * wall_length + 10))
        else:
            text_font = font.Font(None, 40)
            text1 = text_font.render('Аруко маркеров в поле видимости нет', True, (0, 0, 0))
            screen.blit(text1, (10, level_h * wall_length + 10))

    def seeing_area(self, screen):  # Выводим радиус обзора
        draw.circle(screen, (46, 45, 9),
                    (self.rect.centerx, self.rect.centery), 100)


class Wall(sprite.Sprite):  # класс для спрайта стены
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((wall_width, wall_length))
        self.image.fill(wall_color)
        self.rect = Rect(x, y, wall_width, wall_length)


class ArUco(Wall):  # подкласс для арукомаркеров
    def __init__(self, x, y):
        Wall.__init__(self, x, y)
        self.aruco_height = aruco_height + random.randint(- 20, 20)

    def chek_robot(self, robot, walls, target_list, aruc, screen):
        v = Vector3(robot.rect.centerx - self.rect.centerx, robot.rect.centery - self.rect.centery,
                    robot.height - aruc[0].aruco_height)
        # v = Vector2(robot.rect.centerx - self.rect.centerx, robot.rect.centery - self.rect.centery)
        distance_to_marker = v.magnitude()
        z = robot.height - aruc[0].aruco_height
        distance_to_wall = (distance_to_marker ** 2 - z ** 2 ) ** 0.5
        if distance_to_wall <= 100:
            vision = True
            k = 0
            x1 = self.rect.centerx
            y1 = self.rect.centery
            while vision:
            # for i in range(30):
            #     draw.rect(screen, (250, 250, 0), (x1, y1, 1, 1))
                chek_rect = Rect(x1, y1, 1, 1)
                x1 = int(0.01 * v.x * k) + x1
                y1 = int(0.01 * v.y * k) + y1
                k += 1
                for w in walls:
                    if chek_rect.colliderect(w.rect):
                        vision = False
                        break
                    elif chek_rect.colliderect(robot.rect):
                        target_aruco = [aruc, round(distance_to_wall, 2)]
                        target_list.append(target_aruco)
                        vision = False
                        break


class Left(ArUco):  # подкласс для аруко левых маркеров
    def __init__(self, x, y):
        ArUco.__init__(self, x, y)
        self.image = Surface((wall_width / 5, wall_length))
        self.image.fill(ArUco_color)
        self.rect = Rect(x, y, wall_width / 5, wall_length)


class Down(ArUco):  # подкласс для аруко нижних маркеров
    def __init__(self, x, y):
        ArUco.__init__(self, x, y)
        self.image = Surface((wall_width, wall_length / 5))
        self.image.fill(ArUco_color)
        self.rect = Rect(x, y + wall_length * (4 / 5), wall_width, wall_length / 5)


class Right(ArUco):  # подкласс для аруко правых маркеров
    def __init__(self, x, y):
        ArUco.__init__(self, x, y)
        self.image = Surface((wall_width / 5, wall_length))
        self.image.fill(ArUco_color)
        self.rect = Rect(x + wall_width * (4 / 5), y, wall_width / 5, wall_length)


class Up(ArUco):  # подкласс для аруко верхних маркеров
    def __init__(self, x, y):
        ArUco.__init__(self, x, y)
        self.image = Surface((wall_width, wall_length / 5))
        self.image.fill(ArUco_color)
        self.rect = Rect(x, y, wall_width, wall_length / 5)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + win_width / 2, -t + win_height / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - win_width), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - win_width), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)
