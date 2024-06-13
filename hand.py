import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# 関節のxyz座標を取得する(左上を原点とした絶対座標)
'''
0: 手首
1: 親指 付け根
2: 親指 第1関節
3: 親指 第2関節
4: 親指 先端
5: 人差し指 付け根 ***
6: 人差し指 第1関節
7: 人差し指 第2関節
8: 人差し指 先端 ***
9: 中指 付け根
10: 中指 第1関節
11: 中指 第2関節
12: 中指 先端
13: 薬指 付け根
14: 薬指 第1関節
15: 薬指 第2関節
16: 薬指 先端
17: 小指 付け根
18: 小指 第1関節
19: 小指 第2関節
20: 小指 先端
'''
def take_coordinates(coordinates, image):
    if coordinates == None:
        return 0
    
    image_width, image_height = image.shape[1], image.shape[0]
    
    keypoints = []

    for data_point in coordinates:
        xyz_datapoints = data_point.landmark
        for xyz in xyz_datapoints:
            X_value = round(xyz.x * image_width, 2)
            Y_value = round(xyz.y * image_height, 2)
            Z_value = round(xyz.z, 3)
            xyz = [X_value, Y_value, Z_value]
            keypoints.append(xyz)

    return keypoints


# 人差し指の付け根を原点とする相対座標を取得する
def relative_coordinates(keypoints):
    if keypoints == 0:
        return 0
    
    x = keypoints[5][0]
    y = keypoints[5][1]
    z = keypoints[5][2]

    relative_keypoints = []

    for i in range(len(keypoints)):
        relative_keypoints.append([round(keypoints[i][0] - x, 2), round(keypoints[i][1] - y, 2), round(keypoints[i][2] - z, 3)])

    return relative_keypoints


def open_check_by_distance(keypoints, center):

    def thumb_open_check(keypoints, center):
        d4 = np.sqrt(np.square(keypoints[4][0] - center[0]) + np.square(keypoints[4][1] - center[1]))
        d3 = np.sqrt(np.square(keypoints[3][0] - center[0]) + np.square(keypoints[3][1] - center[1]))
        if d4 > d3:
            return True
        else:
            return False
    
    def index_open_check(keypoints, center):
        d5 = np.sqrt(np.square(keypoints[5][0] - center[0]) + np.square(keypoints[5][1] - center[1]))
        d6 = np.sqrt(np.square(keypoints[6][0] - center[0]) + np.square(keypoints[6][1] - center[1]))
        d7 = np.sqrt(np.square(keypoints[7][0] - center[0]) + np.square(keypoints[7][1] - center[1]))
        d8 = np.sqrt(np.square(keypoints[8][0] - center[0]) + np.square(keypoints[8][1] - center[1]))
        if d8 > d7 > d6 > d5:
            return True
        else:
            return False
    
    def middle_open_check(keypoints, center):
        d9 = np.sqrt(np.square(keypoints[9][0] - center[0]) + np.square(keypoints[9][1] - center[1]))
        d10 = np.sqrt(np.square(keypoints[10][0] - center[0]) + np.square(keypoints[10][1] - center[1]))
        d11 = np.sqrt(np.square(keypoints[11][0] - center[0]) + np.square(keypoints[11][1] - center[1]))
        d12 = np.sqrt(np.square(keypoints[12][0] - center[0]) + np.square(keypoints[12][1] - center[1]))
        if d12 > d11 > d10 > d9:
            return True
        else:
            return False
    
    def ring_open_check(keypoints, center):
        d13 = np.sqrt(np.square(keypoints[13][0] - center[0]) + np.square(keypoints[13][1] - center[1]))
        d14 = np.sqrt(np.square(keypoints[14][0] - center[0]) + np.square(keypoints[14][1] - center[1]))
        d15 = np.sqrt(np.square(keypoints[15][0] - center[0]) + np.square(keypoints[15][1] - center[1]))
        d16 = np.sqrt(np.square(keypoints[16][0] - center[0]) + np.square(keypoints[16][1] - center[1]))
        if d16 > d15 > d14 > d13:
            return True
        else:
            return False
    
    def pinky_open_check(keypoints, center):
        d17 = np.sqrt(np.square(keypoints[17][0] - center[0]) + np.square(keypoints[17][1] - center[1]))
        d18 = np.sqrt(np.square(keypoints[18][0] - center[0]) + np.square(keypoints[18][1] - center[1]))
        d19 = np.sqrt(np.square(keypoints[19][0] - center[0]) + np.square(keypoints[19][1] - center[1]))
        d20 = np.sqrt(np.square(keypoints[20][0] - center[0]) + np.square(keypoints[20][1] - center[1]))
        if d20 > d19 > d18 > d17:
            return True
        else:
            return False
    
    thumb = thumb_open_check(keypoints, center)
    index = index_open_check(keypoints, center)
    middle = middle_open_check(keypoints, center)
    ring = ring_open_check(keypoints, center)
    pinky = pinky_open_check(keypoints, center)

    if thumb == True and index == True and middle == True and ring == True and pinky == True:
        return True
    else:
        return False


