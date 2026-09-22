import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";

import { AppLayout } from "../layouts/AppLayout";
import { ConversationsPage } from "../pages/ConversationsPage";
import { DashboardPage } from "../pages/DashboardPage";
import { EvaluationPage } from "../pages/EvaluationPage";
import { QueryPage } from "../pages/QueryPage";
import { SettingsPage } from "../pages/SettingsPage";
import { SkillsPage } from "../pages/SkillsPage";


import {
  NotFoundPage,
} from "../pages/NotFoundPage";

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route
            path="/"
            element={<DashboardPage />}
          />

          <Route
            path="/query"
            element={<QueryPage />}
          />

          <Route
            path="/conversations"
            element={<ConversationsPage />}
          />

          <Route
            path="/skills"
            element={<SkillsPage />}
          />

          <Route
            path="/evaluation"
            element={<EvaluationPage />}
          />

          <Route
            path="/settings"
            element={<SettingsPage />}
          />

          <Route
            path="*"
            element={<NotFoundPage />}
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}