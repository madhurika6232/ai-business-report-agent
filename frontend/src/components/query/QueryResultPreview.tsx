import {
  QueryResult,
} from "./QueryResult";

import type {
  QueryResponse,
} from "../../types/api";


const previewResult: QueryResponse = {
  query:
    "How is the business performing?",

  safe_query:
    "How is the business performing?",

  answer: `
## Summary

The business generated **$13,541,712.78** in revenue from **99,092 orders**, with an average order value of **$136.66**.

## Evidence

1. **Total revenue:** $13,541,712.78
2. **Total orders:** 99,092
3. **Average order value:** $136.66
4. **Total items sold:** 112,279
5. **Unique customers:** 95,774

## Interpretation

The evidence shows a sizable volume of sales activity and a moderate average order value, indicating that the business is operating at substantial scale with a broad customer base.

## Recommended action

Investigate the product mix and customer segmentation to identify opportunities for increasing average order value or expanding the customer base.
`,

  selected_agents: [
    "business",
  ],

  blocked: false,
  block_reason: null,
  pii_detected: false,

  guardrail_validation: {
    output_valid: true,
  },
};


export function QueryResultPreview() {
  return (
    <QueryResult
      result={previewResult}
    />
  );
}