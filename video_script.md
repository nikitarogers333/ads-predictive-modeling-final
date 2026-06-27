# Video Presentation Script

## Slide 1: Problem Statement

This presentation summarizes my predictive modeling project. The goal is to predict whether a red
wine will receive a high sensory quality rating from basic chemistry measurements. I converted the
original quality score into a binary target. A wine rated seven or higher is treated as high
quality. Wines below seven are treated as not high quality. This is useful because organizations
often need to decide which products deserve extra review, more tasting-panel time, or premium
positioning. The model is not intended to replace human tasting. It is a decision-support layer that
ranks wines and helps focus limited attention.

## Slide 2: Business Motivation

The practical motivation is resource allocation. Tasting panels and expert reviews are valuable, but
they take time and coordination. Chemistry measurements are more standardized and can be collected
earlier in the process. If a model can identify wines that are more likely to score well, the
business can send those wines to a deeper review first. That does not mean the model makes the final
decision. It means the model helps create a shortlist. In a real workflow, that shortlist would
still be checked by people with domain knowledge.

## Slide 3: Dataset

The project uses the UCI Wine Quality red wine dataset. It contains 1,599 red wine samples. Each row
represents one wine, and each column records either a chemical property or the sensory quality
score. The predictors include fixed acidity, volatile acidity, citric acid, residual sugar,
chlorides, free sulfur dioxide, total sulfur dioxide, density, pH, sulphates, and alcohol. The
response variable was engineered from the original quality rating. This dataset is a good fit for
the assignment because it is clean, numeric, reproducible, and directly supports a classification
problem.

## Slide 4: Target And Class Balance

The target variable is imbalanced. The high quality class makes up about 13.6% of the data. That
matters because a model could get a high accuracy score by predicting the majority class too often.
In this project, accuracy is still reported, but it is not the main decision metric. The analysis
also reports sensitivity, specificity, precision, F1 score, and ROC AUC. Sensitivity tells us how
many high quality wines were found. Precision tells us how many predicted high quality wines were
actually high quality. F1 balances those two ideas.

## Slide 5: EDA Findings

The exploratory analysis shows that most wines are rated in the middle of the original quality
scale. The high quality group is smaller, but it has visible differences in several predictors. High
quality wines tend to have higher alcohol and higher sulphates. They tend to have lower volatile
acidity and lower density. These relationships make sense chemically and practically, but they are
not perfect separators. The boxplots show overlap between the high and not high classes. That
overlap means a perfect model is not realistic, and the model should be evaluated as a screening
tool.

## Slide 6: Preprocessing

The preprocessing workflow was intentionally simple and reproducible. First, I created a binary
target from the original quality score. Second, I removed the original quality score from the model
matrix so the model could not leak the answer. Third, I checked missing values. There were no
missing cells in the downloaded dataset. Fourth, I standardized numeric predictors for logistic
regression, because that model benefits from comparable scales. The tree-based models were fit on
the original predictor scales because trees split on thresholds and do not require standardization.

## Slide 7: Data Splitting

The data was split into training and test sets using a stratified eighty-twenty split.
Stratification matters here because the high quality class is small. Without stratification, the
test set could accidentally contain too many or too few high quality wines, which would make
evaluation unstable. The training set was used for model fitting, cross-validation, tuning, and
threshold selection. The test set was held out until the final evaluation. This creates a cleaner
estimate of how the selected workflow performs on data not used during model development.

## Slide 8: Validation Design

For validation, I used stratified five-fold cross-validation on the training data. Each fold
preserved the high versus not high class structure as much as possible. The decision tree was tuned
over several complexity parameter values. The random forest was tuned over several mtry values,
which control how many predictors are considered at each split. I also selected the classification
threshold using the cross-validation predictions. This is important because the default threshold of
zero point five is not always appropriate when the positive class is uncommon.

## Slide 9: Model Strategy

I compared three model families. Logistic regression was the baseline. It is easy to interpret, and
it tells us whether a simple linear probability pattern can solve the problem. The decision tree was
the second model. It can capture simple non-linear threshold rules and is still fairly easy to
explain. The random forest was the third model. It averages many trees and usually performs better
when relationships are non-linear or interactive. The final selection prioritized ranking quality,
F1 score, and practical usefulness for identifying high quality candidates.

## Slide 10: Metrics

The main model comparison metrics were ROC AUC, F1 score, accuracy, sensitivity, specificity, and
precision. ROC AUC measures how well the model ranks high quality wines above ordinary wines across
possible thresholds. F1 score balances precision and sensitivity for the high quality class.
Sensitivity matters because missing strong wines would reduce the value of the screening process.
Precision matters because sending too many weak candidates to human reviewers wastes time. Looking
at these metrics together gives a more honest view than accuracy alone.

## Slide 11: Final Test Results

The selected final model is Random forest. On the held-out test set, it produced a ROC AUC of 0.927,
an F1 score of 0.673, and accuracy of 0.894. Sensitivity was 0.795, and specificity was 0.910. These
results mean the final model separated high quality wines from ordinary wines well on the test set.
The model is especially useful as a ranking tool because ROC AUC evaluates the ordering of predicted
probabilities rather than only one fixed cutoff.

## Slide 12: Interpretation

The random forest variable importance results show which predictors were most useful for splitting
the classes. The top predictors were alcohol, volatile acidity, sulphates, density, citric acid.
These are plausible drivers, but they should be interpreted carefully. Variable importance does not
prove causation. It means these measurements helped the model separate wines that received higher
scores from the rest of the samples. The practical interpretation is that the model can produce a
ranked list of wines that are more likely to be high quality. A business could send the highest
scoring wines to extra sensory review first.

## Slide 13: Limitations And Next Steps

The main limitations are the narrow dataset, the absence of brand or price information, the lack of
external validation, and the fact that sensory quality is partly subjective. The dataset covers red
Vinho Verde wine, so results should not be assumed to generalize to all wines. In a production
setting, I would add more samples from more regions, include business variables such as price and
producer, calibrate the predicted probabilities, and test the model on newer external data before
using it operationally.

## Slide 14: Conclusion

The conclusion is that physicochemical measurements can provide useful signal for screening red wine
quality. The model should be used as decision support. It can prioritize wines for additional
review, but it should not make final quality decisions by itself. The best workflow is to treat
model scores as a ranked shortlist, then use expert review for the final call. AI assistance was
used to help organize and prepare materials, and that use is disclosed in the report. Before
submission, the student should review the code, metrics, and narrative closely.
