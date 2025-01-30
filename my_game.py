import pygame
import random

# Pygameの初期化
pygame.init()
pygame.mixer.init()  # サウンド用の初期化

# ゲーム画面の設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# ゲームのタイトルを設定
pygame.display.set_caption("Defend the Earth")

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED   = (255,0,0)

# プレイヤーの設定
player_size = 50
player_pos = [screen_width // 2, screen_height - player_size]
player_speed = 10

# 敵の設定
enemy_size = 50
enemies = []


# アイテムの設定
item_size = 40
item_pos = None  # アイテムの位置
item_active = False  # アイテムが画面上に存在するかどうか
item_image_original = pygame.image.load('P:/Spygame/item1.png')  # アイテムの画像
item_image = pygame.transform.scale(item_image_original, (item_size, item_size))


# 敵の速度
enemy_speed = 1
# 敵の速度増加のためのスコアの閾値
score_for_speed_increase = 1000

# ミサイルの設定
missile_size = [5, 10]
missiles = []

bgm = pygame.mixer.Sound('P:/Spygame/bgm.ogg')  # BGM（バックグラウンドミュージック）
game_over_bgm = pygame.mixer.Sound('P:/Spygame/gameover.ogg')  # ゲームオーバー時のBGM
missile_sound = pygame.mixer.Sound('P:/Spygame/shot.mp3')  # ミサイル発射音
enemy_destroyed_sound = pygame.mixer.Sound('P:/Spygame/crash.mp3')  # 敵撃破音
item_sound = pygame.mixer.Sound('P:/Spygame/item.mp3')  # アイテム取得音

def game_over_bgm_play():
    bgm.stop()  # 現在のBGMを停止
    game_over_bgm.play()

# BGMのループ再生
def start_bgm():
    game_over_bgm.stop
    bgm.play(loops=-1, maxtime=0, fade_ms=0)  # 無限ループ

def wait_for_restart():
    global enemy_speed
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    enemy_speed = 1
                    start_bgm()  # 再開時に通常BGMを再生
                    return True  # 再スタート
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()



# テキストの設定
title_font = pygame.font.Font(None, 100)
title_text = title_font.render('Press Enter to Start', True, WHITE)
start_font = pygame.font.Font(None, 50)
start_text = start_font.render('Press Enter to Start', True, WHITE)
game_over_font = pygame.font.Font(None, 75)
game_over_text = game_over_font.render('GAME OVER', True, WHITE)
game_over_restart_font = pygame.font.Font(None, 36)
game_over_restart_text = start_font.render('Press Enter to Restart or ESC to Quit', True, WHITE)

# スコアの設定
score = 0
score_font = pygame.font.Font(None, 36)

# プレイヤーと敵の画像を読み込む
player_image_original = pygame.image.load('P:/Spygame/me.png')
enemy_image_original = pygame.image.load('P:/Spygame/ene.png')

# 画像のサイズを50ピクセルに設定
player_image = pygame.transform.scale(player_image_original, (player_size, player_size))
enemy_image = pygame.transform.scale(enemy_image_original, (enemy_size, enemy_size))

# 背景画像の読み込み
background_image1 = pygame.image.load('P:/Spygame/sky.jpg')  # 背景画像のファイル名
background = pygame.transform.scale(background_image1, (screen_width, screen_height))

background_image2 = pygame.image.load('P:/Spygame/gameover.jpg')  # 背景画像のファイル名
background2 = pygame.transform.scale(background_image2, (screen_width, screen_height))

# ゲームの基本設定
clock = pygame.time.Clock()
game_over = False

# スコアの描画
def draw_score():
    score_text = score_font.render('Score: ' + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

# 敵の移動
def drop_enemies(enemies):
    delay = random.randint(1, 5)
    if len(enemies) < 10 and random.randint(1, delay) == 1:
        x_pos = random.randint(0, screen_width-enemy_size)
        y_pos = 0
        enemies.append([x_pos, y_pos])


# アイテムの出現
def spawn_item():
    global item_pos, item_active
    if not item_active and random.randint(1, 300) == 1:  # 1/300の確率で出現
        x_pos = random.randint(50, screen_width - 50 - item_size)
        y_pos = 0
        item_pos = [x_pos, y_pos]
        item_active = True

# アイテムの位置更新（落下処理）
def update_item_position():
    global item_pos, item_active
    if item_active:
        # アイテムが下に移動
        item_pos[1] += 5  # 落下速度
        # アイテムが画面外に出たらリセット
        if item_pos[1] > screen_height:
            item_active = False
            item_pos = None

# 敵の描画
def draw_enemies(enemies):
    for enemy_pos in enemies:
        screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))

# プレイヤーの描画
def draw_player():
    screen.blit(player_image, (player_pos[0], player_pos[1]))


# アイテムの描画
def draw_item():
    if item_active and item_pos:
        screen.blit(item_image, (item_pos[0], item_pos[1]))

# 的位置の更新
def update_enemy_positions(enemies, player_pos):
    for idx, enemy_pos in enumerate(enemies):
        if enemy_pos[1] >= 0 and enemy_pos[1] < screen_height:
            enemy_pos[1] += enemy_speed
            # プレイヤーと敵の衝突判定
            if player_pos[1] < enemy_pos[1] + enemy_size and \
               player_pos[0] < enemy_pos[0] + enemy_size and \
               player_pos[0] + player_size > enemy_pos[0]:
                return True
        else:
            enemies.pop(idx)
    return False

