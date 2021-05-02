# 座長配置問題

座長候補者の予定をもとに、最適な座長配置を線形決定する。


## 実行
```bash
pip install scipy
git clone https://github.com/matsui528/zatyou.git
cd zatyou
# cost.csvを編集する
python assign.py cost.csv
```

## 例

### 基本の例
座長候補者の日程が以下のようだったとします

|      | 13:00-13:30 | 13:30-14:00 | 14:00-14:30 | 14:30-15:00 | 
| ---- | ----------- | ----------- | ----------- | ----------- |
| 佐藤 | 〇 | 〇 |    |    |
| 田中 |    | 〇 | 〇 |    |
| 鈴木 | 〇 |    |    | 〇 |
| 加藤 | 〇 | 〇 |    |    |

このとき、`cost.csv`を以下のようにします。すなわち、参加できる部分に1、出来ない部分に0を立てた表を作ります。

```csv
sato,   1, 1, 0, 0
tanaka, 0, 1, 1, 0
suzuki, 1, 0, 0, 1
kato,   1, 1, 0, 0
```
これを実行すると次の結果を得ます。
```bash
input:
      sato [1. 1. 0. 0.]
    tanaka [0. 1. 1. 0.]
    suzuki [1. 0. 0. 1.]
      kato [1. 1. 0. 0.]
assignment:
      sato [1. 0. 0. 0.]
    tanaka [0. 0. 1. 0.]
    suzuki [0. 0. 0. 1.]
      kato [0. 1. 0. 0.]
```
これにより、最適な座長配置が求まりました。


### 中間点の例
座長が出来るか出来ないか微妙な時間があるとしましょう。これを△で表します。
|      | 13:00-13:30 | 13:30-14:00 | 14:00-14:30 | 14:30-15:00 | 
| ---- | ----------- | ----------- | ----------- | ----------- |
| 佐藤 | △ | 〇 |    |    |
| 田中 |    | 〇 | △ |    |
| 鈴木 | 〇 |    |    | 〇 |
| 加藤 | 〇 | 〇 |    |    |

このとき、`cost.csv`を例えば次のようにします。ここでは△に0.5を割り振りました。

```csv
sato,   0.5, 1, 0,   0
tanaka, 0,   1, 0.5, 0
suzuki, 1,   0, 0,   1
kato,   1,   1, 0,   0
```

これを実行すると、次のように、最初のスロットの割り当てが佐藤さんから加藤さんに変わりました。すなわち、△を考慮して最適な配置を計算してくれます。
```bash
input:
      sato [0.5 1.  0.  0. ]
    tanaka [0.  1.  0.5 0. ]
    suzuki [1. 0. 0. 1.]
      kato [1. 1. 0. 0.]
assignment:
      sato [0. 1. 0. 0.]
    tanaka [0. 0. 1. 0.]
    suzuki [0. 0. 0. 1.]
      kato [1. 0. 0. 0.]
```

### 座長候補者よりもスロット数のほうが多い場合
例えば次の例を考えます。座長の人数より座長スロットのほうが多いので、これを実行すると、座長が割り当てられないスロットが発生してしまいます。
|      | 4/2 | 4/3 | 4/4 | 4/5 | 4/6 | 4/7 | 4/8 | 
| ---- | --- | --- | --- | --- | --- | --- | --- |
| 佐藤 | 〇 | 〇 |    |    |    |    | 〇 |
| 田中 |    | 〇 | 〇 |    |    | 〇 |    |
| 鈴木 | 〇 |    |    | 〇 |    |    |    |
| 加藤 | 〇 | 〇 |    |    | 〇 | 〇 |    |
| 松井 | 〇 | 〇 | 〇 | 〇 |    | 〇 | 〇 |

`cost.csv`は次のようになります。

```csv
sato,    1, 1, 0, 0, 0, 0, 1
tanaka,  0, 1, 1, 0, 0, 1, 0
suzuki,  1, 0, 0, 1, 0, 0, 0
kato,    1, 1, 0, 0, 1, 1, 0
matsui,  1, 1, 1, 1, 0, 1, 1
```

結果が次です。
```
input:
      sato [1. 1. 0. 0. 0. 0. 1.]
    tanaka [0. 1. 1. 0. 0. 1. 0.]
    suzuki [1. 0. 0. 1. 0. 0. 0.]
      kato [1. 1. 0. 0. 1. 1. 0.]
    matsui [1. 1. 1. 1. 0. 1. 1.]
assignment:
      sato [1. 0. 0. 0. 0. 0. 0.]
    tanaka [0. 1. 0. 0. 0. 0. 0.]
    suzuki [0. 0. 0. 1. 0. 0. 0.]
      kato [0. 0. 0. 0. 1. 0. 0.]
    matsui [0. 0. 1. 0. 0. 0. 0.]
```
ここでは`4/7`と`4/8`のスロットに誰も配置されません。よって、ここの解決方法は、`4/7`と`4/8`に参加できる佐藤・田中・松井さんのうち2人に2度目の座長をお願いするというものです。

あるいは、松井さんに何度か座長をしてもらうと最初から決めているなら、次のようにmatsui1, matsui2, matsui3を最初に作っておけば、計算できます。

```csv
sato,    1, 1, 0, 0, 0, 0, 1
tanaka,  0, 1, 1, 0, 0, 1, 0
suzuki,  1, 0, 0, 1, 0, 0, 0
kato,    1, 1, 0, 0, 1, 1, 0
matsui1, 1, 1, 1, 1, 0, 1, 1
matsui2, 1, 1, 1, 1, 0, 1, 1
matsui3, 1, 1, 1, 1, 0, 1, 1
```

