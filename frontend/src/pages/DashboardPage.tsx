import {
  BrainCircuit,
  CheckCircle2,
  Gauge,
  ShieldCheck,
} from "lucide-react";

import {
  MetricCard,
} from "../components/dashboard/MetricCard";

import {
  PlatformHealth,
} from "../components/dashboard/PlatformHealth";

import {
  QuickActions,
} from "../components/dashboard/QuickActions";

import {
  useEvaluation,
  useHealth,
  useSkills,
} from "../hooks/usePlatformData";


export function DashboardPage() {
  const health = useHealth();
  const skills = useSkills();
  const evaluation = useEvaluation();

  const baseline =
    evaluation.data?.baseline;

  const evaluatorCount =
    evaluation.data?.evaluator_count;

  const skillCount =
    skills.data?.count;

  const systemHealthy =
    health.data?.status === "ok";

  const isLoading =
    health.isLoading ||
    skills.isLoading ||
    evaluation.isLoading;

  const hasError =
    health.isError ||
    skills.isError ||
    evaluation.isError;

  return (
    <div className="dashboard">
      <section className="dashboard-hero">
        <div>
          <span className="eyebrow">
            Retail Intelligence
          </span>

          <h2>
            Your business,
            <br />
            understood.
          </h2>

          <p>
            Turn retail operations, customer
            signals, and risk data into
            evidence-grounded decisions.
          </p>
        </div>

        <div className="hero-status">
          <div className="hero-status-icon">
            <CheckCircle2 size={21} />
          </div>

          <div>
            <span>Platform status</span>

            <strong>
              {systemHealthy
                ? "Operational"
                : "Checking system"}
            </strong>
          </div>
        </div>
      </section>

      {hasError && (
        <div className="dashboard-alert">
          Some platform information could not
          be loaded. Verify that the RetailOps
          API is running.
        </div>
      )}

      <section className="metric-grid">
        <MetricCard
          label="Quality baseline"
          value={
            baseline?.overall_score != null
              ? baseline.overall_score.toFixed(2)
              : isLoading
                ? "—"
                : "N/A"
          }
          detail={
            baseline?.available
              ? "Official V1 evaluation score"
              : "No evaluation baseline available"
          }
          icon={Gauge}
          tone="primary"
        />

        <MetricCard
          label="Evaluators"
          value={
            evaluatorCount != null
              ? `${evaluatorCount} / ${evaluatorCount}`
              : "—"
          }
          detail="Evaluation framework coverage"
          icon={CheckCircle2}
          tone="success"
        />

        <MetricCard
          label="AI skills"
          value={
            skillCount != null
              ? String(skillCount)
              : "—"
          }
          detail="Available intelligence capabilities"
          icon={BrainCircuit}
          tone="neutral"
        />

        <MetricCard
          label="Release"
          value={
            baseline?.release_decision
              ?.toUpperCase()
              ?? "—"
          }
          detail="Official quality release decision"
          icon={ShieldCheck}
          tone="success"
        />
      </section>

      <section className="dashboard-columns">
        <QuickActions />

        <PlatformHealth
          apiHealthy={systemHealthy}
          baselineAvailable={
            baseline?.available ?? false
          }
          releaseDecision={
            baseline?.release_decision ?? null
          }
        />
      </section>

      <section className="dashboard-card intelligence-panel">
        <div className="card-heading">
          <div>
            <span className="eyebrow">
              Intelligence
            </span>

            <h3>
              Ask the business, not the dashboard
            </h3>
          </div>
        </div>

        <p>
          RetailOps AI routes each question to
          specialist business, operations,
          customer, and risk intelligence while
          grounding the final response in
          verified evidence.
        </p>

        <div className="example-questions">
          <span>
            “How is the business performing?”
          </span>

          <span>
            “Which sellers have the worst delivery
            performance?”
          </span>

          <span>
            “What are customers complaining about?”
          </span>

          <span>
            “Were there unusual delivery anomalies?”
          </span>
        </div>
      </section>
    </div>
  );
}