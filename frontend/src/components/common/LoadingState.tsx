type LoadingStateProps = {
  title?: string;
  description?: string;
};


export function LoadingState({
  title = "Loading",
  description = "Retrieving the latest information.",
}: LoadingStateProps) {
  return (
    <div className="app-state">
      <div className="analysis-spinner" />

      <div>
        <strong>{title}</strong>
        <span>{description}</span>
      </div>
    </div>
  );
}