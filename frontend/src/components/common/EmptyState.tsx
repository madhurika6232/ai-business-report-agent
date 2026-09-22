import {
  Inbox,
} from "lucide-react";


type EmptyStateProps = {
  title: string;
  description: string;
};


export function EmptyState({
  title,
  description,
}: EmptyStateProps) {
  return (
    <div className="app-empty-state">
      <div className="app-empty-icon">
        <Inbox size={20} />
      </div>

      <strong>{title}</strong>
      <span>{description}</span>
    </div>
  );
}