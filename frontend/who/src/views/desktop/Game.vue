<script setup>
    import { connect } from "@/services/websocket";
    import { ref, reactive, onMounted} from "vue";

    let socket;

    const answer = ref("")
    const answerRevealed = ref(false)

    const curtain = ref(true)
    const secondsPerRound = ref()
    const roundTime = ref()
    const timer = ref(null)

    const roundMessage = reactive({
        text: "",
        date: "",    // "11/12/2025"
        time: "",    // "12:50 PM"
        options: []
    });

    async function startCurtain() {
        if (!socket) return
        socket.send(JSON.stringify({
            type : "start_curtain"
        }))
    }

    function formatDate({ day, month, year }) {
        if (!day || !month || !year) return "";

        return `${month}/${day}/${year + 2000}`;
        }

    function formatTime({ hour, minute }) {
        if (hour == null || minute == null) return "";

        const isPM = hour >= 12;
        const displayHour = hour % 12 || 12;
        const paddedMinute = minute.toString().padStart(2, "0");

        return `${displayHour}:${paddedMinute} ${isPM ? "PM" : "AM"}`;
     }

    function normalizeRoundMessage(data) {
        return {
            text: data.text,
            date: formatDate(data.date),
            time: formatTime(data.time),
            options: data.options ?? []
        };
    }

    async function startRound() {
        answer.value = ""
        answerRevealed.value = false
        roundTime.value = secondsPerRound.value

        try {
            const response = await fetch("http://localhost:8000/api/room/get_round_message",
                { 
                    method: "GET" 
                }
            );

            if (!response.ok) {
                throw new Error("Failed to get the message round");
            }

            const data = await response.json();
            const normalized = normalizeRoundMessage(data);

            roundMessage.text = normalized.text;
            roundMessage.date = normalized.date;
            roundMessage.time = normalized.time;
            roundMessage.options = normalized.options;

        } catch (error) {
            alert(error.message);
            
        }

        curtain.value = false;
        startCountdown();
    }

    async function finishRound() {
        answerRevealed.value = true
        // Un peque;o lapso de tiempo aqui . . .
        startCurtain();
    }
    
    function startCountdown() {
        clearInterval(timer.value);

        timer.value = setInterval(() => {
            roundTime.value--;

            if (roundTime.value <= 0){
                clearInterval(timer.value)
                timer.value = null;
                socket.send(JSON.stringify({
                    type : "finish_round"
                }))
            }
        }, 1000)

    }

    async function getSecondsPerRound() {
        try {
            const response = await fetch("http://localhost:8000/api/room/get_seconds_per_round",
                {
                    method : "GET"
                }
            )
            if (!response.ok) { throw new Error("Failed to get the secodns per round") }

            const data = await response.json() 
            secondsPerRound.value = data
            roundTime.value = data

        } catch (error) {
            alert(error.message)
        }
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

            if (msg.type === "error") {
                alert(msg.message)
            }
        });
    }

    onMounted(async () => {
        // Starting the game loop
        await setWebSocket();
        await getSecondsPerRound();
        await startCurtain();
    });
</script>

<template>
    <div v-if=!curtain class="page-center">
        <div class="invisible-card">
            <div class="message-interface">
                <div class="grey-header"></div>
                <div class="date-header">
                    {{ roundMessage.date }}
                </div>
                <div class="scrollable-msg">
                    {{ roundMessage.text }}
                    <div class="time-footer">
                        {{ roundMessage.time }}
                    </div>
                </div>
                <div class="grey-footer"></div>
            </div>

            <div class="text-stacked">
                <div class="game-timer">
                    {{ roundTime }}
                </div>
            <div class="game-answer"
                v-for="(option, index) in roundMessage.options"
                :key="index"
                :class="{
                    correct:   answerRevealed && option === roundMessage.answer,
                    incorrect: answerRevealed && option !== roundMessage.answer}">
                <div class="game-answer-icon">
                    {{ String.fromCharCode(65 + index) }}
                </div>
                    {{ option }}
                </div>     
            </div>
        </div>
    </div>
    <div v-else class="page-center">
        <div class="dots-loader">
            <span></span>
            <span></span>
            <span></span>
            <span></span>
        </div>
    </div>
</template>