[implementing elo](https://mattmazzola.medium.com/implementing-the-elo-rating-system-a085f178e065)
## expected probability for player A vs B
- $E_a$ is the probability for player A
- $R_n$ is the rating for a specific player
# $$E_a = \frac{1}{1 + 10^{\frac{R_b - R_a}{400}}}$$
### new rating for player a, after playing player b
- scaling factor k is generally thirty two, but can be adjusted however
# $$
R_a' = R_a + \frac{R_b - R_a}{1 + 10^{\frac{R_b - R_a}{400}}}
$$

