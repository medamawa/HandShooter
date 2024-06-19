import cv2
import time

import utils.image_utils as image_utils
import utils.home_utils as home_utils

# ホーム画面
def home(window_name, window_size, title_image, background_color):
    # -1: exit, 0: easy, 1: normal, 2: hard
    play_mode = 0

    # home画面の表示開始時刻を取得
    start_time = time.time()
    background_base = home_utils.make_background(background_color)

    while True:
        # 現在時刻を取得
        now = time.time()

        # 背景画像の生成
        background_image = home_utils.animate_background(background_base, background_color, window_size, (now - start_time))

        # press_any_key_image = cv2.imread("src/press_any_key_to_start.png", cv2.IMREAD_UNCHANGED)
        # press_any_key_image = image_utils.resize(press_any_key_image, 0.8)

        image_utils.put_image(background_image, title_image, (int(window_size[0]/2), int(window_size[1]/2) - 100))
        # image_utils.put_image(background_image, press_any_key_image, (int(window_size[0]/2), int(window_size[1]/2) + 150))

        # プレイの選択
        image_utils.put_text_with_background(background_image, "Press Enter", (int(window_size[0]/2), int(window_size[1]/2) + 110), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))
        image_utils.put_text_with_background(background_image, f"Mode: {play_mode}", (int(window_size[0]/2), int(window_size[1]/2) + 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))
    
    
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

