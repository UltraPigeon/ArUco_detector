import pygame as pg
from others import level
from others import classes
from pygame import *


display = (classes.win_width, classes.win_height)
bg_color = (255, 255, 255)
# 1 пиксель равен 3 см
lvl_h = 156
lvl_w = 223


def main():
    pg.init()
    screen = pg.display.set_mode(display)
    pg.display.set_caption('ArUco Detector')
    bg = pg.Surface(display)
    bg.fill(bg_color)
    timer = pg.time.Clock()

    robot = level.robot  # создаем робота по (x,y) координатам
    left = right = down = up = False  # по умолчанию — стоим

    total_level_width = 223 * classes.wall_width  # Высчитываем фактическую ширину уровня
    total_level_height = 156 * classes.wall_length  # высоту
    camera = classes.Camera(classes.camera_configure, total_level_width, total_level_height)

    while 1:
        timer.tick(30)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYUP and e.key == K_UP:
                up = False

        screen.blit(bg, (0, 0))
        # robot.seeing_area(screen)
        entities = level.entities  # Все объекты
        walls = level.walls  # то, во что мы будем врезаться или опираться
        aruco_markers = level.aruco_markers
        entities.add(robot)
        robot.update(left, right, down, up, walls)  # передвижение
        # entities.draw(screen)
        camera.update(robot)
        for e in entities:
            screen.blit(e.image, camera.apply(e))  # отображение
        aruco_in_area = []
        for a in aruco_markers:
            a[0].chek_robot(robot, walls, aruco_in_area, a, screen)
            # print(a[0].aruco_height)
        aruco_in_area = sorted(aruco_in_area, reverse=False, key=lambda x: x[1])
        robot.draw_line(aruco_in_area, screen, robot, lvl_h, camera)
        pg.display.update()  # обновление экрана


if __name__ == "__main__":
    main()
