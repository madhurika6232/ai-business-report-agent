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
  NotFoundPage,
} from "./NotFoundPage";


describe("NotFoundPage", () => {
  it(
    "provides a route back to the overview",
    () => {
      render(
        <MemoryRouter>
          <NotFoundPage />
        </MemoryRouter>,
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
});