# cpu_animation
CPUの内部動作のアニメーションを生成します

cpu_animation.pyを実行すると一秒毎にtest.svgが更新されます．
また，test以下に連番のSVGが生成されます．

pattern.txt内にマイクロな命令を記述したパターンが出力されます．

[命令] [転送先(Yバス)] [転送元A(Aバス)] [転送元B(Bバス)]

という形式．

今は図表内のInstructionがCALLから変更されませんが気にしないでください．