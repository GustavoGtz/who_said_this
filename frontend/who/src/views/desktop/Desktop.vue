<script setup>
import { ref } from "vue";
import { connect } from "@/services/websocket";

const code = ref("");
const name = ref("");
const users = ref([]);
const connected = ref(false);

function hostRoom() {
  const socket = connect((msg) => {
    if (msg.type === "user_joined") {
      users.value.push(msg.name);
    }
  });

  socket.onopen = () => {
    socket.send(JSON.stringify({
      type: "host",
      code: code.value,
    }));
    connected.value = true;
  };
}
</script>

<template>
  <div v-if="!connected">
    <input v-model="code" placeholder="CODE" />
    <button @click="hostRoom">Open Room</button>
  </div>

  <div v-else>
    <h3>Connected Users</h3>
    <ul>
      <li v-for="(u, i) in users" :key="i">{{ u }}</li>
    </ul>
  </div>
</template>