# ミサイル発射
def fire_missile(x, y):
    missiles.append([x, y])
    missile_sound.play()  # ミサイル発射音を再生

# ミサイルの移動
def move_missiles(missiles):
    for missile in missiles:
        missile[1] -= 10
        if missile[1] < 0:
            missiles.remove(missile)

# ミサイルの描画
def draw_missiles(missiles):
    for missile in missiles:
        pygame.draw.rect(screen, RED, (missile[0], missile[1], missile_size[0], missile_size[1]))

# 衝突のチェック
def collision_check(enemies, missiles):
    global score, enemy_speed, score_for_speed_increase
    for enemy in enemies[:]:
        for missile in missiles[:]:
            # 敵とミサイルの衝突判定
            if (missile[0] >= enemy[0] and missile[0] < enemy[0] + enemy_size) and \
               (missile[1] >= enemy[1] and missile[1] < enemy[1] + enemy_size):
                try:
                    enemies.remove(enemy)
                    missiles.remove(missile)
                    score += 100  # スコアを更新
                    enemy_destroyed_sound.play()  # 敵撃破音を再生
                    # 1000点ごとに敵の速度を増加
                    if score % score_for_speed_increase == 0:
                        enemy_speed += 1
                except ValueError:
                    pass
                break

# アイテムの取得処理
def check_item_collision():
    global item_active, item_pos, enemies,destroyed_enemies, score
    if item_active and item_pos:
        destroyed_enemies = 0  # 消えた敵の数をカウント
        for missile in missiles[:]:
            if (missile[0] >= item_pos[0] and missile[0] < item_pos[0] + item_size) and \
               (missile[1] >= item_pos[1] and missile[1] < item_pos[1] + item_size):
                destroyed_enemies = len(enemies)
                enemies.clear()  # すべての敵を消す
                item_active = False  # アイテムを消す
                item_pos = None  # アイテムの位置をリセット
                missiles.remove(missile)  # 衝突したミサイルを削除
                item_sound.play()  # アイテム取得音を再生
                break     

        # 消えた敵の数をスコアに加算
        score += destroyed_enemies * 100
             
# テキストの描画
def draw_centered_text(text, font, color, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(screen_width / 2, y))
    screen.blit(text_surface, text_rect)


start_screen_image = pygame.image.load('P:/Spygame/ene.png')
start_screen = pygame.transform.scale(start_screen_image, (screen_width, screen_height))

# スタート画面
def wait_for_start():
    waiting = True
    while waiting:
        screen.blit(start_screen, (0, 0))
        draw_centered_text('Defend the Earth', title_font, WHITE, screen_height / 3)
        draw_centered_text('Press Enter to Start', start_font, WHITE, screen_height / 2)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# ゲーム開始前の待機状態
wait_for_start()

# ゲーム画面
def game_loop():
    global game_over, player_pos, enemies, missiles

    player_pos = [screen_width // 2, screen_height - player_size]
    enemies = []
    missiles = []
    game_over = False

    start_bgm()

    # ゲームオーバーになるまでループ
    while not game_over:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fire_missile(player_pos[0] + player_size // 2, player_pos[1])
                if event.key == pygame.K_ESCAPE:  # ESCキーでゲーム終了
                    pygame.quit()
                    exit()

        keys = pygame.key.get_pressed()

        # プレイヤーの移動制御
        if keys[pygame.K_LEFT] and player_pos[0] > player_speed:
            player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT] and player_pos[0] < screen_width - player_size - player_speed:
            player_pos[0] += player_speed

        # 画面の更新
        screen.blit(background, (0, 0))  # 背景を描画


        # アイテムの出現処理
        spawn_item()

        # アイテムの位置更新（落下）
        update_item_position()

        # アイテムの取得判定
        check_item_collision()

        # アイテムの描画
        draw_item()

        # 敵の生成と移動
        drop_enemies(enemies)
        if update_enemy_positions(enemies, player_pos):
            game_over = True
            break  # ゲームオーバー時にループを抜ける

        # ミサイルの移動
        move_missiles(missiles)

        # 衝突判定
        collision_check(enemies, missiles)

        # プレイヤーの描画
        draw_player()
        # 敵とミサイルの描画
        draw_enemies(enemies)
        draw_missiles(missiles)

        # スコアの描画
        draw_score()

        pygame.display.update()

        # ゲームの速度制御
        clock.tick(60)

    # ゲームオーバー時の処理
    screen.blit(background_image2, (0, 0))
    draw_centered_text('GAME OVER', game_over_font, WHITE, screen_height / 2 - 50)
    draw_centered_text('Score: ' + str(score), score_font, WHITE, screen_height / 2 + 20)
    draw_centered_text('', score_font, WHITE, screen_height / 2 + 40)
    draw_centered_text('press enter to restart', game_over_restart_font, WHITE, screen_height / 2 + 70)
    draw_centered_text('or', game_over_restart_font, WHITE, screen_height / 2 + 100)
    draw_centered_text('esc to quit', game_over_restart_font, WHITE, screen_height / 2 + 130)
    pygame.display.update()

    game_over_bgm_play()

    return wait_for_restart()



# リスタートまで待機
def wait_for_restart():
    global enemy_speed
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False
                    enemy_speed = 1
                    return True  # 再スタート
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

# ゲーム開始前の待機状態
wait_for_start()

# ゲームループ
restart = True
while restart:
    game_over = False
    score = 0  # スコアをリセット
    player_pos = [screen_width // 2, screen_height - player_size]
    enemies = []
    missiles = []
    restart = game_loop()

pygame.quit()


