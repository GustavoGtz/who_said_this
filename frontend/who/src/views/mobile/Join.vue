<script setup>
import router from "@/router";
import { ref } from "vue";
import { connect } from "@/services/websocket";

const state = ref("home")

const username = ref("")
const roomCode = ref("")

function joinRoom() {
  const socket = connect((msg) => {
    if (msg.type === "error") {
      alert(msg.message)
      socket.close();
      return;
    }

    if (msg.type === "user_joined") {
      state.value = "loading";
    }

    if (msg.type === "game_started"){
            router.push("player/game")
        }
  });

  socket.onopen = () => {
    socket.send(JSON.stringify({
      type: "join",
      code: roomCode.value,
      name: username.value
    }));
  };

  socket.onerror = () => {
    alert("No se pudo conectar al servidor");
  };
}
</script>

<template>
    <div div v-if="state === 'home'" class="page-mobile">
      <h1>WHO SAID THIS?</h1>
        <input v-model="roomCode" placeholder="CODE" />
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