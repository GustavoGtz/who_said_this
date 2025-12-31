const WS_URL =
  (location.protocol === "https:" ? "wss://" : "ws://") +
  location.hostname +
  ":8000/ws";

let socket = null;

export function connect(onMessage) {
  if (!socket) {
    socket = new WebSocket(WS_URL);

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (onMessage) onMessage(data);
    };
  }

  return socket;
}

export function getSocket() {
  return socket;
}

export function closeSocket() {
  if (socket) {
    socket.close();
    socket = null;
  }
}
