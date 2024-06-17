import cv2
import numpy as np
import time

import utils.image_utils as image_utils

# ホーム画面
def home(window_name, window_size, title_image):
    # home画面の表示開始時刻を取得
    start_time = time.time()

    # 背景画像の元となる画像を生成
    background_base = make_background()

    while True:
        # 現在時刻を取得
        now = time.time()

        # 背景画像の生成
        background_image = animate_background(background_base, window_size, (now - start_time))

        press_any_key_image = cv2.imread("src/press_any_key_to_start.png", cv2.IMREAD_UNCHANGED)
        press_any_key_image = image_utils.resize(press_any_key_image, 0.8)

        image_utils.put_image(background_image, title_image, (int(window_size[0]/2), int(window_size[1]/2) - 100))
        image_utils.put_image(background_image, press_any_key_image, (int(window_size[0]/2), int(window_size[1]/2) + 150))
    
        cv2.imshow(window_name, background_image)

        # ESCが押されたら画面を切り替える
        if cv2.waitKey(1) & 0xFF == 27:
            break


# 10x6のグリッドにイカを配置した背景画像の元となる画像を生成
def make_background():
    base = cv2.imread("src/background/base/0.png")
    squid = cv2.imread("src/background/squid/0.png", cv2.IMREAD_UNCHANGED)

    base_height = base.shape[0]
    base_width = base.shape[1]
    squid_height = squid.shape[0]
    squid_width = squid.shape[1]

    # 10x6のグリッドにイカを配置
    for vartical in range(6):
        for horizontal in range(10):
            x = int(base_width / 10 * horizontal + squid_width / 2)
            y = int(base_height / 6 * vartical + squid_height / 2)

            image_utils.put_image(base, squid, (x, y))
    
    return base
            

# 背景画像をアニメーションさせて、装飾を施し、リサイズして返す
# cycle_timeで指定された時間の周期でアニメーションする
def animate_background(base, window_size, diff):
    cycle_time = 60
    vartical_shift = -(diff % cycle_time) * base.shape[0]/ cycle_time
    horizontal_shift = (diff % cycle_time) * base.shape[1]/ cycle_time

    base = np.roll(base, int(vartical_shift), axis=0)
    base = np.roll(base, int(horizontal_shift), axis=1)

    mask = cv2.imread("src/background/mask/0.png", cv2.IMREAD_UNCHANGED)
    
    image_utils.put_image(base, mask, (int(base.shape[1]/2), int(base.shape[0]/2)))
    base = cv2.resize(base, window_size)

    return base
