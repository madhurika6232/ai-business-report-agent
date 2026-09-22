# RetailOps AI — Customer Review Intelligence

## Purpose

The review-intelligence layer converts unstructured customer reviews into
structured customer-experience signals using the Groq API.

LLMs are used for language understanding and synthesis. Deterministic Python
analytics remain responsible for calculating metrics and aggregations.

## Dataset

The processed dataset contains 40,497 usable written customer reviews.

Development and initial analysis use a reproducible 200-review sample to
control API usage and support rapid iteration.

## Classification Taxonomy

Reviews are classified into controlled categories including:

- delivery_delay
- non_delivery
- damaged_product
- wrong_product
- missing_item
- product_quality
- seller_service
- customer_service
- billing_payment
- expectation_mismatch
- positive_feedback
- other

Each classification also contains:

- sentiment
- severity
- confidence
- secondary issue
- English summary

## Structured Output

Groq responses are validated using Pydantic.

Invalid categories, malformed structures, and missing required fields are
rejected rather than silently accepted.

## Reliability

The pipeline includes:

- schema validation
- retry handling
- batch processing
- per-record failure isolation
- persistent classification caching

Cached reviews are not repeatedly sent to the LLM.

## Evaluation

A manually labeled golden evaluation set contains 25 examples including:

- clear complaints
- positive reviews
- ambiguous reviews
- mixed-sentiment reviews
- multiple issue types
- prompt-injection-style review content

Current evaluation results:

- Sentiment accuracy: 88%
- Primary issue accuracy: 92%
- Schema validity rate: 100%
- API/classification failure rate: 0%

These results are based on a small development evaluation set and should not
be interpreted as production-level guarantees.

## Known Weaknesses

Observed weaknesses include:

- ambiguous service complaints
- mixed positive/negative sentiment
- overconfident confidence labels
- occasional unsupported inference during generated summaries

## Prompt Injection

Customer reviews are treated as untrusted data.

Instructions appearing inside customer review text must never override system
instructions or control agent behavior.

Prompt-injection examples are included in the evaluation dataset.

## Operational Grounding

LLM classifications are connected back to structured order data.

In the 200-review development sample:

- 23 reviews were classified as delivery-related complaints
- 10 were classified specifically as delivery-delay complaints
- 4 of those 10 were also late relative to the marketplace estimated date
- structured confirmation rate: 40%

Customer-reported delay and operational lateness are intentionally treated as
different signals.

A customer may perceive delivery as slow even when it occurred within the
marketplace's estimated delivery window.

## Grounded Insight Generation

Groq may synthesize already-calculated evidence into concise business
explanations.

The LLM is instructed to:

- use only supplied evidence
- avoid inventing numbers
- distinguish customer reports from structured evidence
- avoid causal claims
- avoid accusations
- acknowledge uncertainty
- avoid generalizing the development sample to the entire marketplace

## Human Oversight

Generated insights support investigation rather than autonomous action.

The intended workflow is:

Review Data
→ Groq Classification
→ Schema Validation
→ Deterministic Analytics
→ Operational Evidence
→ Groq Explanation
→ Human Review
→ Business Action

## Limitations

The review sample is not necessarily representative of the full marketplace.

The underlying Olist dataset is historical Brazilian marketplace data from
2017–2018.

LLM classifications and summaries may contain errors and should be evaluated
continuously before use in consequential workflows.