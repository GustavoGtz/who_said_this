<script setup>
import { ref } from "vue";

// PLACEHOLDERS
const messageSelection = ref("random")
const rounds = ref(30)
const messageCount = ref(3000)
const secondsPerRound = ref(100)
const maxPlayers = ref(7)
const players = ref(["sissel", "Gustabuu", "Matu", "TacoLoco", "TacoNormal", "Sanes", "Ferminio"])

</script>

<template>
<div class="page-center">
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