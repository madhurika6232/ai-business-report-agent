import {
  BriefcaseBusiness,
  CircleAlert,
  PackageCheck,
  Users,
} from "lucide-react";


const domains = [
  {
    id: "all",
    label: "All skills",
    icon: BriefcaseBusiness,
  },
  {
    id: "business",
    label: "Business",
    icon: BriefcaseBusiness,
  },
  {
    id: "operations",
    label: "Operations",
    icon: PackageCheck,
  },
  {
    id: "customer",
    label: "Customer",
    icon: Users,
  },
  {
    id: "risk",
    label: "Risk",
    icon: CircleAlert,
  },
];


type SkillDomainsProps = {
  selected: string;
  onChange: (
    domain: string,
  ) => void;
};


export function SkillDomains({
  selected,
  onChange,
}: SkillDomainsProps) {
  return (
    <div className="skill-domains">
      {domains.map((domain) => {
        const Icon = domain.icon;

        return (
          <button
            key={domain.id}
            type="button"
            className={
              selected === domain.id
                ? "skill-domain-button skill-domain-button-active"
                : "skill-domain-button"
            }
            onClick={() =>
              onChange(
                domain.id,
              )
            }
          >
            <Icon size={15} />

            {domain.label}
          </button>
        );
      })}
    </div>
  );
}