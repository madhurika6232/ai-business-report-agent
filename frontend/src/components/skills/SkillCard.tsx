import {
  ArrowUpRight,
  BrainCircuit,
} from "lucide-react";

import type {
  Skill,
} from "../../types/api";


type SkillCardProps = {
  skill: Skill;
};


export function SkillCard({
  skill,
}: SkillCardProps) {
  return (
    <article className="skill-card">
      <div className="skill-card-top">
        <div className="skill-icon">
          <BrainCircuit size={18} />
        </div>

        <ArrowUpRight
          className="skill-arrow"
          size={16}
        />
      </div>

      <div className="skill-domain">
        {skill.domain}
      </div>

      <h3>
        {skill.name}
      </h3>

      <p>
        {skill.description}
      </p>
    </article>
  );
}