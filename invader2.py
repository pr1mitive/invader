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

    # スプライトグループを作成して登録
    all = pygame.sprite.RenderUpdates()
    Player.containers = all
    # スプライトの画像を登録
    Player.image = load_image("player.png")
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
    def __init__(self):
        # imageとcontainersはmain()でセットされる
        pygame.sprite.Sprite.__init__(self, self.containers)
        #プレイヤーの大きさを画像の大きさに設定
        self.rect = self.image.get_rect()
        # プレイヤーが画面の一番下
        self.rect.bottom = SCR_RECT.bottom
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

if __name__ == "__main__":
    main()
