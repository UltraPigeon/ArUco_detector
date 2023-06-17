from others import classes
import pygame as pg
import xml.etree.ElementTree as et


# level_map = [
#     '---------------------------------------------------------------',
#     '-      ^                     ^                                -',
#     '-                                                             -',
#     '-                                            --               -',
#     '-      -----   ---------                     --               -',
#     '-     >-----   ---------                     --               -',
#     '-<     --         ^   --                    >------------------',
#     '-      --<            --                     ------------------',
#     '-      --             --<                                     -',
#     '-                     --                                     >-',
#     '-                    >--                                      -',
#     '-                     --<                                     -',
#     '-      --             --                                      -',
#     '-      --     v       --                 v      v             -',
#     '-      ----------   ----        -------------------------------',
#     '-      ----------   ----        -------------------------------',
#     '-                               --                            -',
#     '-                               --                            -',
#     '-                               --                            -',
#     '-      ---          ---                                       -',
#     '-      ---          ---                                       -',
#     '-      ---          ---                                       -',
#     '-                               --                            -',
#     '-                               --                            -',
#     '-                               ---------------               -',
#     '-                                            --               -',
#     '-      -----   ---------                     --               -',
#     '-     >-----   ---------                     --               -',
#     '-<     --         ^   --                    >------------------',
#     '-      --<            --                     ------------------',
#     '-      --             --<                                     -',
#     '-                     --                                     >-',
#     '-                    >--                                      -',
#     '-                     --<                                     -',
#     '-      --             --                                      -',
#     '-      --             --                 v      v             -',
#     '-      --             --        -------------------------------',
#     '-      --     v       --        -------------------------------',
#     '-      ----------   ----        -------------------------------',
#     '-                               --                            -',
#     '-                               --                            -',
#     '-                               --                            -',
#     '-      ---          ---                                       -',
#     '-      ---          ---                                       -',
#     '-      ---          ---                                       -',
#     '-                               --                            -',
#     '-                               --                            -',
#     '-                               ---------------               -',
#     '-                                            --               -',
#     '-      -----   ---------                     --               -',
#     '-     >-----   ---------                     --               -',
#     '-<     --         ^   --                    >------------------',
#     '-      --<            --                     ------------------',
#     '-      --             --<                                     -',
#     '-      ----------   ----        -------------------------------',
#     '-                               --                            -',
#     '-                               --                            -',
#     '-                               --                            -',
#     '-      ---          ---                                       -',
#     '-      ---          ---                                       -',
#     '-      ---          ---                                       -',
#     '-                               --                            -',
#     '-                               --                            -',
#     '-                               ---------------               -',
#     '-                                            --               -',
#     '-      -----   ---------                     --               -',
#     '-     >-----   ---------                     --               -',
#     '-<     --         ^   --                    >------------------',
#     '-      --<            --                     ------------------',
#     '-      --             --<                                     -',
#     '---------------------------------------------------------------']
# level_structure = len(level_map)
entities = pg.sprite.Group()
walls = []  # то, во что мы будем врезаться или опираться
aruco_markers = []
x = y = 0  # координаты
marker_id_count = 1
# for row in level_map:  # вся строка
#     for col in row:  # каждый символ
#         if col == '-':
#             pf = classes.Wall(x, y)
#             entities.add(pf)
#             walls.append(pf)
#         elif col == '<':
#             pf = classes.Left(x, y)
#             entities.add(pf)
#             aruco_markers.append([pf, marker_id_count])
#             marker_id_count += 1
#         elif col == 'v':
#             pf = classes.Down(x, y)
#             entities.add(pf)
#             aruco_markers.append([pf, marker_id_count])
#             marker_id_count += 1
#         elif col == '>':
#             pf = classes.Right(x, y)
#             entities.add(pf)
#             aruco_markers.append([pf, marker_id_count])
#             marker_id_count += 1
#         elif col == '^':
#             pf = classes.Up(x, y)
#             entities.add(pf)
#             aruco_markers.append([pf, marker_id_count])
#             marker_id_count += 1
#         x += classes.wall_width  # блоки платформы ставятся на ширине блоков
#     y += classes.wall_length  # то же самое и с высотой
#     x = 0

root = et.parse('others/ctpo.tmx').getroot()
for tag in root.findall('objectgroup'):
    value = tag.attrib['name']
    if value == 'robot':
        # print(value)
        for r in tag.findall('object'):
            x = float(r.attrib['x'])
            y = float(r.attrib['y'])
            robot = classes.Robot(x, y)
            # print(x, y)

    elif value == 'walls':
        # print(value)
        for w in tag.findall('object'):
            x = float(w.attrib['x'])
            y = float(w.attrib['y'])
            pf = classes.Wall(x, y)
            entities.add(pf)
            walls.append(pf)
            # print(x, y)

    elif value == 'aruc_left':
        # print(value)
        for aruc in tag.findall('object'):
            x = float(aruc.attrib['x'])
            y = float(aruc.attrib['y'])
            pf = classes.Left(x, y)
            entities.add(pf)
            aruco_markers.append([pf, marker_id_count])
            marker_id_count += 1
            # print(x, y)
    elif value == 'aruc_right':
        # print(value)
        for aruc in tag.findall('object'):
            x = float(aruc.attrib['x'])
            y = float(aruc.attrib['y'])
            pf = classes.Right(x, y)
            entities.add(pf)
            aruco_markers.append([pf, marker_id_count])
            marker_id_count += 1
    elif value == 'aruc_up':
        # print(value)
        for aruc in tag.findall('object'):
            x = float(aruc.attrib['x'])
            y = float(aruc.attrib['y'])
            pf = classes.Up(x, y)
            entities.add(pf)
            aruco_markers.append([pf, marker_id_count])
            marker_id_count += 1
    elif value == 'aruc_down':
        # print(value)
        for aruc in tag.findall('object'):
            x = float(aruc.attrib['x'])
            y = float(aruc.attrib['y'])
            pf = classes.Down(x, y)
            entities.add(pf)
            aruco_markers.append([pf, marker_id_count])
            marker_id_count += 1

