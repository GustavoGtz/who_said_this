<script setup>
    import router from "@/router";
    import { connect } from "@/services/websocket";
    import { ref, onMounted} from "vue";

    let socket;
    const curtain = ref(true)
    
    const options = ['A', 'B', 'C', 'D']
    const optionSelected = ref()
    
    const answer = ref("")
    const answerRevealed = ref(false)

    const canAnswer = ref()

    function sendAnswer(index){
        canAnswer.value = false;
        optionSelected.value = index;

        if (!socket) return

        socket.send(JSON.stringify({
            type : "send_answer",
            answer : index
        }))
    }

    async function startRound() {
        answer.value = "";
        answerRevealed.value = false;
        canAnswer.value = true;
        curtain.value = false;
    }

    async function finishRound() {
        answerRevealed.value = true;
        canAnswer.value = false;
    }

    async function setWebSocket() {
        socket = connect((msg) => {
            if (msg.type === "curtain_started") {
                curtain.value = true
            }

            if (msg.type === "round_started") {
                startRound();
            }

            if (msg.type === "round_finished") {
                answer.value = msg.answer
                finishRound();
            }

            if (msg.type == "game_finished") {
                console.log("HOLA")
                router.push("scores")
            }

            if (msg.type === "error") {
                alert(msg.message)
            }
        });
    }

    onMounted(async () => {
        // Starting the game loop
        await setWebSocket();
    });
</script>

<template>
    <div v-if=!curtain>
        <div v-if=!answerRevealed>
            <div class="game-grid">
                <button
                    v-for="(label, index) in options"
                    :key="index"
                    class="game-answer"
                    :class="{
                        unselected: !canAnswer && optionSelected !== index}"
                    :data-index="index"
                    :disabled="!canAnswer"
                    @click="sendAnswer(index)"
                    >
                    {{ label }}
                </button>
            </div>
        </div>

        <div v-else class="page-mobile">
            <h1>
                The answer was: {{ answer }}
            </h1>
        </div>
    </div>
    <div v-else class="page-mobile">
        <div class="dots-loader">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
        </div>
    </div>
</template>