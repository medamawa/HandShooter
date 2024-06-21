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

### title, button
- ![#D84C8D](https://placehold.co/15x15/D84C8D/D84C8D.png) `#D84C8D`
- ![#F9FF5C](https://placehold.co/15x15/F9FF5C/F9FF5C.png) `#F9FF5C`
- ![#81D059](https://placehold.co/15x15/81D059/81D059.png) `#81D059`
- ![#2F22DB](https://placehold.co/15x15/2F22DB/2F22DB.png) `#2F22DB`
- ![#9C2BF6](https://placehold.co/15x15/9C2BF6/9C2BF6.png) `#9C2BF6`

### ink
- ![#EA3BEC](https://placehold.co/15x15/EA3BEC/EA3BEC.png) `#EA3BEC [234, 59, 36]` 
- ![#812DF5](https://placehold.co/15x15/812DF5/812DF5.png) `#812DF5 [129, 45, 245]` 
- ![#EAF866](https://placehold.co/15x15/EAF866/EAF866.png) `#EAF866 [234, 248, 102]` 
- ![#0101ED](https://placehold.co/15x15/0101ED/0101ED.png) `#0101ED [1, 1, 237]` 
- ![#74F8FD](https://placehold.co/15x15/74F8FD/74F8FD.png) `#74F8FD [116, 248, 253]` 
- ![#EA8743](https://placehold.co/15x15/EA8743/EA8743.png) `#EA8743 [234, 135, 67]` 
- ![#BFE34F](https://placehold.co/15x15/BFE34F/BFE34F.png) `#BFE34F [191, 227, 79]` 
- ![#FFFFFF](https://placehold.co/15x15/FFFFFF/FFFFFF.png) `#FFFFFF [255, 255, 255]` 


## Target
| target | score | size | speed |
| --- | --- | --- | --- |
| <img width="100" alt="squid_0" src="src/target/squid/0.png"> | 100p | 100 | 10 |
| <img width="100" alt="squid_1" src="src/target/squid/1.png"> | 150p | 120 | 15 |
| <img width="100" alt="squid_2" src="src/target/squid/2.png"> | 200p | 80 | 25 |
| <img width="100" alt="squid_3" src="src/target/squid/3.png"> | 300p | 80 | 35 |
| <img width="100" alt="squid_4" src="src/target/squid/4.png"> | 500p | 60 | 20 |
| <img width="100" alt="squid_5" src="src/target/squid/5.png"> | 1,000p | 50 | 25 |


## Credit

- サムネ素材館
https://samune-sozaikan.com/
