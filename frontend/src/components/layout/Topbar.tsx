import {
  Bell,
  Search,
} from "lucide-react";


type TopbarProps = {
  title: string;
  description?: string;
};


export function Topbar({
  title,
  description,
}: TopbarProps) {
  return (
    <header className="topbar">
      <div>
        <h1>{title}</h1>

        {description && (
          <p>{description}</p>
        )}
      </div>

      <div className="topbar-actions">
        <div className="search-box">
          <Search size={17} />

          <span>Search RetailOps</span>

          <kbd>⌘ K</kbd>
        </div>

        <button
          className="icon-button"
          type="button"
          aria-label="Notifications"
        >
          <Bell size={19} />
        </button>

        <div className="user-avatar">
          MK
        </div>
      </div>
    </header>
  );
}