import {
  AlertCircle,
} from "lucide-react";

import {
  QueryComposer,
} from "../components/query/QueryComposer";

import {
  QueryResult,
} from "../components/query/QueryResult";

import {
  useRetailOpsQuery,
} from "../hooks/useRetailOpsQuery";

import {
  ApiError,
} from "../services/api";


export function QueryPage() {
  const queryMutation =
    useRetailOpsQuery();

  function submitQuery(
    query: string,
  ) {
    queryMutation.mutate({
      query,
    });
  }

  const error =
    queryMutation.error;

  let errorMessage =
    "RetailOps could not process the request.";

  if (
    error instanceof ApiError
  ) {
    if (error.status === 401) {
      errorMessage =
        "API authentication is required.";
    } else if (
      error.status === 429
    ) {
      errorMessage =
        "The request limit has been reached. Please try again shortly.";
    } else {
      errorMessage =
        error.message;
    }
  }

  return (
    <div className="query-workspace">
      <QueryComposer
        loading={
          queryMutation.isPending
        }
        onSubmit={submitQuery}
      />

      {queryMutation.isPending && (
        <section className="analysis-loading">
          <div className="analysis-spinner" />

          <div>
            <strong>
              Analyzing your question
            </strong>

            <span>
              Routing to the appropriate
              RetailOps intelligence.
            </span>
          </div>
        </section>
      )}

      {queryMutation.isError && (
        <section className="query-error">
          <AlertCircle size={19} />

          <div>
            <strong>
              Analysis unavailable
            </strong>

            <span>
              {errorMessage}
            </span>
          </div>
        </section>
      )}

      {queryMutation.data && (
        <QueryResult
          result={
            queryMutation.data
          }
        />
      )}
    </div>
  );
}