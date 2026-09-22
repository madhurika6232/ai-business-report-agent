# RetailOps AI Evaluation Report

Generated: 2026-08-25T23:58:46.735849+00:00

## Summary

- Overall score: 92.82/100
- Release decision: PASS
- Evaluators run: 7

## Evaluator Scores

| Evaluator | Score | Status |
|---|---:|:---:|
| router | 100.00 | Pass |
| tool_selection | 100.00 | Pass |
| review_classifier | 97.00 | Pass |
| numeric_grounding | 66.35 | Pass |
| guardrails | 100.00 | Pass |
| multi_agent | 100.00 | Pass |
| answer_quality | 100.00 | Pass |

## Detailed Metrics

### router

- exact_route_accuracy: 100.0 (threshold: 95.0, status: pass)
- macro_precision: 100.0 (threshold: N/A, status: pass)
- macro_recall: 100.0 (threshold: N/A, status: pass)
- macro_f1: 100.0 (threshold: 90.0, status: pass)
- failure_rate: 0.0 (threshold: 0.0, status: pass)

### tool_selection

- exact_tool_accuracy: 100.0 (threshold: 95.0, status: pass)
- failure_rate: 0.0 (threshold: 0.0, status: pass)

### review_classifier

- sentiment_accuracy: 88.0 (threshold: 85.0, status: pass)
- issue_accuracy: 100.0 (threshold: 85.0, status: pass)
- schema_validity_rate: 100.0 (threshold: 100.0, status: pass)
- failure_rate: 0.0 (threshold: 0.0, status: pass)

### numeric_grounding

- raw_numeric_faithfulness: 99.05 (threshold: N/A, status: warning)
- unsafe_answers_generated: 1.0 (threshold: N/A, status: warning)
- guardrail_containment_rate: 100.0 (threshold: 100.0, status: pass)

### guardrails

- injection_accuracy: 100.0 (threshold: 100.0, status: pass)
- injection_false_positives: 0.0 (threshold: 0.0, status: pass)
- injection_false_negatives: 0.0 (threshold: 0.0, status: pass)
- pii_accuracy: 100.0 (threshold: 100.0, status: pass)
- pii_false_positives: 0.0 (threshold: 0.0, status: pass)
- pii_false_negatives: 0.0 (threshold: 0.0, status: pass)

### multi_agent

- routing_accuracy: 100.0 (threshold: 100.0, status: pass)
- execution_accuracy: 100.0 (threshold: 100.0, status: pass)
- answer_generation_rate: 100.0 (threshold: 100.0, status: pass)
- error_free_rate: 100.0 (threshold: 100.0, status: pass)

### answer_quality

- relevance: 5.0 (threshold: 4.0, status: pass)
- evidence_use: 5.0 (threshold: 4.0, status: pass)
- clarity: 5.0 (threshold: 4.0, status: pass)
- caution: 5.0 (threshold: 4.0, status: pass)
- actionability: 5.0 (threshold: 4.0, status: pass)
- overall_answer_quality: 5.0 (threshold: 4.0, status: pass)

## Release Gate

Critical failures: None

Non-critical failures: None

Incomplete evaluators: None
