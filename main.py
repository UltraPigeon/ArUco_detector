import pygame as pg
from others import level
from others import classes
from pygame import *


display = (classes.win_width, classes.win_height)
bg_color = (255, 255, 255)
lvl_h = 156
lvl_w = 223
# lvl_h = len(level.level_map)
# lvl_w = len(level.level_map[0])


def main():
    pg.init()
    screen = pg.display.set_mode(display)
    pg.display.set_caption('ArUco Detector')
    bg = pg.Surface(display)
    bg.fill(bg_color)
    timer = pg.time.Clock()

    robot = level.robot  # создаем робота из файла level
    # robot = classes.Robot(15, 15)  # создаем робота по (x,y) координатам
    left = right = down = up = key_d = key_s = key_a = key_w = False
    total_level_width = lvl_w * classes.wall_width  # Высчитываем фактическую ширину уровня
    total_level_height = lvl_h * classes.wall_length  # высоту
    camera = classes.Camera(classes.camera_configure, total_level_width, total_level_height)
    while 1:
        timer.tick(30)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                raise SystemExit
            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYDOWN and e.key == K_DOWN:
                down = True
            if e.type == KEYUP and e.key == K_DOWN:
                down = False
            if e.type == KEYDOWN and e.key == K_UP:
                up = True
            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYDOWN and e.key == K_d:
                if key_d:
                    key_d = False
                else:
                    key_d = True
            if e.type == KEYDOWN and e.key == K_s:
                if key_s:
                    key_s = False
                else:
                    key_s = True
            if e.type == KEYDOWN and e.key == K_a:
                if key_a:
                    key_a = False
                else:
                    key_a = True
            if e.type == KEYDOWN and e.key == K_w:
                if key_w:
                    key_w = False
                else:
                    key_w = True

        screen.blit(bg, (0, 0))
        entities = level.entities  # Все объекты
        walls = level.walls  # то, во что мы будем врезаться или опираться
        aruco_markers = level.aruco_markers
        entities.add(robot)
        robot.update(left, right, down, up, walls)  # передвижение
        camera.update(robot)
        robot_center_x = robot.rect.centerx + camera.state[0]
        robot_center_y = robot.rect.centery + camera.state[1]
        if key_a:
            robot.seeing_area(screen, robot_center_x, robot_center_y)
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        aruco_in_area = []
        for a in aruco_markers:
            a[0].check_robot(robot, walls, aruco_in_area, a)
        aruco_in_area = sorted(aruco_in_area, reverse=False, key=lambda x: x[1])
        robot.draw_line(aruco_in_area, screen, robot, camera)
        if key_s:
            for i in aruco_in_area:
                i[0][0].draw_id(camera, screen, i[0][1])

        if key_d:
            robot.draw_distance(aruco_in_area, screen, robot_center_x, robot_center_y)
        if key_w:
            if len(aruco_in_area) > 1:
                aruco_in_area[0][0][0].triang(aruco_in_area, screen, camera, robot)
        pg.display.update()  # обновление экрана


if __name__ == "__main__":
    main()
