from urpyg import *

diffmap = {
    'easy': 150,
    'normal': 175,
    'hard': 200,
    'impossible': 250,
    'op': 400
}

diff = 'normal'

multiplayer = False

class PongGame(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ppoints = 0
        self.epoints = 0
        self.point_lbl = Label('0   0', self.width / 2, self.height - 50, font = ('Times New Roman', 50))
        self.line_sep = pyglet.shapes.Line(self.width / 2, 0, self.width / 2, self.height, 1, color = (255, 255, 255))

    def init(self):
        self.player = Rectangle(self.width - 25, self.height / 2 - 100, 25, 200, color = (255, 255, 255))
        self.enemy = Rectangle(0, self.height / 2 - 100, 25, 200, color = (255, 255, 255))
        self.ball = Rectangle(self.width / 2, self.height / 2, 15, 15, color = (255, 255, 255))
        self.ball.dx = random.choice([-100, 100])
        self.ball.dy = random.choice([-100, 100])

    def update(self, dt):
        if held_keys['escape']:
            quit()

        if self.ball.dx > 0 and self.ball.dx < 275:
            self.ball.dx += .1
        elif self.ball.dx < 0 and self.ball.dx > -275:
            self.ball.dx -= .1
        elif self.ball.dx > 0 and random.randrange(10000) == 0:
            self.ball.dx += 1
        elif self.ball.dx < 0 and random.randrange(10000) == 0:
            self.ball.dx -= 1

        if self.ball.dy > 0 and self.ball.dy < 275:
            self.ball.dy += .1
        elif self.ball.dy < 0 and self.ball.dy > -275:
            self.ball.dy -= .1
        elif self.ball.dy > 0 and random.randrange(1000) == 0:
            self.ball.dy += 1
        elif self.ball.dy < 0 and random.randrange(1000) == 0:
            self.ball.dy -= 1

        if self.ball.y > self.height - self.ball.height:
            self.ball.dy = -self.ball.dy
        elif self.ball.y < 0:
            self.ball.dy = -self.ball.dy

        if held_keys['up arrow']:
            self.player.y += 200 * dt
        if held_keys['down arrow']:
            self.player.y -= 200 * dt
        if multiplayer:
            if held_keys['w']:
                self.enemy.y += 200 * dt
            if held_keys['s']:
                self.enemy.y -= 200 * dt

        if self.ball.is_colliding(self.player):
            self.ball.dx = -self.ball.dx
        elif self.ball.is_colliding(self.enemy):
            self.ball.dx = -self.ball.dx

        if self.ball.x < -15:
            self.init()
            self.ppoints += 1
            self.point_lbl.text = f'{self.epoints}   {self.ppoints}'
        elif self.ball.x > self.width:
            self.init()
            self.epoints += 1
            self.point_lbl.text = f'{self.epoints}   {self.ppoints}'

        self.ball.x += self.ball.dx * dt
        self.ball.y += self.ball.dy * dt

        if not multiplayer:
            if abs(self.ball.dx) < diffmap[diff]:
                self.enemy.move_towards(self.enemy.x, self.ball.y - 93.5, abs(self.ball.dx) * dt)
            else:
                self.enemy.move_towards(self.enemy.x, self.ball.y - 93.5, diffmap[diff] * dt)

    def render(self):
        self.ball.render()
        self.player.render()
        self.enemy.render()
        self.point_lbl.render()
        self.line_sep.draw()

if __name__ == '__main__':
    if (diffcheck := input('Enter difficulty[easy/NORMAL/hard/impossible/op]: ').lower()) != '':
        if diffcheck in ('easy', 'normal', 'hard', 'impossible', 'op'):
            diff = diffcheck
    if (multicheck := input('Multiplayer[y/N]: ').lower()) != '':
        if multicheck in ('y', 'n'):
            if multicheck == 'y': multiplayer = True

    PongGame(resizable = False, width = 1000, height = 750).run()
