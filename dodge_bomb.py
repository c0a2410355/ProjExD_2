import os
import sys
import random
import time

import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとん or 爆弾 のRect
    戻り値 [横,縦] の bool型 判定結果
    True = はみ出していない false = はみ出している
    """
    yoko = True
    tate = True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False  # 横方向にはみ出ている場合
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False  # 縦方向にはみ出している場合
    return (yoko,tate)

def gameover(screen: pg.Surface) -> None:
    """
    引数 : Surface型のスクリーン
    戻り値 なし
    GAME OVER画面を表示
    """
    # 背景
    bg_img = pg.Surface((WIDTH,HEIGHT))
    pg.draw.rect(bg_img, (0,0,0),pg.Rect(0,0,WIDTH,HEIGHT))
    bg_img.set_alpha(150)
    screen.blit(bg_img,[0,0])
    # テキスト
    font = pg.font.Font(None,80)
    txt = font.render("GAME OVER",True,(255,255,255))
    txt_width = txt.get_width() 
    txt_height = txt.get_height()
    screen.blit(txt,[(WIDTH - txt_width)/2,(HEIGHT - txt_height)/2])  # テキストを中央に配置
    # 画像
    kkSad_img = pg.image.load("fig/8.png")
    kkSad2_img = pg.image.load("fig/8.png")
    kkSad_width = kkSad_img.get_width()
    kkSad_height = kkSad_img.get_height()
    screen.blit(kkSad_img,[( ( WIDTH - kkSad_width + txt_width + kkSad_width) /2 ), ( HEIGHT - kkSad_height ) /2])
    screen.blit(kkSad2_img,[( ( WIDTH - kkSad_width - txt_width - kkSad_width) /2 ), ( HEIGHT - kkSad_height ) /2])
    pg.display.update()
    time.sleep(5)

def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20*r, 20*r))
        bb_img.set_colorkey((0 ,0 ,0 ))
        bb_imgs.append(bb_img)
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)
    bb_accs = [a for a in range(1, 11)]  # 加速のリスト
    return (bb_imgs,bb_accs)

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    DELTA = {pg.K_UP:(0,-5),pg.K_DOWN:(0,5),pg.K_RIGHT:(5,0),pg.K_LEFT:(-5,0),}
    bb_lst = init_bb_imgs()
    ind = 0

    bb_img = pg.Surface((20,20))  # 赤い円を生成
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0 ,0 ,0 ))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)  #爆弾のX座標セット
    bb_rct.centery = random.randint(0,HEIGHT)  #爆弾のY座標セット
    vx = 3
    vy = 3
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        if tmr%250 == 0 and ind < 10:
            ind += 1
        #書き直し
        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        bb_rct = bb_lst[0][ind].get_rect(center=(bb_rct.centerx,bb_rct.centery))
        bb_rct.move_ip(vx*bb_lst[1][ind],vy*bb_lst[1][ind])
        yoko , tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(kk_img, kk_rct)
        screen.blit(bb_lst[0][ind], bb_rct)
        if kk_rct.colliderect(bb_rct):  # こうかとんの衝突判定
            gameover(screen)
            return  # ゲームOVER
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()