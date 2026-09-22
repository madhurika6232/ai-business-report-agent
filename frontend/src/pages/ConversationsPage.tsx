import {
  AlertCircle,
  MessageSquare,
  Plus,
  Trash2,
} from "lucide-react";

import {
  useState,
} from "react";

import {
  ConversationComposer,
} from "../components/conversation/ConversationComposer";

import {
  ConversationMessage,
} from "../components/conversation/ConversationMessage";

import {
  useConversation,
  useDeleteSession,
} from "../hooks/useConversation";

import {
  ApiError,
} from "../services/api";

import type {
  ConversationMessage as ConversationMessageType,
} from "../types/api";

import {
  getOrCreateSessionId,
  resetSessionId,
} from "../utils/session";


export function ConversationsPage() {
  const [
    sessionId,
    setSessionId,
  ] = useState(
    () => getOrCreateSessionId(),
  );

  const [
    messages,
    setMessages,
  ] = useState<
    ConversationMessageType[]
  >([]);

  const conversation =
    useConversation();

  const deleteSession =
    useDeleteSession();

  function startNewConversation() {
    const nextSessionId =
      resetSessionId();

    setSessionId(
      nextSessionId,
    );

    setMessages([]);

    conversation.reset();
    deleteSession.reset();
  }

  function submitMessage(
    content: string,
  ) {
    const userMessage:
      ConversationMessageType = {
        id: crypto.randomUUID(),
        role: "user",
        content,
      };

    setMessages(
      (current) => [
        ...current,
        userMessage,
      ],
    );

    conversation.mutate(
      {
        query: content,
        session_id: sessionId,
      },
      {
        onSuccess: (result) => {
          const assistantMessage:
            ConversationMessageType = {
              id: crypto.randomUUID(),
              role: "assistant",
              content: result.answer,
              originalQuery:
                result.original_query,
              resolvedQuery:
                result.resolved_query,
              selectedAgents:
                result.selected_agents,
            };

          setMessages(
            (current) => [
              ...current,
              assistantMessage,
            ],
          );
        },
      },
    );
  }

  function removeConversation() {
    if (messages.length === 0) {
      startNewConversation();
      return;
    }

    deleteSession.mutate(
      sessionId,
      {
        onSuccess: () => {
          startNewConversation();
        },
      },
    );
  }

  const error =
    conversation.error ??
    deleteSession.error;

  let errorMessage =
    "The conversation could not be updated.";

  if (error instanceof ApiError) {
    if (error.status === 401) {
      errorMessage =
        "API authentication is required.";
    } else if (
      error.status === 429
    ) {
      errorMessage =
        "The request limit has been reached. Please try again shortly.";
    } else {
      errorMessage =
        error.message;
    }
  }

  return (
    <div className="conversation-page">
      <aside className="conversation-panel">
        <button
          type="button"
          className="new-conversation-button"
          onClick={
            startNewConversation
          }
        >
          <Plus size={16} />
          New conversation
        </button>

        <div className="conversation-session-card">
          <span>
            Current session
          </span>

          <strong>
            {sessionId.slice(0, 8)}
          </strong>

          <small>
            Session memory active
          </small>
        </div>

        <button
          type="button"
          className="delete-conversation-button"
          onClick={
            removeConversation
          }
          disabled={
            deleteSession.isPending
          }
        >
          <Trash2 size={15} />

          {deleteSession.isPending
            ? "Deleting..."
            : "Delete session"}
        </button>
      </aside>

      <section className="conversation-workspace">
        <div className="conversation-timeline">
          {messages.length === 0 ? (
            <div className="conversation-empty">
              <div className="conversation-empty-icon">
                <MessageSquare size={22} />
              </div>

              <span className="eyebrow">
                Conversation Intelligence
              </span>

              <h2>
                Continue the analysis.
              </h2>

              <p>
                Start with a business question,
                then ask follow-ups. RetailOps
                will preserve the session context
                and resolve references across
                turns.
              </p>

              <div className="conversation-examples">
                <span>
                  “How was revenue in March 2018?”
                </span>

                <span>
                  “What about the previous month?”
                </span>
              </div>
            </div>
          ) : (
            messages.map(
              (message) => (
                <ConversationMessage
                  key={message.id}
                  message={message}
                />
              ),
            )
          )}

          {conversation.isPending && (
            <div className="conversation-thinking">
              <div className="analysis-spinner" />

              <div>
                <strong>
                  RetailOps is analyzing
                </strong>

                <span>
                  Resolving conversation context
                  and gathering evidence.
                </span>
              </div>
            </div>
          )}

          {error && (
            <div className="conversation-error">
              <AlertCircle size={18} />

              <div>
                <strong>
                  Conversation unavailable
                </strong>

                <span>
                  {errorMessage}
                </span>
              </div>
            </div>
          )}
        </div>

        <div className="conversation-composer-area">
          <ConversationComposer
            loading={
              conversation.isPending
            }
            onSubmit={
              submitMessage
            }
          />

          <span className="conversation-disclaimer">
            RetailOps responses are validated
            against available evidence and
            safety guardrails.
          </span>
        </div>
      </section>
    </div>
  );
}