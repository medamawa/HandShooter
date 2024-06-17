import cv2

# 画像を倍率に合わせてリサイズする
def resize(image, multiplier):
    size = (int(image.shape[1] * multiplier), int(image.shape[0] * multiplier))

    return cv2.resize(image, size)


# 画像の高さに合わせてリサイズする
def resize_with_height(image, height):
    multiplier = height / image.shape[0]

    return resize(image, multiplier)


# 指定された座標に任意の画像を描画する
# center_point(x, y): 画像の中心座標
def put_image(base_image, image, center_point):
    image_height, image_width = image.shape[:2]
    base_height, base_width = base_image.shape[:2]
    point = (center_point[0] - int(image_width/2), center_point[1] - int(image_height/2))

    # 貼り付け先座標の設定
    x1 = max(point[0], 0)
    y1 = max(point[1], 0)
    x2 = min(point[0] + image_width, base_width)
    y2 = min(point[1] + image_height, base_height)

    # 完全にはみ出る場合は計算しない
    if not ((-image_width < point[0] < base_width) and (-image_height < point[1] < base_height)):
        return base_image

    # 貼り付け画像の合成部分
    image_x1 = 0 if x1 > 0 else image_width - (x2 - x1)
    image_y1 = 0 if y1 > 0 else image_height - (y2 - y1)
    image_x2 = image_width if x2 < base_width else base_width - x1
    image_y2 = image_height if y2 < base_height else base_height - y1

    # 合成
    base_image[y1:y2, x1:x2] = base_image[y1:y2, x1:x2] * (1 - image[image_y1:image_y2, image_x1:image_x2, 3:] / 255) \
        + image[image_y1:image_y2, image_x1:image_x2, :3] * (image[image_y1:image_y2, image_x1:image_x2, 3:] / 255)


# テキストを背景付きで描画する
def put_text_with_background(image, text, point, font, size, color, thickness, background_color):
    #背景を描く
    (width, height), baseline= cv2.getTextSize(text, font, size, thickness)
    top_left_point = (point[0], point[1] - height)
    bottom_right_point = (point[0] + width, point[1])
    image = cv2.rectangle(image, top_left_point, bottom_right_point, background_color, -1)

    #textを書く
    image = cv2.putText(image, text, point, font, size, color, thickness)

    return image
