# Executive Summary Deck Outline

Final file: `Executive_Summary-Team1.pptx`

Maximum length: 5 slides.

Audience: non-technical director, VP, or executive-level reader.

## Slide 1: Problem And Data

- Predict whether a red wine will receive a high sensory quality score.
- Dataset is UCI red wine quality data.
- High quality wines are the minority class.
- Business use is early screening before extra tasting-panel review.

## Slide 2: Modeling Approach

- Create binary target from quality score.
- Use stratified train/test split.
- Compare logistic regression, decision tree, and random forest.
- Use cross-validation for tuning and threshold selection.

## Slide 3: Final Model

- Name selected final model.
- Report AUC, F1, and accuracy.
- Explain that F1 matters because high quality wines are uncommon.
- Use ROC curve as main visual.

## Slide 4: Key Drivers

- Show top variable-importance predictors.
- Explain that model drivers are useful signals, not proof of causation.
- Emphasize alcohol, acidity, sulphates, density, and sulfur dioxide if they rank highly.

## Slide 5: Recommendation

- Use model scores to rank wines for extra review.
- Do not use model as final quality decision.
- Improve with external validation and richer business data.
- Disclose AI-assisted support.

