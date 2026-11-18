# ReviewSense BR — evidence-linked review synthesis

This extension combines the published sentiment classifier with structured LLM
synthesis. Sentiment counts are computed in code. LLM conclusions cite review
IDs and literal excerpts; reference integrity is checked after generation.

## Execution

- LLM status: Completed; exploratory qualitative inspection recorded; independent human review remains pending.
- Provider: Groq; Free-plan usage is subject to account quotas.
- Requested model: openai/gpt-oss-120b
- Prompt version: reviewsense-evidence-v2
- Classifier: https://huggingface.co/gimaciel/reviewsense-br-tfidf
- Classifier revision: 5c1bf1a475eee98c2f6710088ff1a4a65f600028
- Offline contract tests: 16; failures: 0; errors: 0.
- Offline tests use simulated responses and do not measure LLM quality.

## Data and limits

The input consists of 12 authored, synthetic restaurant reviews. It is not an
iFood dataset or an independent restaurant benchmark. Existing classifier
metrics apply only to the B2W-Reviews01 product-review experiment.

Real citations do not prove that a claim follows from them. Semantic grounding,
coverage, robustness and usefulness require separate evaluation. Suggested
actions are proposals, not verified causes or guaranteed solutions.

## Reproducibility

The notebook reviewsense_br_genai.ipynb contains the integration and contract
tests. The export records the input, prompt, schema and installed dependencies.
Successful API runs additionally record generated output, response model,
token usage and measured latency. The model API is an external dependency;
no API key is included in the export.

## Links

- Project: https://github.com/GiovanaMaciel/reviewsense-br
- Structured Outputs: https://console.groq.com/docs/structured-outputs
- Free-plan limits: https://console.groq.com/docs/rate-limits

## Recorded results and inspection

The uploaded run recorded 2.6581 seconds, 1,005 input tokens and 1,052 output tokens
for 12 authored synthetic reviews. It produced four praise groups, four complaint
groups and four proposed actions. All 14 literal excerpts match the cited inputs.

[QUALITATIVE_REVIEW.md](QUALITATIVE_REVIEW.md) documents scope generalizations and
proposed wording without modifying `genai_report.json`. `reference_audit.json`
records reference checks; `qualitative_review.csv` records exploratory observations.
The original blank `semantic_review.csv` remains available for independent review.

The notebook is [reviewsense_br_genai.ipynb](../reviewsense_br_genai.ipynb).
The original test record has 16 passing offline tests. The publication source
adds one regression test for stringified JSON finding objects.
