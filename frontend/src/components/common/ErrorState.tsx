import {
  AlertCircle,
  RefreshCw,
} from "lucide-react";


type ErrorStateProps = {
  title?: string;
  description: string;
  onRetry?: () => void;
};


export function ErrorState({
  title = "Something went wrong",
  description,
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="app-state app-state-error">
      <div className="app-state-icon">
        <AlertCircle size={19} />
      </div>

      <div className="app-state-content">
        <strong>{title}</strong>
        <span>{description}</span>
      </div>

      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="state-retry-button"
        >
          <RefreshCw size={13} />
          Retry
        </button>
      )}
    </div>
  );
}