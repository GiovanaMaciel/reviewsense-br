---
language: pt
license: cc-by-nc-sa-4.0
library_name: sklearn
tags:
- sentiment-analysis
- tf-idf
- portuguese
metrics:
- accuracy
- f1
---

# ReviewSense BR

Brazilian Portuguese sentiment classification with TF-IDF and logistic regression.
The experiment compares a trained text classifier with a majority-class baseline
using a stratified train/validation/test protocol.

## Dataset and labels

[B2W-Reviews01](https://github.com/americanas-tech/b2w-reviews01), by B2W Digital,
contains product reviews from Americanas.com collected in 2018.
The dataset and this educational, non-commercial model use CC BY-NC-SA 4.0.
The original CSV and individual reviews are not redistributed in this package.

Labels are proxies derived from star ratings: 1–2 `negativo`, 3 `neutro`, 4–5 `positivo`.
They are not independent human annotations of textual sentiment. Only the review
text is used as a feature; the rating is used exclusively to derive the target.

## Preprocessing and experimental protocol

- Unicode NFKC normalization, whitespace normalization and lowercasing.
- Removal of missing or empty texts, invalid ratings, conflicting class labels
  for identical normalized texts, and repeated normalized texts.
- 126,674 usable reviews from 132,373 original rows.
- Stratified random 70/15/15 train/validation/test split; seed 42.
- Split sizes: 88,671 train, 19,001 validation, 19,002 test.
- TF-IDF: unigrams and bigrams, `min_df=3`, `max_features=40000`, `sublinear_tf=True`.
- Logistic regression: `class_weight='balanced'`, `max_iter=1000`, selected `C=0.5`.
- Selection from `C` values 0.5 and 2.0 by validation Macro-F1.
- Vocabulary fitting occurs within the training pipeline. After selection, the
  final pipeline is refitted on train + validation and evaluated on the reserved test set.

## Held-out test results

| Model | Accuracy | Macro-F1 |
|---|---:|---:|
| Majority-class baseline | 0.6177 | 0.2546 |
| TF-IDF + logistic regression | 0.7918 | 0.7230 |

| Class | Precision | Recall | F1 | Support |
|---|---:|---:|---:|---:|
| negativo | 0.8489 | 0.8791 | 0.8637 | 4889 |
| neutro | 0.3558 | 0.5943 | 0.4451 | 2376 |
| positivo | 0.9364 | 0.7954 | 0.8602 | 11737 |

![Confusion matrix](confusion_matrix.png)

Full scores, data hash, split sizes and configuration are recorded in `metrics.json`.

## Error analysis

The neutral class is the main weakness, with lower precision and F1 than the
negative and positive classes. The test confusion matrix contains 2,041 positive
reviews predicted as neutral. Overall, 3,956 of 19,002 test predictions were incorrect.

Exploratory review inspection showed mixed-sentiment excerpts and positive
language predicted as neutral. These observations do not establish the cause of
each error. Star-derived labels can disagree with the sentiment expressed in text.

In an authored demonstration, the complaint "A comida chegou fria e faltou uma bebida."
was predicted as neutral. This is a qualitative failure case outside the evaluated
product-review domain, not a restaurant benchmark.

## Local inference

The artifact `model.joblib` contains the fitted vectorizer and classifier.
The training Python version is 3.13.18; package versions are
recorded in `requirements.txt`. Load only trusted Joblib artifacts.

```python
import joblib
import pandas as pd

model = joblib.load("model.joblib")
texts = pd.Series(["Não recomendo o produto."])
texts = texts.str.normalize("NFKC").str.replace(r"\s+", " ", regex=True).str.strip().str.lower()
print(model.predict(texts.tolist()))
```

This repository distributes a scikit-learn artifact for local inference.

## Reproducibility

The companion notebook `reviewsense_br.ipynb` contains data acquisition,
preprocessing, training, evaluation and artifact export. Its installation cell
uses IPython syntax supported by Colab and Jupyter. The exported requirements
record the package versions installed during the corresponding run.

## Limitations

- Performance is measured on e-commerce product reviews, without restaurant or delivery validation.
- Ratings provide noisy sentiment proxies, especially for the neutral class.
- Exact duplicates are removed; near duplicates and shared product patterns may remain.
- The random split does not measure temporal or product-group generalization.
- Probability calibration, production monitoring and latency benchmarks are outside the current experiment.

## Planned experiments

- Comparison with a Portuguese Transformer under a documented evaluation protocol.
- LLM-based summaries linked to review evidence, evaluated for faithfulness and coverage.
- Independent evaluation on appropriately sourced restaurant reviews.

Transformer and LLM components are planned work and are not included in this version.
