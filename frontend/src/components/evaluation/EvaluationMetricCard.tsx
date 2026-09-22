import type {
  LucideIcon,
} from "lucide-react";


type EvaluationMetricCardProps = {
  label: string;
  value: string;
  detail: string;
  icon: LucideIcon;
  status?: "success" | "primary" | "neutral";
};


export function EvaluationMetricCard({
  label,
  value,
  detail,
  icon: Icon,
  status = "neutral",
}: EvaluationMetricCardProps) {
  return (
    <article className="evaluation-metric">
      <div
        className={
          `evaluation-metric-icon evaluation-metric-${status}`
        }
      >
        <Icon size={18} />
      </div>

      <span>{label}</span>

      <strong>{value}</strong>

      <small>{detail}</small>
    </article>
  );
}