import {
  render,
  screen,
} from "@testing-library/react";

import userEvent from "@testing-library/user-event";

import {
  describe,
  expect,
  it,
  vi,
} from "vitest";

import {
  EmptyState,
} from "./EmptyState";

import {
  ErrorState,
} from "./ErrorState";

import {
  LoadingState,
} from "./LoadingState";


describe("shared application states", () => {
  it("renders a loading state", () => {
    render(
      <LoadingState
        title="Loading skills"
        description="Retrieving capabilities."
      />,
    );

    expect(
      screen.getByText(
        "Loading skills",
      ),
    ).toBeInTheDocument();
  });


  it("renders an empty state", () => {
    render(
      <EmptyState
        title="No results"
        description="Try another search."
      />,
    );

    expect(
      screen.getByText(
        "No results",
      ),
    ).toBeInTheDocument();
  });


  it("runs the retry action", async () => {
    const user =
      userEvent.setup();

    const retry =
      vi.fn();

    render(
      <ErrorState
        description="API unavailable."
        onRetry={retry}
      />,
    );

    await user.click(
      screen.getByRole(
        "button",
        {
          name: /retry/i,
        },
      ),
    );

    expect(retry).toHaveBeenCalledOnce();
  });
});