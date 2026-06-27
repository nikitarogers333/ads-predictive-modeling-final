# Predicting High Quality Wine From Physicochemical Measurements

Project Status: Final submission package in progress

## Project Objective

This project builds predictive models in R to classify whether a red wine is likely to receive a high sensory quality score based on laboratory physicochemical measurements. The analysis compares logistic regression, decision tree, and random forest models, evaluates performance on a held-out test set, and translates the result into a short executive summary and narrated presentation.

## Contributor

- Nikita Rogers

## Dataset

Dataset: UCI Wine Quality red wine dataset

Source: https://archive.ics.uci.edu/ml/datasets/wine+quality

Unit of observation: one red wine sample

Rows: 1,599

Prediction problem: binary classification

Response variable:

- `High`: original quality score is 7 or higher.
- `NotHigh`: original quality score is below 7.

Predictors:

- fixed acidity
- volatile acidity
- citric acid
- residual sugar
- chlorides
- free sulfur dioxide
- total sulfur dioxide
- density
- pH
- sulphates
- alcohol

## Methods Used

- Exploratory data analysis
- Missing value check
- Feature engineering
- Stratified train/test splitting
- Stratified 5-fold cross-validation
- Logistic regression
- Decision tree tuning
- Random forest tuning
- ROC AUC, accuracy, sensitivity, specificity, precision, and F1 evaluation
- Variable importance
- Non-technical executive summary

## Technologies

- R
- R Markdown
- ggplot2
- dplyr
- readr
- rpart
- randomForest
- pROC
- Git / GitHub
- Python for slide, narration, and packaging automation
- ElevenLabs for disclosed narration generation

## Repository Structure

```text
.
├── README.md
├── report.Rmd
├── submission_checklist.md
├── executive_summary_outline.md
├── video_presentation_outline.md
├── data/
├── code/
├── figures/
├── slides/
└── docs/
```

## How To Run

1. Clone the repository.
2. Open `report.Rmd` in RStudio.
3. Install the packages listed in the first executable code chunk.
4. Knit `report.Rmd` to HTML.

Command line option:

```bash
Rscript -e "rmarkdown::render('report.Rmd', output_file='Report-Team1.html')"
```

The report downloads the dataset automatically if `data/winequality-red.csv` does not exist.

## Deliverables

- `Report-Team1.html`
- `Executive_Summary-Team1.pptx`
- `Video_Presentation-Team1.mp4`
- `video_narration.mp3`
- `video_script.md`
- GitHub repository with this README

## AI Use Disclosure

AI-assisted tools were used to help organize the report structure, draft explanatory language, create reproducible code scaffolding, and prepare presentation materials. The modeling workflow, code execution, output review, and final interpretation were checked in this project repository. AI was used as a support tool and is disclosed in the report because the assignment requires explicit attribution. The final submission should be reviewed by the student before submission so that all methods, code, and conclusions can be explained independently.

## License

For academic use only unless otherwise specified.