def close_check_by_distance(keypoints, center): #tested OK
   d3 = np.sqrt(np.square(keypoints[3][0] - center[0]) + np.square(keypoints[3][1] - center[1]))
   d4 = np.sqrt(np.square(keypoints[4][0] - center[0]) + np.square(keypoints[4][1] - center[1]))
   d5 = np.sqrt(np.square(keypoints[5][0] - keypoints[0][0]) + np.square(keypoints[5][1] - keypoints[0][1]))
   d8 = np.sqrt(np.square(keypoints[8][0] - keypoints[0][0]) + np.square(keypoints[8][1] - keypoints[0][1]))
   d9 = np.sqrt(np.square(keypoints[9][0] - keypoints[0][0]) + np.square(keypoints[9][1] - keypoints[0][1]))
   d12 = np.sqrt(np.square(keypoints[12][0] - keypoints[0][0]) + np.square(keypoints[12][1] - keypoints[0][1]))
   d13 = np.sqrt(np.square(keypoints[13][0] - keypoints[0][0]) + np.square(keypoints[13][1] - keypoints[0][1]))
   d16 = np.sqrt(np.square(keypoints[16][0] - keypoints[0][0]) + np.square(keypoints[16][1] - keypoints[0][1]))
   d17 = np.sqrt(np.square(keypoints[17][0] - keypoints[0][0]) + np.square(keypoints[17][1] - keypoints[0][1]))
   d20 = np.sqrt(np.square(keypoints[20][0] - keypoints[0][0]) + np.square(keypoints[20][1] - keypoints[0][1]))

   if d8 < d5 and d12 < d9 and d16 < d13 and d20 < d17 and d4 < d3:
       return True
   else:
       return False


def calibration(step, image, keypoints):
    print("Calibrating...")

    if step == 0:
        print("Please open your hand.")
        cv2.putText(image, "Please open your hand.", (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        if open_check_by_distance(keypoints, keypoints[0]):
            step = 1

# 射撃判定
def is_shot(prev_relative_keypoints, relative_keypoints, prev_angle, angle):

    # 一コマのうちに20度以上指を動かしたら撃つと判定する
    if abs(prev_angle) - abs(angle) >= 20:
        return True
    # この判定法はキャリブレーションが必要、、、
    elif abs(prev_angle) < 10 and prev_relative_keypoints[8][1] - relative_keypoints[8][1] >= 10:
        return True
    else:
        return False


# 人差し指の先端と付け根の角度を取得する
def get_angle(relative_keypoints):
    if relative_keypoints == 0:
        return 0

    X = relative_keypoints[8][0]
    Y = relative_keypoints[8][1]

    try:
        m = Y/X
    except ZeroDivisionError:
        m = 0
    
    angle = np.arctan(m) * 180 / (np.pi)

    # 上方向を0度として、-180度から180度の範囲になるように変換
    if X > 0:
        angle = angle + 90
    elif X <= 0:
        angle = angle - 90
    
    return round(angle, 1)


def put_text_with_background(image, text, point, font, size, color, thickness, background_color):
    #背景を描く
    (width, height), baseline= cv2.getTextSize(text, font, size, thickness)
    top_left_point = (point[0], point[1] - height)
    bottom_right_point = (point[0] + width, point[1])
    image = cv2.rectangle(image, top_left_point, bottom_right_point, background_color, -1)

    #textを書く
    image = cv2.putText(image, text, point, font, size, color, thickness)

    return image


def put_debug_text(image, keypoints, relative_keypoints):
    # 人差し指の付け根
    place1 = (int((keypoints[5][0])), int((keypoints[5][1])))
    cv2.putText(image, f'// {get_angle(relative_keypoints)}', place1, cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    # 人差し指の先端
    place2 = (int((keypoints[8][0])), int((keypoints[8][1])))
    cv2.putText(image, f'[{float(relative_keypoints[8][0])}, {float(relative_keypoints[8][1])}, {float(relative_keypoints[8][2])}]', place2, cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)

    place3 = ((place2[0] - place1[0]) * 3 + place1[0], (place2[1] - place1[1]) * 3 + place1[1])

    image = cv2.line(image, place1, place3, (0, 255, 0), 3)


def main():
    calibration_step = 0
    init_flag = True
    shot_flag = False
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        while cap.isOpened():
            success, image = cap.read()

            if not success:
                print("Ignoring empty camera frame.")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # 関節の絶対座標wを取得
            keypoints = take_coordinates(results.multi_hand_landmarks, image)

            # 手を正しく認識できている場合は処理を行う
            if keypoints != 0:
                # 人差し指の付け根を原点とする相対座標を取得
                relative_keypoints = relative_coordinates(keypoints)
                angle = get_angle(relative_keypoints)



                # 初期化
                if init_flag:
                    prev_relative_keypoints = relative_keypoints
                    prev_angle = angle
                    init_flag = False

                if is_shot(prev_relative_keypoints, relative_keypoints, prev_angle, angle):
                    print("Shot!")
                    put_text_with_background(image, "Shot!", (100, 300), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))

                # デバッグ用のテキストを描画
                put_debug_text(image, keypoints, relative_keypoints)

                prev_relative_keypoints = relative_keypoints
                prev_angle = angle
            else:
                init_flag = True


            # 検出された手の骨格をカメラ画像に重ねて描画
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # 出力の処理
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
            
            cv2.namedWindow("Hand Shooter", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Hand Shooter", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            put_text_with_background(image, "Hand Shooter", (100, 100), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 5, (255, 255, 255))
            cv2.imshow("Hand Shooter", image)

            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()


if __name__ == "__main__":
    main()