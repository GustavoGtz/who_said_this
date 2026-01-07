<script setup>
import router from "@/router";
import { ref, computed} from "vue";
import { connect, closeSocket} from "@/services/websocket";

let socket
const loading = ref(false)

const username = ref("")

const selection = ref(false)
const messages = ref([])
const maxSelections = ref()
const selectedIndexes = ref([]) 

function toggleMessage(index) {
  console.log(selectedIndexes.value.length)
  console.log(maxSelections.value)
  
  const i = selectedIndexes.value.indexOf(index)

  if (i === -1) {
    selectedIndexes.value.push(index)
  } else {
    selectedIndexes.value.splice(i, 1)
  }
}

const isValid = computed(() => {
  return selectedIndexes.value.length === maxSelections.value
})

function send() {
  loading.value = true;
  socket.send(JSON.stringify({
    type: "send_selections",
    selections: selectedIndexes.value.map(i => messages.value[i])
  }))
}

function joinRoom() {
  socket = connect((msg) => {
    
    if (msg.type === "user_joined") {
      loading.value = true;
    }
    
    if (msg.type === "room_closed") {
      closeSocket();
      loading.value = false;
      selection = false;
      alert(msg.message);
    }

    if (msg.type === "pool_selection_started") {
      selection.value = true;
      loading.value = false;
      messages.value = msg.messages_pool;
      maxSelections.value = msg.chooses;
      selectedIndexes.value = [];
    }
    
    if (msg.type === "game_started"){
      router.push("play/game")
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
    <div v-if=!loading class="page-mobile">
      <div v-if=!selection class="page-mobile">
        <h1>WHO SAID THIS?</h1>
        <input v-model="username" placeholder="YOUR NAME" />
        <button @click="joinRoom">Join</button>
      </div>
      <div v-else class="page-mobile">
        <div 
          class="pool-counter" 
          :class="{
            uncompleted: selectedIndexes.length < maxSelections,
            completed: selectedIndexes.length === maxSelections,
            error: selectedIndexes.length > maxSelections
          }">
          {{ selectedIndexes.length }} / {{ maxSelections }}
        </div>

        <div class="pool-selection">
          <button
            v-for="(msg, index) in messages"
            :key="index"
            :class="{selected : selectedIndexes.includes(index)}"
            @click="toggleMessage(index)">
          {{ msg.text }}
          </button>
        </div>

        <button
          class="send-button"
          :disabled="!isValid"
          @click="send">
          SEND
        </button>
      </div>
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