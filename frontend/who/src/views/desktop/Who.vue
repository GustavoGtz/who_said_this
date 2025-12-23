<script setup>
import { ref, reactive, watch} from "vue";

const state = ref("home")

const members = ref([])
const activeMembers = ref(new Set())

const maxPlayers = ref(4)

const filters = reactive({
  minDate: null,
  maxDate: null,
  minHour: null,
  maxHour: null
})

const messageCount = ref(0)
const loading = ref(false)


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

async function precalculateMessages() {
  console.log("llamdaa a funcion")
}

function toggleMember(name) {
  if (activeMembers.value.has(name)) {
    activeMembers.value.delete(name)
  } else {
    activeMembers.value.add(name)
  }
  precalculateMessages()
}

watch(state, (newState) => {
  if (newState === "loaded") {
    getMembers()
    precalculateMessages(filters)
  }
})

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
  </div>
</template>




