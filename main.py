import pygame as pg
from others import level
from others import classes
from pygame import *


display = (classes.win_width, classes.win_height)  # объявление переменной для сторон экрана приложения
bg_color = (255, 255, 255)  # цвет фона эрана приложения
lvl_h = 156  # высота экрана которая высчитывается вручную в зависимости от высоты поля в Tiled
lvl_w = 223  # ширина экрана -//-
# lvl_h = len(level.level_map)
# lvl_w = len(level.level_map[0])


def main():
    pg.init()  # основной метод с которого начинается работа в pygame
    screen = pg.display.set_mode(display)  # установка экрана приложения и его инициализация
    pg.display.set_caption('ArUco Detector')  # надпись в шапке приложения
    bg = pg.Surface(display)  # установка фона экрана
    bg.fill(bg_color)   # заливка цветом экрана
    timer = pg.time.Clock()  # внутренние часы приложения
    robot = level.robot  # создаем робота из файла level
    # robot = classes.Robot(15, 15)  # создаем робота по (x,y) координатам
    left = right = down = up = key_d = key_s = key_a = key_w = False  # установка кнопок в выключенном состоянии
    total_level_width = lvl_w * classes.wall_width  # Высчитываем фактическую ширину уровня
    total_level_height = lvl_h * classes.wall_length  # высоту
    camera = classes.Camera(classes.camera_configure, total_level_width, total_level_height)  # объявление объекта класса Камера
    while 1:  # основной цикл приложения в котором всё работает
        timer.tick(30)  # кол-во кадров в секунду
        for e in pg.event.get():  # цикл проверки срабатывания кнопок
            if e.type == pg.QUIT:  # проверка на закрытие приложения
                raise SystemExit  # выход из приложения
            if e.type == KEYDOWN and e.key == K_LEFT:    # проверка нажатия на кнопку "стрелка влево"
                left = True
            if e.type == KEYUP and e.key == K_LEFT:  # проверка нажатия на кнопку "стрелка влево"
                left = False
            if e.type == KEYDOWN and e.key == K_RIGHT:  # проверка нажатия на кнопку "стрелка вправо"
                right = True
            if e.type == KEYUP and e.key == K_RIGHT:  # проверка нажатия на кнопку "стрелка вправо"
                right = False
            if e.type == KEYDOWN and e.key == K_DOWN:  # проверка нажатия на кнопку "стрелка вниз"
                down = True
            if e.type == KEYUP and e.key == K_DOWN:  # проверка нажатия на кнопку "стрелка вниз"
                down = False
            if e.type == KEYDOWN and e.key == K_UP:  # проверка нажатия на кнопку "стрелка вверх"
                up = True
            if e.type == KEYUP and e.key == K_UP:  # проверка нажатия на кнопку "стрелка вверх"
                up = False
            if e.type == KEYDOWN and e.key == K_d:  # проверка нажатия на кнопку "D"
                if key_d:
                    key_d = False
                else:
                    key_d = True
            if e.type == KEYDOWN and e.key == K_s:  # проверка нажатия на кнопку "S"
                if key_s:
                    key_s = False
                else:
                    key_s = True
            if e.type == KEYDOWN and e.key == K_a:  # проверка нажатия на кнопку "A"
                if key_a:
                    key_a = False
                else:
                    key_a = True
            if e.type == KEYDOWN and e.key == K_w:  # проверка нажатия на кнопку "W"
                if key_w:
                    key_w = False
                else:
                    key_w = True

        screen.blit(bg, (0, 0))
        entities = level.entities  # Все объекты
        walls = level.walls  # то, во что мы будем врезаться или опираться
        aruco_markers = level.aruco_markers  # список из всех аруко маркеров
        entities.add(robot)  # доьавление робота в группу спрайтов
        robot.update(left, right, down, up, walls)  # передвижение
        camera.update(robot)  # обновление координат камеры с установкой на робота
        robot_center_x = robot.rect.centerx + camera.state[0]  # дополнительная переменная для получения центра робота с учётом движения камеры по оси x
        robot_center_y = robot.rect.centery + camera.state[1]  # дополнительная переменная для получения центра робота с учётом движения камеры по оси y
        if key_a:  # если нажимали кнопку "А"
            robot.seeing_area(screen, robot_center_x, robot_center_y)  # показывает область видимости робота
        for e in entities:  # для всех спрайтов
            screen.blit(e.image, camera.apply(e))  # обновление положений отрисовки с учётом движения камеры
        aruco_in_area = []  # установка пустого списка видимых маркеров для каждого основного цикла
        for a in aruco_markers:  # для всех маркеров
            a[0].check_robot(robot, walls, aruco_in_area, a)  # проверка видимости робота и запись подходящих в список видимых маркеров
        aruco_in_area = sorted(aruco_in_area, reverse=False, key=lambda x: x[1])  # сортировка маркеров по полученному значению дальности до робота
        robot.draw_line(aruco_in_area, screen, robot, camera)  # отрисовка линий до первых двух маркеров из списка видимых
        if key_s:  # если нажимали кнопку "S"
            for i in aruco_in_area:  # для всех маркеров из списка видимых маркеров
                i[0][0].draw_id(camera, screen, i[0][1])  # отрисовка ID всех видимых маркеро
        if key_d:  # если нажимали кнопку "D"
            robot.draw_distance(aruco_in_area, screen, robot_center_x, robot_center_y)  # отрисовка в верхнем левом углу экрана дистанция до первых двух видимых маркеров
        if key_w:  # если нажимали кнопку "W"
            if len(aruco_in_area) > 1:  # если длина списка видимых маркеров больше 1
                aruco_in_area[0][0][0].triang(aruco_in_area, screen, camera, robot)  # получение просчитаных положений робота
        pg.display.update()  # обновление экрана


if __name__ == "__main__":
    main()
