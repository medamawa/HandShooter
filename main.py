import cv2
import mediapipe as mp
import numpy as np

from game import game
from home import home
import utils.game_utils as game_utils

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
    rand = np.random.randint(0, 4)
    title_image_path = f'src/title/{rand}.png'

    # windowの作成
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # 背景画像の読み込み
    background = cv2.imread("src/background.png")
    background = cv2.resize(background, window_size)

    # ホーム画面
    home(background, window_name, window_size, title_image_path)

    # ゲームの開始
    game(window_name, mp_info)


    # 終了処理
    while True:
        cv2.imshow(window_name, background)

        if cv2.waitKey(0) & 0xFF:
            break


if __name__ == "__main__":
    main()