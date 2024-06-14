import cv2
import mediapipe as mp
import numpy as np
import time

import utils

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# 関節のxyz座標を取得する(左上を原点とした絶対座標)
def take_coordinates(coordinates, image):
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


# キャリブレーション処理
def calibration(step, image, keypoints):
    print("Calibrating...")

    if step == 0:
        print("Please open your hand.")
        cv2.putText(image, "Please open your hand.", (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)
        if is_shot(keypoints, keypoints[0]):
            step = 1


# 打ったかどうか判定
def is_shot(prev_relative_keypoints, relative_keypoints, prev_angle, angle):

    # 一コマのうちに20度以上指を動かしたら撃つと判定する
    if abs(prev_angle) - abs(angle) >= 20:
        return True
    # この判定法はキャリブレーションが必要、、、
    elif abs(prev_angle) < 10 and prev_relative_keypoints[8][1] - relative_keypoints[8][1] >= 10:
        return True
    else:
        return False


# 命中したかどうか判定
def is_hit(keypoints, range_multiplier, target_point, target_size):
    aim_point = get_aim_point(keypoints, range_multiplier)

    # 射線とターゲットの距離が一定範囲内にあれば命中と判定
    if np.linalg.norm(np.array(aim_point) - np.array(target_point)) <= target_size:
        return True
    else:
        return False


# 指定された座標にターゲットを描画する
# point(x, y): ターゲットの中心座標
def put_target(image, point, size):
    # target.pngのサイズをもとに、当たり判定と矛盾がないようにサイズを決めている
    # target.pngのサイズが480×480で、的のサイズが410×410のため、410/480倍している
    # また、半径で指定されているので、直径に変換するために2倍している
    # 変数宣言の括弧の要素"(... ,) * 2"はタプルを2回繰り返すことを示している
    image_size = (int(size*2*480/410),) * 2

    target_image = cv2.imread("resources/target.png", cv2.IMREAD_UNCHANGED)
    target_image = cv2.cvtColor(target_image, cv2.COLOR_BGRA2RGBA)
    target_image = cv2.resize(target_image, image_size)

    utils.put_image(image, target_image, point)


# 指定された座標にtarget_bangを描画する
# point(x, y): target_bangの中心座標
def put_bang(image, point, size):
    # target.pngのサイズをもとに、当たり判定と矛盾がないようにサイズを決めている
    # target.pngのサイズが480×480で、的のサイズが410×410のため、410/480倍している
    # また、半径で指定されているので、直径に変換するために2倍している
    image_size = (int(size*2*480/410),) * 2

    bang_image = cv2.imread("resources/target_bang.png", cv2.IMREAD_UNCHANGED)
    bang_image = cv2.cvtColor(bang_image, cv2.COLOR_BGRA2RGBA)
    bang_image = cv2.resize(bang_image, image_size)

    utils.put_image(image, bang_image, point)


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


# デバッグ用のグラフィックを描画
def put_debug_info(image, keypoints, relative_keypoints, results):
    # 検出された手の骨格をカメラ画像に重ねて描画
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())
    
    # 人差し指の付け根
    point1 = (int((keypoints[5][0])), int((keypoints[5][1])))
    cv2.putText(image, f'// {get_angle(relative_keypoints)}', point1, cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    # 人差し指の先端
    point2 = (int((keypoints[8][0])), int((keypoints[8][1])))
    cv2.putText(image, f'[{float(relative_keypoints[8][0])}, {float(relative_keypoints[8][1])}, {float(relative_keypoints[8][2])}]', point2, cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)


# 射線を描画
def put_aim_line(image, keypoints):
    point1 = (int((keypoints[5][0])), int((keypoints[5][1])))
    aim_point = get_aim_point(keypoints, 3)
    image = cv2.line(image, point1, aim_point, (0, 255, 0), 3)


# 照準位置を取得する(銃身の何倍かを射撃距離とする)
def get_aim_point(keypoints, range_multiplier):
    # 人差し指の付け根
    point1 = (int((keypoints[5][0])), int((keypoints[5][1])))
    # 人差し指の先端
    point2 = (int((keypoints[8][0])), int((keypoints[8][1])))

    aim_point = ((point2[0] - point1[0]) * range_multiplier + point1[0], (point2[1] - point1[1]) * range_multiplier + point1[1])

    return aim_point


def main():
    window_name = "Hand Shooter"
    window_size = (1920, 1080)

    # windowの作成
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


    test_img = cv2.imread("resources/target.png")
    while True:
        cv2.imshow(window_name, test_img)
        # 終了処理
        if cv2.waitKey(0) & 0xFF == 27:
            break

    # ゲームの開始
    game(window_name)


    # 終了処理
    full_screen_white = np.ones((window_size[0], window_size[1], 3))*200
    while True:
        cv2.imshow(window_name, full_screen_white)

        if cv2.waitKey(0) & 0xFF == 27:
            break

    






def game(window_name):
    calibration_step = 0
    init_flag = True
    shot_flag = False
    hit_flag = False
    shot_time = 0
    hit_time = 0
    cap = cv2.VideoCapture(0)

    # デバッグ用の変数
    target_point = [500, 400]
    target_size = 100
    range_multiplier = 3
    target_speed = 10
    

    with mp_hands.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:

        while cap.isOpened():

            '''
            1. カメラからの入力処理
            カメラからの入力を取得する。もしカメラからの入力がない場合は例外処理を行う。
            画像データはBGR形式で取得されるため、RGB形式に変換する。
            '''
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                continue

            image.flags.writeable = False
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            '''
            2. 関節認識処理
            手の骨格を認識し、その座標を取得する。
            処理は take_coordinates() で行う。
            得られた関節の座標は keypoints に格納される。
            '''

            # 関節の絶対座標wを取得
            keypoints = take_coordinates(results.multi_hand_landmarks, image)

            '''
            3. 関節座標の処理
            関節座標をもとに、射撃判定・命中判定を行う。
            この処理では、一つ前のフレームの関節座標を利用するので、そのデータが無い場合は初期化処理を行う。
            関節座標が取得できていない場合は、init_flag を True にして初期化する。
            '''

            # 手を正しく認識できている場合は処理を行う
            if keypoints != 0:
                # 人差し指の付け根を原点とする相対座標を取得
                relative_keypoints = relative_coordinates(keypoints)
                angle = get_angle(relative_keypoints)

                # 初期化
                if init_flag:
                    prev_keypoints = keypoints
                    prev_relative_keypoints = relative_keypoints
                    prev_angle = angle
                    init_flag = False
                
                shot_flag = is_shot(prev_relative_keypoints, relative_keypoints, prev_angle, angle)
                hit_flag = is_hit(prev_keypoints, range_multiplier, target_point, target_size)

                prev_keypoints = keypoints
                prev_relative_keypoints = relative_keypoints
                prev_angle = angle
            else:
                init_flag = True
                shot_flag = False
                hit_flag = False
            
            '''
            4. イベント処理
            関節座標の処理結果に応じて、画像に描画する内容を変更する。
            行うイベント処理は以下の通り。

            - 射撃した場合に"Shot!"と表示する
            - 命中した場合には"Hit!"と表示して、的を爆発させる
            - それ以外の場合は、通常の的を表示する

            また、イベントをしばらくの間継続して表示するために、時間を計測している。
            '''
            
            # 関節認識処理終了時の時刻を取得
            now = time.time()
            
            # 打ってから0.5秒間は"Shot!"と表示する
            if shot_flag or now - shot_time < 0.5:
                if shot_flag:
                    shot_time = now
                
                # 命中した場合の処理
                if hit_flag or now - hit_time < 0.5:
                    if hit_flag:
                        hit_time = now
                    put_bang(image, target_point, target_size)
                    utils.put_text_with_background(image, "Hit!", (100, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))
                else:
                    put_target(image, target_point, target_size)
                    utils.put_text_with_background(image, "Bang!", (100, 150), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))
            else:
                put_target(image, target_point, target_size)
            

            # 出力の処理
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


            # 射線を描画
            if keypoints != 0:
                put_aim_line(image, keypoints)

                # デバッグ情報を描画
                put_debug_info(image, keypoints, relative_keypoints, results)

            '''
            5. 画像出力処理
            画像を出力する。
            '''

            # タイトルを付けて画像を表示
            utils.put_text_with_background(image, window_name, (100, 100), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 5, (255, 255, 255))
            cv2.imshow("Hand Shooter", image)

            '''
            6. 値更新処理
            次のフレームに向けて、値を更新する。
            '''

            # 的を動かす
            if target_point[0] < 500 or target_point[0] > 1500:
                target_speed = -target_speed
                target_point[0] += target_speed
            else:
                target_point[0] += target_speed


            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()



if __name__ == "__main__":
    main()