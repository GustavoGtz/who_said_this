<script setup>
import { ref } from "vue";
import { connect } from "@/services/websocket";

const code = ref("");
const name = ref("");
const joined = ref(false);

function joinRoom() {
  const socket = connect((msg) => {
    if (msg.type === "joined") {
      joined.value = true;
    }
  });

  socket.onopen = () => {
    socket.send(JSON.stringify({
      type: "join",
      code: code.value,
      name: name.value
    }));
  };
}
</script>

<template>
  <div v-if="!joined">
    <input v-model="code" placeholder="CODE" />
    <input v-model="name" placeholder="YOUR NAME" />
    <button @click="joinRoom">Join</button>
  </div>

  <div v-else>
    <h2>You joined as {{ name }}</h2>
  </div>
</template>
