<script setup>
import { ref, reactive} from "vue";

const state = ref("loop")

// PLACEHOLDER VARIABLES
const answerTime = ref(60)
const message = reactive({
    text : "Este es un texto de prueba y se puede ver como se escribe un poco mas ya si jaja",
    date : "10-8-2025",
    time : "10:20"
})
const answers = reactive({
    good : "Fermin",
    bad : ["Miguel", "Gustavo", "Mirka"]
})

function startRound() {
    // Put a Cortain for a few sxeconds
    // Generate a new question with the objetct in the backend
    //Put a timer with the question and receive the answers.
}

</script>

<template>
    <div v-if="state === 'loop'" class="page-center">
        <div class="invisible-card">
            <div class="message-interface">
                <div class="grey-header"></div>
                <div class="date-header">
                    {{ message.date }}
                </div>
                <div class="scrollable-msg">
                    {{ message.text }}
                    <div class="time-footer">
                        {{ message.time }}
                    </div>
                </div>
                <div class="grey-footer"></div>
            </div>

            <div class="text-stacked">
                <div class="game-timer">
                    Counter
                </div>         
                <div class="game-answer">
                    <div class="game-answer-icon"> A </div> Fermin
                </div>

                <div class="game-answer">
                    <div class="game-answer-icon"> B </div> Miguel
                </div>

                <div class="game-answer">
                    <div class="game-answer-icon"> C </div> Gustavo
                </div>

                <div class="game-answer">
                    <div class="game-answer-icon"> D </div> Mirka
                </div>
            </div>
        </div>
    </div>
</template>