import pygame
from pygame.locals import *
import os
import random
import sys

SCR_RECT = Rect(0, 0, 640, 480)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"InvaderGame")

    # サウンドのロード
    Player.shot_sound = load_sound("shot.wav")
    # スプライトグループを作成して登録
    all = pygame.sprite.RenderUpdates()
    Player.containers = all
    Shot.containers = all
    Alien.containers = all
    # スプライトの画像を登録
    Player.image = load_image("player.png")
    Shot.image = load_image("shot.png")
    Alien.images = split_image(load_image("alien.png"), 2)

    # 自機を作成
    Player()

    # エイリアンを作成
    for i in range(0, 50):
        x = 20 + (i % 10) * 40
        y = 20 + (i // 10) * 40
        Alien((x,y))

    clock = pygame.time.Clock()
    while True:
        #1秒間に60フレーム以下で実行
        clock.tick(60)
        #スクリーン（背景）を黒で塗り潰し
        screen.fill((0, 0, 0))
        #スプライトを更新
        all.update()
        all.draw(screen)
        pygame.display.update()
        #何らかのイベント処理
        for event in pygame.event.get():
            #閉じるボタンがクリックされたとき
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #ESCキーが押されたとき
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

#プレイヤーのクラスの定義
class Player(pygame.sprite.Sprite):
    """自機"""
    speed = 5  # 移動速度
    reload_time = 15  # リロード時間
    def __init__(self):
        # imageとcontainersはmain()でセットされる
        pygame.sprite.Sprite.__init__(self, self.containers)
        #プレイヤーの大きさを画像の大きさに設定
        self.rect = self.image.get_rect()
        # プレイヤーが画面の一番下
        self.rect.bottom = SCR_RECT.bottom
        #リロードのタイマーを宣言
        self.reload_timer = 0
    def update(self):
        # 押されているキーをチェック
        pressed_keys = pygame.key.get_pressed()
        # 押されているキーに応じてプレイヤーを移動
        if pressed_keys[K_LEFT]:
            #マイナスx（つまり左に）speed分、yに0移動
            self.rect.move_ip(-self.speed, 0)
        elif pressed_keys[K_RIGHT]:
            #プラスx（つまり右に）speed分、yに0移動
            self.rect.move_ip(self.speed, 0)
        self.rect.clamp_ip(SCR_RECT)
        # ミサイルの発射
        if pressed_keys[K_SPACE]:
            # リロード時間が0になるまで再発射できない
            if self.reload_timer > 0:
                # リロード中
                self.reload_timer -= 1
            else:
                # 発射！！！
                Player.shot_sound.play()
                Shot(self.rect.center)  # 作成すると同時にallに追加される
                self.reload_timer = self.reload_time


class Shot(pygame.sprite.Sprite):
    """プレイヤーが発射するミサイル"""
    speed = 9  # 移動速度
    def __init__(self, pos):
        # imageとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.rect.center = pos  # 中心座標をposに
    def update(self):
        #xに0、マイナスy（つまり上に）speed分移動
        self.rect.move_ip(0, -self.speed)  # 上へ移動
        if self.rect.top < 0:  # 上端に達したら除去
            self.kill()


class Alien(pygame.sprite.Sprite):
    """エイリアン"""
    speed = 2  # 移動速度
    animcycle = 18  # アニメーション速度
    frame = 0
    move_width = 230  # 横方向の移動範囲
    def __init__(self, pos):
        # imagesとcontainersはmain()でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        #指定された（x,y）に
        self.rect.center = pos
         # 移動できる左端
        self.left = pos[0]
        # 移動できる右端
        self.right = self.left + self.move_width
    def update(self):
        # 横方向への移動
        #プラスx（つまり右に）speed分、yに0移動
        self.rect.move_ip(self.speed, 0)
        #もし移動できる右端or左端に来たら、speedの符号を入れ替え（つまり移動方向左右反転）
        if self.rect.center[0] < self.left or self.rect.center[0] > self.right:
            self.speed = -self.speed
        # キャラクターアニメーション
        self.frame += 1
        self.image = self.images[int(self.frame/self.animcycle%2)]


#----------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------#
#--------------------------------------以下今回は無視します--------------------------------------#
#----------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------#

#プレイヤーの画像をロード
def load_image(filename, colorkey=None):
    """画像をロードして画像と矩形を返す"""
    filename = os.path.join("data", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image:", filename)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image

def split_image(image, n):
    """横に長いイメージを同じ大きさのn枚のイメージに分割
    分割したイメージを格納したリストを返す"""
    image_list = []
    w = image.get_width()
    h = image.get_height()
    w1 = int(w / n)
    for i in range(0, w, w1):
        surface = pygame.Surface((w1,h))
        surface.blit(image, (0,0), (i,0,w1,h))
        surface.set_colorkey(surface.get_at((0,0)), RLEACCEL)
        surface.convert()
        image_list.append(surface)
    return image_list

def load_sound(filename):
    filename = os.path.join("data", filename)
    return pygame.mixer.Sound(filename)

if __name__ == "__main__":
    main()
