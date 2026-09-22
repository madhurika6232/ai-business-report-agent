import {
  Outlet,
  useLocation,
} from "react-router-dom";

import { Sidebar } from "../components/layout/Sidebar";
import { Topbar } from "../components/layout/Topbar";


const pageMetadata: Record<
  string,
  {
    title: string;
    description: string;
  }
> = {
  "/": {
    title: "Overview",
    description:
      "Monitor business performance and AI intelligence.",
  },
  "/query": {
    title: "Ask RetailOps",
    description:
      "Ask business questions using verified operational evidence.",
  },
  "/conversations": {
    title: "Conversations",
    description:
      "Continue and manage your RetailOps analysis sessions.",
  },
  "/skills": {
    title: "Skills",
    description:
      "Explore the analytical capabilities available to RetailOps AI.",
  },
  "/evaluation": {
    title: "Evaluation",
    description:
      "Monitor AI quality, safety, and release readiness.",
  },
  "/settings": {
    title: "Settings",
    description:
      "Manage application and API preferences.",
  },
};


export function AppLayout() {
  const location = useLocation();

  const metadata =
    pageMetadata[location.pathname]
    ?? pageMetadata["/"];

  return (
    <div className="app-shell">
      <a
        href="#main-content"
        className="skip-link"
      >
        Skip to main content
      </a>

      <Sidebar />

      <div className="app-main">
        <Topbar
          title={metadata.title}
          description={metadata.description}
        />

        <main
          id="main-content"
          className="page-content"
        >
          <Outlet />
        </main>
      </div>
    </div>
  );
}