次が結果です。
```
input:
      sato [1. 1. 0. 0. 0. 0. 1.]
    tanaka [0. 1. 1. 0. 0. 1. 0.]
    suzuki [1. 0. 0. 1. 0. 0. 0.]
      kato [1. 1. 0. 0. 1. 1. 0.]
   matsui1 [1. 1. 1. 1. 0. 1. 1.]
   matsui2 [1. 1. 1. 1. 0. 1. 1.]
   matsui3 [1. 1. 1. 1. 0. 1. 1.]
assignment:
      sato [1. 0. 0. 0. 0. 0. 0.]
    tanaka [0. 1. 0. 0. 0. 0. 0.]
    suzuki [0. 0. 0. 1. 0. 0. 0.]
      kato [0. 0. 0. 0. 1. 0. 0.]
   matsui1 [0. 0. 1. 0. 0. 0. 0.]
   matsui2 [0. 0. 0. 0. 0. 1. 0.]
   matsui3 [0. 0. 0. 0. 0. 0. 1.]
```
このように、松井さんが３回座長をするという仮定の上で、最適な配置を求めることが出来ました。

### 座長を二人配置する例

1スロットあたり、座長が2人必要な場合を考えます。
以下のように、4スロットに9人の座長候補がいるとします。

|      | 13:00-13:30 | 13:30-14:00 | 14:00-14:30 | 14:30-15:00 | 
| ---- | ----------- | ----------- | ----------- | ----------- |
| 佐藤 | 〇 | 〇 |    |    |
| 田中 |    | 〇 |    | 〇 |
| 鈴木 |    |    |    | 〇 |
| 加藤 |    | 〇 |    |    |
| 中村 | 〇 |    |    | 〇 |
| 山田 |    | 〇 |    |    |
| 小林 | 〇 |    | 〇 | 〇 |
| 斎藤 |    |    | 〇 | 〇 |
| 松井 | 〇 | 〇 | 〇 |    |

これをちゃんと解くためには整数計画法で立式しなおす必要があります。
もし適当でいいのでとりあえず解が欲しいなら、
- 一周目をアサインする
- アサインされた人を除いて、二周目をアサインする
とすることができます。すなわち、`cost.csv`を以下のようにします。
```csv
sato,      1, 1, 0, 0
tanaka,    0, 1, 0, 1
suzuki,    0, 0, 0, 1
kato,      0, 1, 0, 0
nakamura,  1, 0, 0, 1
yamada,    0, 1, 0, 0
kobayashi, 1, 0, 1, 1
saito,     0, 0, 1, 1
matsui,    1, 1, 1, 0
```
これを実行すると次のようになります。
```
input:
      sato [1. 1. 0. 0.]
    tanaka [0. 1. 0. 1.]
    suzuki [0. 0. 0. 1.]
      kato [0. 1. 0. 0.]
  nakamura [1. 0. 0. 1.]
    yamada [0. 1. 0. 0.]
 kobayashi [1. 0. 1. 1.]
     saito [0. 0. 1. 1.]
    matsui [1. 1. 1. 0.]
assignment:
      sato [1. 0. 0. 0.]
    tanaka [0. 1. 0. 0.]
    suzuki [0. 0. 0. 1.]
      kato [0. 0. 0. 0.]
  nakamura [0. 0. 0. 0.]
    yamada [0. 0. 0. 0.]
 kobayashi [0. 0. 1. 0.]
     saito [0. 0. 0. 0.]
    matsui [0. 0. 0. 0.]
```
よって、佐藤・田中・鈴木・小林さんに座長が割り振られました。
この４人を取り除いた`cost2.csv`を作り、それを用いて再度実行します。
```csv
kato,      0, 1, 0, 0
nakamura,  1, 0, 0, 1
yamada,    0, 1, 0, 0
saito,     0, 0, 1, 1
matsui,    1, 1, 1, 0
```
この結果は次になります。
```
input:
      kato [0. 1. 0. 0.]
  nakamura [1. 0. 0. 1.]
    yamada [0. 1. 0. 0.]
     saito [0. 0. 1. 1.]
    matsui [1. 1. 1. 0.]
assignment:
      kato [0. 1. 0. 0.]
  nakamura [1. 0. 0. 0.]
    yamada [0. 0. 0. 0.]
     saito [0. 0. 0. 1.]
    matsui [0. 0. 1. 0.]
```
よって、加藤・中村・斎藤・松井に割り振られました。山田さんはお休みです。
結論として、次のようになりました。
|      | 13:00-13:30 | 13:30-14:00 | 14:00-14:30 | 14:30-15:00 | 
| ---- | ----------- | ----------- | ----------- | ----------- |
| 佐藤 | 〇 |    |    |    |
| 田中 |    | 〇 |    |    |
| 鈴木 |    |    |    | 〇 |
| 加藤 |    | 〇 |    |    |
| 中村 | 〇 |    |    |    |
| 山田 |    |    |    |    |
| 小林 |    |    | 〇 |    |
| 斎藤 |    |    |    | 〇 |
| 松井 |    |    | 〇 |    |

この割り振りがうまくいかないときもあります。例えば、一周目で「どのスロットもいける人」をたくさん選んでしまい、二周目の人はスロット選択の余裕がない場合などです。
その場合、一周目を実行するときに「どのスロットもいける人」を除外してみるとよいです。