
def calc_range_multiplier(keypoints, target_point):

    # 人差し指の付け根
    point1 = (int((keypoints[5][0])), int((keypoints[5][1])))
    # 人差し指の先端
    point2 = (int((keypoints[8][0])), int((keypoints[8][1])))

    # x座標での倍率とy座標での倍率の平均を取る
    x_range_multiplier = (target_point[0] - point1[0]) / (point2[0] - point1[0])
    y_range_multiplier = (target_point[1] - point1[1]) / (point2[1] - point1[1])

    range_multiplier = (x_range_multiplier + y_range_multiplier) / 2

    return range_multiplier