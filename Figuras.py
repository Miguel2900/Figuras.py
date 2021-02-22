import pygame
import random

# screen parameters
SIZE = (900, 500)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('MIS PRIMERAS FIGURAS')
pygame.display.set_icon(pygame.image.load('logo.png'))
pygame.init()


# images
menu_bg = pygame.image.load('MenuPrincipal.png')
level1_bg = pygame.image.load('Facil.png')
level2_bg = pygame.image.load('Medio.png')
level3_bg = pygame.image.load('Dificil.png')
victory_bg = pygame.image.load('PantallaGanado.png')
defeat_bg = pygame.image.load('PantallaPerdido.png')
credits_img = pygame.image.load('TextoCreditos.png')

# font
font = pygame.font.Font('Pixelmania.ttf', 25)

# dictionary
figures = {0: 'CIRCULO', 1: 'RECTANGULO', 2: 'CUADRADO', 3: 'ROMBO',
           4: 'CORAZON', 5: 'FLECHA', 6: 'PENTAGONO', 7: 'HEXAGONO', 8: 'CRUZ',
           9: 'ESTRELLA', 10: 'TRIANGULO', 11: 'TRIANGULO', 12: 'TRIANGULO',
           13: 'TRIANGULO', 14: 'ROMBOIDE', 15: 'ELIPSE', 16: 'TRAPECIO',
           17: 'TRAPEZOIDE', 18: 'MEDIO CIRCULO', 19: 'CUBO', 20: 'PIRAMIDE',
           21: 'CILINDRO', 22: 'CONO', 23: 'ESFERA', 24: 'ELIPSOIDE',
           25: 'PRISMA', 26: 'PRISMA'}
triangles = {0: 'EQUILATERO', 1: 'ESCALENO', 2: 'RECTANGULO', 3: 'ISOCELES'}
prism = {5: 'RECTANGULAR', 6: 'TRIANGULAR'}


# Classes
class SpriteSheet:
    def __init__(self, f_name):
        self.image = pygame.image.load(f_name)  # sprite sheet
        self.sprites = []  # list of sprites
        self.current_sprite = 0

    # obtains sprites from the sheet
    def get_sprite(self, width, height, x, y):
        self.sprites.append(self.image.subsurface(x, y, width, height))

    # updates sprites and changes the image
    def update(self, speed):
        self.current_sprite += speed
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]


class Card:
    def __init__(self):
        self.boxes = []
        self.ready = True
        self.guessed = []

    # fill with random numbers the boxes in the card
    def fill_boxes(self, diff):
        j = 0
        if self.ready:
            if diff == 0:
                max_range = 8
            elif diff == 1:
                max_range = 18
            else:
                max_range = 26
            while j < 9:
                rn = random.randint(0, max_range)
                if rn not in self.boxes:
                    self.boxes.append(rn)
                    self.guessed.append(False)
                    j += 1
            self.ready = False


# width & height
AX = 960 / 3
AY = 1280 / 4
FX = 650 / 4
FY = 813 / 5
GX = (476, 591, 707)
GY = (102, 222, 342)


