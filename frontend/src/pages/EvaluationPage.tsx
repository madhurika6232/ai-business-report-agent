import {
  AlertCircle,
  CheckCircle2,
  Gauge,
  ShieldCheck,
} from "lucide-react";

import {
  EvaluationMetricCard,
} from "../components/evaluation/EvaluationMetricCard";

import {
  EvaluatorList,
} from "../components/evaluation/EvaluatorList";

import {
  ThresholdPanel,
} from "../components/evaluation/ThresholdPanel";

import {
  useEvaluation,
} from "../hooks/usePlatformData";


export function EvaluationPage() {
  const evaluation =
    useEvaluation();

  if (evaluation.isLoading) {
    return (
      <div className="evaluation-state">
        <div className="analysis-spinner" />

        <span>
          Loading evaluation baseline...
        </span>
      </div>
    );
  }

  if (
    evaluation.isError ||
    !evaluation.data
  ) {
    return (
      <div className="evaluation-state evaluation-state-error">
        <AlertCircle size={19} />

        <div>
          <strong>
            Evaluation unavailable
          </strong>

          <span>
            Verify that the RetailOps API
            is available.
          </span>
        </div>
      </div>
    );
  }

  const {
    baseline,
    evaluators,
    evaluator_count,
    thresholds,
  } = evaluation.data;

  const releasePassed =
    baseline.release_decision
      ?.toLowerCase() === "pass";

  return (
    <div className="evaluation-page">
      <section className="evaluation-hero">
        <div>
          <span className="eyebrow">
            AI Quality & Safety
          </span>

          <h2>
            Release confidence,
            measured.
          </h2>

          <p>
            Monitor the persisted RetailOps
            evaluation baseline, release gates,
            and quality framework without
            rerunning expensive model
            evaluations.
          </p>
        </div>

        <div className="evaluation-release">
          <div
            className={
              releasePassed
                ? "evaluation-release-icon"
                : "evaluation-release-icon evaluation-release-warning"
            }
          >
            {releasePassed ? (
              <CheckCircle2 size={21} />
            ) : (
              <AlertCircle size={21} />
            )}
          </div>

          <div>
            <span>
              Release decision
            </span>

            <strong>
              {baseline.release_decision
                ?.toUpperCase() ??
                "UNKNOWN"}
            </strong>
          </div>
        </div>
      </section>

      <section className="evaluation-metric-grid">
        <EvaluationMetricCard
          label="Overall score"
          value={
            baseline.overall_score != null
              ? baseline.overall_score.toFixed(
                  2,
                )
              : "N/A"
          }
          detail="Official persisted V1 baseline"
          icon={Gauge}
          status="primary"
        />

        <EvaluationMetricCard
          label="Evaluators"
          value={`${evaluator_count} / ${evaluator_count}`}
          detail="Configured evaluation coverage"
          icon={CheckCircle2}
          status="success"
        />

        <EvaluationMetricCard
          label="Baseline"
          value={
            baseline.available
              ? "Available"
              : "Missing"
          }
          detail={baseline.name}
          icon={ShieldCheck}
          status={
            baseline.available
              ? "success"
              : "neutral"
          }
        />

        <EvaluationMetricCard
          label="Release"
          value={
            baseline.release_decision
              ?.toUpperCase() ??
            "UNKNOWN"
          }
          detail="Current release decision"
          icon={ShieldCheck}
          status={
            releasePassed
              ? "success"
              : "neutral"
          }
        />
      </section>

      <section className="evaluation-layout">
        <EvaluatorList
          evaluators={
            evaluators
          }
        />

        <ThresholdPanel
          thresholds={
            thresholds
          }
        />
      </section>

      <section className="evaluation-note">
        <ShieldCheck size={17} />

        <div>
          <strong>
            Persisted evaluation status
          </strong>

          <span>
            This dashboard reads the saved
            release baseline. Viewing this page
            does not execute Groq-backed
            evaluators or consume evaluation
            quota.
          </span>
        </div>
      </section>
    </div>
  );
}