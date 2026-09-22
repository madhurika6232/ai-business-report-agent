import {
  CheckCircle2,
  ShieldCheck,
  Sparkles,
} from "lucide-react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import {
  AgentBadge,
} from "./AgentBadge";

import type {
  QueryResponse,
} from "../../types/api";


type QueryResultProps = {
  result: QueryResponse;
};


export function QueryResult({
  result,
}: QueryResultProps) {
  if (result.blocked) {
    return (
      <section className="query-result query-blocked">
        <div className="blocked-icon">
          <ShieldCheck size={21} />
        </div>

        <div>
          <span className="eyebrow">
            Request protected
          </span>

          <h3>
            This request was blocked
          </h3>

          <p>
            {result.block_reason ??
              "The request could not be processed safely."}
          </p>
        </div>
      </section>
    );
  }

  return (
    <section className="query-result">
      <div className="result-heading">
        <div className="result-icon">
          <Sparkles size={19} />
        </div>

        <div>
          <span className="eyebrow">
            RetailOps Analysis
          </span>

          <h3>
            Business intelligence response
          </h3>
        </div>

        <span className="grounded-badge">
          <ShieldCheck size={13} />
          <span>Guarded</span>
        </span>
      </div>

      <div className="result-answer">
        <ReactMarkdown
          remarkPlugins={[
            remarkGfm,
          ]}
        >
          {result.answer}
        </ReactMarkdown>
      </div>

      {result.selected_agents.length > 0 && (
        <div className="result-agents">
          <span>
            Intelligence used
          </span>

          <div>
            {result.selected_agents.map(
              (agent) => (
                <AgentBadge
                  key={agent}
                  agent={agent}
                />
              ),
            )}
          </div>
        </div>
      )}

      <div className="trust-strip">
        <span>
          <ShieldCheck size={14} />
          Guardrail protected
        </span>

        <span>
          <CheckCircle2 size={14} />
          Output validated
        </span>

        {result.pii_detected && (
          <span>
            <ShieldCheck size={14} />
            PII protected
          </span>
        )}
      </div>
    </section>
  );
}