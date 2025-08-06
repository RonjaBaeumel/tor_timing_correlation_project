# Timing Correlation Analysis

This document summarizes the results of this timing-based correlation analysis across the tested Tor traffic behaviors.

## Method Summary
- Captured traffic in a local Tor network for 4 traffic types: regular, burst, random, parallel
- Extracted timestamps from `.pcap` files using `tshark`
- Binned timestamps into 100ms windows and normalized
- Computed maximum cross-correlation scores between client and server captures

### Assumption: Known Client–Server Pairs
In this study, each .`pcap` file is recorded from a controlled setup with synchronized Tor client and server sessions. For every clientX.pcap, we know the corresponding serverX.pcap.

This assumption allows us to directly compute cross-correlations between matching pairs, which helps validate the effectiveness of the timing correlation metric under ideal conditions.

 `Note:` In real-world scenarios, such exact pairing is not available to attackers. A practical correlation attack would need to identify the most likely server for each observed client based on correlation scores across all possible combinations.

#### Future work could explore this more realistic threat model by:
- Removing known pairings,
- Performing full NxN correlation analysis (all clients vs. all servers),
- Using ranking-based success metrics (e.g., Top-1 or Top-k match accuracy).

## Results
### Cross-Correlation Scores by Traffic Type
![Correlation Plot](results/correlation_plot.png)

Calculating the cross-correlation between client and server packet timestamps gives a similarity score, meaning a score to measure how well-aligned the patterns are between both sides.
- High correlation score → traffic patterns on both ends are predictable and aligned → easier to correlate (bad for anonymity)
- Low correlation score → more noise, jitter, or randomness → harder to correlate (better for anonymity)


#### Interpretation
| **Traffic Type** | **Median Score** | **Variance** | **Interpretation** |
|------------------|------------------|--------------|---------------------|
| **Burst**        | ~125             | Low          | Low correlation: short, bursty, less predictable traffic |
| **Regular**      | ~170             | Low          | Moderately correlated, regular behavior, predictable timing |
| **Parallel**     | ~180             | Medium       | Concurrent streams increase alignment; correlation slightly higher |
| **Random**       | ~280–300         | High         | Surprisingly high correlation — may not be truly random in timing |

- **Burst**
    - Short traffic bursts likely lead to sparse patterns with minimal alignment between endpoints.
    - Time gaps between bursts reduce the ability to correlate.
    - Consistent with realistic lightweight use or polling behavior.
    - Expected to provide **better anonymity**.

- **Regular**
    - Consistent request intervals and response patterns result in a stable and reproducible correlation structure.
    - Mimics "typical" user behavior like polling APIs or loading a single page.
    - Moderate correlation makes it **somewhat susceptible** to correlation attacks.

- **Parallel**
    - Simultaneous streams generate overlapping traffic at both ends.
    - Increases the overall traffic volume and timing consistency.
    - Can create **accidental synchronization**, raising correlation.
    - Reflects real-world usage like loading multiple resources at once.

- **Random**
    - Very high correlation suggests the traffic is **not truly random in timing**.
    - Could be due to:
    - Poor entropy in randomization
    - Uniform distribution of intervals
    - Synchronized start times or structured packet intervals
    - Needs review: true randomness in traffic timing would typically reduce correlation.
    - As it stands, would be **highly vulnerable** to traffic analysis.


## Conclusion
The experiment confirms that:
- Timing-based correlation is effective under many traffic conditions.
- Traffic shaping (e.g., bursts or delays) can significantly reduce vulnerability.
- Randomness alone does not guarantee safety and can sometimes produce correlatable patterns.