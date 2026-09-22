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
  QueryComposer,
} from "./QueryComposer";


describe(
  "QueryComposer",
  () => {
    it(
      "disables submission when the query is empty",
      () => {
        render(
          <QueryComposer
            loading={false}
            onSubmit={vi.fn()}
          />,
        );

        expect(
          screen.getByRole(
            "button",
            {
              name: "Submit business question",
            },
          ),
        ).toBeDisabled();
      },
    );


    it(
      "fills the query from a suggested question",
      async () => {
        const user =
          userEvent.setup();

        render(
          <QueryComposer
            loading={false}
            onSubmit={vi.fn()}
          />,
        );

        await user.click(
          screen.getByRole(
            "button",
            {
              name:
                "How is the business performing?",
            },
          ),
        );

        expect(
          screen.getByLabelText(
            "Ask RetailOps a business question",
          ),
        ).toHaveValue(
          "How is the business performing?",
        );
      },
    );


    it(
      "submits a typed business question",
      async () => {
        const user =
          userEvent.setup();

        const onSubmit =
          vi.fn();

        render(
          <QueryComposer
            loading={false}
            onSubmit={onSubmit}
          />,
        );

        const input =
          screen.getByLabelText(
            "Ask RetailOps a business question",
          );

        await user.type(
          input,
          "Show delivery performance",
        );

        await user.click(
          screen.getByRole(
            "button",
            {
              name: "Submit business question",
            },
          ),
        );

        expect(
          onSubmit,
        ).toHaveBeenCalledWith(
          "Show delivery performance",
        );
      },
    );
  },
);