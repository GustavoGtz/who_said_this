<script setup>
import router from "@/router";
import { ref } from "vue";
import { connect, closeSocket} from "@/services/websocket";

let socket
const loading = ref(false)

const username = ref("")

function joinRoom() {
  socket = connect((msg) => {
    // cases
    if (msg.type === "user_joined") {
      loading.value = true;
    }
    
    if (msg.type === "room_closed") {
      closeSocket();
      loading.value = false;
      alert(msg.message);
    }
    
    // TODO: Other case for pool_selection
    
    if (msg.type === "game_started"){
      router.push("play/pool")
    }

    if (msg.type === "error") {
      alert(msg.message)
      closeSocket();
    }
  });

  socket.onopen = () => {
    socket.send(JSON.stringify({
      type: "join",
      username: username.value
    }));
  };

  socket.onerror = () => {
    alert("No se pudo conectar al servidor");
  };
}
</script>

<template>
    <div div v-if=!loading class="page-mobile">
      <h1>WHO SAID THIS?</h1>
        <input v-model="username" placeholder="YOUR NAME" />
        <button @click="joinRoom">Join</button>
    </div>

    <div v-else class="page-mobile">
      <h1>Waiting for the host</h1>
      <div class="dots-loader">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>
</template>