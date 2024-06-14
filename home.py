import cv2

import utils.image_utils as image_utils

# ホーム画面
def home(window_name, window_size, background, title_image):
    start_image = background.copy()
    image_utils.put_image(start_image, title_image, (int(window_size[0]/2), int(window_size[1]/2)))

    while True:
        cv2.imshow(window_name, start_image)

        if cv2.waitKey(0) & 0xFF:
            break