import {
  afterEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";

import {
  ApiError,
  retailOpsApi,
} from "./api";


describe("RetailOps API client", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });


  it("loads health status", async () => {
    const fetchMock = vi
      .spyOn(globalThis, "fetch")
      .mockResolvedValue(
        new Response(
          JSON.stringify({
            status: "ok",
            service: "RetailOps AI",
          }),
          {
            status: 200,
            headers: {
              "Content-Type":
                "application/json",
            },
          },
        ),
      );

    const result =
      await retailOpsApi.health();

    expect(result.status).toBe("ok");

    expect(fetchMock).toHaveBeenCalledWith(
      "http://127.0.0.1:8000/health",
      expect.any(Object),
    );
  });


  it("loads skills", async () => {
    vi.spyOn(
      globalThis,
      "fetch",
    ).mockResolvedValue(
      new Response(
        JSON.stringify({
          count: 1,
          domain: null,
          skills: [
            {
              name: "business_summary",
              domain: "business",
              description:
                "Summarize business performance.",
            },
          ],
        }),
        {
          status: 200,
          headers: {
            "Content-Type":
              "application/json",
          },
        },
      ),
    );

    const result =
      await retailOpsApi.skills();

    expect(result.count).toBe(1);

    expect(
      result.skills[0].name,
    ).toBe(
      "business_summary",
    );
  });


  it("throws ApiError for failed requests", async () => {
    vi.spyOn(
      globalThis,
      "fetch",
    ).mockResolvedValue(
      new Response(
        JSON.stringify({
          detail:
            "Invalid or missing API key.",
        }),
        {
          status: 401,
          headers: {
            "Content-Type":
              "application/json",
            "X-Request-ID":
              "request-123",
          },
        },
      ),
    );

    await expect(
      retailOpsApi.query({
        query: "Test query",
      }),
    ).rejects.toMatchObject({
      name: "ApiError",
      status: 401,
      message:
        "Invalid or missing API key.",
      requestId: "request-123",
    });
  });


  it("uses fallback error text for non-json errors", async () => {
    vi.spyOn(
      globalThis,
      "fetch",
    ).mockResolvedValue(
      new Response(
        "Service unavailable",
        {
          status: 503,
        },
      ),
    );

    try {
      await retailOpsApi.health();

      throw new Error(
        "Expected request to fail.",
      );
    } catch (error) {
      expect(
        error,
      ).toBeInstanceOf(
        ApiError,
      );

      expect(
        (error as ApiError).status,
      ).toBe(503);
    }
  });
});