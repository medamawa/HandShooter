import cv2
import numpy as np


# RGBではなく、BGRで指定することに注意
def detect_object(frame, lower_bgr, upper_bgr):

    # 指定された色の範囲内のピクセルをマスクする
    mask = cv2.inRange(frame, lower_bgr, upper_bgr)

    return mask


filepath = "resources/sample.mp4"

cap = cv2.VideoCapture(filepath)

while True:
    # 1フレームずつ取得する。
    ret, frame = cap.read()
    if not ret:
        break

    # コウモリ
    lower_bat = np.array([50, 50, 50])
    upper_bat = np.array([60, 60, 60])
    mask_bat = detect_object(frame, lower_bat, upper_bat)

    # 青ブロック
    lower_blue_block = np.array([145, 50, 50])
    upper_blue_block = np.array([180, 85, 85])
    mask_blue_block = detect_object(frame, lower_blue_block, upper_blue_block)

    # 赤ブロック
    lower_red_block = np.array([50, 50, 145])
    upper_red_block = np.array([85, 85, 180])
    mask_red_block = detect_object(frame, lower_red_block, upper_red_block)

    # フェンス
    lower_fence = np.array([110, 100, 95])
    upper_fensce = np.array([130, 120, 110])
    mask_fence = detect_object(frame, lower_fence, upper_fensce)

    mask = mask_bat + mask_fence + mask_blue_block + mask_red_block

    # マスクを使って元の画像から青色の物体を抽出する
    result = cv2.bitwise_and(frame, frame, mask=mask)

    # 結果を出力
    cv2.imshow("Frame", frame)
    cv2.imshow("Result", result)

    key = cv2.waitKey(30)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
