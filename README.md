# Hand shooting

## How to play

```shell
python main.py
```

## Directory

```
│  game.py
│  home.py
│  main.py
│
├─src
│  │  background.png
│  │  target.png
│  │  ...etc
│  │
│  └─title
│      │  0.png
│      │  1.png
│      └─ ...etc
│
└─utils
    │  game_utils.py
    └─ image_utils.py
```

## Requirements

- Python3
- MediaPipe
- OpenCV

## Technical point

### キャリブレーションで決定する変数

- 人差し指の何倍の長さを射撃位置にするのか

### ホーム画面の背景画像のアニメーション

フレームごとに画像をずらして合成することでアニメーションを実現した。

### ESCで強制終了

### 射撃判定の処理フロー

1. 指の角度変化で射撃を検知 is_shot = True
2. 誤検知につながるので、0.8秒間は射撃判定を行わない
3. 射撃の0.3秒後に着弾する
4. ここで命中判定を行なう is_hit = True

## Color

- ![#D84C8D](https://placehold.co/15x15/D84C8D/D84C8D.png) `#D84C8D`
- ![#F9FF5C](https://placehold.co/15x15/F9FF5C/F9FF5C.png) `#F9FF5C`
- ![#81D059](https://placehold.co/15x15/81D059/81D059.png) `#81D059`
- ![#2F22DB](https://placehold.co/15x15/2F22DB/2F22DB.png) `#2F22DB`
- ![#9C2BF6](https://placehold.co/15x15/9C2BF6/9C2BF6.png) `#9C2BF6`


## Credit

- サムネ素材館
https://samune-sozaikan.com/
