# Questions 1-3: Statistical Models and Answers

## Question 1

> There is a Ben and Jerry's ice cream machine at UTown that charges \$1 to play. Given that the price of a small tub is around \$6, what is the distribution that best models the expected number of tries before successfully grabbing one of the tubs and how would you derive and compute the parameter(s) for this distribution from actual data?
>
> Bonus points for you if you try this in person and provide a GitHub repository to showcase your work.

### Answer

Assume each play is independent and has a constant probability $p$ of winning. Let $T$ be the number of plays through and including the winning play. Then $T$ has a geometric distribution:

$$
P(T=t)=(1-p)^{t-1}p, \quad t=1,2,\ldots
$$

$$
E[T]=\frac{1}{p}, \qquad Var(T)=\frac{1-p}{p^2}.
$$

If the count includes only failures before the win, $F=T-1$, then $E[F]=(1-p)/p$.

There are two practical ways to estimate $p$:

1. **Record every play outcome.** Let $X_i=1$ for a win and $X_i=0$ for a loss. With $n$ recorded plays and $s=\sum_i X_i$ wins, the likelihood is proportional to $p^s(1-p)^{n-s}$, so
   $$
   \hat p=\frac{s}{n}.
   $$
   This is the method used by `analyze.py`. Its input has one `success` value per paid play. It can include all observed attempts even if some sessions ended before a win, provided the probability stayed constant.

2. **Record completed waiting times.** If $m$ sessions each end in a win, and $T_j$ is the number of plays in session $j$ including its winning play, the likelihood is
   $$
   L(p)=p^m(1-p)^{\sum_{j=1}^{m}T_j-m}.
   $$
   Maximizing it gives
   $$
   \hat p=\frac{m}{\sum_{j=1}^{m}T_j}.
   $$
   This is the method used by `analyze_sessions.py`; its input has one `attempts_to_first_win` value per completed session. Do not include an unfinished session in this data file.

For the same complete sessions, the two estimates are equal: $m$ wins divided by the total number of plays. The first method is more flexible when some sessions have no observed win.

At USD 1 per play, the estimated expected spend to win is USD $1/\hat p$. Compared with a tub valued at about USD 6, the expected spend is below the tub value when $p>1/6$. This comparison ignores time, enjoyment, and risk preferences. The repository currently has blank data templates and no in-person UTown observations, so it does not claim an empirical estimate of $p$.

## Question 2

M&M candies are manufactured at two US plants with these color probabilities:

| Color | Cleveland | Hackettstown |
| --- | ---: | ---: |
| Red | 0.131 | 0.125 |
| Orange | 0.205 | 0.250 |
| Yellow | 0.135 | 0.125 |
| Green | 0.198 | 0.125 |
| Blue | 0.207 | 0.250 |
| Brown | 0.124 | 0.125 |

### Answer: compare the plant likelihoods

For a packet with observed color counts $(R,O,Y,G,B,Br)$ and total $n$, model its counts as multinomial under each plant. The log-likelihood ratio is

$$
\Lambda=\log\frac{L_C}{L_H}
=\sum_c x_c\log\left(\frac{p_{C,c}}{p_{H,c}}\right).
$$

Substituting the probabilities in the question gives

$$
\Lambda \approx 0.0469R-0.1985O+0.0770Y+0.4600G-0.1887B-0.0080Br.
$$

If $\Lambda>0$, the observed colors are more likely under Cleveland; if $\Lambda<0$, they are more likely under Hackettstown. The likelihood ratio is $e^{\Lambda}$. With equal prior probabilities and equal misclassification costs, choose the plant with the larger likelihood. A formal test at a specified significance level should set its threshold from the null distribution, which can be calculated from the multinomial model or estimated by simulation.

For scale, the expected counts per 100 candies are:

| Color | Cleveland expected count | Hackettstown expected count |
| --- | ---: | ---: |
| Red | 13.1 | 12.5 |
| Orange | 20.5 | 25.0 |
| Yellow | 13.5 | 12.5 |
| Green | 19.8 | 12.5 |
| Blue | 20.7 | 25.0 |
| Brown | 12.4 | 12.5 |

