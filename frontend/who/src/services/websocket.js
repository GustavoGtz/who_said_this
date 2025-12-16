const WS_URL =
  (location.protocol === "https:" ? "wss://" : "ws://") +
  location.hostname +
  ":8000/ws";

export function connect(onMessage) {
  const socket = new WebSocket(WS_URL)

  socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (onMessage) onMessage(data);
  };

  return socket;
}
