import cv2
import time
import numpy as np

import utils.game_utils as game_utils
import utils.image_utils as image_utils
import utils.tutorial_utils as tutorial_utils


# チュートリアルを行う
# ３つの的を狙ってもらって、射撃距離の倍率を計算する
def turorial(window_name, window_size, title_image, mp_info):
    # キャリブレーション関連の変数
    calibration_step = 0
    calibration_point = []
    calibration_point.append((window_size[0]//2, window_size[1]//2))
    calibration_point.append((window_size[0] - 100, 100))
    calibration_point.append((100, window_size[1] - 100))
    calibrating_range_multiplier = []

    # 初期化
    init_flag = True
    shot_flag = False       # 射撃可能かどうか。Falseの時には射撃できる。射撃してから0.8秒間は確定でTrue。キャリブレーションが終了したらFalseに
    shot_now_flag = False   # 射撃したそのフレームだけTrue
    bang_flag = False       # 着弾後0.5秒間はTrue（射撃後0.3秒〜0.8秒の間はTrue）
    bang_now_flag = False   # 着弾したそのフレームだけTrue（射撃後0.3秒以上経った初めてのフレームでTrue）
    # hit_flag = False        # 命中した場合は、射撃後0.3秒〜0.8秒の間True
    now = time.time()
    shot_time = 0           # 射撃した時刻
    hit_time = 0
    cap = cv2.VideoCapture(0)

    shot_duration = 0.3     # 射撃してから着弾するまで
    bang_duration = 0.5     # 着弾してから消えるまで
    duration = shot_duration + bang_duration    # 一連の処理にかかる時間

    target_point = calibration_point[0]
    target_size = 100

    # デバッグ用の変数
    ink_color = np.random.randint(0, 8)
    range_multiplier = 3    # デフォルト値


    cap = cv2.VideoCapture(0)

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

                # 射撃判定(射撃してから0.8秒間は射撃判定を行わない)
                shot_now_flag = False
                bang_now_flag = False
                if shot_flag == False:
                    shot_now_flag = game_utils.is_shot(prev_relative_keypoints, relative_keypoints, prev_angle, angle)
                    shot_flag = shot_now_flag
                
                # 射撃したフレームにて、照準の座標を着弾点として保管
                # このフレームでrange_multiplierを計算する
                if shot_now_flag:
                    bang_point = aim_point
                    calibrating_range_multiplier.append(tutorial_utils.calc_range_multiplier(prev_keypoints, target_point))

                
                # 着弾判定と命中判定
                # 射撃したフレームを除いておかないと、挙動がおかしくなる（shot_timeの更新がこの後行われるため）
                if shot_flag and now - shot_time > shot_duration and shot_now_flag == False:
                    # 射撃後0.3秒以上経った初めてのフレームで着弾とする
                    # このフレームで命中判定を行う
                    if bang_flag == False:
                        bang_now_flag = True
                        bang_flag = True
                else:
                    bang_flag = False

                # 一つ前のフレームの座標を更新
                prev_keypoints = keypoints
                prev_relative_keypoints = relative_keypoints
                prev_angle = angle
            else:
                init_flag = True
            
            '''
            4. イベント処理
            関節座標の処理結果に応じて、画像に描画する内容を変更する。
            行うイベント処理は以下の通り。

            - 射撃した場合に"Shot!"と表示する
            - 着弾した場合には"Bang!"と表示して、銃痕を描画する
            - 命中した場合には"Hit!"と表示して、的を爆発させる
            - それ以外の場合は、通常の的を表示する

            また、イベントをしばらくの間継続して表示するために、時間を計測している。
            '''
            
            # 関節認識処理終了時の時刻を取得
            now = time.time()
            
            # 射撃後0.8秒間の処理
            if shot_flag:
                # 射撃したフレームにはshot_timeを更新する
                if shot_now_flag:
                    shot_time = now
                
                if bang_flag:
                    game_utils.put_target(image, target_point, target_size)
                    image_utils.put_text_with_background(image, "Bang!", (100, 220), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))
                    image_utils.put_text_with_background(image, f"{calibrating_range_multiplier[-1]}", (100, 260), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))
                else:
                    game_utils.put_target(image, target_point, target_size)
                    image_utils.put_text_with_background(image, "Shot!", (100, 220), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3, (0, 0, 0))

                # 銃痕を描画
                if bang_flag:
                    if bang_now_flag:
                        # inkの種類をランダムに決定
                        ink_type = np.random.randint(0, 2)
                    
                    game_utils.put_ink(image, window_size, target_point, ink_type, ink_color)
            else:
                game_utils.put_target(image, target_point, target_size)
            
            if keypoints != 0:
                # レティクルを描画
                game_utils.put_reticle(image, window_size, aim_point)
            

            # 出力の処理
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


            # 射線を描画
            if keypoints != 0:
                game_utils.put_aim_line(image, keypoints, range_multiplier)

                # デバッグ情報を描画
                game_utils.put_debug_info(image, keypoints, relative_keypoints, mp_info, results)

            '''
            5. 画像出力処理
            画像を出力する。
            '''

            # タイトルを付けて画像を表示
            game_utils.put_title(image, title_image)
            cv2.imshow(window_name, image)

            '''
            6. 値更新処理
            次のフレームに向けて、値を更新する。
            '''

            key = cv2.waitKey(1)

            if bang_flag == True and key == 32:  # Spaceキーが押されたら次のステップへ
                shot_flag = False
                calibration_step += 1
                # キャリブレーションの値に合わせて射撃距離を変更する
                range_multiplier = sum(calibrating_range_multiplier) / len(calibrating_range_multiplier)
                
                # キャリブレーションのステップに合わせてターゲットの座標を変更する
                if calibration_step >= 3:
                    print("DONE")
                    break
                else:
                    target_point = calibration_point[calibration_step]
                    target_size = 100

            elif bang_flag == True and key == 9: # Tabキーが押されたらリセット
                shot_flag = False
                calibrating_range_multiplier.pop()

            elif key == 27:   # ESCキーが押されたら終了
                break

    cap.release()

    print(calibrating_range_multiplier, range_multiplier)

    

    return range_multiplier