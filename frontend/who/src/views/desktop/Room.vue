<script setup>
import router from "@/router";
import { ref, onMounted, computed} from "vue";
import { connect } from "@/services/websocket";

let socket;
const roomCode = ref("PAPU")
const players = ref([])
const maxPlayers = ref(0)
const messageCount = ref()


const messageSelection = ref("random")
const rounds = ref(30)
const secondsPerRound = ref(100)
const samplesPerPlayer = ref(10)
const choosesPerPlayer = ref(5)

const totalMessages = computed(() => {
    return messageSelection.value === 'random'
    ? rounds.value
    : players.value.length * choosesPerPlayer.value
})

const hasPlayers = computed(() => players.value.length > 0)

const randomModeValid = computed(() => {
  return (
    hasPlayers.value &&
    rounds.value > 0 &&
    rounds.value <= messageCount.value
  )
})

const poolModeValid = computed(() => {
  return (
    hasPlayers.value &&
    choosesPerPlayer.value > 0 &&
    players.value.length * choosesPerPlayer.value <= messageCount.value
  )
})

const canHostGame = computed(() => {
  return messageSelection.value === 'random'
    ? randomModeValid.value
    : poolModeValid.value
})


onMounted(() => {
    getRoomMessagesNumber();
    getMaxPlayers();
    hostRoom();
});

function hostRoom() {
    socket = connect((msg) => {

        if (msg.type === "user_joined") {
            players.value.push(msg.name);
        }

        if (msg.type === "user_left") {
            players.value = players.value.filter(
                (player) => player !== msg.name
            );
        }

        if (msg.type === "game_started"){
            router.push("game")
        }
    });

    socket.onopen = () => {
        socket.send(JSON.stringify({
        type: "host",
        code: roomCode.value,
        }));
    };
}

async function hostGame() {
    if (!canHostGame.value) {
        alert("Invalid game configuration")
        return
    }

    let payload

    if (messageSelection.value === 'random') {
        payload = {
            number : rounds.value
        }
    } else {
    payload = {
        players: players.value.length,
        choosesPerPlayer: choosesPerPlayer.value
        }
    }

    try {
        const response = await fetch(
        "http://localhost:8000/api/set_random_messages",
        {
            method: "POST",
            headers: {
            "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
        }
        )

        if (!response.ok) {
            throw new Error("Failed to host the game")
        }

        await response.json()

        socket.send(JSON.stringify({
            type: "start_game",
            code: roomCode.value
        }))
    } catch (error) {
        alert(error.message)
    }
}


async function getMaxPlayers() {
    try {
        const response = await fetch("http://localhost:8000/api/get_max_players",
        {
            method: "GET"
        }
    )
    if (!response.ok) {
        throw new Error("Failed to get the max players")
    }
    
    const data = await response.json()
    maxPlayers.value = data
    } catch (error) {
        alert(error.message)
    } 
}

async function getRoomMessagesNumber() {
    try {
        const response = await fetch("http://localhost:8000/api/get_room_messages_number",
        {
            method: "GET"
        }
    )
    if (!response.ok) {
        throw new Error("Failed to get the messages number")
    }
    
    const data = await response.json()
    messageCount.value = data
    } catch (error) {
        alert(error.message)
    } 
}

</script>

<template>
<div class="page-center">
    <p class="big-text">
        ROOM CODE: <strong>{{roomCode}}</strong>
    </p>
    <div class="members-card">
        <h1>Players {{ players.length }} / {{ maxPlayers }}</h1>
        <label
        v-for="name in players"
        :key="name">
        {{ name }}
    </label>
    </div>
    <div class="invisible-card">
        <div class="text-stack">
            <strong>Message Selection Method</strong>
            <label>
                <input
                    type="radio"
                    value="random"
                    v-model="messageSelection"
                />
                <strong>RANDOM</strong>
            </label>
            <div v-if="messageSelection === 'random'" class="sub-options">
                <label>
                    <strong>Rounds</strong>
                    <input class="input-row" type="number" v-model="rounds" />
                </label>
            </div>

            <label>
                <input
                    type="radio"
                    value="pool"
                    v-model="messageSelection"
                />
                <strong>POOL SELECTION</strong>
            </label>

            <div v-if="messageSelection === 'pool'" class="sub-options">
                <label>
                    <strong>Samples per Player</strong>
                    <input class="input-row" type="number" v-model="samplesPerPlayer" />
                </label>
            <label>
                <strong>Chooses per Player</strong>
                <input class="input-row" type="number" v-model="choosesPerPlayer" />
            </label>
            </div>
        </div>

        <div class="text-stack">
            <strong>Secs per Round</strong>
            <input
                type="number"
                class="big-input"
                min="1"
                v-model="secondsPerRound"
                />
        </div>

        <div class="text-stack">
            <button
                class="btn btn-secondary"
                :disabled="!canHostGame"
                @click="hostGame()">
                START THE GAME
            </button>
            <div class="mini-hint">
                You will be playing with {{ totalMessages }} messages from over {{ messageCount }} messages
            </div>
        </div>
    </div>
</div>
</template>