const SESSION_STORAGE_KEY =
  "retailops_session_id";


export function createSessionId(): string {
  return crypto.randomUUID();
}


export function getOrCreateSessionId(): string {
  const existing =
    sessionStorage.getItem(
      SESSION_STORAGE_KEY,
    );

  if (existing) {
    return existing;
  }

  const sessionId =
    createSessionId();

  sessionStorage.setItem(
    SESSION_STORAGE_KEY,
    sessionId,
  );

  return sessionId;
}


export function resetSessionId(): string {
  const sessionId =
    createSessionId();

  sessionStorage.setItem(
    SESSION_STORAGE_KEY,
    sessionId,
  );

  return sessionId;
}


export function clearSessionId(): void {
  sessionStorage.removeItem(
    SESSION_STORAGE_KEY,
  );
}