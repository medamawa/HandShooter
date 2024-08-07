import cv2
import mediapipe as mp
import numpy as np

from game import game
from home import home
from turorial import turorial
from result import result

import utils.game_utils as game_utils
import utils.image_utils as image_utils

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
mp_info = (mp_drawing, mp_drawing_styles, mp_hands)


def main():
    window_name = "Hand Shooter"
    window_size = (1920, 1080)

    # windowの作成
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # タイトル画像の読み込み
    rand = np.random.randint(0, 5)
    title_image_path = f'src/title/{rand}.png'
    title_image = cv2.imread(title_image_path, cv2.IMREAD_UNCHANGED)
    title_image = image_utils.resize_with_height(title_image, int(window_size[1]/4))

    # ホーム画面の背景色
    background_color = np.random.randint(0, 5)

    # ホーム画面
    # -1: exit, 0: easy, 1: normal, 2: hard
    play_mode = home(window_name, window_size, title_image, background_color)

    # チュートリアル
    # range_multiplier = turorial(window_name, window_size, title_image, mp_info)
    range_multiplier = 3

    while play_mode != -1:
        # ゲームの開始
        score = game(window_name, window_size, title_image, mp_info, range_multiplier, play_mode)

        # 結果画面
        play_mode = result(window_name, window_size, title_image, background_color, score, play_mode)


if __name__ == "__main__":
    main()