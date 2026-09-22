import {
  ArrowUp,
  Sparkles,
} from "lucide-react";

import {
  useState,
} from "react";


type QueryComposerProps = {
  loading: boolean;
  onSubmit: (
    query: string,
  ) => void;
};


const suggestions = [
  "How is the business performing?",
  "Which sellers have the worst delivery performance?",
  "What are customers complaining about?",
  "Were there unusual delivery anomalies?",
];


export function QueryComposer({
  loading,
  onSubmit,
}: QueryComposerProps) {
  const [
    query,
    setQuery,
  ] = useState("");

  function submit() {
    const cleaned =
      query.trim();

    if (
      !cleaned ||
      loading
    ) {
      return;
    }

    onSubmit(
      cleaned,
    );
  }

  return (
    <section className="query-composer-card">
      <div className="query-composer-heading">
        <div className="query-spark">
          <Sparkles size={18} />
        </div>

        <div>
          <span className="eyebrow">
            AI Business Analyst
          </span>

          <h2>
            What would you like to understand?
          </h2>

          <p>
            Ask about business performance,
            operations, customers, or risk.
          </p>
        </div>
      </div>

      <div className="query-input-shell">
        <textarea
          aria-label="Ask RetailOps a business question"
          value={query}
          onChange={(event) =>
            setQuery(
              event.target.value,
            )
          }
          onKeyDown={(event) => {
            if (
              event.key === "Enter" &&
              !event.shiftKey
            ) {
              event.preventDefault();
              submit();
            }
          }}
          placeholder="Ask RetailOps a business question..."
          rows={4}
          maxLength={2000}
        />

        <div className="query-input-footer">
          <span>
            Enter to send · Shift + Enter
            for a new line
          </span>

          <button
            type="button"
            className="query-submit"
            aria-label="Submit business question"
            onClick={submit}
            disabled={
              loading ||
              !query.trim()
            }
          >
            {loading
              ? "Analyzing"
              : "Ask RetailOps"}

            <ArrowUp size={15} />
          </button>
        </div>
      </div>

      <div className="suggestion-section">
        <span>
          Try asking
        </span>

        <div className="suggestion-grid">
          {suggestions.map(
            (suggestion) => (
              <button
                key={suggestion}
                type="button"
                onClick={() =>
                  setQuery(
                    suggestion,
                  )
                }
              >
                {suggestion}
              </button>
            ),
          )}
        </div>
      </div>
    </section>
  );
}