import {
  CheckCircle2,
} from "lucide-react";

import type {
  EvaluatorSummary,
} from "../../types/api";


type EvaluatorListProps = {
  evaluators: EvaluatorSummary[];
};


export function EvaluatorList({
  evaluators,
}: EvaluatorListProps) {
  return (
    <section className="evaluation-card">
      <div className="evaluation-card-heading">
        <div>
          <span className="eyebrow">
            Evaluation Suite
          </span>

          <h3>
            Quality coverage
          </h3>
        </div>

        <span className="evaluation-count-badge">
          {evaluators.length} evaluators
        </span>
      </div>

      <div className="evaluator-list">
        {evaluators.map(
          (evaluator) => (
            <div
              key={evaluator.name}
              className="evaluator-row"
            >
              <div className="evaluator-check">
                <CheckCircle2 size={16} />
              </div>

              <div className="evaluator-info">
                <strong>
                  {evaluator.name.replace(
                    /_/g,
                    " ",
                  )}
                </strong>

                <span>
                  {evaluator.description}
                </span>
              </div>

              <span className="evaluator-category">
                {evaluator.category}
              </span>
            </div>
          ),
        )}
      </div>
    </section>
  );
}