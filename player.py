import pygame as pg
import config
import math

class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 小车的状态
        self.width = 100
        self.height = 50
        self.angle = 270  # 车头与x轴正方向的夹角

        # 小车的实现
        self.image_src = pg.image.load("static/img/car.png").convert()  # 把原图存下来
        self.image = pg.transform.scale(self.image_src, (self.width, self.height))
        self.image = pg.transform.rotate(self.image, -self.angle)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.center = (config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2)
        self.last_time = pg.time.get_ticks()  # 返回当前时刻; 单位是毫秒
        self.delta_time = 0  # 两针之间的时间间隔

        # 直线移动
        self.velocity_forward_lim = 400
        self.velocity_backward_lim = 100
        self.velocity = 0
        self.acceleration = 300
        self.friction = 0.99

        # 转弯
        self.rotate_velocity = 0  # 角速度, 即每秒转动多少角度
        self.rotate_velocity_lim = 120


    def update_delta_time(self):
        current_time = pg.time.get_ticks()
        self.delta_time = (current_time - self.last_time) / 1000  #将单位变成毫秒
        self.last_time = current_time

    def input(self):
        key_pressed = pg.key.get_pressed()  # 返回一个字典
        # 前进后退输入
        if key_pressed[pg.K_w]:  # 运行时要英文输入法
            self.velocity += self.acceleration * self.delta_time
            self.velocity = min(self.velocity, self.velocity_forward_lim)  # 正向速度不超限
        elif key_pressed[pg.K_s]:
            self.velocity -= self.acceleration * self.delta_time
            self.velocity = max(self.velocity, -self.velocity_backward_lim)  # 反向速度不超限
        else:
            self.velocity = int(self.friction * self.velocity)

        # 转向输入
        velocity_signal = 1
        if self.velocity < 0: velocity_signal = -1
        if key_pressed[pg.K_d]:
            self.rotate_velocity = self.rotate_velocity_lim * velocity_signal
        elif key_pressed[pg.K_a]:
            self.rotate_velocity = - self.rotate_velocity_lim * velocity_signal
        else:
            self.rotate_velocity = 0

    def rotate(self, direction=1):
        self.angle += self.rotate_velocity * self.delta_time * direction  # 撞墙后 direction 变成 -1
        self.image = pg.transform.scale(self.image_src, (self.width, self.height))
        self.image = pg.transform.rotate(self.image, -self.angle)
        self.image.set_colorkey("black")
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move(self, direction=1):
        if direction == 1 and abs(self.velocity) > 60: self.rotate(direction)  # 当速度超过60才可以转弯 且 当没有发生碰撞时才转弯

        vx = self.velocity * math.cos(math.pi * self.angle / 180) * direction
        vy = self.velocity * math.sin(math.pi * self.angle / 180) * direction
        self.rect.x += vx * self.delta_time
        self.rect.y += vy * self.delta_time

        if direction == -1 and abs(self.velocity) > 60: self.rotate(direction)

    def crash(self):
        self.move(-1)
        self.velocity *= -0.4  # 弹性碰撞
        self.velocity = min(self.velocity, - self.velocity_backward_lim)
        # self.rotate_velocity *= -0.4 # 弹性碰撞

    def update(self):  # 更新下一帧小车的位置
        self.update_delta_time()
        self.input()
        self.move(1)


