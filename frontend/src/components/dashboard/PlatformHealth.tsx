import {
  CheckCircle2,
  ShieldCheck,
} from "lucide-react";


type PlatformHealthProps = {
  apiHealthy: boolean;
  baselineAvailable: boolean;
  releaseDecision: string | null;
};


export function PlatformHealth({
  apiHealthy,
  baselineAvailable,
  releaseDecision,
}: PlatformHealthProps) {
  return (
    <section className="dashboard-card platform-health">
      <div className="card-heading">
        <div>
          <span className="eyebrow">
            Platform
          </span>

          <h3>AI system health</h3>
        </div>

        <span
          className={
            apiHealthy
              ? "health-badge"
              : "health-badge health-badge-warning"
          }
        >
          {apiHealthy
            ? "Operational"
            : "Unavailable"}
        </span>
      </div>

      <div className="health-list">
        <div className="health-row">
          <CheckCircle2 size={17} />

          <div>
            <strong>Production API</strong>
            <span>
              FastAPI service connectivity
            </span>
          </div>

          <span className="health-status">
            {apiHealthy
              ? "Healthy"
              : "Offline"}
          </span>
        </div>

        <div className="health-row">
          <ShieldCheck size={17} />

          <div>
            <strong>Guardrails</strong>
            <span>
              Injection and PII protection
            </span>
          </div>

          <span className="health-status">
            Protected
          </span>
        </div>

        <div className="health-row">
          <CheckCircle2 size={17} />

          <div>
            <strong>Evaluation baseline</strong>

            <span>
              retailops_baseline_v1
            </span>
          </div>

          <span className="health-status">
            {baselineAvailable
              ? releaseDecision?.toUpperCase()
              : "Unavailable"}
          </span>
        </div>
      </div>
    </section>
  );
}