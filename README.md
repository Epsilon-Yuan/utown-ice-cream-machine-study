# Question 1

> There is a Ben and Jerry's ice cream machine at UTown that charges \$1 to play. Given that the price of a small tub is around \$6, what is the distribution that best models the expected number of tries before successfully grabbing one of the tubs and how would you derive and compute the parameter(s) for this distribution from actual data?
>
> Bonus points for you if you try this in person and provide a GitHub repository to showcase your work.

## Solution

Assume each play is independent and has the same probability of winning, $p$. The number of plays through the first win, $T$, follows a geometric distribution:

$$
P(T=t)=(1-p)^{t-1}p, \quad t=1,2,\ldots
$$

$$
E[T]=\frac{1}{p}, \qquad \operatorname{Var}(T)=\frac{1-p}{p^2}.
$$

If counting only the failures before the winning play, the expected number is $(1-p)/p$.

### Method 1: Record every play

Record each paid play as a success (`1`) or failure (`0`). For $n$ plays with $s$ wins, the maximum-likelihood estimate is

$$
\hat p=\frac{s}{n}=\frac{\text{number of wins}}{\text{number of plays}}.
$$

The program `analyze.py` reads one `success` value per row and computes this estimate.

### Method 2: Record completed waiting times

For each session that ends in a win, record the total number of plays up to and including that win. If there are $m$ completed sessions with waiting times $T_1,\ldots,T_m$, then

$$
\hat p=\frac{m}{\sum_{j=1}^{m}T_j}.
$$

The program `analyze_sessions.py` reads one `attempts_to_first_win` value per completed session. Do not put sessions with no observed win in this file.

The attempt-level program also reports a 95% Wilson interval for $p$, transformed to an interval for the expected number of plays, $1/p$. The methods give the same point estimate when they use the same complete sessions; the first method can also include individual plays from sessions that ended before a win.

Each play costs USD 1, so the estimated expected spend is USD $1/\hat p$. Compared with a tub valued at about USD 6, expected spend is below its value when $p>1/6$. This comparison does not account for time or enjoyment.

## Data and programs

Fill the appropriate CSV with real observations. Each row in the first file is one play; each row in the second file is one completed session.

| Program | Data file | Required column | Row represents |
| --- | --- | --- | --- |
| `analyze.py` | `data/attempts_template.csv` | `success` (`1` = win, `0` = loss) | One paid play |
| `analyze_sessions.py` | `data/completed_sessions_template.csv` | `attempts_to_first_win` (positive integer) | One session ending in a win |

Run either program with:

```bash
python analyze.py data/attempts_template.csv
python analyze_sessions.py data/completed_sessions_template.csv
```

The CSVs contain headers only; no in-person UTown observations have been collected for this project.
