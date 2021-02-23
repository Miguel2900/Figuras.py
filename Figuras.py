import pygame
import random

# screen parameters
SIZE = (900, 500)
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('MIS PRIMERAS FIGURAS')
pygame.display.set_icon(pygame.image.load('logo.png'))
pygame.init()


# images
menu_bg = pygame.image.load('MenuPrincipal.png')  # image for the menu background
level1_bg = pygame.image.load('Facil.png')  # image for the level 1 background
level2_bg = pygame.image.load('Medio.png')  # image for the level 2 background
level3_bg = pygame.image.load('Dificil.png')  # image for the level 3 background
victory_bg = pygame.image.load('PantallaGanado.png')  # image for the victory background
defeat_bg = pygame.image.load('PantallaPerdido.png')  # image for the defeat background
credits_img = pygame.image.load('TextoCreditos.png')  # image for the credits background
rules_bg = pygame.image.load('Reglas.png') # images for the rules background

#sounds
click = pygame.mixer.Sound('click_sound.wav')
click.set_volume(.3)
correct = pygame.mixer.Sound('correct_sound.wav')
error = pygame.mixer.Sound('error_sound.wav')
error.set_volume(.3)
victory = pygame.mixer.Sound('victory_sound.wav')
defeat = pygame.mixer.Sound('defeat_sound.wav')

# font
font = pygame.font.Font('Pixelmania.ttf', 25)  # font used for displaying the figures names

# banks of figure names
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
        self.current_sprite = 0  # id for current sprite

    # obtains sprites from the sheet
    def get_sprite(self, width, height, x, y):
        self.sprites.append(self.image.subsurface(x, y, width, height))  # adds cut images to the list of sprites

    # updates sprites and changes the image
    def update(self, speed, skip=0):
        if skip == 0:  # used when trying to skip the last frames on music and sound options
            length = len(self.sprites)
        else:
            length = len(self.sprites) - 1
        self.current_sprite += speed
        if self.current_sprite >= length:
            self.current_sprite = 0
        self.image = self.sprites[int(self.current_sprite)]  # stores the image to print it


