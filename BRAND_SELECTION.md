# Brand Selection Candidates

Based on a complete pass of the dataset, we calculated accurate conversation metrics to rank candidate brands.

## Scoring Methodology
The final score is a weighted combination of normalized metrics (0-1):
- **Volume (0.2)**: High volume allows for robust evaluation sets.
- **Response Rate (0.2)**: Indicates completeness of brand representation.
- **Multi-turn (0.3)**: Measures complex conversations requiring context.
- **Depth (0.2)**: Average turns per thread.
- **Quality (0.1)**: Proxy using length of responses.

## Top 10 Brands

| Rank | Brand | Brand Vol | Cust Vol | Resp Rate | Multi-turn % | Avg Depth | Final Score |
|---|---|---|---|---|---|---|---|
| 1 | AmazonHelp | 169840 | 169840 | 1.00 | 0.49 | 2.5 | 0.88 |
| 2 | ATVIAssist | 17650 | 18871 | 0.94 | 0.67 | 2.6 | 0.76 |
| 3 | VerizonSupport | 17966 | 17966 | 1.00 | 0.53 | 2.5 | 0.73 |
| 4 | idea_cares | 15724 | 15724 | 1.00 | 0.46 | 2.5 | 0.66 |
| 5 | VirginTrains | 27817 | 28784 | 0.97 | 0.50 | 2.4 | 0.66 |
| 6 | XboxSupport | 24557 | 24557 | 1.00 | 0.43 | 2.4 | 0.65 |
| 7 | MicrosoftHelps | 11304 | 11304 | 1.00 | 0.44 | 2.4 | 0.64 |
| 8 | O2 | 16212 | 16212 | 1.00 | 0.44 | 2.4 | 0.64 |
| 9 | YahooCare | 906 | 920 | 0.98 | 0.49 | 2.4 | 0.63 |
| 10 | AmericanAir | 36764 | 36764 | 1.00 | 0.40 | 2.4 | 0.63 |

## Recommendations
I recommend choosing one of the top 3 brands for the final agent. High multi-turn ratio is especially important for testing historical retrieval.

> Please review the `data/processed/brand_ranking.csv` file for complete auditing of all brands and raw metrics.