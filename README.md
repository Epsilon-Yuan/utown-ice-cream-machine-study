# Questions 1-3: Statistical Models and Answers

## Question 1

> There is a Ben and Jerry's ice cream machine at UTown that charges \$1 to play. Given that the price of a small tub is around \$6, what is the distribution that best models the expected number of tries before successfully grabbing one of the tubs and how would you derive and compute the parameter(s) for this distribution from actual data?
>
> Bonus points for you if you try this in person and provide a GitHub repository to showcase your work.

### Answer: a geometric waiting time

Assume each paid play has two outcomes, win or loss, and that plays are independent with the same win probability p. Let T count all plays up to and including the first win. A geometric distribution is then the natural starting model:

$$
P(T=t)=(1-p)^{t-1}p,\quad t=1,2,\ldots,\quad 0<p\leq1.
$$

$$
E[T]=\frac{1}{p},\qquad Var(T)=\frac{1-p}{p^2}.
$$

If only failures before the win are counted, let F=T-1. Its support starts at zero and its mean is:

$$
E[F]=\frac{1-p}{p}.
$$

These are model assumptions, not facts established about the machine. Player skill, changes in the tub positions, or an attempt-dependent payout mechanism could make a constant-p independent-trial model unsuitable. Actual observations are needed to assess the fit. The stated prices do not determine p; in particular, they do not imply that p equals 1/6.

### Method 1: Record every play outcome

Record 1 for a win and 0 for a loss. With n recorded plays and s wins, the likelihood and log-likelihood are:

$$
L(p)=p^s(1-p)^{n-s}
$$

$$
\ell(p)=s\log(p)+(n-s)\log(1-p).
$$

Setting the derivative to zero gives the maximum-likelihood estimate:

$$
\hat p=\frac{s}{n}.
$$

The program `analyze.py` reads one `success` value per play. Include failures from players who stop without a win. When stopping and inclusion rules are ignorable for this likelihood, recording all observed plays still gives the estimate above. Keep the observation plan independent of favorable results.

Its Wilson interval is an approximate binomial interval for a number of plays fixed before the outcomes are seen. It does not automatically retain 95% coverage if collection stops at a chosen number of wins or after inspecting the results. Such designs need intervals calibrated to their stopping rule.

### Method 2: Record complete waiting times

Select sessions before their outcomes are known and follow every selected session until its first win. For m such sessions, let T_j be the number of plays in session j, including the winning play. Then:

$$
L(p)=p^m(1-p)^{\sum_{j=1}^{m}T_j-m}
$$

$$
\hat p=\frac{m}{\sum_{j=1}^{m}T_j}.
$$

The program `analyze_sessions.py` reads one `attempts_to_first_win` value per session. This method is appropriate only when all selected sessions are followed through the win. Watching many players and keeping only those who win, while dropping quitters or unfinished sessions, generally selects shorter waits and overestimates p. If any selected sessions end without a win, use the attempt-level records and retain their failures.

For the same fully observed sessions, both methods give the same estimate. The reciprocal of the waiting-time sample mean is a maximum-likelihood estimate of p, but it is generally biased upward in finite samples; the sample mean itself is unbiased for the expected waiting time under the geometric model.

### Expected spending and the bonus

At a cost of 1 per play, the estimated expected spending per win is 1/p_hat in the same currency. The stated tub value of 6 gives the following comparison:

$$
E[\text{spending}]=\frac{1}{p},\qquad
E[\text{spending}]<6\ \text{when}\ p>\frac{1}{6}.
$$

This is a spending benchmark, not an estimate of the machine's win probability or the operator's break-even point.

The local repository contains two programs and two empty CSV templates, with no recorded in-person observations or empirical success-rate result. Preparing a repository alone does not complete the bonus's in-person requirement. For the full bonus, submit genuine field observations and the GitHub repository link.

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

### Bonus: examine the chi-square assumptions

> The methodology in this [article](https://blogs.sas.com/content/iml/2017/02/20/proportion-of-colors-mandms.html?utm_source=Twitter&utm_medium=social-voicestorm&utm_content=1f687eef-9380-4f8e-a23d-469c2cab502d) is flawed. Can you explain why? The answer has something to do with chi-square so if you proposed to use chi-square, you should think harder about the assumptions behind chi-square.

The important question is whether the ordinary chi-square null distribution describes the data collection process. Chi-square testing is not inherently inappropriate for candy colors.

**Independence concerns the individual observations, not the six count totals.** In a fixed-size multinomial sample, the color counts are dependent because they sum to the sample size. That dependence is already built into Pearson's test and its five degrees of freedom. It is not a reason to reject the test. The elementary candy observations must instead be sampled in a way that justifies the multinomial model. Expected cell counts must also be sufficiently large; the 712-candy example easily satisfies the usual expected-count check. See the [NIST description of the test](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35f.htm).

**The article's sampling design leaves independence and homogeneity uncertain.** It describes weekly scoops from communal containers filled using large bags. Shared, varying packet or batch composition can create dependence or extra variation that ordinary pooled multinomial inference misses. However, being in the same bag does not itself prove dependence, and mixing plants does not automatically invalidate a chi-square test. If a source is independently selected for every candy with a fixed mixing probability, the resulting colors are still independent with one fixed mixture vector. Sampling without replacement also need not be a serious problem when the sampled fraction of a well-mixed population is small. The pooled totals do not establish which mechanism applied; packet or batch records are needed to assess it.

**There is a documented concern about data-dependent continuation.** The article describes a nonsignificant preliminary analysis at about 300 candies, inspection of the green/blue discrepancies, and a decision to collect more. The ordinary final chi-square p-value does not account for an arbitrary outcome-driven stopping or reporting rule. Its nominal significance level is therefore not automatically justified for the procedure actually used. The article does not give enough detail to establish the exact error rate or to claim that collection repeatedly continued until significance. A prespecified final sample size, a separate confirmation sample, or a method calibrated for the actual sequential design would address this concern. [Time-uniform inference](https://arxiv.org/abs/1810.08240) is one way to allow repeated monitoring.

**The scope of the conclusion also matters.** Rejecting the 2008 mix only rejects that benchmark; it does not identify a plant. Non-rejection of Cleveland means compatibility, not proof of Cleveland provenance. The strongest defensible critique checks the sampling and monitoring assumptions and the interpretation of non-rejection. It should not assert, without evidence, that the article's candies were dependent or that all chi-square tests are invalid here. A multinomial likelihood-ratio method inherits the same sampling assumptions.

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
