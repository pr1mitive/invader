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
    # スプライトの画像を登録
    Player.image = load_image("player.png")
    Shot.image = load_image("shot.png")
    # 自機を作成
    Player()

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


#プレイヤーの画像をロード（今回は無視します）
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

def load_sound(filename):
    filename = os.path.join("data", filename)
    return pygame.mixer.Sound(filename)

if __name__ == "__main__":
    main()
