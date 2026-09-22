import {
  BriefcaseBusiness,
  CircleAlert,
  PackageCheck,
  Users,
} from "lucide-react";


type AgentBadgeProps = {
  agent: string;
};


const agentIcons = {
  business: BriefcaseBusiness,
  operations: PackageCheck,
  customer: Users,
  risk: CircleAlert,
};


export function AgentBadge({
  agent,
}: AgentBadgeProps) {
  const Icon =
    agentIcons[
      agent as keyof typeof agentIcons
    ] ?? BriefcaseBusiness;

  return (
    <span className="agent-badge">
      <Icon size={13} />

      {agent}
    </span>
  );
}