from urpyg import *
import socket, time, threading

class Player1:
    y = 750 / 2 - 100

class Player2:
    y = 750 / 2 - 100

class Ball:
    x = 1000 / 2
    y = 750 / 2

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

        self.enemy.y = Player2.y
        Player1.y = self.player.y
        Ball.x = self.ball.x
        Ball.y = self.ball.y

    def render(self):
        self.ball.render()
        self.player.render()
        self.enemy.render()
        self.point_lbl.render()
        self.line_sep.draw()

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((input('ip: '), 8080))
    sock.listen()
    conn, addr = sock.accept()
    def sock_thread_func():
        while 1:
            data = conn.recv(1024).decode()
            if not data:
                quit()
            Player2.y = float(data)
            conn.sendall((str(Player1.y) + ' ' + str(Ball.x) + ' ' + str(Ball.y)).encode())
            time.sleep(1 / 60)
    sock_thread = threading.Thread(target = sock_thread_func)
    sock_thread.start()
    PongGame(resizable = False, width = 1000, height = 750).run()
