# Timing Correlation Analysis

This document summarizes the results of timing-based correlation analysis across different Tor traffic behaviors.

## Method Summary

- Captured traffic in a local Tor network for 4 traffic types: regular, burst, parallel, random
- Extracted timestamps from `.pcap` files using `tshark`
- Binned timestamps into 100ms windows and normalized
- Computed maximum cross-correlation scores between client and server captures

## Results

### Cross-Correlation Scores by Traffic Type

![Correlation Plot](results/correlation_plot.png)

#### Interpretation

- **Random traffic** shows the highest variance and maximum scores — making it potentially more exposed.
- **Burst traffic** consistently has the lowest correlation, suggesting it may help defend against linkability.
- **Parallel traffic** shows moderate vulnerability, possibly due to overlapping flows.
- **Regular traffic** has stable but moderately high correlation scores.

## Conclusion

The experiment confirms that:
- Timing-based correlation is effective under many traffic conditions.
- Traffic shaping (e.g., bursts or delays) can significantly reduce vulnerability.
- Randomness alone does not guarantee safety and can sometimes produce correlatable patterns.

