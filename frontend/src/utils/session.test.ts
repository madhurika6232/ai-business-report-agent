import {
  beforeEach,
  describe,
  expect,
  it,
} from "vitest";

import {
  clearSessionId,
  createSessionId,
  getOrCreateSessionId,
  resetSessionId,
} from "./session";


describe(
  "conversation session utilities",
  () => {
    beforeEach(() => {
      sessionStorage.clear();
    });

    it(
      "creates a valid session id",
      () => {
        const sessionId =
          createSessionId();

        expect(sessionId).toBeTruthy();

        expect(
          sessionId.length,
        ).toBeGreaterThan(10);
      },
    );


    it(
      "reuses the existing session id",
      () => {
        const first =
          getOrCreateSessionId();

        const second =
          getOrCreateSessionId();

        expect(second).toBe(first);
      },
    );


    it(
      "resets the session id",
      () => {
        const first =
          getOrCreateSessionId();

        const second =
          resetSessionId();

        expect(second).not.toBe(
          first,
        );

        expect(
          getOrCreateSessionId(),
        ).toBe(second);
      },
    );


    it(
      "clears the session id",
      () => {
        const first =
          getOrCreateSessionId();

        clearSessionId();

        const second =
          getOrCreateSessionId();

        expect(second).not.toBe(
          first,
        );
      },
    );
  },
);