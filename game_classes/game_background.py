from game_classes.sea import Sea
from user_interface.shared_window import SharedWindow
from pplay.sprite import Sprite
from random import choice, randint
from math import sin
import time

class GameBackground:
    islandborder = 0
    showFps = True
    cannon = None
    cannonShoot = False
    canoonballs = []

    def __init__(self):
        self.tile_size = 64
        self.window = SharedWindow.instance
        self.windowxsize = SharedWindow.instance.width
        self.windowysize = SharedWindow.instance.height
        self.ygridqtt = self.windowysize//self.tile_size + 2
        self.xgridqtt = self.windowxsize//self.tile_size + 2
        self.islandborder = 4*64
        GameBackground.cannon = Sprite("images/game_background/scallywag/canhao3.png", frames=3)
        GameBackground.cannon.set_total_duration(1000)
        self.pirate = Sprite("images/game_background/scallywag/pirate.png", frames=6)
        self.pirate.set_total_duration(1500)

        GameBackground.cannon.set_position(self.islandborder-20-GameBackground.cannon.width, self.windowysize//2-GameBackground.cannon.height//2)
        self.pirate.set_position(GameBackground.cannon.x, GameBackground.cannon.y- self.pirate.height)
        self.objects = []
        self.seagulls = []
        self.lastSeagull = time.time()
        self.seagull_speed = 205
        GameBackground._set_island_border(self.islandborder)
        self.island_animate = 3
        self.island = self._create_island()
        self.sea_background = Sea(-0.3, 0.001)
        self.fps = 0
        self.countfps = 0
        self.lastFps = time.time()

    @classmethod
    def shoot_Cannon(cls, posxalvo,posyalvo):
        cls.cannonShoot = True
        tempo = 0.2
        cls.cannon.set_curr_frame(1)

        ball = Sprite("images/game_background/scallywag/cannonball.png", frames=2)
        posxfinal = posxalvo - ball.width/2
        posyfinal = posyalvo - ball.height/2
        ball.set_total_duration(50)
        ball.set_position(GameBackground.cannon.x + GameBackground.cannon.width,GameBackground.cannon.y + GameBackground.cannon.height//2 - ball.height//2)
        velocidade = ((posxfinal-ball.x)//tempo, (posyfinal-ball.y)//tempo)
        GameBackground.canoonballs.append([ball, velocidade, (posxalvo,posyalvo)])

    def reset(self):
        self.seagulls.clear()
        for line in self.island:
            line.clear()


    @classmethod
    def _set_island_border(cls, border):
        cls.islandborder = border

    def generate_seagull(self):
        if time.time() - self.lastSeagull >= 10:
            self.lastSeagull = time.time()
            self.seagulls.append(Sprite("./assets/seagull_animation.png", frames=8))
            self.seagulls[-1].set_total_duration(1000)
            self.seagulls[-1].set_position(self.windowxsize, randint(0, self.windowysize - self.seagulls[-1].height))

    def move_seagulls(self):
        self.generate_seagull()
        for seag in self.seagulls:
            seag.x -= self.seagull_speed*self.window.delta_time()
            seag.update()
            seag.draw()
            if seag.x < -1*seag.width:
                self.seagulls.remove(seag)

    def printFps(self):
        if GameBackground.showFps:
            self.countfps += 1
            if time.time() - self.lastFps >= 2:
                self.lastFps = time.time()
                self.fps = self.countfps
                self.countfps = 0
            SharedWindow.draw_text(SharedWindow.instance, f"Fps: {self.fps}",20, SharedWindow.instance.height-60, 20,(0,0,0), font_name="./fonts/CutePixel.ttf", bold= True  )
        else:
            self.countfps = 0

    def _out_sand_animate(self):
        for line in self.island:
            line[-1].x = self.islandborder + sin(time.time())*self.island_animate*0.3 -64

    def _create_island(self):
        sand_list = []
        for i in range(-1, self.ygridqtt):
            sand_line = []
            for j in range(-1,3):
                sand_path = choice([1,2,3,4,4,4])
                sand = Sprite(f"images/game_background/scallywag/grassfinal{sand_path}.png", frames=1)
                sand.set_position(self.tile_size*j, self.tile_size*i)
                sand_line.append(sand)
            out_sand = Sprite("images/game_background/scallywag/shore2.png",frames=4)
            out_sand.set_total_duration(700)
            out_sand.set_position(self.tile_size*3, self.tile_size*i)
            sand_line.append(out_sand)
            sand_list.append(sand_line)
        treasure = Sprite("images/game_background/scallywag/treasure.png", frames=1)
        treasure.set_position(0, self.pirate.y-treasure.height/2)
        self.objects.append(treasure)
        tree = Sprite("images/game_background/scallywag/finaltree1.png", frames=1)
        tree.set_position(0, self.windowysize-tree.height)
        self.objects.append(tree)
        tree = Sprite("images/game_background/scallywag/finaltree2.png", frames=1)
        tree.set_position(0, self.pirate.y + tree.height)
        self.objects.append(tree)
        tree = Sprite("images/game_background/scallywag/finaltree1.png", frames=1)
        tree.set_position(64, self.pirate.y + 3*tree.height)
        self.objects.append(tree)
        tree = Sprite("images/game_background/scallywag/pedra.png", frames=1)
        tree.set_position(self.islandborder-self.tile_size-40, self.pirate.y + 2*tree.height)
        self.objects.append(tree)
        return sand_list

    def _sand_draw(self):
        #self._out_sand_animate()

        for line in self.island:
            for sand_tile in line:
                sand_tile.draw()
                if sand_tile.total_frames>1:
                    sand_tile.update()

    def _sea_draw(self):
        self.sea_background()

    def _points_draw(self, pontos):
        SharedWindow.draw_text(SharedWindow.instance,str(pontos), 20, SharedWindow.instance.height-30, 40,(0,0,0), font_name="./fonts/CutePixel.ttf", bold= True )

    def draw_cannon(self):
        self.pirate.draw()
        self.pirate.update()
        if GameBackground.cannon is not None:

            GameBackground.cannon.draw()
            if GameBackground.cannonShoot:
                GameBackground.cannon.update()
                if GameBackground.cannon.curr_frame == 0:
                    GameBackground.cannonShoot = False
                    GameBackground.cannon.set_curr_frame(0)
            for item in GameBackground.canoonballs:
                item[0].draw()
                item[0].x += item[1][0] * self.window.delta_time()
                item[0].y += item[1][1] * self.window.delta_time()
                if item[0].x >= item[2][0]:
                    GameBackground.canoonballs.remove(item)
                if item[0].curr_frame == 0:
                    item[0].update()

    def draw_objects(self):
        for obj in self.objects:
            obj.draw()
    def __call__(self, pontos):
        self._sea_draw()
        self._sand_draw()


        self.draw_objects()
        self.printFps()
        self._points_draw(pontos)
        self.draw_cannon()
        self.move_seagulls()
