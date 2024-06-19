import cv2
import time

import utils.image_utils as image_utils
import utils.game_utils as game_utils
import utils.home_utils as home_utils

# 結果画面
def result(window_name, window_size, title_image, background_color, score):
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
    
        cv2.imshow(window_name, background_image)

        key = cv2.waitKey(1)

        if key == 13:           # Enterが押されたらゲーム続行
            return True
        elif key == 27:         # ESCが押されたらゲーム終了
            return False
    