import {
  useQuery,
} from "@tanstack/react-query";

import {
  retailOpsApi,
} from "../services/api";


export function useHealth() {
  return useQuery({
    queryKey: ["health"],
    queryFn: () =>
      retailOpsApi.health(),
    refetchInterval: 30_000,
  });
}


export function useSkills() {
  return useQuery({
    queryKey: ["skills"],
    queryFn: () =>
      retailOpsApi.skills(),
  });
}


export function useEvaluation() {
  return useQuery({
    queryKey: ["evaluation"],
    queryFn: () =>
      retailOpsApi.evaluation(),
  });
}

export function useSkillsByDomain(
  domain: string,
) {
  return useQuery({
    queryKey: [
      "skills",
      domain,
    ],
    queryFn: () =>
      retailOpsApi.skills(
        domain,
      ),
    enabled: Boolean(domain),
  });
}