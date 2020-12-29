import random

import pygame

from graphic.loader import load_image


class TrafficLamp(pygame.sprite.Sprite):
    # Lamp status
    GREEN = 1
    RED = 2
    YELLOW = 3

    # time out for lamp switch from GREEN to RED and backward
    TIMEOUT = 600
    LAMP_RED_IMG = "traffic_lamp_red.png"
    LAMP_GREEN_IMG = "traffic_lamp_green.png"
    LAMP_YELLOW_IMG = "traffic_lamp_yellow.png"

    def __init__(self, init_x, init_y, dir, numberical_order, status=None, remaining_time=None):
        pygame.sprite.Sprite.__init__(self)

        if status is None:
            # status = random.randint(1, 3)
            status = 1
        if remaining_time is None:
            remaining_time = random.randint(5, 15) * 60

        print(status, " - ", int(remaining_time / 60))
        # current status of traffic lamp
        self.status = status
        # time remaining before traffic lamp change status
        self.remaining_time = remaining_time
        print(self.remaining_time)
        # traffic lamp position
        self.x = init_x
        self.y = init_y
        # traffic lamp direction (0, 90, 180, 270)
        self.dir = dir
        self.image = self.set_traffic_lamp_img()
        self.rect = self.image.get_rect()
        self.rect_w = self.rect.size[0]
        self.rect_h = self.rect.size[1]
        self.rect.center = self.x, self.y
        self.numberical_order = numberical_order

    def __init__(self, traffic_coordinates, status=None, remaining_time=None):
        pygame.sprite.Sprite.__init__(self)

        if status is None:
            # status = random.randint(1, 2)
            status = 1
        if remaining_time is None:
            remaining_time = random.randint(5, 15) * 60

        print(status, " - ", int(remaining_time / 60))
        # current status of traffic lamp
        self.status = status
        # time remaining before traffic lamp change status
        self.remaining_time = remaining_time
        print(self.remaining_time)
        # traffic lamp position
        self.x = traffic_coordinates[0]
        self.y = traffic_coordinates[1]
        # traffic lamp direction (0, 90, 180, 270)
        self.dir = traffic_coordinates[2]
        self.image = self.set_traffic_lamp_img()
        self.rect = self.image.get_rect()
        self.rect_w = self.rect.size[0]
        self.rect_h = self.rect.size[1]
        self.rect.center = self.x, self.y
        self.numberical_order = traffic_coordinates[3]


    def set_traffic_lamp_img(self):
        if self.status == TrafficLamp.RED:
            self.image = load_image(TrafficLamp.LAMP_RED_IMG)
            self.rect = self.image.get_rect()
            self.rect_w = self.rect.size[0]
            self.rect_h = self.rect.size[1]
            return pygame.transform.scale(self.image, (int(self.rect_w / 2), int(self.rect_h / 2)))
        elif self.status == TrafficLamp.GREEN:
            self.image = load_image(TrafficLamp.LAMP_GREEN_IMG)
            self.rect = self.image.get_rect()
            self.rect_w = self.rect.size[0]
            self.rect_h = self.rect.size[1]
            return pygame.transform.scale(self.image, (int(self.rect_w / 2), int(self.rect_h / 2)))
        elif self.status == TrafficLamp.YELLOW:
            self.image = load_image(TrafficLamp.LAMP_YELLOW_IMG)
            self.rect = self.image.get_rect()
            self.rect_w = self.rect.size[0]
            self.rect_h = self.rect.size[1]
            return pygame.transform.scale(self.image, (int(self.rect_w / 2), int(self.rect_h / 2)))

    def switch_status(self):
        if self.status == TrafficLamp.RED:
            self.pre_status = TrafficLamp.RED
            self.status = TrafficLamp.GREEN
            self.remaining_time = 600
        elif self.status == TrafficLamp.GREEN:
            self.pre_status = TrafficLamp.GREEN
            self.status = TrafficLamp.YELLOW
            self.remaining_time = 180
        elif self.status == TrafficLamp.YELLOW:
            self.pre_status = TrafficLamp.YELLOW
            self.status = TrafficLamp.RED
            self.remaining_time = 420

        self.image = self.set_traffic_lamp_img()
        self.rect = self.image.get_rect()
        pass

    # Realign the map
    def update(self, cam_x, cam_y):
        self.rect.center = self.x - cam_x + 800, self.y - cam_y + 500
        self.remaining_time -= 1
        if self.remaining_time == 0:
            self.switch_status()

    def render(self, screen):
        lamp_font = pygame.font.SysFont(None, 25)
        # render text
        label = lamp_font.render(str(int(self.remaining_time / 60)), 1, (0, 0, 0))
        screen.blit(label, (self.rect.center[0] + 30, self.rect.center[1]))
        if self.status == 1:
            return (10 - int(self.remaining_time / 60)) / 20, self.numberical_order
        if self.status == 2:
            return (13 - int(self.remaining_time / 60)) / 20, self.numberical_order
        if self.status == 3:
            return (20 - int(self.remaining_time / 60)) / 20, self.numberical_order
