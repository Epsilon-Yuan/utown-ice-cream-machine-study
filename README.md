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

There are two practical ways to estimate the win probability.

### Method 1: Record every play outcome

Let X_i equal 1 for a win and 0 for a loss. For n recorded plays, let s be the total number of wins. The likelihood and maximum-likelihood estimate are:

$$
s=\sum_{i=1}^{n}X_i
$$

$$
L(p)\propto p^s(1-p)^{n-s}
$$

$$
\hat p=\frac{s}{n}
$$

The program analyze.py uses this method. Its input has one success value per paid play. It can include observed attempts from sessions that ended before a win, provided the win probability stayed constant.

### Method 2: Record completed waiting times

For m sessions that each ended in a win, let T_j be the number of plays in session j, including the winning play. The likelihood and maximum-likelihood estimate are:

$$
L(p)=p^m(1-p)^{\sum_{j=1}^{m}T_j-m}
$$

$$
\hat p=\frac{m}{\sum_{j=1}^{m}T_j}
$$

The program analyze_sessions.py uses this method. Its input has one attempts_to_first_win value per completed session. Do not include an unfinished session in this data file.

For the same complete sessions, the two estimates are equal: $m$ wins divided by the total number of plays. The first method is more flexible when some sessions have no observed win.


## Question 2

> M&M candies are manufactured at two different plants in the US with the following color distribution:
>
> Cleveland: Red=0.131, Orange=0.205, Yellow=0.135, Green=0.198, Blue=0.207, and Brown=0.124.
>
> Hackettstown: Red=0.125, Orange=0.25, Yellow=0.125, Green=0.125, Blue=0.25, and Brown=0.125.
>
> Suppose you bought many packets of M&M, how can you determine which plant these packets came with statistical testing?

### Answer: specify the sampling model and hypotheses

Keep each packet's color counts. First consider the hypothesis that all sampled candies come from one plant, with independent colors and the supplied fixed probability vector. Conditional on the number of candies, the counts are multinomial.

Write p_C and p_H for the Cleveland and Hackettstown vectors. A direct comparison can test Hackettstown against Cleveland:

$$
H_0:p=p_H,\qquad H_1:p=p_C.
$$

For observed counts x_c across the six colors, the common multinomial coefficient cancels from the likelihood ratio:

$$
\Lambda=\log\frac{L_C}{L_H}
=\sum_c x_c\log\left(\frac{p_{C,c}}{p_{H,c}}\right).
$$

The numerical weights, in red, orange, yellow, green, blue, brown order, are:

| Color | Cleveland probability | Hackettstown probability | Log-ratio weight |
| --- | ---: | ---: | ---: |
| Red | 0.131 | 0.125 | 0.046884 |
| Orange | 0.205 | 0.250 | -0.198451 |
| Yellow | 0.135 | 0.125 | 0.076961 |
| Green | 0.198 | 0.125 | 0.459953 |
| Blue | 0.207 | 0.250 | -0.188742 |
| Brown | 0.124 | 0.125 | -0.008032 |

Thus:

$$
\Lambda\approx0.046884R-0.198451O+0.076961Y
+0.459953G-0.188742B-0.008032Br.
$$

A positive value favors Cleveland; a negative value favors Hackettstown. Choosing the larger likelihood is a classification rule. With equal prior probabilities and equal error costs, its cutoff is zero. That cutoff alone is not a 5% significance test.

For a formal fixed-sample test at level alpha, use the upper tail of Lambda under the Hackettstown multinomial null. For example, the exact p-value is:

$$
p_{\text{test}}=P_H\bigl(\Lambda(X)\geq\Lambda(x_{\text{observed}})\bigr).
$$

It can be evaluated by summing the relevant multinomial probabilities or simulated under the null using the planned sample size. Do not automatically compare twice this log-ratio with a chi-square distribution: these are two fixed, non-nested plant models, so a Wilks chi-square calibration does not follow.

Both the likelihood method and an ordinary multinomial chi-square test require a suitable sampling model. Merely changing the statistic does not fix dependence within packets. If all packets have one common plant probability vector and satisfy the model, their counts can be pooled. If packets may come from different plants, classify them separately or fit a packet-level mixture model. With batch dependence or extra packet variation, use independent packets/batches as sampling units and model that variation. The larger likelihood also cannot establish provenance if both supplied models fit badly.

### Numerical example using the article's reported data

The linked article provides observed counts, which can be used as a worked example. These are its published data, not a new sample collected for this repository:

| Color | Observed | Expected under Cleveland | Expected under Hackettstown |
| --- | ---: | ---: | ---: |
| Red | 108 | 93.272 | 89 |
| Orange | 133 | 145.960 | 178 |
| Yellow | 103 | 96.120 | 89 |
| Green | 139 | 140.976 | 89 |
| Blue | 133 | 147.384 | 178 |
| Brown | 96 | 88.288 | 89 |
| Total | 712 | 712 | 712 |

Using unrounded weights gives:

$$
\Lambda=24.656156,\qquad \frac{L_C}{L_H}\approx5.1054\times10^{10}.
$$

Under the assumed model, the data favor Cleveland strongly relative to Hackettstown. This likelihood ratio is not a posterior probability and is not a p-value.

For comparison, the ordinary Pearson goodness-of-fit statistic for a specified plant is:

$$
X_g^2=\sum_c\frac{(O_c-np_{g,c})^2}{np_{g,c}}.
$$

With six fixed probabilities and no fitted parameters, its usual reference has five degrees of freedom. The article's counts give these nominal results:

| Null probability vector | Pearson statistic | df | Nominal p-value |
| --- | ---: | ---: | ---: |
| Cleveland | 6.073951 | 5 | 0.299090 |
| Hackettstown | 57.651685 | 5 | 3.7113e-11 |
| 2008 mix used in the article | 17.353052 | 5 | 0.00387668 |

