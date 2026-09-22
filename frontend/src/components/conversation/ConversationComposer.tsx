import {
  ArrowUp,
} from "lucide-react";

import {
  useState,
} from "react";


type ConversationComposerProps = {
  loading: boolean;
  onSubmit: (
    message: string,
  ) => void;
};


export function ConversationComposer({
  loading,
  onSubmit,
}: ConversationComposerProps) {
  const [
    message,
    setMessage,
  ] = useState("");

  function submit() {
    const cleaned =
      message.trim();

    if (
      !cleaned ||
      loading
    ) {
      return;
    }

    onSubmit(cleaned);
    setMessage("");
  }

  return (
    <div className="conversation-composer">
      <textarea
        value={message}
        onChange={(event) =>
          setMessage(
            event.target.value,
          )
        }
        onKeyDown={(event) => {
          if (
            event.key === "Enter" &&
            !event.shiftKey
          ) {
            event.preventDefault();
            submit();
          }
        }}
        placeholder="Ask a follow-up question..."
        rows={2}
        maxLength={2000}
      />

      <button
        type="button"
        onClick={submit}
        disabled={
          loading ||
          !message.trim()
        }
        aria-label="Send message"
      >
        <ArrowUp size={17} />
      </button>
    </div>
  );
}