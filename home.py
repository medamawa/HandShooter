import cv2

import utils.image_utils as image_utils

# ホーム画面
def home(background, window_name, window_size, title_image_path):
    start_image = background.copy()
    title_image = cv2.imread(title_image_path, cv2.IMREAD_UNCHANGED)
    title_image = image_utils.resize_with_height(title_image, int(window_size[1]/4))
    image_utils.put_image(start_image, title_image, (int(window_size[0]/2), int(window_size[1]/2)))

    while True:
        cv2.imshow(window_name, start_image)

        if cv2.waitKey(0) & 0xFF:
            break