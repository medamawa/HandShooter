import cv2
import numpy as np

import utils.image_utils as image_utils


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


# 命中したターゲットがあるかどうか判定
def get_hit_target(aim_point, target_list, len):

    hit_target = None

    # ターゲットのリストを逆順に参照して、最も手前のターゲットから判定する
    for i, target in enumerate(reversed(target_list)):
        if is_hit(aim_point, target["point"], target["size"]):
            hit_target = len - i - 1    # 順方向でのインデックスに変換
            target_list[hit_target]["is_hit"] = True
            break

    return hit_target


# 命中したかどうか判定
def is_hit(aim_point, target_point, target_size):

    # 射線とターゲットの距離が一定範囲内にあれば命中と判定
    if np.linalg.norm(np.array(aim_point) - np.array(target_point)) <= target_size:
        return True
    else:
        return False


# レティクルの表示
def put_reticle(image, window_size, point):
    reticle_image = cv2.imread("src/reticle.png", cv2.IMREAD_UNCHANGED)
    reticle_image = cv2.cvtColor(reticle_image, cv2.COLOR_BGRA2RGBA)
    reticle_image = image_utils.resize_with_height(reticle_image, int(window_size[1]/12))

    image_utils.put_image(image, reticle_image, point)


# ターゲットを全て描画する
def put_targets(image, target_list, hit_target=None):
    for i, target in enumerate(target_list):
        if i == hit_target:
            put_hit_target(image, target)
        else:
            put_a_target(image, target)


# 指定されたターゲットを描画する
def put_a_target(image, target):
    # target.pngのサイズをもとに、当たり判定と矛盾がないようにサイズを決めている
    # target.pngのサイズが480×480で、的のサイズが410×410のため、410/480倍している
    # また、半径で指定されているので、直径に変換するために2倍している
    # 変数宣言の括弧の要素"(... ,) * 2"はタプルを2回繰り返すことを示している
    image_size = (int(target["size"]*2*480/410),) * 2

    target_image = cv2.imread(f'src/target/{target["type"]}/{target["color"]}.png', cv2.IMREAD_UNCHANGED)
    target_image = cv2.cvtColor(target_image, cv2.COLOR_BGRA2RGBA)
    target_image = cv2.resize(target_image, image_size)

    image_utils.put_image(image, target_image, target["point"])


# 命中されたターゲットを描画する
def put_hit_target(image, target):
    # target.pngのサイズをもとに、当たり判定と矛盾がないようにサイズを決めている
    # target.pngのサイズが480×480で、的のサイズが410×410のため、410/480倍している
    # また、半径で指定されているので、直径に変換するために2倍している
    image_size = (int(target["size"]*2*480/410),) * 2

    if target["type"] == "squid":
        bang_image = cv2.imread(f'src/target/{target["type"]}_hit/{target["color"]}.png', cv2.IMREAD_UNCHANGED)
    elif target["type"] == "obstacle":      # 障害物の場合は画像が変わらない
        bang_image = cv2.imread(f'src/target/{target["type"]}/{target["color"]}.png', cv2.IMREAD_UNCHANGED)
    bang_image = cv2.cvtColor(bang_image, cv2.COLOR_BGRA2RGBA)
    bang_image = cv2.resize(bang_image, image_size)

    image_utils.put_image(image, bang_image, target["point"])


# 指定された座標にinkを描画する
# point(x, y): inkの中心座標
def put_ink(image, window_size, point, type, color):

    ink_image = cv2.imread(f'src/ink/{type}/{color}.png', cv2.IMREAD_UNCHANGED)
    ink_image = cv2.cvtColor(ink_image, cv2.COLOR_BGRA2RGBA)
    ink_image = image_utils.resize_with_height(ink_image, int(window_size[1]/6))

    image_utils.put_image(image, ink_image, point)


# タイトルを描画
def put_title(base_image, title_image):
    title_image_half = image_utils.resize(title_image, 0.5)
    point = (30+int(title_image_half.shape[1]/2), 30+int(title_image_half.shape[0]/2))
    image_utils.put_image(base_image, title_image_half, point)


