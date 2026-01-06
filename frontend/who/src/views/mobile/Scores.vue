<script setup>
    import { connect } from "@/services/websocket";
    import { ref, onMounted } from "vue";

    let socket;

    const username = ref("")
    const score = ref(0)

    async function showScores() {
        if (!socket) return
        socket.send(JSON.stringify({
            type : "show_scores"
        }))
    }

    async function setWebSocket() {
        socket = connect((msg) => {
            if (msg.type === "score_showed") {
                username.value = msg.username
                score.value = msg.score
            }

            if (msg.type === "error") {
                alert(msg.message)
            }
        });
    }

    onMounted(async () => {
        await setWebSocket();
    });
</script>

<template>
    <div class="page-mobile">
        <div class="big-text">
            The game has ended
        </div>

        <div class="big-text">
            {{ username }}, you scored {{ score }} pts.
        </div>
    </div>
</template>