The 2008 vector, in the same color order, is (0.13, 0.20, 0.14, 0.16, 0.24, 0.13). These p-values reproduce the ordinary fixed-sample calculations; their interpretation still depends on the sampling and monitoring issues in the bonus. Not rejecting Cleveland does not prove that it is the source.

The assignment gives no counts for the packets you personally bought, so their source cannot be determined from the question's probability vectors alone. Substitute those packets' actual counts for a real analysis.

### Optional sample-size calculation

For one independently sampled candy, the log-ratio has mean 0.02685419 and variance 0.05771025 under Cleveland, and mean -0.02482755 and variance 0.04560301 under Hackettstown. For the cutoff-zero classifier, the normal approximation to a 5% error probability gives:

$$
n_C\approx\left(\frac{1.644854\sqrt{0.05771025}}{0.02685419}\right)^2
=216.513
$$

$$
n_H\approx\left(\frac{1.644854\sqrt{0.04560301}}{0.02482755}\right)^2
=200.161.
$$

Rounding upward suggests about 217 independent candies from one common source. This is an approximate classification planning figure, not an exact guarantee or a count of independent packets.
### Bonus: why the article's chi-square analysis is questionable

> The methodology in this [article](https://blogs.sas.com/content/iml/2017/02/20/proportion-of-colors-mandms.html?utm_source=Twitter&utm_medium=social-voicestorm&utm_content=1f687eef-9380-4f8e-a23d-469c2cab502d) is flawed. Can you explain why? The answer has something to do with chi-square so if you proposed to use chi-square, you should think harder about the assumptions behind chi-square.

The article reports 712 candies collected as one scoop per week over multiple weeks from communal containers refilled with large bags. It first tested those pooled counts against an older 2008 color mix. Crucially, it also says that after analyzing about 300 candies, the chi-square test was not significant; after looking at the residual pattern and noticing green and blue contributed most to the discrepancy, the author decided to collect more data. The conventional chi-square p-value computed on the final 712 candies treats the sample size and analysis as if they had been fixed in advance. Because the decision to continue was influenced by interim results, the nominal 5% p-value need not have its advertised Type I error rate. The final test should account for sequential monitoring or use a fresh, independent confirmation sample.

The usual Pearson goodness-of-fit reference distribution also relies on independent categorical observations from one fixed probability vector, with sufficiently large expected counts. Sparse expected counts are not the problem here. The collection design raises a separate independence and homogeneity concern: candies in a scoop may come from the same bag or production lot, and repeated samples from replenished containers may reflect batches. The article later discovers that the two plants use different color mixes. If packages or scoops have different plant/batch compositions, treating all 712 individual candies as independent draws from one fixed mix can underestimate variability and make the chi-square p-value too small. This concern depends on the actual sampling and mixing process; it cannot be resolved from pooled color totals alone.

Finally, rejecting the 2008 color vector establishes only that the pooled sample differs from that benchmark. It does not identify either factory. A chi-square goodness-of-fit test would be valid for the narrow null if the candies were an independent random sample from one homogeneous source with a fixed mix, and the sample size had not been selected based on interim outcomes. To compare plants, retain counts by packet or batch, record manufacturing codes if available, and use a packet-level multinomial or hierarchical model. If sequential looks are planned, use a sequentially valid procedure or a separately collected validation sample.

For a single homogeneous source with observed counts $O_c$, the usual goodness-of-fit statistic is

$$
X_g^2=\sum_c\frac{(O_c-np_{g,c})^2}{np_{g,c}}, \quad df=5,
$$

when the six probabilities are fixed in advance and the multinomial assumptions hold. The statistic cannot be calculated without observed counts.

## Question 3

> Suppose you observed k people playing the Ben and Jerry's ice cream machine at UTown. You counted the number of times N that the machine was played in order to get k tubs of ice cream. What distribution will best fit the expected number of times N one would have to play to obtain k tubs of ice cream?

### Answer: trials through the k-th win

Under independent plays with one constant success probability p, let N count the total plays through the k-th win. Then N follows a negative binomial distribution in the total-trials convention:

$$
P(N=n)=\binom{n-1}{k-1}p^k(1-p)^{n-k},\quad n=k,k+1,\ldots
$$

The last play must be a win. The first n-1 plays must contain k-1 wins, which explains the binomial coefficient. Equivalently, N is the sum of k independent geometric waiting times:

$$
E[N]=\frac{k}{p},\qquad Var(N)=\frac{k(1-p)}{p^2}.
$$

Here k is the target number of wins/tubs. The number of people alone does not determine this distribution: observing k people who may quit without winning is not the same experiment. If the number of plays is fixed in advance and the number of wins is counted, that win count is binomial instead.

Some software defines a negative binomial variable as the number of failures, F=N-k. In that convention:

$$
P(F=f)=\binom{f+k-1}{k-1}p^k(1-p)^f,\quad f=0,1,2,\ldots
$$

$$
E[F]=\frac{k(1-p)}{p},\qquad Var(F)=\frac{k(1-p)}{p^2}.
$$

If collection really stops at the k-th win, the likelihood gives:

$$
\hat p=\frac{k}{N}.
$$

This is a maximum-likelihood estimate, not generally an unbiased estimate under this stopping rule. Inference should use the negative-binomial sampling design. An estimate from earlier data can be used to predict k future wins via k/p_hat.

If players have different success probabilities, their waiting times generally have different geometric parameters and their sum is not a standard negative binomial. If the machine changes its probability after failures or wins, the independent constant-p model also needs revision. The geometric and negative binomial distributions are justified starting models under the stated assumptions, not empirically established fits to this particular machine.
