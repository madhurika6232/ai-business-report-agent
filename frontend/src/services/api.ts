import type {
  ApiErrorPayload,
  ConversationRequest,
  ConversationResponse,
  EvaluationResponse,
  HealthResponse,
  QueryRequest,
  QueryResponse,
  SessionSummary,
  SkillsResponse,
} from "../types/api";


const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  "";



export class ApiError extends Error {
  status: number;
  requestId: string | null;

  constructor(
    message: string,
    status: number,
    requestId: string | null = null,
  ) {
    super(message);

    this.name = "ApiError";
    this.status = status;
    this.requestId = requestId;
  }
}


async function request<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const headers = new Headers(
    options.headers,
  );

  headers.set(
    "Content-Type",
    "application/json",
  );



  const response = await fetch(
    `${API_BASE_URL}${path}`,
    {
      ...options,
      headers,
    },
  );

  const requestId =
    response.headers.get(
      "X-Request-ID",
    );

  if (!response.ok) {
    let payload: ApiErrorPayload = {};

    try {
      const responseBody =
        await response.json();

      payload =
        responseBody as ApiErrorPayload;
    } catch {
      // The response may not contain JSON.
    }

    const message =
      payload.detail ??
      payload.error ??
      `Request failed with status ${response.status}.`;

    throw new ApiError(
      message,
      response.status,
      requestId,
    );
  }

  const data =
    await response.json();

  return data as T;
}


export const retailOpsApi = {
  health(): Promise<HealthResponse> {
    return request<HealthResponse>(
      "/health",
    );
  },

  ready(): Promise<HealthResponse> {
    return request<HealthResponse>(
      "/ready",
    );
  },

  query(
    payload: QueryRequest,
  ): Promise<QueryResponse> {
    return request<QueryResponse>(
      "/api/v1/query",
      {
        method: "POST",
        body: JSON.stringify(
          payload,
        ),
      },
    );
  },

  conversation(
    payload: ConversationRequest,
  ): Promise<ConversationResponse> {
    return request<ConversationResponse>(
      "/api/v1/conversation",
      {
        method: "POST",
        body: JSON.stringify(
          payload,
        ),
      },
    );
  },

  getSession(
    sessionId: string,
  ): Promise<SessionSummary> {
    const encodedSessionId =
      encodeURIComponent(
        sessionId,
      );

    return request<SessionSummary>(
      `/api/v1/sessions/${encodedSessionId}`,
      {},
    );
  },

  deleteSession(
    sessionId: string,
  ): Promise<{
    session_id: string;
    deleted: boolean;
  }> {
    const encodedSessionId =
      encodeURIComponent(
        sessionId,
      );

    return request<{
      session_id: string;
      deleted: boolean;
    }>(
      `/api/v1/sessions/${encodedSessionId}`,
      {
        method: "DELETE",
      },
    );
  },

  skills(
    domain?: string,
  ): Promise<SkillsResponse> {
    const queryString =
      domain
        ? `?domain=${encodeURIComponent(domain)}`
        : "";

    return request<SkillsResponse>(
      `/api/v1/skills${queryString}`,
    );
  },

  evaluation():
    Promise<EvaluationResponse> {
    return request<EvaluationResponse>(
      "/api/v1/evaluation",
    );
  },
};