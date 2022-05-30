from urpyg import *
import socket, threading, time

class Points:
    epoints = 0
    ppoints = 0

class Player1:
    y = 700 / 2 - 100

class Player2:
    y = 700 / 2 - 100

class Ball:
    x = 1000 / 2
    y = 700 / 2

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

    def update(self, dt):
        self.epoints, self.ppoints = Points.epoints, Points.ppoints

        if held_keys['escape']:
            quit()

        if held_keys['up arrow']:
            self.enemy.y += 200 * dt
        if held_keys['down arrow']:
            self.enemy.y -= 200 * dt

        self.point_lbl.text = f'{self.epoints}   {self.ppoints}'

        self.ball.x = Ball.x
        self.ball.y = Ball.y
        Player2.y = self.enemy.y
        self.player.y = Player1.y

    def render(self):
        self.ball.render()
        self.player.render()
        self.enemy.render()
        self.point_lbl.render()
        self.line_sep.draw()

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((input('ip: '), int(input('port: '))))
    def sock_thread_func():
        while 1:
            sock.sendall(str(Player2.y).encode())
            data = sock.recv(1024).decode()
            data = data.split(' ')
            Player1.y = float(data[0])
            Ball.x = float(data[1])
            Ball.y = float(data[2])
            Points.ppoints = int(data[3])
            Points.epoints = int(data[4])
            time.sleep(1 / 60)
    sock_thread = threading.Thread(target = sock_thread_func)
    sock_thread.start()
    PongGame(resizable = False, width = 1000, height = 700).run()
