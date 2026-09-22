export type HealthResponse = {
  status: string;
  service: string;
};


export type QueryRequest = {
  query: string;
};


export type QueryResponse = {
  query: string;
  safe_query: string | null;
  answer: string;
  selected_agents: string[];
  blocked: boolean;
  block_reason: string | null;
  pii_detected: boolean;
  guardrail_validation:
    | Record<string, unknown>
    | null;
};


export type ConversationRequest = {
  query: string;
  session_id: string;
};


export type ConversationResponse = {
  session_id: string;
  original_query: string;
  resolved_query: string;
  answer: string;
  selected_agents: string[];
};


export type SessionSummary = {
  session_id: string;
  turn_count: number;
  last_query: string | null;
  last_selected_agents: string[];
};


export type Skill = {
  name: string;
  domain: string;
  description: string;
};


export type SkillsResponse = {
  count: number;
  domain: string | null;
  skills: Skill[];
};


export type EvaluatorSummary = {
  name: string;
  category: string;
  description: string;
};


export type EvaluationBaseline = {
  name: string;
  available: boolean;
  status?: string;
  overall_score: number | null;
  release_decision: string | null;
};


export type EvaluationResponse = {
  evaluator_count: number;
  evaluators: EvaluatorSummary[];

  thresholds: Record<
    string,
    Record<string, number>
  >;

  baseline: EvaluationBaseline;
};


export type ApiErrorPayload = {
  detail?: string;
  error?: string;
  request_id?: string;
};

export type ConversationRole =
  | "user"
  | "assistant";


export type ConversationMessage = {
  id: string;
  role: ConversationRole;
  content: string;
  originalQuery?: string;
  resolvedQuery?: string;
  selectedAgents?: string[];
};