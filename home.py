import cv2

import utils.image_utils as image_utils

# ホーム画面
def home(window_name, window_size, title_image):
    home_image = background(window_size)
    press_any_key_image = cv2.imread("src/press_any_key_to_start.png", cv2.IMREAD_UNCHANGED)
    press_any_key_image = image_utils.resize(press_any_key_image, 0.8)

    image_utils.put_image(home_image, title_image, (int(window_size[0]/2), int(window_size[1]/2) - 100))
    image_utils.put_image(home_image, press_any_key_image, (int(window_size[0]/2), int(window_size[1]/2) + 150))

    while True:
        cv2.imshow(window_name, home_image)

        # 任意のキーが押されたら画面を切り替える
        if cv2.waitKey(0) & 0xFF:
            break

def background(window_size):
    background = cv2.imread("src/background/0/squid.png")
    background = cv2.resize(background, window_size)
    # squid = cv2.imread("src/background/0/mask.png", cv2.IMREAD_UNCHANGED)
    # squid = cv2.resize(squid, window_size)
    
    # image_utils.put_image(background, squid, (int(window_size[0]/2), int(window_size[1]/2)))

    return background

