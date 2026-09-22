import type {
  LucideIcon,
} from "lucide-react";


type MetricCardProps = {
  label: string;
  value: string;
  detail: string;
  icon: LucideIcon;
  tone?: "primary" | "success" | "neutral";
};


export function MetricCard({
  label,
  value,
  detail,
  icon: Icon,
  tone = "neutral",
}: MetricCardProps) {
  return (
    <article className="metric-card">
      <div
        className={`metric-icon metric-icon-${tone}`}
      >
        <Icon size={19} />
      </div>

      <div className="metric-label">
        {label}
      </div>

      <div className="metric-value">
        {value}
      </div>

      <div className="metric-detail">
        {detail}
      </div>
    </article>
  );
}