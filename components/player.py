import pygame as pg
import os
import config
import math
base_dir = os.path.dirname(os.path.dirname(__file__))  # 从components目录回到主目录
image_path = os.path.join(base_dir, 'static', 'img', 'car.png')
crash_audio_path = os.path.join(base_dir, 'static', 'audio', 'crash.mp3')
move_audio_path = os.path.join(base_dir, 'static', 'audio', 'move.mp3')

class Player(pg.sprite.Sprite):
    def __init__(self, player_center_x, player_center_y, player_angle):
        super().__init__()
        # 小车的状态
        self.width = config.PLAYER_WIDTH
        self.height = config.PLAYER_HEIGHT
        self.angle = player_angle  # 车头与x轴正方向的夹角 ****
        # self.image_src = pg.image.load("../static/img/car.png").convert()  # 把原图存下来
        self.image_src = pg.image.load(image_path).convert()
        self.image = pg.transform.scale(self.image_src, (self.width, self.height))
        self.image = pg.transform.rotate(self.image, -self.angle)
        self.image.set_colorkey("black")
        self.rect = self.image.get_rect()
        self.rect.center = (player_center_x, player_center_y)  # 中心坐标 ****
        self.last_time = pg.time.get_ticks()  # 返回当前时刻; 单位是毫秒
        self.delta_time = 0  # 两针之间的时间间隔

        # 直线移动
        self.velocity_forward_lim = 600
        self.velocity_backward_lim = 200
        self.velocity = 0
        self.acceleration = 300
        self.friction = 0.99
        self.velocity_signal = 0
        # XXXX self.velocity_signal = 1
        # XXXX if self.velocity < 0: self.velocity_signal = -1  # 判断是前进还是倒车
        # 这两段逻辑不能写在 __init__ 函数中, 因为这样, 它们只会被执行一次 (在实例化类的时候)

        # 转弯
        self.rotate_velocity = 0  # 角速度, 即每秒转动多少角度
        self.rotate_velocity_lim = 120

        # 音效
        self.crash_audio = pg.mixer.Sound(crash_audio_path)
        self.crash_audio.set_volume(0.2)
        self.move_audio = pg.mixer.Sound(move_audio_path)
        self.move_audio.set_volume(0.2)
        self.move_audio_channel = pg.mixer.Channel(7)


    def update_delta_time(self):
        current_time = pg.time.get_ticks()
        self.delta_time = (current_time - self.last_time) / 1000  #将单位变成毫秒
        self.last_time = current_time

    def input(self):
        key_pressed = pg.key.get_pressed()  # 返回一个字典
        # 前进后退输入
        if key_pressed[pg.K_w]:  # 运行时要英文输入法
            if not self.move_audio_channel.get_busy(): self.move_audio_channel.play(self.move_audio)
            self.velocity += self.acceleration * self.delta_time
            self.velocity = min(self.velocity, self.velocity_forward_lim)  # 正向速度不超限
        elif key_pressed[pg.K_s]:
            if not self.move_audio_channel.get_busy(): self.move_audio_channel.play(self.move_audio)
            self.velocity -= self.acceleration * self.delta_time
            self.velocity = max(self.velocity, -self.velocity_backward_lim)  # 反向速度不超限
        else:
            if self.move_audio_channel.get_busy(): self.move_audio_channel.stop()
            self.velocity = int(self.friction * self.velocity)

        # 转向输入
        self.velocity_signal = 1
        if self.velocity < 0: self.velocity_signal = -1  # 判断是前进还是倒车
        if key_pressed[pg.K_d]:
            self.rotate_velocity = self.rotate_velocity_lim * self.velocity_signal
        elif key_pressed[pg.K_a]:
            self.rotate_velocity = - self.rotate_velocity_lim * self.velocity_signal
        else:
            self.rotate_velocity = 0

    def rotate(self):
        self.angle += self.rotate_velocity * self.delta_time
        self.image = pg.transform.scale(self.image_src, (self.width, self.height))
        self.image = pg.transform.rotate(self.image, -self.angle)
        self.image.set_colorkey("black")
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def move(self):
        vx = self.velocity * math.cos(math.pi * self.angle / 180)
        vy = self.velocity * math.sin(math.pi * self.angle / 180)
        self.rect.x += vx * self.delta_time
        self.rect.y += vy * self.delta_time

        if abs(self.velocity) > 60: self.rotate()  # 当速度绝对值超过60才可以转弯

    def crash(self):
        self.crash_audio.play()
        # self.velocity = - 0.8 * self.velocity  # 碰撞时, 速度反向; 但是这样写, 持续碰撞后, 速度趋于零, 不动了, 优化成以下写法
        self.velocity = - 0.5 * self.velocity_signal * max(abs(self.velocity), self.velocity_backward_lim)
        self.move()

    def update(self):  # 更新下一帧小车的位置
        self.update_delta_time()
        self.input()
        self.move()


