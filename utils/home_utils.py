import cv2
import numpy as np

import utils.image_utils as image_utils


# 10x6のグリッドにイカを配置した背景画像の元となる画像を生成
def make_background(color):
    base = cv2.imread(f'src/background/base/{color}.png')
    squid = cv2.imread(f'src/background/squid/{color}.png', cv2.IMREAD_UNCHANGED)

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
def animate_background(base, color, window_size, diff):
    cycle_time = 60
    vartical_shift = -(diff % cycle_time) * base.shape[0]/ cycle_time
    horizontal_shift = (diff % cycle_time) * base.shape[1]/ cycle_time

    base = np.roll(base, int(-horizontal_shift), axis=0)
    base = np.roll(base, int(horizontal_shift), axis=1)

    mask = cv2.imread(f'src/background/mask/{color}.png', cv2.IMREAD_UNCHANGED)
    
    image_utils.put_image(base, mask, (int(base.shape[1]/2), int(base.shape[0]/2)))
    base = cv2.resize(base, window_size)

    return base