# all stages of the game
class GameStage:
    def __init__(self):
        self.stage = 0
        self.actual_stage = 0
        self.card = Card()
        self.easy_figures = SpriteSheet('Figuras1.png')
        self.medium_figures = SpriteSheet('Figuras1.png')
        self.hard_figures = SpriteSheet('Figuras_3d1.png')
        self.tiger = SpriteSheet('animals.png')
        self.panda = SpriteSheet('animals.png')
        self.sloth = SpriteSheet('animals.png')
        self.frog = SpriteSheet('animals.png')
        self.medal = SpriteSheet('animals.png')
        self.mark = SpriteSheet('marks1.png')
        self.credits_bg = SpriteSheet('Fondo_geometrico1.png')
        self.figures_ready = True
        self.figures = []
        self.corrects = 0
        self.errors = 0
        self.actual_figure = 0
        self.get_sprites()

    # Fills the list figures with random values
    def fill_figures(self, min_value, max_value, stg):
        i = 0
        if self.figures_ready:
            self.actual_stage = stg
            while i <= max_value:
                rn = random.randint(min_value, max_value)
                if rn not in self.figures:
                    self.figures.append(rn)
                    i += 1
            self.figures_ready = False

    # checks if the figure choosen is the same as the one asked
    def check_figure(self, i):
        if i != -1:
            if self.card.boxes[i] == self.figures[self.actual_figure]:
                self.actual_figure += 1
                self.corrects += 1
                self.card.guessed[i] = True
                return
        elif self.figures[self.actual_figure] not in self.card.boxes and i == -1:
            self.actual_figure += 1
            return
        self.errors += 1
        draw_img(self.mark.sprites[1], 0, 0)
        pygame.display.flip()
        pygame.time.delay(500)
        return

    # reset values in order to proceed
    def reset(self, stg):
        self.stage = stg
        self.actual_stage = stg
        self.errors = 0
        self.actual_figure = 0
        self.corrects = 0
        self.figures_ready = True
        self.figures = []
        self.card.ready = True
        self.card.boxes = []
        self.card.guessed = []

    # obtains sprites for each object
    def get_sprites(self):
        self.tiger.get_sprite(AX, AY, 0, 0)
        self.tiger.get_sprite(AX, AY, AX, 0)
        self.panda.get_sprite(AX, AY, AX * 2, 0)
        self.panda.get_sprite(AX, AY, 0, AY)
        self.sloth.get_sprite(AX, AY, AX, AY)
        self.sloth.get_sprite(AX, AY, AX * 2, AY)
        self.frog.get_sprite(AX, AY, 0, AY * 2)
        self.frog.get_sprite(AX, AY, AX, AY * 2)
        self.frog.get_sprite(AX, AY, AX * 2, AY * 2)
        self.medal.get_sprite(AX, AY, 0, AY * 3)
        self.medal.get_sprite(AX, AY, AX, AY * 3)
        self.medal.get_sprite(AX, AY, AX * 2, AY * 3)
        self.mark.get_sprite(FX, FY, 0, 0)
        self.mark.get_sprite(FX, FY, 0, FY)
        self.easy_figures.get_sprite(FX, FY, 0, 0)
        self.easy_figures.get_sprite(FX, FY, FX, 0)
        self.easy_figures.get_sprite(FX, FY, FX * 2, 0)
        self.easy_figures.get_sprite(FX, FY, FX * 3, 0)
        self.easy_figures.get_sprite(FX, FY, 0, FY)
        self.easy_figures.get_sprite(FX, FY, FX, FY)
        self.easy_figures.get_sprite(FX, FY, FX * 2, FY)
        self.easy_figures.get_sprite(FX, FY, FX * 3, FY)
        self.easy_figures.get_sprite(FX, FY, 0, FY * 2)
        self.medium_figures.sprites = self.easy_figures.sprites
        self.medium_figures.get_sprite(FX, FY, FX, FY * 2)
        self.medium_figures.get_sprite(FX, FY, FX * 2, FY * 2)
        self.medium_figures.get_sprite(FX, FY, FX * 3, FY * 2)
        self.medium_figures.get_sprite(FX, FY, 0, FY * 3)
        self.medium_figures.get_sprite(FX, FY, FX, FY * 3)
        self.medium_figures.get_sprite(FX, FY, FX * 2, FY * 3)
        self.medium_figures.get_sprite(FX, FY, FX * 3, FY * 3)
        self.medium_figures.get_sprite(FX, FY, 0, FY * 4)
        self.medium_figures.get_sprite(FX, FY, FX, FY * 4)
        self.medium_figures.get_sprite(FX, FY, FX * 2, FY * 4)
        self.hard_figures.sprites = self.medium_figures.sprites
        self.hard_figures.get_sprite(FX, FY, 0, 0)
        self.hard_figures.get_sprite(FX, FY, FX, 0)
        self.hard_figures.get_sprite(FX, FY, FX * 2, 0)
        self.hard_figures.get_sprite(FX - 1, FY, FX * 3, 0)
        self.hard_figures.get_sprite(FX, FY, 0, FY)
        self.hard_figures.get_sprite(FX, FY, FX, FY)
        self.hard_figures.get_sprite(FX, FY, FX * 2, FY)
        self.hard_figures.get_sprite(FX - 1, FY, FX * 3, FY)
        self.credits_bg.get_sprite(900, 900, 0, 0)
        self.credits_bg.get_sprite(900, 900, 900, 0)
        self.credits_bg.get_sprite(900, 900, 0, 900)

    # shows the medal earned
    def victory(self):
        draw_img(victory_bg)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.reset(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if 35 <= mouse_pos[0] <= 139 and 461 <= mouse_pos[1] <= 480:
                        self.reset(0)
                        return
                    if 679 <= mouse_pos[0] <= 884 and 461 <= mouse_pos[1] <= 480:
                        self.reset(self.actual_stage + 1)
                        return
        if self.errors == 0:
            draw_img(self.medal.sprites[2], int(450 - AX / 2), int(250 - AY / 2 + 50))
        if self.errors == 1:
            draw_img(self.medal.sprites[1], int(450 - AX / 2), int(250 - AY / 2 + 50))
        if self.errors == 2:
            draw_img(self.medal.sprites[0], int(450 - AX / 2), int(250 - AY / 2 + 50))
        pygame.display.flip()

    def defeat(self):
        draw_img(defeat_bg)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.reset(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        pygame.display.flip()

    # Draws the figure or the mark
    def draw_figure(self, diff):
        i = 0
        k = 0
        if diff == 1:
            diff_figures = self.easy_figures
        elif diff == 2:
            diff_figures = self.medium_figures
        else:
            diff_figures = self.hard_figures
        while i < 3:
            j = 0
            while j < 3:
                if not self.card.guessed[k]:
                    draw_img(diff_figures.sprites[self.card.boxes[k]], int(GX[j] + 49 - 162 / 2), int(GY[i] + 49 - 162 / 2))
                else:
                    draw_img(self.mark.sprites[0], int(GX[j] + 49 - 162 / 2), int(GY[i] + 49 - 162 / 2))
                j += 1
                k += 1
            i += 1

    # show credits
    def credits(self, y):
        self.credits_bg.update(0.5)
        draw_img(self.credits_bg.image, 0, -20)
        draw_img(credits_img, 0, y)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stage = 0  # returns to menu
                return 0
        if y == -2480:
            y = 0
            self.stage = 0
        else:
            y += -.8
        clock.tick(30)
        return y

    # main menu
    def menu(self):
        draw_img(menu_bg)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if 700 <= mouse_pos[0] <= 875 and 289 <= mouse_pos[1] <= 320:
                        self.stage = 1  # takes to level 1
                    if 608 <= mouse_pos[0] <= 875 and 348 <= mouse_pos[1] <= 377:
                        self.stage = 4  # takes to credits
                    if 720 <= mouse_pos[0] <= 875 and 405 <= mouse_pos[1] <= 433:
                        return False
                    if 166 <= mouse_pos[0] <= 282 and 185 <= mouse_pos[1] <= 497:
                        self.stage = 2
        pygame.display.flip()
        clock.tick(30)
        return True

    # level 1
    def level_1(self):
        draw_img(level1_bg)
        self.card.fill_boxes(0)
        self.fill_figures(0, 8, 1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.reset(0)
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if 476 <= mouse_pos[0] <= 574 and 102 <= mouse_pos[1] <= 200:
                        self.check_figure(0)
                    if 591 <= mouse_pos[0] <= 689 and 102 <= mouse_pos[1] <= 200:
                        self.check_figure(1)
                    if 707 <= mouse_pos[0] <= 805 and 102 <= mouse_pos[1] <= 200:
                        self.check_figure(2)
                    if 476 <= mouse_pos[0] <= 574 and 222 <= mouse_pos[1] <= 320:
                        self.check_figure(3)
                    if 591 <= mouse_pos[0] <= 689 and 222 <= mouse_pos[1] <= 320:
                        self.check_figure(4)
                    if 707 <= mouse_pos[0] <= 805 and 222 <= mouse_pos[1] <= 320:
                        self.check_figure(5)
                    if 476 <= mouse_pos[0] <= 574 and 342 <= mouse_pos[1] <= 440:
                        self.check_figure(6)
                    if 591 <= mouse_pos[0] <= 689 and 342 <= mouse_pos[1] <= 440:
                        self.check_figure(7)
                    if 707 <= mouse_pos[0] <= 805 and 342 <= mouse_pos[1] <= 440:
                        self.check_figure(8)
        if self.corrects == 9:
            self.stage = 5  # takes to victory
            return
        if self.errors == 3:
            self.stage = 6
            return
        self.panda.update(0.08)
        draw_img(self.panda.image)
        draw_img(font.render(f'{figures[self.figures[self.actual_figure]]}', False, (255, 255, 255)), 0, 300)
        self.draw_figure(1)
        clock.tick(30)
        pygame.display.flip()

    # level 2
    def level_2(self):
        draw_img(level2_bg)
        self.card.fill_boxes(1)
        self.fill_figures(0, 18, 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.reset(0)
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if 476 <= mouse_pos[0] <= 574 and 102 <= mouse_pos[1] <= 200:
                        self.check_figure(0)
                    if 591 <= mouse_pos[0] <= 689 and 102 <= mouse_pos[1] <= 200:
                        self.check_figure(1)
                    if 707 <= mouse_pos[0] <= 805 and 102 <= mouse_pos[1] <= 200:
                        self.check_figure(2)
                    if 476 <= mouse_pos[0] <= 574 and 222 <= mouse_pos[1] <= 320:
                        self.check_figure(3)
                    if 591 <= mouse_pos[0] <= 689 and 222 <= mouse_pos[1] <= 320:
                        self.check_figure(4)
                    if 707 <= mouse_pos[0] <= 805 and 222 <= mouse_pos[1] <= 320:
                        self.check_figure(5)
                    if 476 <= mouse_pos[0] <= 574 and 342 <= mouse_pos[1] <= 440:
                        self.check_figure(6)
                    if 591 <= mouse_pos[0] <= 689 and 342 <= mouse_pos[1] <= 440:
                        self.check_figure(7)
                    if 707 <= mouse_pos[0] <= 805 and 342 <= mouse_pos[1] <= 440:
                        self.check_figure(8)
                    if 92 <= mouse_pos[0] <= 306 and 460 <= mouse_pos[1] <= 477:
                        self.check_figure(-1)
        if self.corrects == 9:
            self.stage = 5  # takes to victory
            return
        if self.errors == 3:
            self.stage = 6
            return
        self.tiger.update(0.08)
        draw_img(self.tiger.image)
        draw_img(font.render(f'{figures[self.figures[self.actual_figure]]}', False, (255, 255, 255)), 0, 300)
        if 10 <= self.figures[self.actual_figure] <= 13:
            draw_img(font.render(f'{triangles[self.figures[self.actual_figure] % 10] }', False, (255, 255, 255)), 0, 350)
        self.draw_figure(2)
        clock.tick(30)
        pygame.display.flip()

    def level_3(self):
        draw_img(level3_bg)
        self.card.fill_boxes(2)
        self.fill_figures(0, 26, 3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.reset(0)
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if 476 <= mouse_pos[0] <= 574 and 102 <= mouse_pos[1] <= 200:
                        self.check_figure(0)
                    if 591 <= mouse_pos[0] <= 689 and 102 <= mouse_pos[1] <= 200:
                        self.check_figure(1)
                    if 707 <= mouse_pos[0] <= 805 and 102 <= mouse_pos[1] <= 200:
                        self.check_figure(2)
                    if 476 <= mouse_pos[0] <= 574 and 222 <= mouse_pos[1] <= 320:
                        self.check_figure(3)
                    if 591 <= mouse_pos[0] <= 689 and 222 <= mouse_pos[1] <= 320:
                        self.check_figure(4)
                    if 707 <= mouse_pos[0] <= 805 and 222 <= mouse_pos[1] <= 320:
                        self.check_figure(5)
                    if 476 <= mouse_pos[0] <= 574 and 342 <= mouse_pos[1] <= 440:
                        self.check_figure(6)
                    if 591 <= mouse_pos[0] <= 689 and 342 <= mouse_pos[1] <= 440:
                        self.check_figure(7)
                    if 707 <= mouse_pos[0] <= 805 and 342 <= mouse_pos[1] <= 440:
                        self.check_figure(8)
                    if 166 <= mouse_pos[0] <= 282 and 185 <= mouse_pos[1] <= 497:
                        self.check_figure(-1)
        if self.corrects == 9:
            self.stage = 5  # takes to victory
            return
        if self.errors == 3:
            self.stage = 6
            return
        self.sloth.update(0.08)
        draw_img(self.sloth.image)
        draw_img(font.render(f'{figures[self.figures[self.actual_figure]]}', False, (255, 255, 255)), 0, 300)
        if 10 <= self.figures[self.actual_figure] <= 13:
            draw_img(font.render(f'{triangles[self.figures[self.actual_figure] % 10]}', False, (255, 255, 255)), 0, 350)
        if 25 <= self.figures[self.actual_figure] <= 26:
            draw_img(font.render(f'{prism[self.figures[self.actual_figure] % 20]}', False, (255, 255, 255)), 0, 350)
        self.draw_figure(2)
        clock.tick(30)
        pygame.display.flip()


# functions
def draw_img(img, x=0, y=0):
    screen.blit(img, (x, y))


# variables
clock = pygame.time.Clock()
stage = GameStage()


def main():
    y = 0
    run = True
    while run:
        if stage.stage == 0:  # if its menu
            run = stage.menu()
        elif stage.stage == 1:  # if its level 1
            stage.level_1()
        elif stage.stage == 2:  # if its level 2
            stage.level_2()
        elif stage.stage == 3:  # if its level 3
            stage.level_3()
        elif stage.stage == 4:  # if its credits
            y = stage.credits(y)
        elif stage.stage == 5:  # if its victory
            stage.victory()
        elif stage.stage == 6:  # if defeat
            stage.defeat()
    pygame.quit()


if __name__ == '__main__':
    main()
