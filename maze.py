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

        self.load_sizes()

        self._rect = pg.shapes.Rectangle(self._plan // 10 - self._compensator, self._plan // 10 - self._compensator, self._b, self._b,
                                            color = (30, 30, 30),
                                            batch = self._batch)

        pg.clock.schedule_interval(self.update, 1/120)

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
        self._compensator = (self._plan // 10) // 2

    def resize_repos(self):
        self.load_sizes()

        self._rect.x = self._plan // 10 - self._compensator + self._paddingX
        self._rect.y = self._plan // 10 - self._compensator + self._paddingY

        self._rect.width = self._b 
        self._rect.height = self._b

    def border_collision(self, rect):
        if rect.x <= self._paddingX + self._compensator:
            rect.x = self._paddingX + self._compensator

        if rect.x >= self.width - self._paddingX - self._compensator - rect.width:
            rect.x = self.width - self._paddingX - self._compensator - rect.width

        if rect.y <= self._paddingY + self._compensator:
            rect.y = self._paddingY + self._compensator
        
        if rect.y >= self.height - self._paddingY - self._compensator - rect.height:
            rect.y = self.height - self._paddingY - self._compensator - rect.height

    def update(self, dt):
        if self._keyRight:
            self._rect.x += 1

        if self._keyLeft:
            self._rect.x -= 1

        if self._keyUp:
            self._rect.y += 1

        if self._keyDown:
            self._rect.y -= 1
        
        self.border_collision(self._rect)

    def on_draw(self):
        self.clear()
        self._batch.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol in [pg.window.key.LEFT, pg.window.key.RIGHT, pg.window.key.DOWN, pg.window.key.UP, pg.window.key.NUM_0, pg.window.key.SPACE]:
            if symbol == pg.window.key.LEFT: self._keyLeft = True

            if symbol == pg.window.key.UP: self._keyUp = True

            if symbol == pg.window.key.DOWN: self._keyDown = True

            if symbol == pg.window.key.RIGHT: self._keyRight = True

    def on_key_release(self, symbol, modifiers):
        if symbol in [pg.window.key.LEFT, pg.window.key.RIGHT, pg.window.key.DOWN, pg.window.key.UP, pg.window.key.NUM_0, pg.window.key.SPACE]:
            if symbol == pg.window.key.LEFT: self._keyLeft = False

            if symbol == pg.window.key.UP: self._keyUp = False

            if symbol == pg.window.key.DOWN: self._keyDown = False

            if symbol == pg.window.key.RIGHT: self._keyRight = False

    def on_resize(self, width, height):
        self.resize_repos()

        return super().on_resize(width, height)

if __name__ == '__main__':
    window = App(resizable = True)
    pg.app.run()
