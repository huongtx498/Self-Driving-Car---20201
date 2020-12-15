import random
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from graphic.car import calculate_angle
from graphic import car
from pygame.locals import *
import graphic.traffic_lamp as traffic_lamp
import graphic.stone as stone
import pygame
import graphic.maps as maps
import graphic.camera as camera

def main():
    clock = pygame.time.Clock()
    running = True

    cam = camera.Camera()

    stone_impediment = stone.Stone(200, 200, 90, 0)

    map_s = pygame.sprite.Group()
    map_s.add(maps.Map(0, 0, 2))

    start_x = maps.MAP_NAVS[0][0]
    start_y = maps.MAP_NAVS[0][1]
    maps.FINISH_INDEX = len(maps.MAP_NAVS) - 1

    start_angle = calculate_angle(maps.MAP_NAVS[0][0],
                                  maps.MAP_NAVS[0][1], maps.MAP_NAVS[1][0], maps.MAP_NAVS[1][1])
    # tính góc của xe: input x1, y1, x2, y2
    print("Start angle: ", start_angle)
    print("Finish index: ", maps.FINISH_INDEX)
# khởi tạo đối tượng car với tọa độ x, y và góc hướng
    controlled_car = car.Car(start_x, start_y, start_angle)
    cars = pygame.sprite.Group()  # nhóm đối tượng car
    cars.add(controlled_car)

# sprite: 1 đối tượng trong game
# sprite.group: nhóm các đối tượng vào cùng 1 group để thực hiện việc vẽ lại đồng thời
    traffic_lamps = pygame.sprite.Group()  # nhóm các đối tượng đèn
    for lamp_pos in maps.TRAFFIC_LAMP_COORDINATES:
        traffic_lamps.add(traffic_lamp.TrafficLamp(lamp_pos))

    stones = pygame.sprite.Group()  # nhóm đối tượng stone
    stones.add(stone_impediment)

    stone_status = (stone_impediment.status, len(maps.MAP_NAVS) - 1)

# di chuyển camera theo car
    cam.set_pos(controlled_car.x, controlled_car.y)
    flag = 0
    pygame.display.flip()
    while running:
        flag += 1
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYUP:
                if keys[K_p]:
                    pass

                if keys[K_q]:
                    pygame.quit()
                    sys.exit(0)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
                break

            # mouse event

            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
                if pressed1:
                    print("left click")
                    current_index = controlled_car.current_nav_index
                    random_index = random.randrange(
                        current_index + 3, current_index + 6)
                    if random_index <= (len(maps.MAP_NAVS) - 3) and stone_impediment.status == 0:
                        x = maps.MAP_NAVS[random_index][0]
                        y = maps.MAP_NAVS[random_index][1]
                        stone_impediment.switch_status(x, y)
                        stone_status = (stone_impediment.status, random_index)
                    else:
                        stone_impediment.switch_status(0, 0)
                        stone_status = (0, len(maps.MAP_NAVS) - 1)

        cam.set_pos(controlled_car.x, controlled_car.y)

        screen.blit(background, (0, 0))

        # update and render map
        map_s.update(cam.x, cam.y)
        map_s.draw(screen)

        # update and render traffic lamps
        traffic_lamps_status = []
        traffic_lamps.update(cam.x, cam.y)
        traffic_lamps.draw(screen)

        stones.update(cam.x, cam.y)
        stones.draw(screen)

        for lamp in traffic_lamps:
            lamp_status = lamp.render(screen)
            traffic_lamps_status.append(lamp_status)

        # update and render car
        cars.update(cam.x, cam.y, traffic_lamps_status, stone_status, flag)
        cars.draw(screen)
        # blue = 230, 30, 30
        # point1 = 635, 525
        # point2 = 165, 167
        # pygame.draw.lines(screen, blue, False, [(100,100), (150,200), (200,100), point1, point2], 5)
        pygame.display.flip()

        clock.tick(60)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1600, 1000))
    pygame.display.set_caption("Self Driving Car")
    pygame.mouse.set_visible(True)
    font = pygame.font.Font(None, 24)

    CENTER_W = int(pygame.display.Info().current_w / 2)
    CENTER_H = int(pygame.display.Info().current_h / 2)

    # new background surface
    background = pygame.Surface(screen.get_size())
    background = background.convert_alpha(background)
    background.fill((82, 86, 94))

    # main loop
    main()

    pygame.quit()
    sys.exit(0)
