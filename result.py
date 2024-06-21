import cv2
import time

import utils.image_utils as image_utils
import utils.game_utils as game_utils
import utils.home_utils as home_utils

# 結果画面
def result(window_name, window_size, title_image, background_color, score):
    # -1: exit, 0: easy, 1: normal, 2: hard
    play_mode = 0

    # テキスト画像の読み込み
    score_image = cv2.imread("src/text/score.png", cv2.IMREAD_UNCHANGED)

    # ボタン画像の読み込み
    easy_button = cv2.imread("src/button/easy.png", cv2.IMREAD_UNCHANGED)
    easy_button = image_utils.resize(easy_button, 0.5)
    easy_selected_button = cv2.imread("src/button/easy_selected.png", cv2.IMREAD_UNCHANGED)
    easy_selected_button = image_utils.resize(easy_selected_button, 0.5)
    normal_button = cv2.imread("src/button/normal.png", cv2.IMREAD_UNCHANGED)
    normal_button = image_utils.resize(normal_button, 0.5)
    normal_selected_button = cv2.imread("src/button/normal_selected.png", cv2.IMREAD_UNCHANGED)
    normal_selected_button = image_utils.resize(normal_selected_button, 0.5)
    hard_button = cv2.imread("src/button/hard.png", cv2.IMREAD_UNCHANGED)
    hard_button = image_utils.resize(hard_button, 0.5)
    hard_selected_button = cv2.imread("src/button/hard_selected.png", cv2.IMREAD_UNCHANGED)
    hard_selected_button = image_utils.resize(hard_selected_button, 0.5)

    # result画面の表示開始時刻を取得
    start_time = time.time()
    background_base = home_utils.make_background(background_color)

    while True:
        # 現在時刻を取得
        now = time.time()

        # 背景画像の生成
        background_image = home_utils.animate_background(background_base, background_color, window_size, (now - start_time))

        # タイトル画像の表示
        image_utils.put_image(background_image, title_image, (int(window_size[0]/2), int(window_size[1]/2) - 100))

        # スコアの表示
        score_len = len(str(score))
        image_utils.put_image(background_image, score_image, (int(window_size[0]/2) - 130 - 24*(score_len-1), int(window_size[1]/2) + 100))
        score_point = (int(window_size[0]/2) + 260 + 48*(score_len-1), int(window_size[1]/2) + 100)
        game_utils.put_score(background_image, score_point, score)

        # プレイの選択
        if play_mode == 0:
            image_utils.put_image(background_image, easy_selected_button, (int(window_size[0]/2) - 250, int(window_size[1]/2) + 250))
            image_utils.put_image(background_image, normal_button, (int(window_size[0]/2), int(window_size[1]/2) + 250))
            image_utils.put_image(background_image, hard_button, (int(window_size[0]/2) + 250, int(window_size[1]/2) + 250))
        elif play_mode == 1:
            image_utils.put_image(background_image, easy_button, (int(window_size[0]/2) - 250, int(window_size[1]/2) + 250))
            image_utils.put_image(background_image, normal_selected_button, (int(window_size[0]/2), int(window_size[1]/2) + 250))
            image_utils.put_image(background_image, hard_button, (int(window_size[0]/2) + 250, int(window_size[1]/2) + 250))
        elif play_mode == 2:
            image_utils.put_image(background_image, easy_button, (int(window_size[0]/2) - 250, int(window_size[1]/2) + 250))
            image_utils.put_image(background_image, normal_button, (int(window_size[0]/2), int(window_size[1]/2) + 250))
            image_utils.put_image(background_image, hard_selected_button, (int(window_size[0]/2) + 250, int(window_size[1]/2) + 250))

        # # デバッグ情報
        # image_utils.put_text_with_background(background_image, f"Score: {score}p", (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))
        # image_utils.put_text_with_background(background_image, "Press Enter or ESC", (100, 140), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))
        # image_utils.put_text_with_background(background_image, f"Mode: {play_mode}", (100, 180), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))
    
        cv2.imshow(window_name, background_image)

        key = cv2.waitKey(1)
        if key == 13:       # Enterが押されたら画面を切り替える
            return play_mode
        elif key == 27:     # ESCが押されたら終了
            return -1
        elif key == 2:      # 左矢印
            if play_mode > 0:
                play_mode -= 1
        elif key == 3:      # 右矢印
            if play_mode < 2:
                play_mode += 1
