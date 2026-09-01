# Analysis Notes

## Reproducible headline metrics

- Synthetic records: 120
- Generated leavers: 24
- Generated attrition rate: 20.0%
- Highest generated department attrition rate: Customer Support

## Method

1. Generated a deterministic fictional workforce with a fixed random seed.
2. Validated unique IDs and allowed category values.
3. Calculated headcount, leaver count, attrition rate, average engagement, average performance, and average training hours.
4. Compared department and tenure groups using counts and rates.
5. Documented synthetic-data and non-causality limitations.

## Interpretation

The dashboard is descriptive. Differences are intentionally generated for learning and do not prove that engagement, absence, tenure, department, or any other field causes attrition.

## Suggested Power BI measures

```text
Headcount = DISTINCTCOUNT(HR[Employee_ID])
Leavers = CALCULATE([Headcount], HR[Attrition] = "Yes")
Attrition Rate = DIVIDE([Leavers], [Headcount])
Average Engagement = AVERAGE(HR[Engagement_Score])
Average Training Hours = AVERAGE(HR[Training_Hours_YTD])
```

## Interview preparation

Be ready to explain:

- why rate denominators matter;
- why synthetic data was used;
- why descriptive association is not causation;
- how missing values, duplicates, and inconsistent categories would be checked;
- what additional business context would be required before recommending action.
