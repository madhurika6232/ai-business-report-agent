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
  AppRouter,
} from "./AppRouter";


vi.mock(
  "../pages/DashboardPage",
  () => ({
    DashboardPage: () => (
      <div>Dashboard Test Page</div>
    ),
  }),
);

vi.mock(
  "../pages/QueryPage",
  () => ({
    QueryPage: () => (
      <div>Query Test Page</div>
    ),
  }),
);

vi.mock(
  "../pages/ConversationsPage",
  () => ({
    ConversationsPage: () => (
      <div>Conversations Test Page</div>
    ),
  }),
);

vi.mock(
  "../pages/SkillsPage",
  () => ({
    SkillsPage: () => (
      <div>Skills Test Page</div>
    ),
  }),
);

vi.mock(
  "../pages/EvaluationPage",
  () => ({
    EvaluationPage: () => (
      <div>Evaluation Test Page</div>
    ),
  }),
);

vi.mock(
  "../pages/SettingsPage",
  () => ({
    SettingsPage: () => (
      <div>Settings Test Page</div>
    ),
  }),
);


describe(
  "AppRouter",
  () => {
    beforeEach(() => {
      window.history.pushState(
        {},
        "",
        "/",
      );
    });


    it(
      "renders the overview route",
      () => {
        render(
          <AppRouter />,
        );

        expect(
          screen.getByText(
            "Dashboard Test Page",
          ),
        ).toBeInTheDocument();
      },
    );


    it(
      "renders the query route",
      () => {
        window.history.pushState(
          {},
          "",
          "/query",
        );

        render(
          <AppRouter />,
        );

        expect(
          screen.getByText(
            "Query Test Page",
          ),
        ).toBeInTheDocument();
      },
    );


    it(
      "renders the conversations route",
      () => {
        window.history.pushState(
          {},
          "",
          "/conversations",
        );

        render(
          <AppRouter />,
        );

        expect(
          screen.getByText(
            "Conversations Test Page",
          ),
        ).toBeInTheDocument();
      },
    );


    it(
      "renders the skills route",
      () => {
        window.history.pushState(
          {},
          "",
          "/skills",
        );

        render(
          <AppRouter />,
        );

        expect(
          screen.getByText(
            "Skills Test Page",
          ),
        ).toBeInTheDocument();
      },
    );


    it(
      "renders the evaluation route",
      () => {
        window.history.pushState(
          {},
          "",
          "/evaluation",
        );

        render(
          <AppRouter />,
        );

        expect(
          screen.getByText(
            "Evaluation Test Page",
          ),
        ).toBeInTheDocument();
      },
    );


    it(
      "renders the settings route",
      () => {
        window.history.pushState(
          {},
          "",
          "/settings",
        );

        render(
          <AppRouter />,
        );

        expect(
          screen.getByText(
            "Settings Test Page",
          ),
        ).toBeInTheDocument();
      },
    );


    it(
      "renders the 404 page for an unknown route",
      () => {
        window.history.pushState(
          {},
          "",
          "/does-not-exist",
        );

        render(
          <AppRouter />,
        );

        expect(
          screen.getByRole(
            "heading",
            {
              name: "Page not found.",
            },
          ),
        ).toBeInTheDocument();

        expect(
          screen.getByRole(
            "link",
            {
              name: /return to overview/i,
            },
          ),
        ).toHaveAttribute(
          "href",
          "/",
        );
      },
    );
  },
);