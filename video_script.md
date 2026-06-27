# Video Presentation Script

## Slide 1: Problem Statement

This presentation summarizes my predictive modeling project. The goal is to predict whether an
online shopping session will generate revenue from behavior observed during the visit. I converted
the original Revenue field into a binary target called Purchase versus NoPurchase. This framing is
useful because e-commerce teams often need to decide which sessions deserve a marketing action, live
support, or retargeting follow-up. The model is not intended to make automatic customer-treatment
decisions by itself. It is a decision-support layer that ranks sessions by estimated purchase
intent.

## Slide 2: Business Motivation

The practical motivation is resource allocation. Most website sessions do not purchase, and
interventions are not free. Discounts can reduce margin, retargeting costs money, and live support
has limited capacity. If a model can identify sessions that are more likely to buy, the business can
prioritize those sessions for controlled experiments. That does not prove an intervention creates
incremental revenue. It means the model gives the business a stronger shortlist for testing than
broad untargeted rules.

## Slide 3: Dataset

The project uses the UCI Online Shoppers Purchasing Intention dataset. It contains 12,330 website
sessions. Each row represents one visit session. The predictors include administrative page
activity, informational page activity, product-related page activity, time spent on pages, bounce
rates, exit rates, page value, special day timing, month, operating system, browser, region, traffic
source, visitor type, and weekend status. The response is whether the session generated revenue.
This dataset is a strong fit for the assignment because it is public, reproducible, business-
focused, and contains both numeric and categorical predictors.

## Slide 4: Target And Class Balance

The target variable is imbalanced. Purchase sessions make up about 15.5% of the data. That matters
because a model could look accurate by predicting NoPurchase too often. In this project, accuracy is
reported, but it is not the only decision metric. The analysis also reports sensitivity,
specificity, precision, F1 score, and ROC AUC. Sensitivity tells us how many actual purchase
sessions were found. Precision tells us how many predicted purchase sessions were truly purchases.
F1 balances those two ideas.

## Slide 5: EDA Findings

The exploratory analysis shows clear but imperfect signal. Purchase sessions tend to have higher
page value and more product engagement. No-purchase sessions tend to show higher bounce rates and
higher exit rates. Conversion rates also vary by month and visitor type, which supports including
categorical predictors. The boxplots still show overlap between the purchase and no-purchase
classes. That overlap is important because it means a perfect classifier is unrealistic. The model
should be evaluated as a probability ranking tool, not as a simple rule that always knows who will
buy.

## Slide 6: Preprocessing

The preprocessing workflow was reproducible and focused on the modeling problem. First, I created
the binary purchase target from the Revenue field. Second, I removed the original Revenue field from
the model matrix so the model could not leak the answer. Third, I checked missing values and found
no missing cells. Fourth, I converted month, visitor type, weekend, operating system, browser,
region, and traffic type into categorical predictors. Fifth, I collapsed rare technical categories
into Other. Finally, I standardized numeric predictors for logistic regression while leaving tree-
based models on their original scales.

## Slide 7: Data Splitting

The data was split into training and test sets using a stratified eighty-twenty split.
Stratification matters because the purchase class is much smaller than the no-purchase class.
Without stratification, the test set could accidentally contain too many or too few purchase
sessions, which would make evaluation unstable. The training set was used for model fitting, cross-
validation, tuning, and threshold selection. The test set was held out until the final evaluation.
This gives a cleaner estimate of how the selected workflow performs on data not used during
development.

## Slide 8: Validation Design

For validation, I used stratified cross-validation on the training data. Each fold preserved the
purchase versus no-purchase class structure as much as possible. The decision tree was tuned over
several complexity parameter values. The random forest was tuned over several mtry values, which
control how many predictors are considered at each split. I also selected the classification
threshold using the cross-validation predictions. This matters because the default threshold of zero
point five is not always appropriate when the positive class is uncommon.

## Slide 9: Model Strategy

I compared three model families. Logistic regression was the baseline. It is easy to interpret, and
it tests whether a simpler linear probability pattern can solve the problem. The decision tree was
the second model. It can capture simple non-linear threshold rules and is still fairly easy to
explain. The random forest was the third model. It averages many trees and usually performs better
when relationships are non-linear or interactive. The final selection prioritized ranking quality,
F1 score, and practical usefulness for identifying purchase sessions.

## Slide 10: Metrics

The main model comparison metrics were ROC AUC, F1 score, accuracy, sensitivity, specificity, and
precision. ROC AUC measures how well the model ranks purchase sessions above no-purchase sessions
across possible thresholds. F1 score balances precision and sensitivity for the purchase class.
Sensitivity matters because missing likely buyers reduces the value of the screening process.
Precision matters because sending too many false positives into an intervention wastes money or
support capacity. Looking at these metrics together gives a more honest view than accuracy alone.

## Slide 11: Final Test Results

The selected final model is Random forest. On the held-out test set, it produced a ROC AUC of 0.935,
an F1 score of 0.716, and accuracy of 0.909. Sensitivity was 0.738, and specificity was 0.941. These
results mean the final model separated purchase sessions from no-purchase sessions well on the test
set. The model is especially useful as a ranking tool because ROC AUC evaluates the ordering of
predicted probabilities rather than only one fixed cutoff.

## Slide 12: Interpretation

The random forest variable importance results show which predictors were most useful for separating
the classes. The top predictors were PageValues, ExitRates, ProductRelated_Duration, Month,
ProductRelated. These are plausible session-intent signals, but they should be interpreted
carefully. Variable importance does not prove causation. It means these variables helped the model
separate sessions that generated revenue from sessions that did not. The practical interpretation is
that the model can produce a ranked list of sessions that are more likely to purchase. A business
could use that ranked list to design better marketing or support experiments.

## Slide 13: Limitations And Next Steps

The main limitations are the single e-commerce context, the absence of product and customer-history
variables, the lack of margin and campaign-cost data, and the need to confirm how page value would
be available in a live workflow. In a production setting, I would add product category, price,
inventory, customer history, acquisition channel, ad spend, and margin. I would also calibrate
predicted probabilities, test a model without page value if needed, and validate any intervention
with an A/B test before using it operationally.

## Slide 14: Conclusion

The conclusion is that online session behavior can provide useful signal for predicting purchase
conversion. The model should be used as decision support. It can prioritize sessions for marketing
or support experiments, but it should not be used as the only rule for customer treatment. The best
workflow is to treat model scores as a ranked shortlist, then test interventions with controlled
experiments. AI assistance was used to help organize and prepare materials, and that use is
disclosed in the report and repository.
