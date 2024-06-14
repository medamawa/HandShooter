import cv2
import mediapipe as mp
import numpy as np

from game import game
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
    screen = np.ones((window_size[0], window_size[1], 3))*255

    # スタート画面
    start_image = screen.copy()
    title_image = cv2.imread("src/title.png", cv2.IMREAD_UNCHANGED)
    title_image = cv2.resize(title_image, (int(window_size[0]/4), int(window_size[1]/4)))
    image_utils.put_image(start_image, title_image, (int(window_size[0]/2), int(window_size[1]/2)))

    while True:
        cv2.imshow(window_name, title_image)
        # 終了処理
        if cv2.waitKey(0) & 0xFF == 27:
            break

    # ゲームの開始
    game(window_name, mp_info)


    # 終了処理
    while True:
        cv2.imshow(window_name, screen)

        if cv2.waitKey(0) & 0xFF == 27:
            break


if __name__ == "__main__":
    main()