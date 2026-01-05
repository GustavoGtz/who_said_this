<script setup>
    import router from "@/router";
    import {ref, onMounted, computed} from "vue";
    import { connect } from "@/services/websocket";

    let socket;

    const players = ref([])
    const maxPlayers = ref()

    const messageCount = ref()

    const secondsPerRound = ref(5)
    const messageSelection = ref("random")
    const rounds = ref(30)
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
    
    async function startGame() {
        if (!canHostGame.value) {
            alert("Invalid game configuration")
            return
        }

        await setSecondsPerRounds()

        if (messageSelection.value === 'random'){
            const payload = {
                number_of_messages : rounds.value
            }

            try {
                const response = await fetch("http://localhost:8000/api/room/randomize_messages",
                    {
                        method : "POST",
                        headers : {
                            "Content-Type": "application/json",
                        },
                        body : JSON.stringify(payload)
                    }
                )
                if (!response.ok) { throw new Error("Failed to start the game") }

                const data = await response.json()
                socket.send(JSON.stringify({
                    type : "start_game"
                }))
            } catch (error) {
                alert(error.message)
            }
        }
        else{
            // TODO: Do another view to all this proceess (with his mobile view too)!
            alert("Game mode not implemented yet!")
            return
        }
    }

    async function setSecondsPerRounds() {
        try {

            const payload = {
                seconds : secondsPerRound.value
            }

            const response = await fetch("http://localhost:8000/api/room/set_seconds_per_round",
                {
                    method : "POST",
                    headers : {
                            "Content-Type": "application/json",
                        },
                    body : JSON.stringify(payload)
                }
            )
            if (!response.ok) { throw new Error("Failed to set the seconds per round") }

            const data = await response.json() 

        } catch (error) {
            alert(error.message)
        }
    }

    async function getMaxPlayers() {
        try {
            const response = await fetch("http://localhost:8000/api/room/get_max_players",
                {
                    method : "GET"
                }
            )
            if (!response.ok) { throw new Error("Failed to get the max players") }

            const data = await response.json() 
            maxPlayers.value = data

        } catch (error) {
            alert(error.message)
        }
    }

    async function getMessagesCount() {
        try {
            const response = await fetch("http://localhost:8000/api/room/get_messages_count",
            {
                method: "GET"
            }
        )
        if (!response.ok) { throw new Error("Failed to get the messages number") }
        
        const data = await response.json()
        messageCount.value = data

        } catch (error) {
            alert(error.message)
        } 
    }
    
    async function hostParty() {
        socket = connect((msg) => {
            // cases
            if (msg.type === "user_joined") {
                players.value.push(msg.username)
            }

            if (msg.type === "user_left") {
                players.value = players.value.filter(
                    (player) => player !== msg.username
                );
            }

            if (msg.type === "game_started") {
                router.push("game")
            }

            if (msg.type === "error") {
                alert(msg.message)
            }
        });

        socket.onopen = () => {
            socket.send(JSON.stringify({
                type : "host"
            }))
        };

        socket.onerror = () => {
            alert("No se pudo hostear el servidor");
        };
    }

    onMounted(async () => {
        await getMaxPlayers();
        await getMessagesCount();
        await hostParty();
    });

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
                    v-model="messageSelection"/>
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
                    v-model="messageSelection"/>
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
                    v-model="secondsPerRound"/>
            </div>

            <div class="text-stack">
                <button
                    class="btn btn-secondary"
                    :disabled="!canHostGame"
                    @click="startGame()">
                    START THE GAME
                </button>
                <div class="mini-hint">
                    You will be playing with {{ totalMessages }} messages from over {{ messageCount }} messages
                </div>
            </div>
        </div>
    </div>
</template>