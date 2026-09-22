import {
  render,
  screen,
} from "@testing-library/react";

import {
  beforeEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";

import {
  EvaluationPage,
} from "./EvaluationPage";

import {
  useEvaluation,
} from "../hooks/usePlatformData";


vi.mock(
  "../hooks/usePlatformData",
  () => ({
    useEvaluation: vi.fn(),
  }),
);


const mockedUseEvaluation =
  vi.mocked(useEvaluation);


const evaluationData = {
  evaluator_count: 7,

  evaluators: [
    {
      name: "router",
      category: "routing",
      description:
        "Evaluate agent-routing accuracy.",
    },
    {
      name: "guardrails",
      category: "safety",
      description:
        "Evaluate application guardrails.",
    },
  ],

  thresholds: {
    router: {
      exact_route_accuracy: 95,
      macro_f1: 90,
      failure_rate: 0,
    },

    guardrails: {
      injection_accuracy: 100,
      pii_accuracy: 100,
    },
  },

  baseline: {
    name: "retailops_baseline_v1",
    available: true,
    overall_score: 92.82,
    release_decision: "pass",
  },
};


describe(
  "EvaluationPage",
  () => {
    beforeEach(() => {
      mockedUseEvaluation.mockReturnValue(
        {
          data: evaluationData,
          isLoading: false,
          isError: false,
        } as unknown as ReturnType<
          typeof useEvaluation
        >,
      );
    });


    it(
      "renders the persisted baseline",
      () => {
        render(
          <EvaluationPage />,
        );

        expect(
          screen.getByText(
            "92.82",
          ),
        ).toBeInTheDocument();

        expect(
          screen.getAllByText(
            "PASS",
          ).length,
        ).toBeGreaterThan(0);

        expect(
          screen.getByText(
            "retailops_baseline_v1",
          ),
        ).toBeInTheDocument();
      },
    );


    it(
      "renders evaluator definitions",
      () => {
        render(
          <EvaluationPage />,
        );

        expect(
          screen.getAllByText(
            "router",
          ).length,
        ).toBeGreaterThan(0);

        expect(
          screen.getAllByText(
            "guardrails",
          ).length,
        ).toBeGreaterThan(0);

        expect(
          screen.getByText(
            "Evaluate agent-routing accuracy.",
          ),
        ).toBeInTheDocument();

        expect(
          screen.getByText(
            "Evaluate application guardrails.",
          ),
        ).toBeInTheDocument();
      },
    );


    it(
      "renders release thresholds",
      () => {
        render(
          <EvaluationPage />,
        );

        expect(
          screen.getByText(
            "exact route accuracy",
          ),
        ).toBeInTheDocument();

        expect(
          screen.getByText(
            "macro f1",
          ),
        ).toBeInTheDocument();

        expect(
          screen.getByText(
            "injection accuracy",
          ),
        ).toBeInTheDocument();
      },
    );


    it(
      "shows loading state",
      () => {
        mockedUseEvaluation.mockReturnValue(
          {
            data: undefined,
            isLoading: true,
            isError: false,
          } as ReturnType<
            typeof useEvaluation
          >,
        );

        render(
          <EvaluationPage />,
        );

        expect(
          screen.getByText(
            "Loading evaluation baseline...",
          ),
        ).toBeInTheDocument();
      },
    );


    it(
      "shows API failure state",
      () => {
        mockedUseEvaluation.mockReturnValue(
          {
            data: undefined,
            isLoading: false,
            isError: true,
          } as ReturnType<
            typeof useEvaluation
          >,
        );

        render(
          <EvaluationPage />,
        );

        expect(
          screen.getByText(
            "Evaluation unavailable",
          ),
        ).toBeInTheDocument();

        expect(
          screen.getByText(
            "Verify that the RetailOps API is available.",
          ),
        ).toBeInTheDocument();
      },
    );
  },
);