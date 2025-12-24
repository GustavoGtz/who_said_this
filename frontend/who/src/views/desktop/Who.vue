<script setup>
import { ref, reactive, watch} from "vue";

const state = ref("home")
const maxPlayers = ref(4)

const members = ref([])
const activeMembers = ref(new Set())
const messageCount = ref(0)
const filters = reactive({
  min_date: null,
  max_date: null,
  min_time: null,
  max_time: null
})


async function uploadChat(file) {
  if (!file) return
  state.value = "loading"

  const formData = new FormData()
  formData.append("file", file)

  try {
    const response = await fetch("http://localhost:8000/api/load_chat",
      {
        method: "POST",
        body: formData
      }
    )

    if (!response.ok) {
      throw new Error("Failed to upload chat")
    }
    const data = await response.json()
    state.value = "loaded"

  } catch (error) {
    alert(error.message)
    state.value = "home"
  }
}

async function getMembers() {
  try {
    const response = await fetch("http://localhost:8000/api/get_members",
      {
        method: "GET"
      }
    )

    if (!response.ok) {
      throw new Error("Failed to get the members")
    }

    const data = await response.json()
    members.value = data
    activeMembers.value = new Set(data)  
  } catch (error) {
    alert(error.message)
  }
}

function toggleMember(name) {
  if (activeMembers.value.has(name)) {
    activeMembers.value.delete(name)
  } else {
    activeMembers.value.add(name)
  }
  precalculateMessages()
}

function dateStringToObject(date) {
  if (!date) return null
  const [year, month, day] = date.split('-').map(Number)
  return {day, month, year}
}

function timeStringToObject(time) {
  if (!time) return null

  const [hour, minute] = time.split(":").map(Number)
  return { hour, minute }
}

async function precalculateMessages() {
  try {
    const payload = {
      members: [...activeMembers.value],
      min_date: dateStringToObject(filters.min_date),
      max_date: dateStringToObject(filters.max_date),
      min_time: timeStringToObject(filters.min_time),
      max_time: timeStringToObject(filters.max_time)  
    }

    console.log(payload)

    const response = await fetch("http://localhost:8000/api/get_messages_number",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      }
    )

    if (!response.ok) {
      throw new Error("Failed to get the number of messages")
    }

    const data = await response.json()
    messageCount.value = data
  } catch (error) {
    alert(error.message)
  }
}

function hostGame() {
  // CREATE THE OBJET OF THE PARY CONTROLLER
  // START THE NEW SCENE WITH WEB SOCKETS
  console.log("HOSTEAR GAME!")
}

watch(state, (newState) => {
  if (newState === "loaded") {
    getMembers()
    precalculateMessages(filters)
  }
})

watch(
  () => [
    filters.min_date,
    filters.max_date,
    filters.min_time,
    filters.max_time
  ],
  () => {
    precalculateMessages()
  }
)

</script>

<template>
  <!-- HOME SCREEN -->
  <div v-if="state === 'home'" class="page-center">
    <div class="card">
      <h1>WHO SAID THIS?</h1>

      <p>Upload your friends WhatsApp Chat History to start the party</p>

      <label class="btn btn-primary">
        Load Chat
        <input
          type="file"
          hidden
          @change="e => uploadChat(e.target.files[0])"
        />
      </label>

      <p class="hint">
        <a
          href="https://faq.whatsapp.com/1180414079177245/?cms_platform=android"
          target="_blank"
          rel="noopener"
        >
          If you don't know how to get your WhatsApp Chat History
        </a>
      </p>
    </div>
  </div>

  <!-- LOADING SCREEN -->
  <div v-else-if="state === 'loading'" class="page-center">
    <div class="dots-loader">
      <span></span>
      <span></span>
      <span></span>
      <span></span>
    </div>

  </div>

  <!-- HOST CONFIG SCREEN -->
  <!-- QUE DEBERIA HACER AQUI?
   1, Cargar los miembros por medio de una API (le van adeolver una lista de nombres),
      y generar un tablero interactivo donde se podra pulsar cada uno de los nombrees para desactivarlos
   2, Debe hnaber una seccion para que se peudai ntroducor el MAX players.
   3. Debe haber 4 filtros, min date, max date, min hour, max hour.
   4. Debe haver un texto reractivo ab ajo a la izquierda, cada vez qeu ase pulse ya sea algo de 1 o algo de 
      3, se debera a llamar uan funcion del backend para precalcular con los datos de 1 y 3 para detemrinra
    cauntos mensajes hay ahora.
  5. Finalmnete, debera haver un host Game boton asociado a una funcion del API que se ria como inicialziar con la partida.-->
  <div v-else class="page-center">
    <div class="members-card">
      <h1>Members Pool</h1>
      <button
        v-for="name in members"
        :key="name"
        :class="{ inactive: !activeMembers.has(name) }"
        @click="toggleMember(name)">
        {{ name }}
      </button>
      <p>
      You can <strong>select</strong> or <strong>deselect</strong> the members of the chat that you want to be in he game with your <strong>click</strong>
      </p>
    </div>
    <div class="invisible-card">
      <div class="text-stack">
        <strong>MAX PLAYERS:</strong>
        <input
          type="number"
          class="big-input"
          min="1"
          v-model="maxPlayers"
        />
      </div>
      
      <div class="text-stack">
        <label>
          <strong>Min Date</strong>
          <input class="input-row" type="date" v-model="filters.min_date"/>
        </label>

        <label>
          <strong>Max Date</strong>
          <input class="input-row" type="date" v-model="filters.max_date" />
        </label>
      </div>

      <div class="text-stack">
        <label>
          <strong>Min Time</strong>
          <input class="input-row" type="time" v-model="filters.min_time" />
        </label>

        <label>
          <strong>Max Time</strong>
          <input class="input-row" type="time" v-model="filters.max_time" />
        </label>
      </div>
    </div>

    <div class="invisible-card">
      <p>There is <strong>{{ messageCount }} messages</strong> in the game</p>
      <button
         class="btn btn-secondary"
         @click="hostGame()">
         HOST THE GAME
      </button>
    </div>
  </div>
</template>




