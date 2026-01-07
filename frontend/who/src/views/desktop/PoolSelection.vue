<script setup>
    import router from "@/router"
    import { ref, computed, onMounted } from "vue"
    import { connect } from "@/services/websocket"

    let socket

    const selectionsSended = ref(0)
    const numClients = ref(0)

    async function getClientsNumber() {
        try {
            const response = await fetch("http://localhost:8000/api/room/get_clients_number",
                {
                    method : "GET"
                }
            )
            if (!response.ok) { throw new Error("Failed to get the number of clients") }

            const data = await response.json() 
            numClients.value = data

        } catch (error) {
            alert(error.message)
        }
    }

    async function setWebSocket() {
        socket = connect((msg) => {
            if (msg.type === "selection_registered") {
                selectionsSended.value = msg.selections_sended
                numClients.value = msg.num_clients
            }

            if (msg.type === "game_started") {
                router.push("game")
            }

            if (msg.type === "error") {
                alert(msg.message)
            }
        })
    }

    const counterState = computed(() => {
        if (selectionsSended.value > numClients.value) return "error"
        if (selectionsSended.value < numClients.value) return "uncompleted"
        return "completed"
    })

    onMounted(async () => {
        await getClientsNumber();
        await setWebSocket();
    })
</script>

<template>
  <div class="page-center">
    <div class="pool-counter" :class="counterState">
      {{ selectionsSended }} / {{ numClients }}
    </div>
  </div>
</template>

