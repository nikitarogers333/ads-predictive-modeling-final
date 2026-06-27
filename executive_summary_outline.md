# Executive Summary Deck Outline

Final file: `Executive_Summary-Team1.pptx`

Maximum length: 5 slides.

Audience: non-technical director, VP, or executive-level reader.

## Slide 1: Problem And Data

- Predict whether an online shopping session will generate revenue.
- Dataset is UCI Online Shoppers Purchasing Intention data.
- Purchases are the minority class.
- Business use is ranking sessions for targeted marketing or on-site intervention.

## Slide 2: Modeling Approach

- Create binary target from the Revenue field.
- Use stratified train/test split.
- Compare logistic regression, decision tree, and random forest.
- Use cross-validation for tuning and threshold selection.

## Slide 3: Final Model

- Name selected final model.
- Report AUC, F1, and accuracy.
- Explain that F1 matters because purchase sessions are uncommon.
- Use ROC curve as main visual.

## Slide 4: Key Drivers

- Show top variable-importance predictors.
- Explain that model drivers are predictive signals, not proof of causation.
- Emphasize page value, exit rate, product engagement, month, and traffic source if they rank highly.

## Slide 5: Recommendation

- Use model scores to rank sessions for controlled experiments.
- Do not assume targeted action creates incremental revenue without A/B testing.
- Improve with product, customer, pricing, margin, and campaign data.
- Disclose AI-assisted support.
