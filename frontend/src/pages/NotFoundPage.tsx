import {
  ArrowLeft,
  SearchX,
} from "lucide-react";

import {
  Link,
} from "react-router-dom";


export function NotFoundPage() {
  return (
    <div className="not-found-page">
      <div className="not-found-icon">
        <SearchX size={24} />
      </div>

      <span className="eyebrow">
        404
      </span>

      <h2>
        Page not found.
      </h2>

      <p>
        The page you're looking for doesn't
        exist in the RetailOps workspace.
      </p>

      <Link
        to="/"
        className="not-found-link"
      >
        <ArrowLeft size={14} />
        Return to overview
      </Link>
    </div>
  );
}