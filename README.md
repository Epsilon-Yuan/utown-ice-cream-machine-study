# Question 1

> There is a Ben and Jerry's ice cream machine at UTown that charges $1 to play. Given that the price of a small tub is around $6, what is the distribution that best models the expected number of tries before successfully grabbing one of the tubs and how would you derive and compute the parameter(s) for this distribution from actual data?
>
> Bonus points for you if you try this in person and provide a GitHub repository to showcase your work.

## Solution

若每次尝试相互独立，且成功概率固定为 \(p\)，则成功前的尝试次数服从**几何分布**。令 \(T\) 为直到成功为止的总尝试次数（包含成功的那一次）：

\[
P(T=t)=(1-p)^{t-1}p,\quad t=1,2,\ldots
\]

\[
E[T]=\frac{1}{p},\qquad \operatorname{Var}(T)=\frac{1-p}{p^2}.
\]

若“成功前的次数”只计算失败次数，则其期望是 \((1-p)/p\)。

本项目的程序用**每次尝试的成功/失败记录**估计 \(p\)：每行代表一次投币尝试，`success=1` 表示成功拿到冰淇淋，`success=0` 表示失败。若共记录 \(n\) 次尝试、其中成功 \(s\) 次，则最大似然估计为

\[
\hat p=\frac{s}{n}=\frac{\text{成功次数}}{\text{尝试总次数}}.
\]

将 \(\hat p\) 代入几何分布，平均需要 \(1/\hat p\) 次尝试，平均花费约为 \$\(1/\hat p\)。以一桶约 $6 作为价值基准，期望花费低于 $6 的条件是 \(p>1/6\)。

## Data

上传或填写 `data/attempts.csv`，只需一列：

| Column | Description |
| --- | --- |
| `success` | 每次尝试的结果：`1` = 成功，`0` = 失败；一行对应一次尝试 |

采数模板：[data/attempts_template.csv](data/attempts_template.csv)。填好记录后运行：

```bash
python analyze.py data/attempts.csv
```

程序会计算 \(\hat p\)、95% Wilson 区间、估计的期望尝试次数及花费。**目前尚无 UTown 现场观测数据**；仓库提供的是空白模板和分析程序，不代表已完成现场实验。
