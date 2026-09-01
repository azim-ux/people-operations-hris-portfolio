# Research Foundation

## Evidence-to-design map

| Design choice | Evidence basis | Implementation | Boundary |
|---|---|---|---|
| Versioned skill vocabulary | O*NET 31.0 provides a maintained occupational database and reusable content | 20 local competencies retain O*NET occupation-code provenance | O*NET descriptors require local role validation |
| Multiple assessment standards | Workplace competence is better represented by fit-for-purpose evidence than a single survey | Work samples, simulations, rubrics, document audits, and multi-rater evidence | Scores are synthetic; no reliability or validity coefficient is claimed |
| Competency model distinct from job analysis | Sanchez and Levine distinguish strategic competency modeling from conventional job analysis | Broad enterprise capabilities coexist with department skills | Broad constructs can become fuzzy unless behavioral indicators are maintained |
| Four-level evaluation | Kirkpatrick separates Reaction, Learning, Behavior, and Results | IDP records include one governed field per level | Higher levels require stronger designs and should not be inferred from lower levels |
| Cohort-level business outcomes | Operational metrics belong at the process/cohort level | Yield, scrap, and savings are shown as governed aggregate results | The demonstration is non-causal and does not attribute results to individuals |

## Primary sources

### O*NET database

The official O*NET Resource Center identifies O*NET 31.0 as the current database, released in August 2026. The database is sponsored by the U.S. Department of Labor, Employment and Training Administration and developed by the National Center for O*NET Development. O*NET data are distributed under CC BY 4.0.

- O*NET Resource Center, [Current database](https://www.onetcenter.org/database.html).
- O*NET Resource Center, [Database releases archive](https://www.onetcenter.org/db_releases.html).

The lab uses occupational codes as provenance anchors, not as a claim that the local competency wording is an official O*NET descriptor. Local names, categories, proficiency targets, and assessment standards are designed for this synthetic scenario.

### Competency modeling and measurement

Sanchez and Levine (2009) explain that competency modeling and traditional job analysis serve related but different purposes. Competencies are often broader, more strategy-linked constructs; conventional internal-consistency logic may therefore be insufficient on its own. This supports explicit behavioral evidence, multi-rater agreement where appropriate, and disciplined version control.

Lin, Livesey, and Tuzinski (2023) describe modular workplace competency assessment and the value of tailoring evidence to the construct and work context. The lab accordingly avoids treating completion as mastery and assigns an assessment standard to every competency.

- Sanchez, J. I., & Levine, E. L. (2009). [What is (or should be) the difference between competency modeling and traditional job analysis?](https://doi.org/10.1016/j.hrmr.2008.10.002) *Human Resource Management Review, 19*(2), 53–63.
- Lin, Y., Livesey, P. V., & Tuzinski, K. (2023). [Assessing competencies in the workplace: A modular approach](http://jattjournal.net/index.php/atp/article/view/157796). *Journal of Applied Testing Technology, 24*(1), 14–33.

### Kirkpatrick model

The official model defines four distinct levels: Reaction, Learning, Behavior, and Results. The supporting guidance treats evaluation as a connected process that starts with desired organizational results and the critical behaviors required to reach them.

- Kirkpatrick Partners, [The Kirkpatrick Model](https://www.kirkpatrickpartners.com/the-kirkpatrick-model/).
- Kirkpatrick Partners, [The New World Kirkpatrick Model overview](https://www.kirkpatrickpartners.com/wp-content/uploads/2024/03/the-new-world-kirkpatrick-model.pdf).

## Measurement stance

The dashboard uses descriptive, governed indicators:

1. **Current proficiency** is a synthetic 1–5 workforce average tied to the listed assessment standard.
2. **Target proficiency** is a role/strategy baseline and must be approved by skill owners.
3. **Gap** equals current minus target; a negative number indicates a development priority.
4. **Mastery** is a constructed percentage used for portfolio demonstration.
5. **Nine-box placement** is produced by explicit three-point performance and potential inputs.
6. **Level 4** figures are illustrative cohort outcomes, not proof that training caused the change.

## What is deliberately not claimed

- No predictive validity, criterion validity, test reliability, or return-on-investment coefficient has been estimated.
- No individual employment decision should be made from these records.
- No demographic fairness analysis is possible because protected attributes are intentionally absent.
- No finding generalizes beyond this synthetic 70-person scenario.
- The business outcomes are non-causal; a production evaluation would need an agreed counterfactual or other defensible design.

## Production evidence roadmap

Before deployment, convene role incumbents and subject-matter experts; define observable behavior anchors; pilot the assessments; test inter-rater agreement and score stability where applicable; monitor missingness and adverse patterns; document accommodations; and review targets at each ontology release. Level 4 analysis should pre-register the business metric, attribution window, comparison design, and confounder log.
