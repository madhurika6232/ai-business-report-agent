import {
  useMutation,
} from "@tanstack/react-query";

import {
  retailOpsApi,
} from "../services/api";

import type {
  QueryRequest,
} from "../types/api";


export function useRetailOpsQuery() {
  return useMutation({
    mutationFn: (
      payload: QueryRequest,
    ) => retailOpsApi.query(
      payload,
    ),
  });
}