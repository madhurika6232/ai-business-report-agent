import {
  render,
  screen,
} from "@testing-library/react";

import {
  describe,
  expect,
  it,
} from "vitest";

import {
  QueryResult,
} from "./QueryResult";

import type {
  QueryResponse,
} from "../../types/api";


const result: QueryResponse = {
  query:
    "How is the business performing?",

  safe_query:
    "How is the business performing?",

  answer: `
## Summary

Revenue was **$13.5M**.

## Evidence

1. Total orders: **99,092**
2. Average order value: **$136.66**
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


describe(
  "QueryResult",
  () => {
    it(
      "renders markdown as formatted content",
      () => {
        render(
          <QueryResult
            result={result}
          />,
        );

        expect(
          screen.getByRole(
            "heading",
            {
              name: "Summary",
            },
          ),
        ).toBeInTheDocument();

        expect(
          screen.getByText(
            "$13.5M",
          ),
        ).toBeInTheDocument();

        expect(
          screen.queryByText(
            "**$13.5M**",
          ),
        ).not.toBeInTheDocument();
      },
    );


    it(
      "shows the selected intelligence agent",
      () => {
        render(
          <QueryResult
            result={result}
          />,
        );

        expect(
          screen.getByText(
            "business",
          ),
        ).toBeInTheDocument();
      },
    );


    it(
      "renders blocked requests safely",
      () => {
        render(
          <QueryResult
            result={{
              ...result,
              blocked: true,
              block_reason:
                "Unsafe request.",
            }}
          />,
        );

        expect(
          screen.getByText(
            "This request was blocked",
          ),
        ).toBeInTheDocument();

        expect(
          screen.getByText(
            "Unsafe request.",
          ),
        ).toBeInTheDocument();
      },
    );
  },
);