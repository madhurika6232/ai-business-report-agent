import {
  useMutation,
} from "@tanstack/react-query";

import {
  retailOpsApi,
} from "../services/api";

import type {
  ConversationRequest,
} from "../types/api";


export function useConversation() {
  return useMutation({
    mutationFn: (
      payload: ConversationRequest,
    ) =>
      retailOpsApi.conversation(
        payload,
      ),
  });
}


export function useDeleteSession() {
  return useMutation({
    mutationFn: (
      sessionId: string,
    ) =>
      retailOpsApi.deleteSession(
        sessionId,
      ),
  });
}