const wsBaseUrl =
  import.meta.env.VITE_WS_BASE_URL

export function connectGameWebSocket(
  gameId: string,
): WebSocket {

  const socket = new WebSocket(
    `${wsBaseUrl}/games/${gameId}/ws`,
  )

  return socket
}