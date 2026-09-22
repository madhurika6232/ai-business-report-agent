from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Skill:
    """Definition of a reusable RetailOps capability."""

    name: str
    description: str
    domain: str
    handler: Callable


class SkillRegistry:
    """Registry for discovering and executing RetailOps skills."""

    def __init__(self):
        self._skills: dict[str, Skill] = {}

    def register(
        self,
        skill: Skill,
    ) -> None:
        """Register a skill."""

        if skill.name in self._skills:
            raise ValueError(
                f"Skill already registered: {skill.name}"
            )

        self._skills[skill.name] = skill

    def get(
        self,
        name: str,
    ) -> Skill:
        """Retrieve a skill by name."""

        if name not in self._skills:
            raise KeyError(
                f"Unknown skill: {name}"
            )

        return self._skills[name]

    def list_skills(
        self,
        domain: str | None = None,
    ) -> list[Skill]:
        """List registered skills, optionally filtered by domain."""

        skills = list(
            self._skills.values()
        )

        if domain is not None:
            skills = [
                skill
                for skill in skills
                if skill.domain == domain
            ]

        return skills

    def execute(
        self,
        name: str,
        **kwargs,
    ):
        """Execute a registered skill."""

        skill = self.get(name)

        return skill.handler(
            **kwargs
        )

    def __len__(self) -> int:
        return len(self._skills)