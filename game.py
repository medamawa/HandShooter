import cv2
import time
import numpy as np

import utils.game_utils as game_utils
import utils.image_utils as image_utils

def game(window_name, window_size, title_image, mp_info):
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
    ink_color = np.random.randint(0, 8)
    

    with mp_info[2].Hands(
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
            keypoints = game_utils.take_coordinates(results.multi_hand_landmarks, image)

            '''
            3. 関節座標の処理
            関節座標をもとに、射撃判定・命中判定を行う。
            この処理では、一つ前のフレームの関節座標を利用するので、そのデータが無い場合は初期化処理を行う。
            関節座標が取得できていない場合は、init_flag を True にして初期化する。
            '''

            # 手を正しく認識できている場合は処理を行う
            if keypoints != 0:
                # 人差し指の付け根を原点とする相対座標を取得
                relative_keypoints = game_utils.relative_coordinates(keypoints)
                angle = game_utils.get_angle(relative_keypoints)

                # 初期化
                if init_flag:
                    prev_keypoints = keypoints
                    prev_relative_keypoints = relative_keypoints
                    prev_angle = angle
                    init_flag = False
                
                # 照準の座標を取得
                aim_point = game_utils.get_aim_point(prev_keypoints, range_multiplier)
                # 射撃判定
                shot_flag = game_utils.is_shot(prev_relative_keypoints, relative_keypoints, prev_angle, angle)
                # 命中判定
                if shot_flag:
                    hit_flag = game_utils.is_hit(aim_point, target_point, target_size)
                else:
                    hit_flag = False

                # 一つ前のフレームの座標を更新
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

                # 銃痕を描画
                game_utils.put_ink(image, window_size, aim_point, ink_color)
                
                # 命中した場合の処理
                if hit_flag or now - hit_time < 0.5:
                    if hit_flag:
                        hit_time = now
                    game_utils.put_bang(image, target_point, target_size)
                    image_utils.put_text_with_background(image, "Hit!", (100, 220), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))
                else:
                    game_utils.put_target(image, target_point, target_size)
                    image_utils.put_text_with_background(image, "Bang!", (100, 220), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))
            else:
                game_utils.put_target(image, target_point, target_size)
            

            # 出力の処理
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


            # 射線を描画
            if keypoints != 0:
                game_utils.put_aim_line(image, keypoints)

                # デバッグ情報を描画
                game_utils.put_debug_info(image, keypoints, relative_keypoints, mp_info, results)

            '''
            5. 画像出力処理
            画像を出力する。
            '''

            # タイトルを付けて画像を表示
            # image_utils.put_text_with_background(image, window_name, (100, 100), cv2.FONT_HERSHEY_PLAIN, 6, (0, 0, 0), 5, (255, 255, 255))
            game_utils.put_title(image, title_image)
            cv2.imshow(window_name, image)

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


            if cv2.waitKey(1) & 0xFF == 27:
                break

    cap.release()
