<script setup>
import { ref, onMounted} from "vue";
import { connect } from "@/services/websocket";

const roomCode = ref("PAPU")
const players = ref([])
const maxPlayers = ref(0)

onMounted(() => {
    getMaxPlayers();
    hostRoom();
});

// PLACEHOLDERS
const messageSelection = ref("random")
const rounds = ref(30)
const messageCount = ref(3000)
const secondsPerRound = ref(100)

function hostRoom() {
    const socket = connect((msg) => {
        if (msg.type === "user_joined") {
            players.value.push(msg.name);
        }

        if (msg.type === "user_left") {
            players.value = players.value.filter(
                (player) => player !== msg.name
            );
        }
    });

    socket.onopen = () => {
        socket.send(JSON.stringify({
        type: "host",
        code: roomCode.value,
        }));
    };
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
                @click="hostGame()">
                START THE GAME
            </button>
            <div class="mini-hint">
                You will be playing with {{ rounds }} messages from over a {{ messageCount }} messages
            </div>
        </div>
    </div>
</div>
</template>