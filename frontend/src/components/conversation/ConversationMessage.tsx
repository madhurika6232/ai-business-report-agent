import {
  Bot,
  User,
} from "lucide-react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import {
  AgentBadge,
} from "../query/AgentBadge";

import type {
  ConversationMessage as ConversationMessageType,
} from "../../types/api";


type ConversationMessageProps = {
  message: ConversationMessageType;
};


export function ConversationMessage({
  message,
}: ConversationMessageProps) {
  const isUser =
    message.role === "user";

  return (
    <article
      className={
        isUser
          ? "conversation-message conversation-message-user"
          : "conversation-message conversation-message-assistant"
      }
    >
      <div className="message-avatar">
        {isUser
          ? <User size={16} />
          : <Bot size={17} />}
      </div>

      <div className="message-content">
        <div className="message-meta">
          <strong>
            {isUser
              ? "You"
              : "RetailOps AI"}
          </strong>

          {!isUser && (
            <span>
              Evidence-grounded analysis
            </span>
          )}
        </div>

        <div className="message-body">
          {isUser ? (
            <p>
              {message.content}
            </p>
          ) : (
            <ReactMarkdown
              remarkPlugins={[
                remarkGfm,
              ]}
            >
              {message.content}
            </ReactMarkdown>
          )}
        </div>

        {!isUser &&
          message.resolvedQuery &&
          message.originalQuery !==
            message.resolvedQuery && (
            <div className="resolved-query">
              <span>
                Context resolved as
              </span>

              <strong>
                {message.resolvedQuery}
              </strong>
            </div>
          )}

        {!isUser &&
          message.selectedAgents &&
          message.selectedAgents.length > 0 && (
            <div className="message-agents">
              {message.selectedAgents.map(
                (agent) => (
                  <AgentBadge
                    key={agent}
                    agent={agent}
                  />
                ),
              )}
            </div>
          )}
      </div>
    </article>
  );
}