import {
  describe,
  expect,
  it,
} from "vitest";


describe(
  "production frontend configuration",
  () => {
    it(
      "does not require a browser API key",
      () => {
        expect(
          import.meta.env
            .VITE_RETAILOPS_API_KEY,
        ).toBeUndefined();
      },
    );


    it(
      "does not expose a Groq key",
      () => {
        expect(
          import.meta.env
            .VITE_GROQ_API_KEY,
        ).toBeUndefined();
      },
    );
  },
);