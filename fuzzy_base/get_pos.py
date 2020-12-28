import pygame
from pygame.locals import *
import xlrd
import sys
import os
from tkinter import *
from tkinter import messagebox

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
# import graphic.maps as maps
from graphic.button import Button

pygame.init()
SIZE = (767, 557)
screen = pygame.display.set_mode(SIZE)
backg = pygame.image.load('../media/map.png')
screen.blit(backg, (0, 0))

# draw button
continueBtn = Button((82, 190, 128), 20, 20, 100, 40, 'Run')
resetBtn = Button((93, 173, 226), 20, 80, 100, 40, 'Reset')
quitBtn = Button((236, 112, 99), 20, 140, 100, 40, 'Quit')

continueBtn.draw(screen, (0, 0, 0))
resetBtn.draw(screen, (0, 0, 0))
quitBtn.draw(screen, (0, 0, 0))

position = 0
pygame.display.update()
Running = True
MAP_FULLNAVS = []
start_point = 0
end_point = 0


def get_nav():
    with xlrd.open_workbook('../media/toa-do.xlsx') as book:
        sheet = book.sheet_by_index(0)
        for row_num in range(sheet.nrows):
            row_value = sheet.row_values(row_num)
            MAP_FULLNAVS.append(
                (row_value[1], row_value[2], int(row_value[0])))


get_nav()


def get_nearest(u):
    DIS = []
    d = 0
    for nav in MAP_FULLNAVS:
        d = abs(u[0] - nav[0]) + abs(u[1] - nav[1])
        DIS.append(d)
    min_index = DIS.index(min(DIS))
    return MAP_FULLNAVS[min_index][2]


while Running:
    for evnt in pygame.event.get():
        if evnt.type == pygame.QUIT:
            pygame.quit()
        elif evnt.type == pygame.MOUSEBUTTONDOWN:
            if 20 <= pygame.mouse.get_pos()[0] <= 120:
                if 20 <= pygame.mouse.get_pos()[1] <= 60:
                    if start_point == 0 and end_point == 0 or start_point == end_point:
                        Tk().wm_withdraw()  # to hide the main window
                        messagebox.showinfo(
                            'Cảnh báo', 'Vui lòng chọn điểm phù hợp !')
                    else:
                        Running = False
                if 80 <= pygame.mouse.get_pos()[1] <= 120:
                    start_point = 0
                    end_point = 0
                    print(
                        "------------------------------------------------------------")
                    print("START POINT:", start_point)
                    print(
                        "------------------------------------------------------------")
                    print("END POINT:", end_point)
                    print(
                        "------------------------------------------------------------")
                    screen.blit(backg, (0, 0))
                    continueBtn.draw(screen, (0, 0, 0))
                    resetBtn.draw(screen, (0, 0, 0))
                    quitBtn.draw(screen, (0, 0, 0))
                    pygame.display.flip()

                if 140 <= pygame.mouse.get_pos()[1] <= 180:
                    pygame.quit()
            else:
                x, y = evnt.pos
                icon = pygame.image.load('../media/point.png')
                icon = pygame.transform.scale(icon, (30, 30))
                screen.blit(icon, (x - 15, y - 30))
                pygame.display.update()
                u = (x, y)
                # lay toa do diem dau-cuoi
                if start_point == 0:
                    start_point = get_nearest(u)
                    print(
                        "------------------------------------------------------------")
                    print("START POINT:", start_point)
                else:
                    end_point = get_nearest(u)
                    print(
                        "------------------------------------------------------------")
                    print("END POINT:", end_point)
                    print(
                        "------------------------------------------------------------")
