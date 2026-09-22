import {
  render,
  screen,
} from "@testing-library/react";

import userEvent from "@testing-library/user-event";

import {
  beforeEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";

import {
  SkillsPage,
} from "./SkillsPage";

import {
  useSkills,
} from "../hooks/usePlatformData";


vi.mock(
  "../hooks/usePlatformData",
  () => ({
    useSkills: vi.fn(),
  }),
);


const mockedUseSkills =
  vi.mocked(useSkills);


const skills = [
  {
    name: "business_summary",
    domain: "business",
    description:
      "Summarize overall business performance.",
  },
  {
    name: "monthly_performance",
    domain: "business",
    description:
      "Analyze monthly revenue and order trends.",
  },
  {
    name: "delivery_performance",
    domain: "operations",
    description:
      "Analyze delivery performance.",
  },
  {
    name: "review_analysis",
    domain: "customer",
    description:
      "Analyze customer review sentiment.",
  },
  {
    name: "delivery_anomalies",
    domain: "risk",
    description:
      "Detect unusual delivery behavior.",
  },
];


describe(
  "SkillsPage",
  () => {
    beforeEach(() => {
      mockedUseSkills.mockReturnValue(
        {
          data: {
            count: skills.length,
            domain: null,
            skills,
          },
          isLoading: false,
          isError: false,
        } as unknown as ReturnType<
          typeof useSkills
        >,
      );
    });


    it(
      "renders skills returned by the API",
      () => {
        render(
          <SkillsPage />,
        );

        expect(
          screen.getByText(
            "business_summary",
          ),
        ).toBeInTheDocument();

        expect(
          screen.getByText(
            "delivery_performance",
          ),
        ).toBeInTheDocument();

        expect(
          screen.getByText(
            "review_analysis",
          ),
        ).toBeInTheDocument();
      },
    );


    it(
      "filters skills by domain",
      async () => {
        const user =
          userEvent.setup();

        render(
          <SkillsPage />,
        );

        await user.click(
          screen.getByRole(
            "button",
            {
              name: "Operations",
            },
          ),
        );

        expect(
          screen.getByText(
            "delivery_performance",
          ),
        ).toBeInTheDocument();

        expect(
          screen.queryByText(
            "business_summary",
          ),
        ).not.toBeInTheDocument();

        expect(
          screen.queryByText(
            "review_analysis",
          ),
        ).not.toBeInTheDocument();
      },
    );


    it(
      "filters skills using search",
      async () => {
        const user =
          userEvent.setup();

        render(
          <SkillsPage />,
        );

        await user.type(
          screen.getByPlaceholderText(
            "Search skills...",
          ),
          "review",
        );

        expect(
          screen.getByText(
            "review_analysis",
          ),
        ).toBeInTheDocument();

        expect(
          screen.queryByText(
            "business_summary",
          ),
        ).not.toBeInTheDocument();
      },
    );


    it(
      "shows an empty state for no matches",
      async () => {
        const user =
          userEvent.setup();

        render(
          <SkillsPage />,
        );

        await user.type(
          screen.getByPlaceholderText(
            "Search skills...",
          ),
          "nothing-matches-this",
        );

        expect(
          screen.getByText(
            "No matching skills",
          ),
        ).toBeInTheDocument();
      },
    );
  },
);