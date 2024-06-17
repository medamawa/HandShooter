import cv2

import utils.image_utils as image_utils

# ホーム画面
def home(window_name, window_size, title_image):
    background = background(window_size)
    press_any_key_image = cv2.imread("src/press_any_key_to_start.png", cv2.IMREAD_UNCHANGED)
    press_any_key_image = image_utils.resize(press_any_key_image, 0.8)

    image_utils.put_image(background, title_image, (int(window_size[0]/2), int(window_size[1]/2) - 100))
    image_utils.put_image(background, press_any_key_image, (int(window_size[0]/2), int(window_size[1]/2) + 150))

    while True:
        cv2.imshow(window_name, background)

        # 任意のキーが押されたら画面を切り替える
        if cv2.waitKey(0) & 0xFF:
            break

def background(window_size):
    background = cv2.imread("src/background/0/squid.png")
    mask = cv2.imread("src/background/0/mask.png", cv2.IMREAD_UNCHANGED)
    
    image_utils.put_image(background, mask, (int(background.shape[1]/2), int(background.shape[0]/2)))
    background = cv2.resize(background, window_size)

    return background

