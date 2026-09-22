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
  ConversationMessage,
} from "./ConversationMessage";


describe(
  "ConversationMessage",
  () => {
    it(
      "renders a user message",
      () => {
        render(
          <ConversationMessage
            message={{
              id: "1",
              role: "user",
              content:
                "What about the previous month?",
            }}
          />,
        );

        expect(
          screen.getByText(
            "What about the previous month?",
          ),
        ).toBeInTheDocument();
      },
    );


    it(
      "shows resolved conversation context",
      () => {
        render(
          <ConversationMessage
            message={{
              id: "2",
              role: "assistant",
              content:
                "**Revenue:** $1,222,941.11",
              originalQuery:
                "What about the previous month?",
              resolvedQuery:
                "What was revenue in February 2018?",
              selectedAgents: [
                "business",
              ],
            }}
          />,
        );

        expect(
          screen.getByText(
            "Context resolved as",
          ),
        ).toBeInTheDocument();

        expect(
          screen.getByText(
            "What was revenue in February 2018?",
          ),
        ).toBeInTheDocument();

        expect(
          screen.getByText(
            "business",
          ),
        ).toBeInTheDocument();
      },
    );
  },
);