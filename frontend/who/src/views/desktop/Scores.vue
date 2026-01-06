<script setup>
    import { connect } from "@/services/websocket";
    import { ref, onMounted } from "vue";

    let socket;

    const scores = ref([])

    async function showScores() {
        if (!socket) return
        socket.send(JSON.stringify({
            type : "show_scores"
        }))
    }

    async function setWebSocket() {
        socket = connect((msg) => {
            if (msg.type === "scores_showed") {
                scores.value = msg.scores
                console.log(scores.value)
            }

            if (msg.type === "error") {
                alert(msg.message)
            }
        });
    }

    onMounted(async () => {
        await setWebSocket();
        await showScores();
    });
</script>

<template>
    <div class="page-center">
        <div class="big-text">
            RESULTS
        </div>

        <div>
            <div
                class="score-display"
                v-for="(s, index) in scores"
                :key="s.username">
            <span class="rank">{{ index + 1 }}º</span>
            <span class="username">{{ s.username }}</span>
            <span class="score">{{ s.score }} pts</span>
            </div>
        </div>
    </div>
</template>