Green is the most informative single color in the likelihood ratio; orange and blue support Hackettstown. Brown contributes very little. The directional Kullback-Leibler divergences are $D(C\|H)\approx0.02685$ and $D(H\|C)\approx0.02483$ nats per candy. For the per-candy log-likelihood ratio $W$, its variances are approximately $Var_C(W)=0.05771$ and $Var_H(W)=0.04560$. With an equal-prior classifier using threshold $\Lambda=0$, a normal approximation for a 5% error rate gives

$$
n_C\approx\left(\frac{1.645\sqrt{0.05771}}{0.02685}\right)^2\approx217, \qquad
n_H\approx\left(\frac{1.645\sqrt{0.04560}}{0.02483}\right)^2\approx201.
$$

Thus about 217 independently sampled candies is a rough planning figure for errors around 5% under either plant. Package-to-package variation can increase the required sample size.

The question supplies the plant probabilities but no observed packet counts, so it is not possible to identify the source of a particular real packet or calculate its p-value yet. Keep the color counts for each packet separate. If all packets are assumed to come from one plant, sum the packet log-likelihood ratios. If packets can come from different plants, classify or model them at the packet level; pooling them can hide a mixture. Package manufacturing codes can provide a direct source label for validation.

### Bonus: why the article's chi-square analysis is questionable

The linked [SAS article](https://blogs.sas.com/content/iml/2017/02/20/proportion-of-colors-mandms.html?utm_source=Twitter&utm_medium=social-voicestorm&utm_content=1f687eef-9380-4f8e-a23d-469c2cab502d) analyzes 712 candies collected as scoops over multiple weeks from communal containers supplied by large bags. It tests the pooled counts against an older, single set of 2008 proportions. The article later reports that the two plants use different color mixes.

A Pearson chi-square goodness-of-fit test assumes independent categorical observations drawn from one fixed probability vector (and sufficiently large expected counts). The important concern is not sparse expected counts: with 712 candies, the expected counts under the published proportions are large. Rather, candies from the same package or production lot may share a source and production conditions, so treating all 712 as independent draws can understate sampling variation. A mixture of plant-specific mixes also does not have the same package-level sampling behavior as independent draws from one homogeneous batch. If those assumptions fail, the usual chi-square reference distribution and p-value may be unreliable, often making evidence look stronger than it is.

There is also a scope issue: rejecting the 2008 proportions shows inconsistency with that particular benchmark; by itself it does not identify Cleveland or Hackettstown. If candies truly were random independent draws from a well-mixed bin with one fixed color vector, a chi-square test against a specified vector would be valid for that narrow null. The article's sampling design and later-discovered plant differences do not establish that assumption for the intended factory inference. A stronger analysis keeps packets as sampling units, records plant codes where possible, and uses packet-level multinomial or overdispersed/hierarchical models.

For a single homogeneous source with observed counts $O_c$, the usual goodness-of-fit statistic is

$$
X_g^2=\sum_c\frac{(O_c-np_{g,c})^2}{np_{g,c}}, \quad df=5,
$$

when the six probabilities are fixed in advance and the multinomial assumptions hold. The statistic cannot be calculated without observed counts.

## Question 3

Suppose $k$ people each win one tub, and $N$ is the total number of plays needed to obtain those $k$ wins.

### Answer

If all plays are independent and share one constant success probability $p$, then $N$ follows a negative binomial distribution: it is the total number of trials required to obtain $k$ successes.

$$
P(N=n)=\binom{n-1}{k-1}p^k(1-p)^{n-k}, \quad n=k,k+1,\ldots
$$

$$
E[N]=\frac{k}{p}, \qquad Var(N)=\frac{k(1-p)}{p^2}.
$$

Equivalently, $N$ is the sum of $k$ independent geometric waiting times. If counting only failures, let $F=N-k$; then

$$
P(F=f)=\binom{f+k-1}{k-1}p^k(1-p)^f, \quad f=0,1,2,\ldots
$$

If the observed total is $N$ plays for $k$ wins, the maximum-likelihood estimate is $\hat p=k/N$. Using an estimate from prior or independent data, the expected plays to obtain $k$ future tubs is $k/\hat p$. If player skill or machine conditions cause different success probabilities, the waiting times have different geometric parameters and their sum is not a standard negative binomial distribution; a model allowing player or session variation is then more appropriate.
