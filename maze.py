from random import randint
import pyglet as pg

class App(pg.window.Window):
    def __init__(self, *args, **kwards):
        super().__init__(*args, **kwards)
        
        self._batch = pg.graphics.Batch()

        self._style = self.WINDOW_STYLE_OVERLAY
        self.set_location(0, 30)

        self._keyLeft = False
        self._keyUp = False
        self._keyDown = False
        self._keyRight = False

        self._COLOR_WHITE = (255, 255, 255)
        self._COLOR_BLACK = (0, 0, 0)

        self._colorH = self._COLOR_BLACK
        self._colorV = self._COLOR_BLACK

        self._pillarsH = []
        self._pillarsV = []

        self.load_sizes()

        self._rect = pg.shapes.Rectangle(self._plan // 10 - self._compensator, self._plan // 10 - self._compensator, self._b, self._b,
                                            color = (30, 30, 30),
                                            batch = self._batch)

        self._rect_coords = {'x' : 0, 'y' : 0}

        for counterY in range(11):
            lineH = []
            lineV = []

            for counterX in range(10):
                if counterY == 0 or counterY == 10: self._colorH = self._COLOR_WHITE
                else: self._colorH = self._COLOR_BLACK

                if counterX == 0 and counterY < 10 or counterY == 10: self._colorV = self._COLOR_WHITE
                else: self._colorV = self._COLOR_BLACK

                lineH.append(pg.shapes.Rectangle((self._plan * counterX) - self._compensator + self._paddingX, (self._plan * counterY) - self._compensator + self._paddingY, self._plan, self._plan // 10,
                                                    color = self._colorH,
                                                    batch = self._batch))

                if counterY == 10:
                    pivotY = counterY
                    pivotX = counterX
                    counterY = counterX
                    counterX = 10

                lineV.append(pg.shapes.Rectangle((self._plan * counterX) - self._compensator + self._paddingX, (self._plan * counterY) - self._compensator + self._paddingY, self._plan // 10, self._plan,
                                                    color = self._colorV,
                                                    batch = self._batch))

                if counterX == 10:
                    counterX = pivotX
                    counterY = pivotY

            self._pillarsH.append(lineH)
            self._pillarsV.append(lineV)

        self.sheduler_make_maze()

    def sheduler_make_maze(self):
        self._clock_counter = 0
        pg.clock.schedule_interval(self.try_make_a_maze, .1)

    def try_make_a_maze(self, dt):
        self._pillarsH[randint(1, 9)][randint(0, 9)].color = (0, 0, 0, 0)
        self._pillarsV[randint(0, 9)][randint(1, 9)].color = (0, 0, 0, 0)

        self._clock_counter += 1

        if self._clock_counter >= 100:
            pg.clock.unschedule(self.try_make_a_maze)

    def load_sizes(self):
        if self.width < self.height: 
            self._plan = self.width // 10
            self._paddingX = (self.width % 10) // 2
            self._paddingY = (self.height - self.width) // 2

        else: 
            self._plan = self.height // 10
            self._paddingX = (self.width - self.height) // 2
            self._paddingY = (self.height % 10) // 2

        self._b = self._plan - (self._plan // 10)
        self._compensator = (self._plan // 10) / 2

    def resize_repos(self):
        self.load_sizes()

        self.move_rect()

        self._rect.width = self._b 
        self._rect.height = self._b

        counterY = 0
        for pillars in self._pillarsH: 
            counterX = 0

            for pillar in pillars:
                pillar.x = (self._plan * counterX) - self._compensator + self._paddingX
                pillar.y = (self._plan * counterY) - self._compensator + self._paddingY

                pillar.width = self._plan 
                pillar.height = self._plan // 10
                
                counterX += 1

            counterY += 1

        counterY = 0
        for pillars in self._pillarsV: 
            counterX = 0

            for pillar in pillars:
                if counterY == 10:
                    pivotY = counterY
                    pivotX = counterX
                    counterY = counterX
                    counterX = 10
                    
                pillar.x = (self._plan * counterX) - self._compensator + self._paddingX
                pillar.y = (self._plan * counterY) - self._compensator + self._paddingY

                pillar.width = self._plan // 10
                pillar.height = self._plan
                
                if counterX == 10:
                    counterX = pivotX
                    counterY = pivotY
                
                counterX += 1

            counterY += 1

    def on_draw(self):
        self.clear()
        self._batch.draw()

    def move_rect(self):
        self._rect.x = self._paddingX + self._compensator + self._rect_coords['x'] * (self._compensator * 2 + self._rect.width)
        self._rect.y = self._paddingY + self._compensator + self._rect_coords['y'] * (self._compensator * 2 + self._rect.height)

    def on_key_press(self, symbol, modifiers):
        if symbol in [pg.window.key.LEFT, pg.window.key.RIGHT, pg.window.key.DOWN, pg.window.key.UP, pg.window.key.NUM_0, pg.window.key.ENTER]:
            if symbol == pg.window.key.LEFT:
                if self._rect_coords['x'] > 0:
                    if self._pillarsV[self._rect_coords['y']][self._rect_coords['x']].color[3] == 0:
                        self._rect_coords['x'] -= 1
                        self.move_rect()

            if symbol == pg.window.key.UP:
                if self._rect_coords['y'] < 9:
                    if self._pillarsH[self._rect_coords['y'] + 1][self._rect_coords['x']].color[3] == 0:
                        self._rect_coords['y'] += 1
                        self.move_rect()

            if symbol == pg.window.key.DOWN:
                if self._rect_coords['y'] > 0:
                    if self._pillarsH[self._rect_coords['y']][self._rect_coords['x']].color[3] == 0:
                        self._rect_coords['y'] -= 1
                        self.move_rect()

            if symbol == pg.window.key.RIGHT:
                if self._rect_coords['x'] < 9:
                    if self._pillarsV[self._rect_coords['y']][self._rect_coords['x'] + 1].color[3] == 0:
                        self._rect_coords['x'] += 1
                        self.move_rect()

            if symbol == pg.window.key.NUM_0:
                pg.clock.unschedule(self.try_make_a_maze)
                
                for counter0_9 in range(10):
                    for counter1_9 in range(1, 10, 1):
                        self._pillarsH[counter1_9][counter0_9].color = (0, 0, 0, 0)
                        self._pillarsV[counter0_9][counter1_9].color = (0, 0, 0, 0)
            
            if symbol == pg.window.key.ENTER:
                pg.clock.unschedule(self.try_make_a_maze)
                
                for counter0_9 in range(10):
                    for counter1_9 in range(1, 10, 1):
                        self._pillarsH[counter1_9][counter0_9].color = (0, 0, 0, 255)
                        self._pillarsV[counter0_9][counter1_9].color = (0, 0, 0, 255)

                self.sheduler_make_maze()

    def on_resize(self, width, height):
        self.resize_repos()

        return super().on_resize(width, height)

if __name__ == '__main__':
    window = App(resizable = True)
    pg.app.run()