class Card:
    def __init__(self):
        self.boxes = []  # list of the boxes
        self.ready = True  # determines if its ready to be filled the list again
        self.guessed = []  # list of guessed figures

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
                if rn not in self.boxes:  # stores only different values
                    self.boxes.append(rn)
                    self.guessed.append(False)  # Fills the guessed list of False values
                    j += 1
            self.ready = False  # not ready to be filled with random values


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
        self.stage = 0  # control which stage is displayed
        self.actual_stage = 0  # saves the stage when another is called
        self.card = Card()  # creating a card object
        self.all_figures = SpriteSheet('Figuras1.png')  # object for all figures pictures
        self.tiger = SpriteSheet('animals.png')  # object for tiger pictures
        self.panda = SpriteSheet('animals.png')  # object for panda pictures
        self.sloth = SpriteSheet('animals.png')  # object for sloth pictures
        self.frog = SpriteSheet('animals.png')  # object for frog pictures
        self.medal = SpriteSheet('animals.png')  # object for medal pictures
        self.mark = SpriteSheet('marks1.png')  # object for mark pictures
        self.lives = []  # list for the lives 
        self.lives.append(SpriteSheet('corazon.png'))
        self.lives.append(SpriteSheet('corazon.png'))
        self.lives.append(SpriteSheet('corazon.png'))
        self.sound_options = SpriteSheet('sound_option.png')  # object for sound options
        self.music_options = SpriteSheet('sound_option.png')  # object for music options
        self.sound_playing = True  # state of sound
        self.music_playing = True  # state of music
        self.credits_bg = SpriteSheet('Fondo_geometrico1.png')  # object for the credits background
        self.figures_ready = True  # determines if figures list is ready to be filled the list again
        self.figures = []  # figures list
        self.corrects = 0  # correct count
        self.errors = 0  # errors count
        self.actual_figure = 0  # id for the figure
        self.get_sprites()  # function to trim and save the different sprites

    # Fills the list figures with random values
    def fill_figures(self, min_value, max_value, stg):
        i = 0
        if self.figures_ready:  # verify if its ready the list to be filled
            self.actual_stage = stg
            while i <= max_value:
                rn = random.randint(min_value, max_value)
                if rn not in self.figures:  # stores only different values
                    self.figures.append(rn)
                    i += 1
            self.figures_ready = False  # not ready to be filled with random values

    # checks if the figure choosen is the same as the one asked
    def check_figure(self, i):
        if i != -1:  # i is the selected box, -1 is next figure button
            if self.card.boxes[i] == self.figures[self.actual_figure]:
                self.actual_figure += 1  # moves to the next figure to guess
                self.corrects += 1
                self.card.guessed[i] = True  # marks if the figures was guessed
                self.play_sound(correct)
                return
        elif self.figures[self.actual_figure] not in self.card.boxes and i == -1:  # checks if the figure skipped -
            # -was not in the card
            self.actual_figure += 1
            self.play_sound(correct)
            return
        self.errors += 1
        self.lives[self.errors - 1].update(1)  # empties the heart figure to represent error made
        draw_img(self.mark.sprites[1], 641 - 250, 271 - 250)
        self.play_sound(error)
        pygame.display.flip()
        pygame.time.delay(1000)
        return

    # reset values in order to proceed
    def reset(self, stg):
        i = 0
        while i < 3:
            if self.lives[i].current_sprite == 1:  # if hearts are empty, refills them
                self.lives[i].update(1)
            i += 1
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

    # toggles the music on and off
    def music_toggle(self):
        if self.music_playing:
            self.music_options.current_sprite = 13 #
            self.music_options.update(1)
            self.music_playing = False
            pygame.mixer.music.pause()
        else:
            self.music_playing = True
            pygame.mixer.music.unpause()

    # toggles the sounds on and off
    def sound_toggle(self):
        if self.sound_playing:
            self.sound_options.current_sprite = 2
            self.sound_options.update(1)
            self.sound_playing = False
        else:
            self.sound_playing = True

    def play_sound(self, sound):
        if self.sound_playing:
            sound.play()

    # shows the medal earned
    def victory(self):
        draw_img(victory_bg)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.reset(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.play_sound(click)
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if 35 <= mouse_pos[0] <= 139 and 461 <= mouse_pos[1] <= 480:
                        self.reset(0)  # if clicked returns to main menu and resets variables
                        return
                    if 679 <= mouse_pos[0] <= 884 and 461 <= mouse_pos[1] <= 480:
                        self.reset(self.actual_stage + 1)  # if clicked goes to next level, credits if it´s 3 level
                        return
        # draws medal according to error value, 0 - gold, 1 - silver, 2 - bronze
        draw_img(self.medal.sprites[(self.errors - 2) * (-1)], int(450 - AX / 2), int(250 - AY / 2 + 50))
        pygame.display.flip()

    # shows the defeat screen
    def defeat(self):
        draw_img(defeat_bg)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.reset(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.play_sound(click)
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if 17 <= mouse_pos[0] <= 121 and 456 <= mouse_pos[1] <= 475:
                        self.reset(0)
                    if 622 <= mouse_pos[0] <= 875 and 456 <= mouse_pos[1] <= 475:
                        self.reset(self.actual_stage)
        pygame.display.flip()

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
        if y == -2480: # stops drawing the image
            y = 0
            self.reset(0)  # returns to menu
        else:
            y += -.8
        clock.tick(30)
        return y

    # Draws the figure or the mark
    def draw_figure(self):
        i = 0
        k = 0
        x = 323
        while i < 3:
            j = 0
            draw_img(self.lives[i].image, x, 10)
            while j < 3:
                if not self.card.guessed[k]:
                    draw_img(self.all_figures.sprites[self.card.boxes[k]], int(GX[j] + 49 - 162 / 2),
                             int(GY[i] + 49 - 162 / 2))  # draws the corresponding image in the box
                else:  # if the figure in the box has been guessed, it´s replaces by a check mark
                    draw_img(self.mark.sprites[0], int(GX[j] + 49 - 162 / 2), int(GY[i] + 49 - 162 / 2))
                j += 1
                k += 1
            i += 1
            x += 35

    # draws the rules page
    def rules(self):
        draw_img(rules_bg)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stage = 0
                self.reset(0)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.play_sound(click)
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if 693 <= mouse_pos[0] <= 878 and 462 <= mouse_pos[1] <= 481:
                        self.stage = 1
        pygame.display.flip()

    #*******************************Main stages***********************************************
    # main menu
    def menu(self):
        draw_img(menu_bg)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.play_sound(click)
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if 700 <= mouse_pos[0] <= 875 and 289 <= mouse_pos[1] <= 320:
                        self.stage = 7  # takes to rules
                    if 608 <= mouse_pos[0] <= 875 and 348 <= mouse_pos[1] <= 377:
                        self.stage = 4  # takes to credits
                    if 720 <= mouse_pos[0] <= 875 and 405 <= mouse_pos[1] <= 433:
                        return False  # returns false to stop main loop
                    # if 166 <= mouse_pos[0] <= 282 and 185 <= mouse_pos[1] <= 497:
                    # self.stage = 2
                    if 796 <= mouse_pos[0] <= 824 and 13 <= mouse_pos[1] <= 47:
                        self.music_toggle()  # toggles music
                    if 856 <= mouse_pos[0] <= 877 and 12 <= mouse_pos[1] <= 47:
                        self.sound_toggle()  # toggles sound
        if self.music_playing:
            self.music_options.update(.5, 1)
        if self.sound_playing:
            self.sound_options.update(.1, 1)
        draw_img(self.music_options.image, 780)
        draw_img(self.sound_options.image, 840)
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
                self.play_sound(click)
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
                    if 10 <= mouse_pos[0] <= 64 and 37 <= mouse_pos[1] <= 64:
                        self.stage = 0
                        self.reset(0)
                        return
                    if 796 <= mouse_pos[0] <= 824 and 13 <= mouse_pos[1] <= 47:
                        self.music_toggle()
                    if 856 <= mouse_pos[0] <= 877 and 12 <= mouse_pos[1] <= 47:
                        self.sound_toggle()
        if self.corrects == 9:
            self.stage = 5  # takes to victory
            self.play_sound(victory)
            return
        if self.errors == 3:
            self.stage = 6
            self.play_sound(defeat)
            return
        self.panda.update(0.08)
        if self.music_playing:
            self.music_options.update(.5, 1)
        if self.sound_playing:
            self.sound_options.update(.1, 1)
        draw_img(self.panda.image, int(450 / 2 - AX / 2), 70)
        draw_img(self.music_options.image, 780)
        draw_img(self.sound_options.image, 840)
        text = font.render(f'{figures[self.figures[self.actual_figure]]}', False, (255, 255, 255))
        draw_img(text, 450 / 2 - text.get_width() / 2, 400)
        self.draw_figure()
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
                self.play_sound(click)
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
                    if 10 <= mouse_pos[0] <= 64 and 37 <= mouse_pos[1] <= 64:
                        self.stage = 0
                        self.reset(0)
                        return
                    if 796 <= mouse_pos[0] <= 824 and 13 <= mouse_pos[1] <= 47:
                        self.music_toggle()
                    if 856 <= mouse_pos[0] <= 877 and 12 <= mouse_pos[1] <= 47:
                        self.sound_toggle()
        if self.corrects == 9:
            self.stage = 5  # takes to victory
            self.play_sound(victory)
            return
        if self.errors == 3:
            self.stage = 6
            self.play_sound(defeat)
        self.tiger.update(0.08)
        if self.music_playing:
            self.music_options.update(.5, 1)
        if self.sound_playing:
            self.sound_options.update(.1, 1)
        draw_img(self.tiger.image, int(450 / 2 - AX / 2))
        draw_img(self.music_options.image, 780)
        draw_img(self.sound_options.image, 840)
        text = font.render(f'{figures[self.figures[self.actual_figure]]}', False, (255, 255, 255))
        draw_img(text, 450 / 2 - text.get_width() / 2, 300)
        if 10 <= self.figures[self.actual_figure] <= 13:
            text = font.render(f'{triangles[self.figures[self.actual_figure] % 10]}', False, (255, 255, 255))
            draw_img(text, 450 / 2 - text.get_width() / 2, 350)
        self.draw_figure()
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
                self.play_sound(click)
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
                    if 10 <= mouse_pos[0] <= 64 and 37 <= mouse_pos[1] <= 64:
                        self.stage = 0
                        self.reset(0)
                        return
                    if 796 <= mouse_pos[0] <= 824 and 13 <= mouse_pos[1] <= 47:
                        self.music_toggle()
                    if 856 <= mouse_pos[0] <= 877 and 12 <= mouse_pos[1] <= 47:
                        self.sound_toggle()
        if self.corrects == 9:
            self.stage = 5  # takes to victory
            self.play_sound(victory)
            return
        if self.errors == 3:
            self.stage = 6
            self.play_sound(defeat)
        self.sloth.update(0.08)
        if self.music_playing:
            self.music_options.update(.5, 1)
        if self.sound_playing:
            self.sound_options.update(.1, 1)
        draw_img(self.sloth.image, int(450 / 2 - AX / 2))
        draw_img(self.music_options.image, 780)
        draw_img(self.sound_options.image, 840)
        text = font.render(f'{figures[self.figures[self.actual_figure]]}', False, (255, 255, 255))
        draw_img(text, 450 / 2 - text.get_width() / 2, 300)
        if 10 <= self.figures[self.actual_figure] <= 13:
            text = font.render(f'{triangles[self.figures[self.actual_figure] % 10]}', False, (255, 255, 255))
            draw_img(text, 450 / 2 - text.get_width() / 2, 350)
        if 25 <= self.figures[self.actual_figure] <= 26:
            text = font.render(f'{prism[self.figures[self.actual_figure] % 20]}', False, (255, 255, 255))
            draw_img(text, 450 / 2 - text.get_width() / 2, 350)
        self.draw_figure()
        clock.tick(30)
        pygame.display.flip()

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
        self.mark.sprites[1] = pygame.transform.scale(self.mark.sprites[1], (500, 500))
        self.all_figures.get_sprite(FX, FY, 0, 0)
        self.all_figures.get_sprite(FX, FY, FX, 0)
        self.all_figures.get_sprite(FX, FY, FX * 2, 0)
        self.all_figures.get_sprite(FX, FY, FX * 3, 0)
        self.all_figures.get_sprite(FX, FY, 0, FY)
        self.all_figures.get_sprite(FX, FY, FX, FY)
        self.all_figures.get_sprite(FX, FY, FX * 2, FY)
        self.all_figures.get_sprite(FX, FY, FX * 3, FY)
        self.all_figures.get_sprite(FX, FY, 0, FY * 2)
        self.all_figures.get_sprite(FX, FY, FX, FY * 2)
        self.all_figures.get_sprite(FX, FY, FX * 2, FY * 2)
        self.all_figures.get_sprite(FX, FY, FX * 3, FY * 2)
        self.all_figures.get_sprite(FX, FY, 0, FY * 3)
        self.all_figures.get_sprite(FX, FY, FX, FY * 3)
        self.all_figures.get_sprite(FX, FY, FX * 2, FY * 3)
        self.all_figures.get_sprite(FX, FY, FX * 3, FY * 3)
        self.all_figures.get_sprite(FX, FY, 0, FY * 4)
        self.all_figures.get_sprite(FX, FY, FX, FY * 4)
        self.all_figures.get_sprite(FX, FY, FX * 2, FY * 4)
        self.all_figures.image = pygame.image.load('Figuras_3d1.png')  # changes to a new image to get sprites
        self.all_figures.get_sprite(FX, FY, 0, 0)
        self.all_figures.get_sprite(FX, FY, FX, 0)
        self.all_figures.get_sprite(FX, FY, FX * 2, 0)
        self.all_figures.get_sprite(FX - 1, FY, FX * 3, 0)
        self.all_figures.get_sprite(FX, FY, 0, FY)
        self.all_figures.get_sprite(FX, FY, FX, FY)
        self.all_figures.get_sprite(FX, FY, FX * 2, FY)
        self.all_figures.get_sprite(FX - 1, FY, FX * 3, FY)
        self.lives[0].get_sprite(42, 42, 0, 0)
        self.lives[0].get_sprite(42, 42, 42, 0)
        self.lives[0].update(0)
        self.lives[1].get_sprite(42, 42, 0, 0)
        self.lives[1].get_sprite(42, 42, 42, 0)
        self.lives[1].update(0)
        self.lives[2].get_sprite(42, 42, 0, 0)
        self.lives[2].get_sprite(42, 42, 42, 0)
        self.lives[2].update(0)
        self.sound_options.get_sprite(64, 64, 0, 0)
        self.sound_options.get_sprite(64, 64, 64, 0)
        self.sound_options.get_sprite(64, 64, 128, 0)
        self.sound_options.get_sprite(64, 64, 192, 0)
        self.music_options.get_sprite(64, 64, 0, 64)
        self.music_options.get_sprite(64, 64, 64, 64)
        self.music_options.get_sprite(64, 64, 128, 64)
        self.music_options.get_sprite(64, 64, 192, 64)
        self.music_options.get_sprite(64, 64, 0, 128)
        self.music_options.get_sprite(64, 64, 64, 128)
        self.music_options.get_sprite(64, 64, 128, 128)
        self.music_options.get_sprite(64, 64, 192, 128)
        self.music_options.get_sprite(64, 64, 0, 192)
        self.music_options.get_sprite(64, 64, 64, 192)
        self.music_options.get_sprite(64, 64, 128, 192)
        self.music_options.get_sprite(64, 64, 192, 192)
        self.music_options.get_sprite(64, 64, 0, 256)
        self.music_options.get_sprite(64, 64, 64, 256)
        self.music_options.get_sprite(64, 64, 128, 256)
        self.credits_bg.get_sprite(900, 900, 0, 0)
        self.credits_bg.get_sprite(900, 900, 900, 0)
        self.credits_bg.get_sprite(900, 900, 0, 900)


# functions
def draw_img(img, x=0, y=0):
    screen.blit(img, (x, y))


# variables
clock = pygame.time.Clock()
stage = GameStage()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.set_volume(.2)
pygame.mixer.music.play(-1)


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
        elif stage.stage == 7:
            stage.rules()
    pygame.quit()


if __name__ == '__main__':
    main()
