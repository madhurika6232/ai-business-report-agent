import {
  AlertCircle,
  BrainCircuit,
  Search,
} from "lucide-react";

import {
  useMemo,
  useState,
} from "react";

import {
  SkillCard,
} from "../components/skills/SkillCard";

import {
  SkillDomains,
} from "../components/skills/SkillDomains";

import {
  useSkills,
} from "../hooks/usePlatformData";


export function SkillsPage() {
  const [
    selectedDomain,
    setSelectedDomain,
  ] = useState("all");

  const [
    search,
    setSearch,
  ] = useState("");

  const skillsQuery =
    useSkills();

  const skills = useMemo(
    () => {
      const allSkills =
        skillsQuery.data?.skills ?? [];

      const normalizedSearch =
        search
          .trim()
          .toLowerCase();

      return allSkills.filter(
        (skill) => {
          const domainMatches =
            selectedDomain === "all" ||
            skill.domain.toLowerCase() ===
              selectedDomain;

          const searchMatches =
            !normalizedSearch ||
            skill.name
              .toLowerCase()
              .includes(
                normalizedSearch,
              ) ||
            skill.description
              .toLowerCase()
              .includes(
                normalizedSearch,
              );

          return (
            domainMatches &&
            searchMatches
          );
        },
      );
    },
    [
      skillsQuery.data,
      selectedDomain,
      search,
    ],
  );

  return (
    <div className="skills-page">
      <section className="skills-hero">
        <div>
          <span className="eyebrow">
            Intelligence Catalog
          </span>

          <h2>
            Specialist intelligence,
            on demand.
          </h2>

          <p>
            Explore the analytical
            capabilities available across
            business, operations, customer,
            and risk intelligence.
          </p>
        </div>

        <div className="skills-count">
          <BrainCircuit size={20} />

          <div>
            <strong>
              {skillsQuery.data?.count ??
                "—"}
            </strong>

            <span>
              Available skills
            </span>
          </div>
        </div>
      </section>

      <section className="skills-toolbar">
        <SkillDomains
          selected={
            selectedDomain
          }
          onChange={
            setSelectedDomain
          }
        />

        <div className="skills-search">
          <Search size={16} />

          <input
            value={search}
            onChange={(event) =>
              setSearch(
                event.target.value,
              )
            }
            placeholder="Search skills..."
          />
        </div>
      </section>

      {skillsQuery.isLoading && (
        <div className="skills-state">
          <div className="analysis-spinner" />

          <span>
            Loading intelligence
            capabilities...
          </span>
        </div>
      )}

      {skillsQuery.isError && (
        <div className="skills-state skills-state-error">
          <AlertCircle size={18} />

          <span>
            Skills could not be loaded.
            Verify that the RetailOps API
            is available.
          </span>
        </div>
      )}

      {!skillsQuery.isLoading &&
        !skillsQuery.isError && (
          <>
            <div className="skills-results-header">
              <span>
                {selectedDomain === "all"
                  ? "All capabilities"
                  : `${selectedDomain} intelligence`}
              </span>

              <strong>
                {skills.length}
                {" "}
                {skills.length === 1
                  ? "skill"
                  : "skills"}
              </strong>
            </div>

            {skills.length > 0 ? (
              <section className="skills-grid">
                {skills.map(
                  (skill) => (
                    <SkillCard
                      key={`${skill.domain}-${skill.name}`}
                      skill={skill}
                    />
                  ),
                )}
              </section>
            ) : (
              <div className="skills-empty">
                <Search size={21} />

                <strong>
                  No matching skills
                </strong>

                <span>
                  Try another search or
                  intelligence domain.
                </span>
              </div>
            )}
          </>
        )}
    </div>
  );
}