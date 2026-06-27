# Predicting Online Purchase Conversion From Session Behavior

Project Status: Final submission package complete

## Project Objective

This project builds predictive models in R to classify whether an online shopping session is likely to generate revenue based on session behavior and traffic attributes. The analysis compares logistic regression, decision tree, and random forest models, evaluates performance on a held-out test set, and translates the result into an executive summary and narrated presentation.

## Contributor

- Nikita Rogers

## Dataset

Dataset: UCI Online Shoppers Purchasing Intention dataset

Source: https://archive.ics.uci.edu/dataset/468/online+shoppers+purchasing+intention+dataset

Unit of observation: one online shopping session

Rows: 12,330

Prediction problem: binary classification

Response variable:

- `Purchase`: session generated revenue.
- `NoPurchase`: session did not generate revenue.

Predictors include:

- administrative page counts and duration
- informational page counts and duration
- product-related page counts and duration
- bounce rates
- exit rates
- page values
- special-day timing
- month
- operating system
- browser
- region
- traffic type
- visitor type
- weekend status

## Methods Used

- Exploratory data analysis
- Missing value check
- Categorical preprocessing
- Rare-category collapsing
- Stratified train/test splitting
- Stratified cross-validation
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
- tidyr
- readr
- rpart
- randomForest
- pROC
- Git / GitHub
- Python for slide, narration, and packaging automation
- Edge TTS for disclosed narration generation

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

The report downloads the UCI dataset automatically if `data/online_shoppers_intention.csv` does not exist.

## Deliverables

- `Report-Team1.html`
- `Executive_Summary-Team1.pptx`
- `Video_Presentation-Team1.mp4`
- `video_narration.mp3`
- `video_script.md`
- GitHub repository with this README

## AI Use Disclosure

AI-assisted tools were used to help organize the report structure, draft explanatory language, create reproducible code scaffolding, and prepare presentation materials. AI was used as a support tool and is disclosed in the report because the assignment requires explicit attribution. The repository includes the R Markdown source, code appendix, generated outputs, and interpretation needed to inspect the analysis independently.

## License

For academic use only unless otherwise specified.
