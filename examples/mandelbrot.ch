# Mandelbrot 集 ASCII 渲染（纯 ChickenStack 定点运算）
# 寄存器: W/H 画布, M 最大迭代, S 定点比例, Q 逃逸阈值
# X/Y 像素坐标, A/B 实部虚部, C/D 当前点, I 迭代, F 继续标志, T/U/Z 临时

80 W
30 H
60 M
10000 S
s 4 * Q

0 Y
1
[
  $
  0 X
  1
  [
    $
    x 400 * 22000 - C
    y 800 * 12000 - D
    0 A
    0 B
    0 I
    1
    [
      $
      a a * s / b b * s / + Z
      m i >
      z q > 0 =
      *
      : F
      {
        a a * s / b b * s / - c + T
        a b * 2 * s / d + U
        t A
        u B
        i 1 + I
      }
      f
    ]
    $
    i 0 = { 32 | 6 i > { 46 | 12 i > { 58 | 18 i > { 45 | 24 i > { 61 | 30 i > { 43 | 36 i > { 42 | 42 i > { 35 | 48 i > { 37 | 64 } } } } } } } } }
    "
    x 1 + X
    w x >
  ]
  $
  10 "
  y 1 + Y
  h y >
]
$
