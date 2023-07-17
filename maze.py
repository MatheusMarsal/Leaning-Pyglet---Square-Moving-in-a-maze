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

        self._rect = pg.shapes.Rectangle(30, 30, 100, 100,
                                            color = (30, 30, 30),
                                            batch = self._batch)

        pg.clock.schedule_interval(self.update, 1/120)

    def border_collision(self, rect):
        if rect.x <= 0:
            rect.x = 0

        if rect.x >= self.width - rect.width:
            rect.x = self.width - rect.width

        if rect.y <= 0:
            rect.y = 0
        
        if rect.y >= self.height - rect.height:
            rect.y = self.height - rect.height

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

if __name__ == '__main__':
    window = App(resizable = True)
    pg.app.run()