# プレイモードを描画
def put_play_mode(base_image, play_mode_image):
    point = (300, 155+int(play_mode_image.shape[0]/2))
    image_utils.put_image(base_image, play_mode_image, point)


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
def put_debug_info(image, keypoints, relative_keypoints, mp_info, results):
    # 検出された手の骨格をカメラ画像に重ねて描画
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_info[0].draw_landmarks(
                image,
                hand_landmarks,
                mp_info[2].HAND_CONNECTIONS,
                mp_info[1].get_default_hand_landmarks_style(),
                mp_info[1].get_default_hand_connections_style())
    
    # 人差し指の付け根
    point1 = (int((keypoints[5][0])), int((keypoints[5][1])))
    cv2.putText(image, f'// {get_angle(relative_keypoints)}', point1, cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
    # 人差し指の先端
    point2 = (int((keypoints[8][0])), int((keypoints[8][1])))
    cv2.putText(image, f'[{float(relative_keypoints[8][0])}, {float(relative_keypoints[8][1])}, {float(relative_keypoints[8][2])}]', point2, cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255), 3)


# 射線を描画
def put_aim_line(image, keypoints, range_multiplier):
    point1 = (int((keypoints[5][0])), int((keypoints[5][1])))
    aim_point = get_aim_point(keypoints, range_multiplier)
    image = cv2.line(image, point1, aim_point, (0, 255, 0), 3)


# 照準位置を取得する(銃身の何倍かを射撃距離とする)
def get_aim_point(keypoints, range_multiplier):
    # 人差し指の付け根
    point1 = (int((keypoints[5][0])), int((keypoints[5][1])))
    # 人差し指の先端
    point2 = (int((keypoints[8][0])), int((keypoints[8][1])))

    aim_point = (int((point2[0] - point1[0]) * range_multiplier + point1[0]), int((point2[1] - point1[1]) * range_multiplier + point1[1]))

    return aim_point


# ターゲットの移動処理
def update_target_point(target_list, window_size):

    window_width = window_size[0]
    window_height = window_size[1]

    # ターゲットが画面端に到達したかどうか判定
    # 到達している場合にTrueを返す
    def left_check(target):
        return target["point"][0] < 200 and target["speed"] < 0
    def right_check(target):
        return target["point"][0] > window_width-200 and target["speed"] > 0
    def top_check(target):
        return target["point"][1] < 150 and target["speed"] < 0
    def bottom_check(target):
        return target["point"][1] > window_height-150 and target["speed"] > 0
    def negative_top_check(target):
        return target["point"][1] < 150 and target["speed"] > 0
    def negative_bottom_check(target):
        return target["point"][1] > window_height-150 and target["speed"] < 0
    
    for target in target_list:
        if target["movement"] == 1:     # 横移動
            if left_check(target) or right_check(target):
                target["speed"] = -target["speed"]
            
            target["point"][0] += target["speed"]
        
        elif target["movement"] == 2:   # 縦移動
            if top_check(target) or bottom_check(target):
                target["speed"] = -target["speed"]
            
            target["point"][1] += target["speed"]
        
        elif target["movement"] == 3:   # 斜め移動(左下から右上)
            if left_check(target) or right_check(target) or negative_top_check(target) or negative_bottom_check(target):
                target["speed"] = -target["speed"]
            
            target["point"][0] += target["speed"]
            target["point"][1] -= target["speed"]

            if left_check(target) or right_check(target) or negative_top_check(target) or negative_bottom_check(target):
                target["movement"] = 4
        
        elif target["movement"] == 4:   # 斜め移動(左上から右下)
            if left_check(target) or right_check(target) or top_check(target) or bottom_check(target):
                target["speed"] = -target["speed"]
            
            target["point"][0] += target["speed"]
            target["point"][1] += target["speed"]

            if left_check(target) or right_check(target) or top_check(target) or bottom_check(target):
                target["movement"] = 3


