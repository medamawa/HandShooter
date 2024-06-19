import cv2
import time

import utils.image_utils as image_utils
import utils.game_utils as game_utils
import utils.home_utils as home_utils

# 結果画面
def result(window_name, window_size, title_image, background_color, score):
    # -1: exit, 0: easy, 1: normal, 2: hard
    play_mode = 0

    # result画面の表示開始時刻を取得
    start_time = time.time()
    background_base = home_utils.make_background(background_color)

    while True:
        # 現在時刻を取得
        now = time.time()

        # 背景画像の生成
        background_image = home_utils.animate_background(background_base, background_color, window_size, (now - start_time))

        image_utils.put_image(background_image, title_image, (int(window_size[0]/2), int(window_size[1]/2) - 100))
        game_utils.put_score(background_image, window_size, score)

        # スコアの表示
        image_utils.put_text_with_background(background_image, f"Score: {score}p", (int(window_size[0]/2), int(window_size[1]/2) + 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))
    
        # プレイの選択
        image_utils.put_text_with_background(background_image, "Press Enter or ESC", (int(window_size[0]/2), int(window_size[1]/2) + 190), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))
        image_utils.put_text_with_background(background_image, f"Mode: {play_mode}", (int(window_size[0]/2), int(window_size[1]/2) + 230), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))
    
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
