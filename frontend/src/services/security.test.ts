import {
  describe,
  expect,
  it,
} from "vitest";


describe(
  "frontend secret safety",
  () => {
    it(
      "does not expose a RetailOps API key through Vite",
      () => {
        expect(
          import.meta.env
            .VITE_RETAILOPS_API_KEY,
        ).toBeUndefined();
      },
    );
  },
);