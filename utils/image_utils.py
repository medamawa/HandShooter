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
# point(x, y): 画像の中心座標
def put_image(base_image, image, point):
    # 貼り付け先座標の設定
    x1 = max(point[0] - int(image.shape[1]/2), 0)
    y1 = max(point[1] - int(image.shape[0]/2), 0)
    x2 = x1 + image.shape[1]
    y2 = y1 + image.shape[0]

    # 合成
    base_image[y1:y2, x1:x2] = base_image[y1:y2, x1:x2] * (1 - image[:, :, 3:] / 255) + image[:, :, :3] * (image[:, :, 3:] / 255)


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
