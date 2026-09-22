import {
  ArrowRight,
  BrainCircuit,
  MessageSquare,
  Sparkles,
} from "lucide-react";

import {
  Link,
} from "react-router-dom";


const actions = [
  {
    title: "Ask RetailOps",
    description:
      "Analyze business performance using verified evidence.",
    path: "/query",
    icon: Sparkles,
  },
  {
    title: "Continue analysis",
    description:
      "Return to a multi-turn business conversation.",
    path: "/conversations",
    icon: MessageSquare,
  },
  {
    title: "Explore skills",
    description:
      "Discover the intelligence capabilities available.",
    path: "/skills",
    icon: BrainCircuit,
  },
];


export function QuickActions() {
  return (
    <section className="dashboard-card">
      <div className="card-heading">
        <div>
          <span className="eyebrow">
            Workspace
          </span>

          <h3>Quick actions</h3>
        </div>
      </div>

      <div className="quick-actions">
        {actions.map((action) => {
          const Icon = action.icon;

          return (
            <Link
              key={action.path}
              to={action.path}
              className="quick-action"
            >
              <div className="quick-action-icon">
                <Icon size={18} />
              </div>

              <div>
                <strong>
                  {action.title}
                </strong>

                <span>
                  {action.description}
                </span>
              </div>

              <ArrowRight
                className="quick-action-arrow"
                size={17}
              />
            </Link>
          );
        })}
      </div>
    </section>
  );
}