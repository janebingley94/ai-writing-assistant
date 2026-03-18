export async function readSSE(
  response: Response,
  onToken: (token: string) => void,
  onDone?: () => void,
) {
  if (!response.body) {
    throw new Error("No response body");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value, { stream: true });
    const lines = chunk.split("\n");

    for (const line of lines) {
      if (!line.startsWith("data:")) continue;
      const data = line.replace("data:", "").trim();
      if (!data) continue;
      if (data === "[DONE]") {
        onDone?.();
        continue;
      }
      onToken(data);
    }
  }
}
