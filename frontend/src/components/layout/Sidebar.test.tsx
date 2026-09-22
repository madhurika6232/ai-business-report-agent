import {
  MemoryRouter,
} from "react-router-dom";

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
  Sidebar,
} from "./Sidebar";


describe(
  "Sidebar",
  () => {
    it(
      "exposes the primary application routes",
      () => {
        render(
          <MemoryRouter>
            <Sidebar />
          </MemoryRouter>,
        );

        expect(
          screen.getByRole(
            "navigation",
            {
              name:
                "Primary navigation",
            },
          ),
        ).toBeInTheDocument();

        expect(
          screen.getByRole(
            "link",
            {
              name: "Overview",
            },
          ),
        ).toHaveAttribute(
          "href",
          "/",
        );

        expect(
          screen.getByRole(
            "link",
            {
              name: "Ask RetailOps",
            },
          ),
        ).toHaveAttribute(
          "href",
          "/query",
        );

        expect(
          screen.getByRole(
            "link",
            {
              name: "Conversations",
            },
          ),
        ).toHaveAttribute(
          "href",
          "/conversations",
        );

        expect(
          screen.getByRole(
            "link",
            {
              name: "Skills",
            },
          ),
        ).toHaveAttribute(
          "href",
          "/skills",
        );

        expect(
          screen.getByRole(
            "link",
            {
              name: "Evaluation",
            },
          ),
        ).toHaveAttribute(
          "href",
          "/evaluation",
        );
      },
    );


    it(
      "provides access to settings",
      () => {
        render(
          <MemoryRouter>
            <Sidebar />
          </MemoryRouter>,
        );

        expect(
          screen.getByRole(
            "link",
            {
              name:
                "Application settings",
            },
          ),
        ).toHaveAttribute(
          "href",
          "/settings",
        );
      },
    );
  },
);