# スコアの表示
def put_score(image, point, score):
    score_image_width = 80
    comma_image_width = 40

    comma_image = cv2.imread('src/char/comma.png', cv2.IMREAD_UNCHANGED)
    p_image = cv2.imread('src/char/p.png', cv2.IMREAD_UNCHANGED)
    image_utils.put_image(image, p_image, point)

    for i, str_num in enumerate(reversed(list(str(score)))):
        num = int(str_num)

        if i % 3 == 0 and i != 0:
            point = (point[0] - (comma_image_width + score_image_width) / 2, point[1])
            image_utils.put_image(image, comma_image, point)
            point = (point[0] - (comma_image_width + score_image_width) / 2, point[1])
        else:
            point = (point[0] - score_image_width, point[1])
        
        num_image = cv2.imread(f'src/char/{num}.png', cv2.IMREAD_UNCHANGED)

        image_utils.put_image(image, num_image, point)
    
    return point


# 加算されたスコアの表示
def put_got_score(image, point, score):
    score_image_width = 40
    comma_image_width = 20

    comma_image = cv2.imread('src/char/comma.png', cv2.IMREAD_UNCHANGED)
    comma_image = image_utils.resize(comma_image, 0.5)
    p_image = cv2.imread('src/char/p.png', cv2.IMREAD_UNCHANGED)
    p_image = image_utils.resize(p_image, 0.5)
    plus_image = cv2.imread('src/char/plus.png', cv2.IMREAD_UNCHANGED)
    plus_image = image_utils.resize(plus_image, 0.5)

    image_utils.put_image(image, p_image, point)

    for i, str_num in enumerate(reversed(list(str(score)))):
        num = int(str_num)

        if i % 3 == 0 and i != 0:
            point = (point[0] - (comma_image_width + score_image_width) / 2, point[1])
            image_utils.put_image(image, comma_image, point)
            point = (point[0] - (comma_image_width + score_image_width) / 2, point[1])
        else:
            point = (point[0] - score_image_width, point[1])
        
        num_image = cv2.imread(f'src/char/{num}.png', cv2.IMREAD_UNCHANGED)
        num_image = image_utils.resize(num_image, 0.5)

        image_utils.put_image(image, num_image, point)
    
    point = (point[0] - score_image_width, point[1])
    image_utils.put_image(image, plus_image, point)


# ランクの表示
def put_rank(image, point, score):
    '''
    C  : 0 - 300
    B  : 300 - 800
    A  : 800 - 1500
    S  : 1500 - 2500
    S+ : 2500 - 4000
    X  : 4000 -
    '''
    if score < 300:
        rank = 0
    elif score < 800:
        rank = 1
    elif score < 1500:
        rank = 2
    elif score < 2500:
        rank = 3
    elif score < 4000:
        rank = 4
    else:
        rank = 5


    rank_image = cv2.imread(f'src/rank/{rank}.png', cv2.IMREAD_UNCHANGED)
    rank_image = cv2.cvtColor(rank_image, cv2.COLOR_BGRA2RGBA)

    point = (point[0] - rank_image.shape[1]/2, point[1])
    image_utils.put_image(image, rank_image, point)


# 時計の表示
def put_clock(image, window_size, time, game_time=70):
    point = (window_size[0]/2, 100)
    num_image_width = 80
    colon_image_width = 40

    colon_image = cv2.imread('src/char/colon.png', cv2.IMREAD_UNCHANGED)
    image_utils.put_image(image, colon_image, point)

    m = int(game_time - time) // 60
    s = int(game_time - time) % 60

    for i, str_num in enumerate(reversed(list(str(m)))):
        num = int(str_num)

        m_point = (point[0] - (num_image_width + colon_image_width) / 2 - i * num_image_width, point[1])
        
        num_image = cv2.imread(f'src/char/{num}.png', cv2.IMREAD_UNCHANGED)

        image_utils.put_image(image, num_image, m_point)

    for i, str_num in enumerate(list(str(s).zfill(2))):
        num = int(str_num)

        s_point = (point[0] + (num_image_width + colon_image_width) / 2 + i * num_image_width, point[1])
        
        num_image = cv2.imread(f'src/char/{num}.png', cv2.IMREAD_UNCHANGED)

        image_utils.put_image(image, num_image, s_point)


