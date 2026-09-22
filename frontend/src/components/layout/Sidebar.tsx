import {
  BarChart3,
  Bot,
  BrainCircuit,
  LayoutDashboard,
  MessageSquare,
  Settings,
  Sparkles,
} from "lucide-react";

import {
  NavLink,
} from "react-router-dom";


const navigation = [
  {
    label: "Overview",
    path: "/",
    icon: LayoutDashboard,
  },
  {
    label: "Ask RetailOps",
    path: "/query",
    icon: Sparkles,
  },
  {
    label: "Conversations",
    path: "/conversations",
    icon: MessageSquare,
  },
  {
    label: "Skills",
    path: "/skills",
    icon: BrainCircuit,
  },
  {
    label: "Evaluation",
    path: "/evaluation",
    icon: BarChart3,
  },
];


export function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-icon">
          <Bot size={22} />
        </div>

        <div>
          <div className="brand-name">
            RetailOps
          </div>

          <div className="brand-subtitle">
            AI Intelligence
          </div>
        </div>
      </div>

      <div className="sidebar-section-label">
        Workspace
      </div>

      <nav
        className="sidebar-nav"
        aria-label="Primary navigation"
      >
        {navigation.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/"}
              className={({ isActive }) =>
                isActive
                  ? "nav-item nav-item-active"
                  : "nav-item"
              }
            >
              <Icon size={19} />

              <span>
                {item.label}
              </span>
            </NavLink>
          );
        })}
      </nav>

      <div className="sidebar-footer">
        <NavLink
          to="/settings"
          aria-label="Application settings"
          className={({ isActive }) =>
            isActive
              ? "nav-item nav-item-active"
              : "nav-item"
          }
        >
          <Settings size={19} />

          <span>
            Settings
          </span>
        </NavLink>

        <div className="system-status">
          <span className="status-dot" />

          <div>
            <strong>
              System operational
            </strong>

            <span>
              Production API
            </span>
          </div>
        </div>
      </div>
    </aside>
  );
}