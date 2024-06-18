import cv2
import mediapipe as mp
import numpy as np

from game import game
from home import home
from turorial import turorial

import utils.game_utils as game_utils
import utils.image_utils as image_utils

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_info = (mp_drawing, mp_drawing_styles, mp_hands)


# キャリブレーション処理
def calibration(step, image, keypoints):
    print("Calibrating...")

    if step == 0:
        print("Please open your hand.")
        cv2.putText(image, "Please open your hand.", (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        if game_utils.is_shot(keypoints, keypoints[0]):
            step = 1


def main():
    window_name = "Hand Shooter"
    window_size = (1920, 1080)

    # windowの作成
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # タイトル画像の読み込み
    rand = np.random.randint(0, 4)
    title_image_path = f'src/title/{rand}.png'
    title_image = cv2.imread(title_image_path, cv2.IMREAD_UNCHANGED)
    title_image = image_utils.resize_with_height(title_image, int(window_size[1]/4))

    # ホーム画面
    home(window_name, window_size, title_image)

    # チュートリアル
    # range_multiplier = turorial(window_name, window_size, title_image, mp_info)
    range_multiplier = 3

    # ゲームの開始
    game(window_name, window_size, title_image, mp_info, range_multiplier)

    # 終了処理
    home(window_name, window_size, title_image)


if __name__ == "__main__":
    main()