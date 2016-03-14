# 本软件只针对 http://cn.vonvon.net/quiz/743 颜色自动找色
## exe是由pyinstaller生成
## GIF 由 LICEcap 制作
## 自动找色需要跟着软件来设置一下颜色方块的左上角以及右下角
### 算法不是非常完善, 偏移量设置不好会导致过不到 50 关
### 其实就是根据左上角和右下角, 来做了一个计算题, 计算分割线以及色块的宽度, 提取色块中心点的颜色值与前面及后面色块的值进行比较

 ![image](https://github.com/M3oM3oBug/FindColor/raw/master/FindColor.gif)
